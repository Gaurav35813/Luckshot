"""
Luckshot - A Lucky Number Guessing Game
Streamlit App
"""

import streamlit as st
import random
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎰 Luckshot",
    page_icon="🎰",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto Mono', monospace;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Header ── */
.game-title {
    font-family: 'Oswald', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    letter-spacing: 6px;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.game-subtitle {
    text-align: center;
    color: #aaa;
    font-size: 0.85rem;
    letter-spacing: 3px;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* ── Cards ── */
.card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

/* ── Prize Table ── */
.prize-row {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #ddd;
    font-size: 0.9rem;
}
.prize-row:last-child { border-bottom: none; }
.prize-amount { color: #ffd200; font-weight: 600; }

/* ── Result Banners ── */
.result-win {
    background: linear-gradient(135deg, #1a472a, #2d6a4f);
    border: 2px solid #52b788;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    color: #b7e4c7;
    font-size: 1.2rem;
    font-weight: 600;
}
.result-lose {
    background: linear-gradient(135deg, #4a1942, #6d2b3d);
    border: 2px solid #c77dff;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    color: #e0aaff;
    font-size: 1.2rem;
}
.result-timeout {
    background: linear-gradient(135deg, #3d2c00, #6b4b00);
    border: 2px solid #ffc300;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    color: #ffd60a;
    font-size: 1.1rem;
}

/* ── Dice / number slots ── */
.slots {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 1rem 0;
}
.slot-box {
    width: 70px; height: 70px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Oswald', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    border: 2px solid;
}
.slot-hit  { background: rgba(82,183,136,0.2); border-color: #52b788; color: #b7e4c7; }
.slot-miss { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.15); color: #ccc; }

/* ── Buttons ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    color: #1a1a2e;
    font-family: 'Oswald', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 2px;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1.5rem;
    cursor: pointer;
    transition: opacity 0.2s;
}
div.stButton > button:hover { opacity: 0.85; }
div.stButton > button:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Number input ── */
input[type="number"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 1.4rem !important;
    text-align: center !important;
}

/* ── Ticket input ── */
.stNumberInput label { color: #aaa !important; font-size: 0.85rem !important; letter-spacing: 2px; }

/* ── Section labels ── */
.section-label {
    color: #888;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Ticker ── */
.timer-bar-container {
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    height: 8px;
    margin-top: 0.5rem;
    overflow: hidden;
}
.timer-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    transition: width 1s linear;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
def reset_game():
    st.session_state.update({
        "phase": "ticket",      # ticket → guessing → result
        "guess": None,
        "result": None,
        "lucky_numbers": [],
        "time_started": None,
        "timed_out": False,
    })

if "phase" not in st.session_state:
    reset_game()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<p class="game-title">🎰 LUCKSHOT</p>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">PICK YOUR NUMBER · WIN BIG MONEY</p>', unsafe_allow_html=True)

# ── Prize Table ───────────────────────────────────────────────────────────────
with st.expander("💰 Prize Structure", expanded=False):
    st.markdown("""
    <div class="card">
        <div class="prize-row"><span>🥇 First Lucky Number matches</span><span class="prize-amount">₹25</span></div>
        <div class="prize-row"><span>🥈 Second Lucky Number matches</span><span class="prize-amount">₹15</span></div>
        <div class="prize-row"><span>🥉 Third Lucky Number matches</span><span class="prize-amount">₹45</span></div>
        <div class="prize-row"><span>❌ No match</span><span class="prize-amount">₹0</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — Ticket Purchase
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "ticket":
    st.markdown('<p class="section-label">Step 1 · Buy Your Ticket</p>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card">The ticket costs exactly <b style="color:#ffd200">₹10</b>. '
        'Enter the correct amount to enter the game.</div>',
        unsafe_allow_html=True,
    )

    ticket_price = st.number_input(
        "ENTER TICKET PRICE (₹)",
        min_value=0, max_value=100,
        value=0, step=1,
        key="ticket_input",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💳  PAY & ENTER", key="pay_btn"):
            if ticket_price == 10:
                st.session_state.phase = "guessing"
                st.session_state.time_started = time.time()
                st.rerun()
            else:
                st.error("❌ Wrong amount! Please pay exactly ₹10 to play.")

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Guessing (with 10-second timer)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "guessing":
    elapsed = time.time() - st.session_state.time_started
    remaining = max(0, 10 - elapsed)

    st.markdown('<p class="section-label">Step 2 · Choose Your Lucky Number</p>', unsafe_allow_html=True)

    # Timer display
    pct = int((remaining / 10) * 100)
    color = "#52b788" if pct > 50 else "#ffc300" if pct > 20 else "#e63946"
    st.markdown(
        f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;color:#ccc;margin-bottom:0.4rem;">
                <span>⏱ Time Remaining</span>
                <span style="color:{color};font-weight:700">{remaining:.1f}s</span>
            </div>
            <div class="timer-bar-container">
                <div class="timer-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}cc);"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if remaining <= 0:
        # Timed out — auto-submit with no guess
        st.session_state.phase = "result"
        st.session_state.timed_out = True
        st.session_state.lucky_numbers = [
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
        ]
        st.rerun()

    guess = st.number_input(
        "PICK A NUMBER (0 – 9)",
        min_value=0, max_value=9,
        value=0, step=1,
        key="guess_input",
        disabled=(remaining <= 0),
    )

    if st.button("🎯  LOCK IN MY GUESS", disabled=(remaining <= 0)):
        st.session_state.guess = guess
        st.session_state.phase = "result"
        st.session_state.timed_out = False
        st.session_state.lucky_numbers = [
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
        ]
        st.rerun()

    # Auto-refresh every second so the timer updates
    time.sleep(1)
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — Result
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "result":
    a1, a2, a3 = st.session_state.lucky_numbers
    b = st.session_state.guess

    # Determine outcome
    if st.session_state.timed_out or b is None:
        outcome = "timeout"
        prize = 0
    elif b == a1:
        outcome = "win1"
        prize = 25
    elif b == a2:
        outcome = "win2"
        prize = 15
    elif b == a3:
        outcome = "win3"
        prize = 45
    else:
        outcome = "lose"
        prize = 0

    st.markdown('<p class="section-label">Result</p>', unsafe_allow_html=True)

    # Show lucky number slots
    slot_html = '<div class="slots">'
    for i, num in enumerate([a1, a2, a3]):
        hit = (b == num) and outcome != "timeout"
        css_class = "slot-hit" if hit else "slot-miss"
        slot_html += f'<div class="slot-box {css_class}">{num}</div>'
    slot_html += "</div>"
    st.markdown(
        f'<div class="card"><div class="section-label" style="text-align:center">🎲 Lucky Numbers Drawn</div>{slot_html}</div>',
        unsafe_allow_html=True,
    )

    # Your guess
    if not st.session_state.timed_out:
        st.markdown(
            f'<div class="card" style="text-align:center;color:#ccc;">Your Guess: '
            f'<span style="font-size:1.6rem;font-weight:700;color:#ffd200">{b}</span></div>',
            unsafe_allow_html=True,
        )

    # Result banner
    if outcome == "timeout":
        st.markdown(
            '<div class="result-timeout">⏰ Time\'s up! You didn\'t guess in time. Better luck next round!</div>',
            unsafe_allow_html=True,
        )
    elif outcome in ("win1", "win2", "win3"):
        medal = {"win1": "🥇", "win2": "🥈", "win3": "🥉"}[outcome]
        st.markdown(
            f'<div class="result-win">{medal} Congratulations! You matched a lucky number!<br>'
            f'<span style="font-size:2rem;color:#ffd200">You won ₹{prize}!</span></div>',
            unsafe_allow_html=True,
        )
        st.balloons()
    else:
        st.markdown(
            f'<div class="result-lose">😔 Sorry, <b>{b}</b> didn\'t match any lucky number this time.<br>'
            'Try again — your luck might change!</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  PLAY AGAIN"):
        reset_game()
        st.rerun()
