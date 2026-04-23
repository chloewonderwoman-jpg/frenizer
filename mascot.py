import streamlit.components.v1 as components

MESSAGES = {
    "idle": [
        "Hey, I'm Fren!<br>Tell me when you're ready to study.",
        "Ready when you are!<br>Select a task to get started.",
    ],
    "timer": [
        "Stay focused!<br>Break time is coming soon 🔥",
        "Phone on silent,<br>you've got this session!",
        "Keep it up,<br>you're almost there!",
    ],
    "paused": [
        "Well deserved break!<br>Resume whenever you're ready.",
        "Take a breath,<br>Fren is waiting for you.",
    ],
    "win": [
        "Goal reached!<br>Frenizer is so proud of you 🏆",
        "You nailed it!<br>Go enjoy a real break.",
        "Incredible!<br>Keep up that momentum 🌟",
    ],
    "cheer": [
        "You're doing amazing!<br>Keep it up 💜",
        "Let's keep the rhythm!<br>You're on the right track.",
    ],
}

def _get_message(state: str, task_id=None) -> str:
    msgs = MESSAGES.get(state, MESSAGES["idle"])
    idx = (hash(str(task_id)) if task_id is not None else 0) % len(msgs)
    return msgs[idx]

def show_fren(state: str = "idle", task_id=None, height: int = 320):
    """
    Affiche la mascotte Fren.
    state : 'idle' | 'timer' | 'paused' | 'win' | 'cheer'
    """
    msg = _get_message(state, task_id)

    # Fren is drawn centered at cx=160 in a 320x300 viewBox
    COLORS = {
        "idle":   ("#c8e4ff", "#80b8f0", "#1a3a6a", "#3a70a0"),
        "timer":  ("#ffe8a8", "#e0a030", "#3a1800", "#805010"),
        "paused": ("#d8ccf8", "#9878e8", "#2a1060", "#5030a0"),
        "win":    ("#b8f0d4", "#50c880", "#0a3a18", "#1a6030"),
        "cheer":  ("#d8ccf8", "#9878e8", "#2a1060", "#5030a0"),
    }
    fill, stroke, eye_col, mouth_col = COLORS.get(state, COLORS["idle"])

    BUBBLE_COL = {"idle":"#80b8f0","timer":"#e0a030","paused":"#9878e8","win":"#50c880","cheer":"#9878e8"}
    bc = BUBBLE_COL.get(state, "#80b8f0")

    ANIM = {
        "idle":   "float 3.2s ease-in-out infinite",
        "timer":  "float 1.5s ease-in-out infinite",
        "paused": "float 4s ease-in-out infinite",
        "win":    "floatFast 0.85s ease-in-out infinite",
        "cheer":  "wiggle 0.6s ease-in-out infinite",
    }
    anim = ANIM.get(state, ANIM["idle"])

    ex, ey = 160, 150

    if state == "idle":
        eyes = f"""
        <ellipse cx="{ex-18}" cy="{ey}" rx="11" ry="7" fill="{eye_col}"/>
        <ellipse cx="{ex+18}" cy="{ey}" rx="11" ry="7" fill="{eye_col}"/>
        <rect x="{ex-29}" y="{ey-9}" width="22" height="8" rx="3" fill="{fill}"/>
        <rect x="{ex+7}" y="{ey-9}" width="22" height="8" rx="3" fill="{fill}"/>
        <ellipse cx="{ex-16}" cy="{ey-1}" rx="4" ry="3" fill="white" opacity=".7"/>
        <ellipse cx="{ex+20}" cy="{ey-1}" rx="4" ry="3" fill="white" opacity=".7"/>"""
    elif state == "timer":
        eyes = f"""
        <path d="M {ex-30} {ey-8} Q {ex-18} {ey-15} {ex-6} {ey-8}" fill="none" stroke="{eye_col}" stroke-width="2"/>
        <ellipse cx="{ex-18}" cy="{ey+2}" rx="11" ry="10" fill="{eye_col}"/>
        <path d="M {ex+6} {ey-8} Q {ex+18} {ey-15} {ex+30} {ey-8}" fill="none" stroke="{eye_col}" stroke-width="2"/>
        <ellipse cx="{ex+18}" cy="{ey+2}" rx="11" ry="10" fill="{eye_col}"/>
        <ellipse cx="{ex-15}" cy="{ey-1}" rx="4" ry="4" fill="white" opacity=".7"/>
        <ellipse cx="{ex+21}" cy="{ey-1}" rx="4" ry="4" fill="white" opacity=".7"/>"""
    elif state == "win":
        eyes = f"""
        <text x="{ex-30}" y="{ey+8}" font-family="Arial" font-size="20" fill="{eye_col}">★</text>
        <text x="{ex+10}" y="{ey+8}" font-family="Arial" font-size="20" fill="{eye_col}">★</text>"""
    else:
        eyes = f"""
        <ellipse cx="{ex-18}" cy="{ey}" rx="12" ry="13" fill="{eye_col}"/>
        <ellipse cx="{ex+18}" cy="{ey}" rx="12" ry="13" fill="{eye_col}"/>
        <ellipse cx="{ex-15}" cy="{ey-4}" rx="5" ry="5" fill="white" opacity=".7"/>
        <ellipse cx="{ex+21}" cy="{ey-4}" rx="5" ry="5" fill="white" opacity=".7"/>"""

    my = 174
    if state == "timer":
        mouth = f'<rect x="{ex-12}" y="{my+2}" width="24" height="4" rx="2" fill="{mouth_col}"/>'
    elif state in ("win", "cheer", "paused"):
        mouth = f'<path d="M {ex-20} {my} Q {ex} {my+20} {ex+20} {my}" fill="none" stroke="{mouth_col}" stroke-width="2.5" stroke-linecap="round"/>'
    else:
        mouth = f'<path d="M {ex-15} {my} Q {ex} {my+12} {ex+15} {my}" fill="none" stroke="{mouth_col}" stroke-width="2" stroke-linecap="round"/>'

    if state in ("win", "cheer"):
        arms = f"""
        <ellipse cx="{ex-86}" cy="132" rx="10" ry="19" fill="{fill}" stroke="{stroke}" stroke-width="1" transform="rotate(-45,{ex-86},132)"/>
        <ellipse cx="{ex+86}" cy="132" rx="10" ry="19" fill="{fill}" stroke="{stroke}" stroke-width="1" transform="rotate(45,{ex+86},132)"/>"""
    else:
        arms = f"""
        <ellipse cx="{ex-76}" cy="180" rx="10" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="1" transform="rotate(15,{ex-76},180)"/>
        <ellipse cx="{ex+76}" cy="180" rx="10" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="1" transform="rotate(-15,{ex+76},180)"/>"""

    extras = ""
    if state == "idle":
        extras = f'<text x="{ex+62}" y="120" font-family="Arial" font-size="12" fill="{stroke}">z</text><text x="{ex+72}" y="106" font-family="Arial" font-size="14" fill="{stroke}">z</text><text x="{ex+84}" y="90" font-family="Arial" font-size="16" fill="{stroke}">Z</text>'
    elif state == "timer":
        extras = f'<path d="M {ex+64} 124 Q {ex+68} 134 {ex+62} 140 Q {ex+56} 146 {ex+60} 133 Z" fill="#90d0f8" opacity=".8" style="animation:sweat 1.6s ease-in-out infinite"/>'
    if state in ("win", "cheer"):
        extras += f'<text x="{ex-95}" y="102" font-family="Arial" font-size="17" fill="#f8c020" style="animation:pop .8s infinite 0s">★</text><text x="{ex+75}" y="97" font-family="Arial" font-size="14" fill="#c088f0" style="animation:pop .8s infinite .3s">★</text>'
    if state in ("win", "cheer", "paused"):
        extras += f'<ellipse cx="{ex-32}" cy="164" rx="9" ry="6" fill="#f090b0" opacity=".4"/><ellipse cx="{ex+32}" cy="164" rx="9" ry="6" fill="#f090b0" opacity=".4"/>'
    if state == "win":
        extras += f'<ellipse cx="{ex}" cy="102" rx="16" ry="12" fill="#f8d020" stroke="#b09010" stroke-width=".6"/><rect x="{ex-8}" y="102" width="16" height="12" rx="1" fill="#f8d020" stroke="#b09010" stroke-width=".6"/><rect x="{ex-3}" y="114" width="6" height="8" rx="1" fill="#b09010"/><rect x="{ex-9}" y="121" width="18" height="4" rx="1" fill="#f8d020"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 300"
     style="width:100%;max-width:240px;display:block;margin:0 auto">
  <defs>
    <style>
      @keyframes float {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
      @keyframes floatFast {{0%,100%{{transform:translateY(0) rotate(-3deg)}}50%{{transform:translateY(-12px) rotate(3deg)}}}}
      @keyframes wiggle {{0%,100%{{transform:rotate(0)}}25%{{transform:rotate(-8deg)}}75%{{transform:rotate(8deg)}}}}
      @keyframes pop {{0%{{opacity:0;transform:scale(0)}}50%{{opacity:1;transform:scale(1.3)}}100%{{opacity:.8;transform:scale(1)}}}}
      @keyframes sweat {{0%,100%{{transform:translateY(0);opacity:.8}}50%{{transform:translateY(6px);opacity:.3}}}}
    </style>
  </defs>

  <!-- Speech bubble -->
  <rect x="172" y="12" width="136" height="62" rx="11" fill="white" stroke="{bc}" stroke-width="1"/>
  <polygon points="176,62 158,74 180,74" fill="white" stroke="{bc}" stroke-width="1"/>
  <foreignObject x="178" y="17" width="124" height="56">
    <div xmlns="http://www.w3.org/1999/xhtml"
         style="font-family:sans-serif;font-size:11px;color:#222;line-height:1.55">{msg}</div>
  </foreignObject>

  <!-- Fren animated group -->
  <g style="animation:{anim}">
    <ellipse cx="{ex-52}" cy="136" rx="12" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
    <ellipse cx="{ex+52}" cy="136" rx="12" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
    <ellipse cx="{ex}" cy="174" rx="60" ry="68" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
    {arms}
    {eyes}
    {mouth}
    {extras}
  </g>

  <!-- Name tag -->
  <rect x="124" y="258" width="72" height="20" rx="10" fill="#1a1a2e"/>
  <text x="160" y="273" text-anchor="middle"
        font-family="Helvetica Neue,Arial,sans-serif"
        font-size="10" font-weight="700" letter-spacing="2" fill="white">FREN</text>
</svg>"""

    components.html(svg, height=height, scrolling=False)