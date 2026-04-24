import streamlit as st
from datetime import date, datetime
from database import get_todos, add_todo, update_todo, delete_todo
import time

# ── FRENIZER ──────────────────────────────────────────────
from mascot import show_fren
# ─────────────────────────────────────────────────────────

st.set_page_config(page_title="Frenizer", page_icon="🤍", layout="wide")
st.title("Frenizer")
st.markdown("""
<style>

.stApp {

    background-color: #0E1117;

    color: white;

}

.block-container {

    padding-top: 2rem;

    padding-left: 4rem;

    padding-right: 4rem;

    max-width: 1400px;

}

h1 {

    font-size: 60px !important;

    font-weight: 800 !important;

}

.stButton>button {

    background: linear-gradient(90deg,#ff4b4b,#ff7b00);

    color: white;

    border-radius: 12px;

    border: none;

    font-weight: bold;

}
</style>

""", unsafe_allow_html=True)
st.markdown("""

            <style>

/* App Background */

.stApp {

    background: linear-gradient(135deg, #0E1117, #161B22);

    color: white;

}

/* Main Content Width + Padding */

.block-container {

    padding-top: 2rem;

    padding-left: 4rem;

    padding-right: 4rem;

    max-width: 1300px;

}

/* Titles */

h1 {

    font-size: 56px !important;

    font-weight: 800 !important;

    color: white !important;

}

h2, h3 {

    color: white !important;

}

/* Cards / Containers */

div[data-testid="stVerticalBlock"] > div {

    background: rgba(255,255,255,0.03);

    border: 1px solid rgba(255,255,255,0.06);

    padding: 18px;

    border-radius: 18px;

    margin-bottom: 14px;

}

/* Input Fields */

input, textarea {

    border-radius: 14px !important;

    background: rgba(255,255,255,0.05) !important;

    color: white !important;

}

/* Buttons */

.stButton button {

    background: linear-gradient(90deg,#ff5c5c,#ff8a5c);

    color: white;

    border: none;

    border-radius: 14px;

    padding: 10px 20px;

    font-weight: 700;

    transition: 0.3s;

}

.stButton button:hover {

    transform: scale(1.04);

    box-shadow: 0 0 18px rgba(255,92,92,0.4);

}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {

    gap: 30px;

    border-bottom: 1px solid rgba(255,255,255,0.08);

}

.stTabs [data-baseweb="tab"] {

    color: #aaaaaa;

    font-size: 18px;

    font-weight: 600;

}

.stTabs [aria-selected="true"] {

    color: white !important;

    border-bottom: 3px solid #ff5c5c;

}

/* Selectbox */

div[data-baseweb="select"] {

    background: rgba(255,255,255,0.05);

    border-radius: 14px;

}

/* Slider */

.stSlider {

    padding-top: 10px;

}

/* Checkbox text */

label {

    color: white !important;

}
</style>

""", unsafe_allow_html=True)
 
def get_countdown(deadline):
    deadline_date = datetime.fromisoformat(deadline).date()
    today = date.today()
    days_left = (deadline_date - today).days

    if days_left > 1:
        return f"{days_left} days left"
    if days_left == 1:
        return "1 day left"
    if days_left == 0:
        return "Today"
    if days_left == -1:
        return "1 day overdue"
    return f"{abs(days_left)} days overdue"

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def draw_timer_circle(remaining, total_seconds):
    progress = 0 if total_seconds <= 0 else (total_seconds - remaining) / total_seconds
    progress = max(0, min(progress, 1))
    degrees = int(progress * 360)
    time_text = format_time(remaining)

    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin: 20px 0 10px 0;">
            <div style="
                width: 220px;
                height: 220px;
                border-radius: 50%;
                background: conic-gradient(white 0deg {degrees}deg, #2b2b2b {degrees}deg 360deg);
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <div style="
                    width: 176px;
                    height: 176px;
                    border-radius: 50%;
                    background: #0e1117;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                    font-weight: 700;
                    font-family: monospace;
                ">
                    {time_text}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_paused" not in st.session_state:
    st.session_state.timer_paused = False
if "timer_task_id" not in st.session_state:
    st.session_state.timer_task_id = None
if "timer_task_title" not in st.session_state:
    st.session_state.timer_task_title = ""
if "timer_end_time" not in st.session_state:
    st.session_state.timer_end_time = None
if "timer_total_seconds" not in st.session_state:
    st.session_state.timer_total_seconds = None
if "timer_remaining_on_pause" not in st.session_state:
    st.session_state.timer_remaining_on_pause = None

tab1, tab2 = st.tabs(["Todos", "Focus Timer"])

with tab1:
    with st.form("new_todo_form", clear_on_submit=True):
        title = st.text_input("New todo")
        deadline = st.date_input("Deadline", value=date.today())
        submitted = st.form_submit_button("Add")

    if submitted and title.strip():
        add_todo(title.strip(), deadline.isoformat())
        st.rerun()

    todos = get_todos()
    active = [t for t in todos if not t["completed"]]
    completed = [t for t in todos if t["completed"]]

    if active:
        st.subheader("Todos")
        for todo in active:
            col1, col2, col3 = st.columns([6, 3, 2])

            with col1:
                checked = st.checkbox(
                    todo["title"],
                    value=todo["completed"],
                    key=f"check_{todo['id']}"
                )
                if checked != todo["completed"]:
                    update_todo(todo["id"], checked)
                    st.rerun()

            with col2:
                st.write(get_countdown(todo["deadline"]))

            with col3:
                if st.button("Delete", key=f"delete_{todo['id']}"):
                    delete_todo(todo["id"])
                    st.rerun()
    else:
        st.info("No active todos.")

    if completed:
        st.subheader("Completed")
        for todo in completed:
            col1, col2, col3 = st.columns([6, 3, 2])

            with col1:
                st.markdown(f"<span style='color: gray'>{todo['title']}</span>", unsafe_allow_html=True)
                checked = st.checkbox(
                    "",
                    value=True,
                    key=f"check_completed_{todo['id']}"
                )
                if not checked:
                    update_todo(todo["id"], False)
                    st.rerun()

            with col2:
                st.markdown(
                    f"<span style='color: gray'>{get_countdown(todo['deadline'])}</span>",
                    unsafe_allow_html=True
                )

            with col3:
                if st.button("Delete", key=f"delete_completed_{todo['id']}"):
                    delete_todo(todo["id"])
                    st.rerun()

with tab2:
    todos = get_todos()
    active = [t for t in todos if not t["completed"]]

    st.subheader("Focus Timer")

    timer_active = (
        st.session_state.timer_task_id is not None
        and st.session_state.timer_total_seconds is not None
    )

    if timer_active:
        if st.session_state.timer_paused:
            remaining = st.session_state.timer_remaining_on_pause
        else:
            remaining = int(st.session_state.timer_end_time - time.time())

        # ── FREN : timer terminé → état "win" ─────────────────
        if remaining <= 0 and not st.session_state.timer_paused:
            update_todo(st.session_state.timer_task_id, True)
            show_fren("win", task_id=st.session_state.timer_task_id)   # 🏆 win
            st.success(f"Done: {st.session_state.timer_task_title}")
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.timer_task_id = None
            st.session_state.timer_task_title = ""
            st.session_state.timer_end_time = None
            st.session_state.timer_total_seconds = None
            st.session_state.timer_remaining_on_pause = None
            st.rerun()
        # ──────────────────────────────────────────────────────

        st.write(f"Task: {st.session_state.timer_task_title}")

        # ── FREN : layout côte-à-côte avec le timer circle ────
        fren_col, timer_col = st.columns([1, 2])
        with fren_col:
            if st.session_state.timer_paused:
                show_fren("paused", task_id=st.session_state.timer_task_id)  # 😌 paused
            else:
                show_fren("timer", task_id=st.session_state.timer_task_id)   # 🔥 focus
        with timer_col:
            draw_timer_circle(remaining, st.session_state.timer_total_seconds)
        # ──────────────────────────────────────────────────────

        col1, col2, col3 = st.columns(3)

        with col1:
            if not st.session_state.timer_paused:
                if st.button("Pause timer"):
                    st.session_state.timer_paused = True
                    st.session_state.timer_running = False
                    st.session_state.timer_remaining_on_pause = remaining
                    st.rerun()
            else:
                if st.button("Continue timer"):
                    st.session_state.timer_paused = False
                    st.session_state.timer_running = True
                    st.session_state.timer_end_time = time.time() + st.session_state.timer_remaining_on_pause
                    st.rerun()

        with col2:
            if st.button("Stop timer"):
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_task_id = None
                st.session_state.timer_task_title = ""
                st.session_state.timer_end_time = None
                st.session_state.timer_total_seconds = None
                st.session_state.timer_remaining_on_pause = None
                st.rerun()

        with col3:
            if st.button("Complete task now"):
                update_todo(st.session_state.timer_task_id, True)
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.timer_task_id = None
                st.session_state.timer_task_title = ""
                st.session_state.timer_end_time = None
                st.session_state.timer_total_seconds = None
                st.session_state.timer_remaining_on_pause = None
                st.rerun()

        if not st.session_state.timer_paused:
            time.sleep(1)
            st.rerun()
        else:
            st.info("Timer paused.")
    else:
        # ── FREN : écran d'accueil → état "idle" ──────────────
        show_fren("idle")                                              # 😴 idle
        # ──────────────────────────────────────────────────────

        if not active:
            st.info("No active todos available.")
        else:
            task_options = {todo["title"]: todo["id"] for todo in active}
            selected_title = st.selectbox("Select a task", list(task_options.keys()))
            duration = st.slider("Select time", min_value=10, max_value=360, value=25, step=5)

            if st.button("Start timer"):
                total_seconds = duration * 60
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.timer_task_id = task_options[selected_title]
                st.session_state.timer_task_title = selected_title
                st.session_state.timer_end_time = time.time() + total_seconds
                st.session_state.timer_total_seconds = total_seconds
                st.session_state.timer_remaining_on_pause = None
 
                st.rerun()
st.divider()

st.subheader("📅 Weekly Planner")

from datetime import datetime

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

cols = st.columns(7)

for i, day in enumerate(days):

    with cols[i]:

        st.markdown(f"### {day}")

        for todo in todos:

            deadline = datetime.fromisoformat(todo["deadline"])

            todo_day = deadline.strftime("%a")

            if todo_day == day:

                st.write("•", todo["title"])

                #st.rerun()

