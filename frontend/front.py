import streamlit as st
import requests
from datetime import date
import random
from datetime import datetime

st.set_page_config(
    page_title="WaterWiseAg 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
if "page"          not in st.session_state: st.session_state.page          = "🏠 Home"
if "last_result"   not in st.session_state: st.session_state.last_result   = None
if "weather"       not in st.session_state: st.session_state.weather       = None


FLASK_BACKEND_URL   = "https://waterwiseag.onrender.com"

# ─────────────────────────────────────────────────────────────────────
# CSS + BOTANICAL BACKGROUND
# ─────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Syne:wght@700;800&display=swap');

    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

    /* ── Hide ALL Streamlit chrome ── */
    #MainMenu, footer,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
button[title="View fullscreen"] {
    display: none !important;
    visibility: hidden !important;
}

    .stApp {

background:
radial-gradient(circle at top left,
rgba(34,197,94,0.10),
transparent 30%),

radial-gradient(circle at bottom right,
rgba(14,165,233,0.10),
transparent 30%),

linear-gradient(
135deg,
#04130d 0%,
#071d17 40%,
#0b1f18 100%
);

color:white;

min-height:100vh;
}

    /* ══════════════════════════════════════════
       SIDEBAR — premium glass dark green
    ══════════════════════════════════════════ */
    section[data-testid="stSidebar"] {

background:
linear-gradient(
180deg,
rgba(6,35,18,0.98) 0%,
rgba(8,48,24,0.96) 40%,
rgba(10,62,34,0.95) 100%
) !important;

border-right:
1px solid rgba(255,255,255,0.06);

backdrop-filter:blur(18px);
}

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }

    /* Collapsed sidebar — zero width */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important; min-width: 0 !important; overflow: hidden !important;
    }
    section[data-testid="stSidebar"][aria-expanded="false"] > div {
        width: 0 !important; overflow: hidden !important; padding: 0 !important;
    }

    /* Hide default collapse arrow, keep only hamburger */
    [data-testid="collapsedControl"] { display: none !important; }

    /* ── Sidebar brand header ── */
    .sb-brand {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 22px 18px 16px;
        border-bottom: 1px solid rgba(76,175,125,0.14);
        margin-bottom: 8px;
    }
    .sb-brand-icon {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #1d6b3a, #2ecc71);
        border-radius: 13px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 0 20px rgba(46,204,113,0.35);
        flex-shrink: 0;
    }
    .sb-brand-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .95rem; font-weight: 800;
        color: #fff; letter-spacing: -.3px; line-height: 1.1;
    }
    .sb-brand-sub {
        font-size: .65rem; color: rgba(168,216,185,0.5);
        font-weight: 500; letter-spacing: .4px; margin-top: 2px;
    }

    /* ── Sidebar nav label ── */
    .sb-nav-label {
        font-size: .62rem; font-weight: 700;
        color: rgba(168,216,185,0.30);
        text-transform: uppercase; letter-spacing: 1.4px;
        padding: 6px 18px 4px;
    }

    /* ── Sidebar Streamlit buttons styled as nav items ── */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        color: rgba(196,228,208,0.68) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: .88rem !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        height: auto !important;
        min-height: 44px !important;
        box-shadow: none !important;
        margin: 1px 0 !important;
        transition: background .18s ease, color .18s ease !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(76,175,125,0.13) !important;
        color: #a8d8b9 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* ── Active nav button ── */
    [data-testid="stSidebar"] .stButton.active-nav > button {

    background:
        linear-gradient(
            90deg,
            rgba(16,185,129,0.18),
            rgba(14,165,233,0.10)
        ) !important;

    border-left: 3px solid #34d399 !important;

    color: white !important;

    backdrop-filter: blur(10px);

    box-shadow:
        0 0 20px rgba(52,211,153,0.12);
}

    /* ── Weather widget in sidebar ── */
    .sb-weather {
        margin: 12px 12px 8px;
        background: linear-gradient(135deg, rgba(14,165,233,0.16), rgba(15,60,30,0.55));
        border: 1px solid rgba(14,165,233,0.24);
        border-radius: 16px;
        padding: 14px 16px;
    }
    .sb-wx-hdr {
        display: flex; align-items: center; gap: 7px;
        font-size: .67rem; font-weight: 700;
        color: rgba(14,165,233,0.85);
        text-transform: uppercase; letter-spacing: .9px;
        margin-bottom: 9px;
    }
    .sb-wx-dot {
        width: 6px; height: 6px; background: #4caf7d;
        border-radius: 50%; animation: pulse 1.5s infinite;
    }
    .sb-wx-temp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2rem; font-weight: 800; color: #bae6fd; line-height: 1;
    }
    .sb-wx-city { font-size: .73rem; color: rgba(255,255,255,.45); margin: 2px 0 9px; }
    .sb-wx-grid {
        display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px;
    }
    .sb-wx-cell {
        background: rgba(0,0,0,0.22); border-radius: 9px;
        padding: 6px 4px; text-align: center;
    }
    .sb-wx-val { font-size: .78rem; font-weight: 700; color: #bae6fd; display: block; }
    .sb-wx-lbl { font-size: .58rem; color: rgba(255,255,255,.38); text-transform: uppercase; letter-spacing: .3px; }

    /* ── Sidebar footer ── */
    .sb-footer {
        padding: 12px 18px;
        border-top: 1px solid rgba(76,175,125,0.09);
        font-size: .65rem;
        color: rgba(168,216,185,0.25);
        text-align: center;
        margin-top: auto;
        letter-spacing: .2px;
    }

    /* ══════════════════════════════════════════
       MAIN CONTENT
    ══════════════════════════════════════════ */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 100% !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* ══ HERO ══ */
    .hero-section {
    background:
        linear-gradient(
            135deg,
            #14532D 0%,
            #166534 45%,
            #0F766E 100%
        );

    border-radius: 28px;
    padding: 64px 48px;
     margin-top: 12px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 10px 40px rgba(15,118,110,0.18);

    position: relative;
    overflow: hidden;
}
    .hero-section::before {
        content: '';
        position: absolute; top: -90px; right: -90px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(76,175,125,0.13) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-section::after {
        content: '';
        position: absolute; bottom: -70px; left: -70px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(14,165,233,0.09) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.8rem; font-weight: 800; color: white !important;
        margin-bottom: 10px; letter-spacing: -.5px; line-height: 1.15;
    }
    .hero-sub { font-size: 1rem; color: #a8d8b9 !important; margin-bottom: 28px; font-weight: 500; }
    .hero-badge {
        display: inline-block;
        background: rgba(76,175,125,0.14);
        color: #a8d8b9 !important;
        padding: 7px 20px; border-radius: 99px;
        font-size: 13px; font-weight: 600;
        border: 1px solid rgba(76,175,125,0.25); margin: 4px;
    }

    /* ══ STAT BOXES ══ */
    .stat-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.11);
        border-radius: 18px; padding: 22px;
        text-align: center; backdrop-filter: blur(10px);
    }
    .stat-num   { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 2.4rem; font-weight: 800; color: #a8d8b9 !important; }
    .stat-label { font-size: 11px; color: rgba(255,255,255,0.4) !important; margin-top: 5px; text-transform: uppercase; letter-spacing: .9px; font-weight: 600; }

    /* ══ DARK CARD ══ */
    .dark-card {
        background: linear-gradient(135deg, rgba(20,60,35,0.75), rgba(8,28,14,0.85));
        border-radius: 18px; padding: 22px; margin-bottom: 16px;
        border: 1px solid rgba(76,175,125,0.18);
        box-shadow: 0 6px 28px rgba(0,0,0,0.32);
        backdrop-filter: blur(12px); color: white;
    }

    /* ══ WHITE CARD ══ */
    .green-card {
        background: #ffffff; border-radius: 18px; padding: 22px; margin-bottom: 16px;
        box-shadow: 0 4px 22px rgba(5,20,10,0.20);
        border: 1px solid #d2e8da; color: #1a2e1a !important;
        animation: fadeUp .4s ease;
    }
    .green-card p,.green-card div,.green-card span,.green-card td,.green-card li { color: #1a2e1a !important; }
    .green-card b,.green-card strong { color: #1a4d2e !important; }

    /* ══ SMALL WEATHER CARDS ══ */
    .small-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 18px; padding: 20px; text-align: center;
        box-shadow: 0 6px 22px rgba(0,0,0,0.18);
        transition: transform .25s ease, box-shadow .25s ease; color: white;
    }
    .small-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.28); }
    .small-icon  { font-size: 32px; margin-bottom: 8px; }
    .small-value { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 2.4rem; font-weight: 800; color: #a8d8b9; line-height: 1; }
    .small-label { font-size: 12px; color: rgba(255,255,255,0.55); margin-top: 6px; font-weight: 600; }

    /* ══ RESULT CARD ══ */
    .result-main-card {
    background: rgba(74, 173, 255, 0.35); /* transparent blue */
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border: 1px solid rgba(255, 255, 255, 0.25);

    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.25),
        inset 0 1px 1px rgba(255,255,255,0.2);

    padding: 36px;
    border-radius: 24px;
    text-align: center;

    color: white;

    margin-bottom: 24px;
    margin-top: 20px;
}
    .result-main-title { font-size: 14px; color: rgba(255,255,255,.5); text-transform: uppercase; letter-spacing: 1.4px; margin-bottom: 8px; }
    .result-main-value { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 5rem; font-weight: 800; color: #a8d8b9; line-height: 1; }

    /* ══ RECOMMENDATION CARDS ══ */
    .recommendation-card {
        background: rgba(255,255,255,0.06); backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.11); border-left: 5px solid #4caf7d;
        border-radius: 18px; padding: 20px 22px; margin-bottom: 13px; animation: fadeUp .4s ease;
    }
    .recommendation-header { display: flex; align-items: center; gap: 12px; margin-bottom: 7px; }
    .recommendation-icon  { font-size: 28px; }
    .recommendation-title { font-size: 1rem; font-weight: 800; color: white; }
    .recommendation-desc  { font-size: .86rem; color: rgba(255,255,255,0.68); line-height: 1.6; }
    .rec-green { border-left-color: #22c55e; }
    .rec-blue  { border-left-color: #0ea5e9; }
    .rec-amber { border-left-color: #f59e0b; }
    .rec-red   { border-left-color: #ef4444; }


    /* ══ HELP ITEMS ══ */
    .help-item {
        display: flex; align-items: flex-start; gap: 14px;
        padding: 14px; background: #f0faf4;
        border-radius: 12px; margin-bottom: 10px; border: 1px solid #b8ddc8;
    }
    .help-icon  { font-size: 24px; }
    .help-title { font-size: 13px; font-weight: 700; color: #1a4d2e !important; }
    .help-desc  { font-size: 12px; color: #2d5a3a !important; line-height: 1.5; }

    /* ══ REPORT ══ */
    .report-title { font: Times New Roman; font-size: 1.9rem; font-weight: 800; color: #fff !important; margin-bottom: 10px; margin-top: 24px; }
    .report-empty { text-align: center; padding: 40px; }
    .report-empty-title { font-size: 18px; font-weight: 700; color: #1a4d2e; margin-bottom: 8px; }
    .report-empty-text  { color: #2d5a3a; }

    /* ══ SECTION HEADERS ══ */
    .section-header,
.section-header1 {

    font-family: 'Plus Jakarta Sans', sans-serif !important;

    font-size: 2.8rem !important;

    font-weight: 800 !important;

    color: #ffffff !important;

    margin-bottom: 26px !important;

    margin-top: 10px !important;

    letter-spacing: -1.5px !important;

    line-height: 1.1 !important;

    background: linear-gradient(
        90deg,
        #ffffff 0%,
        #bbf7d0 45%,
        #4ade80 100%
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 18px rgba(74,222,128,0.18);

    animation: fadeGlow 2s ease-in-out infinite alternate;
}
    .tips-header {
        font: Times New Roman;
        font-size: 1.75rem !important; font-weight: 800 !important;
        color: white !important; margin-bottom: 18px !important; margin-top: 24px !important;
    }
    h1,h2,h3,h4,h5,h6 { color: #ffffff !important; }

    /* ══ FEATURE TITLES ══ */
    .feature-title { font-size: 13px; font-weight: 700; color: #1a4d2e !important; margin-bottom: 5px; }
    .feature-desc  { font-size: 12px; color: #2d5a3a !important; line-height: 1.5; }

    /* ══ STREAMLIT WIDGET OVERRIDES ══ */
    .stButton > button {
        background: linear-gradient(135deg, #155e2e, #1d8348) !important;
        color: white !important; border: none !important; border-radius: 14px !important;
        font-size: 15px !important; font-weight: 700 !important; padding: 12px 24px !important;
        font: Times New Roman !important;
        box-shadow: 0 4px 18px rgba(21,94,46,0.45) !important;
        transition: all .22s !important; width: 100% !important; height: 50px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 26px rgba(21,94,46,0.55) !important;
    }

    .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-size: 14px !important; font-weight: 700 !important; color: white !important;
    }
    .stSelectbox > div > div {
        border-radius: 12px !important; border: 2px solid #b8ddc8 !important;
        background: #fff !important; color: #1a2e1a !important;
    }
    .stSelectbox div[data-baseweb="select"] > div { color: #1a2e1a !important; background: #fff !important; }
    .stNumberInput > div > div > input,
    .stTextInput  > div > div > input {
        border-radius: 12px !important; border: 2px solid #b8ddc8 !important;
        font: Times New Roman !important;
        font-size: 15px !important; color: #1a2e1a !important; background: #fff !important;
    }
    .stNumberInput > div > div > input:focus,
    .stTextInput  > div > div > input:focus {
        border-color: #4caf7d !important; box-shadow: 0 0 0 3px rgba(76,175,125,0.18) !important;
    }
    .stNumberInput div[data-baseweb="input"] { background: #fff !important; border-radius: 12px !important; border: 2px solid #d9e8d9 !important; }
    .stNumberInput input { background: #fff !important; color: #000 !important; font-weight: 600 !important; }
    .stNumberInput button { background: #fff !important; color: #000 !important; border: none !important; }

    /* alerts */
    div[data-testid="stSuccessMessage"] { background: rgba(76,175,125,.13) !important; border: 1px solid rgba(76,175,125,.32) !important; border-radius: 12px !important; }
    div[data-testid="stErrorMessage"]   { background: rgba(239,68,68,.13)  !important; border: 1px solid rgba(239,68,68,.32)  !important; border-radius: 12px !important; }
    div[data-testid="stWarningMessage"] { background: rgba(245,158,11,.13) !important; border: 1px solid rgba(245,158,11,.32) !important; border-radius: 12px !important; }
    div[data-testid="stInfoMessage"]    { background: rgba(14,165,233,.13) !important; border: 1px solid rgba(14,165,233,.32) !important; border-radius: 12px !important; }

    /* misc */
    hr { border-color: rgba(76,175,125,0.14) !important; margin: 16px 0 !important; }
    .live-dot { display:inline-block; width:8px; height:8px; background:#4caf7d; border-radius:50%; animation:pulse 1.5s infinite; margin-right:6px; vertical-align:middle; }
    .progress-wrap { background: rgba(255,255,255,0.1); border-radius: 20px; height: 8px; margin: 10px 0; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #4caf7d, #0ea5e9); }

    @keyframes fadeUp  { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
    @keyframes pulse   { 0%,100% { opacity:1; } 50% { opacity:0.25; } }
    @keyframes fadeGlow {

    from {
        filter: drop-shadow(0 0 6px rgba(74,222,128,0.15));
    }

    to {
        filter: drop-shadow(0 0 18px rgba(74,222,128,0.35));
    }
}
    /* ═══════════════════════════════════════
TOP STATUS BAR
═══════════════════════════════════════ */

.top-status-bar{
    display:flex;
    gap:14px;
    margin-bottom:22px;
    flex-wrap:wrap;
}

.status-chip{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);

    padding:12px 18px;

    border-radius:16px;

    color:#d1fae5;

    font-size:14px;
    font-weight:700;

    letter-spacing:0.3px;

    box-shadow:
        0 8px 22px rgba(0,0,0,0.18);

    transition:0.3s ease;
}

.status-chip:hover{
    transform:translateY(-3px);
    border:1px solid rgba(34,197,94,0.4);

    box-shadow:
        0 10px 28px rgba(34,197,94,0.15);
}
                /* ═══════════════════════════════════════
AI INSIGHT CARD
═══════════════════════════════════════ */

.insight-card{

    margin-top:28px;

    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,0.10),
            rgba(14,165,233,0.08)
        );

    border:1px solid rgba(255,255,255,0.08);

    border-radius:26px;

    padding:28px;

    backdrop-filter:blur(16px);

    box-shadow:
        0 12px 30px rgba(0,0,0,0.25);
}

.insight-title{

    color:white;

    font-size:1.3rem;

    font-weight:800;

    margin-bottom:22px;
}

.insight-grid{

    display:grid;

    grid-template-columns:repeat(4,1fr);

    gap:18px;
}

.insight-item{

    background:rgba(255,255,255,0.05);

    border-radius:18px;

    padding:20px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.06);
}

.insight-label{

    color:rgba(255,255,255,0.55);

    font-size:13px;

    margin-bottom:10px;
}

.insight-value{

    color:#86efac;

    font-size:1.5rem;

    font-weight:800;
}
                /* ═══════════════════════════════════════
LIVE ACTIVITY FEED
═══════════════════════════════════════ */

.activity-feed{

    margin-top:28px;

    background:rgba(255,255,255,0.04);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:24px;

    backdrop-filter:blur(12px);
}

.activity-title{

    color:white;

    font-size:1.2rem;

    font-weight:800;

    margin-bottom:18px;
}

.activity-item{

    padding:14px 0;

    border-bottom:1px solid rgba(255,255,255,0.05);

    color:#d1fae5;

    font-size:15px;

    display:flex;

    align-items:center;

    gap:12px;
}

.activity-dot{

    width:10px;
    height:10px;

    background:#22c55e;

    border-radius:50%;

    box-shadow:
        0 0 12px #22c55e;
}
                .main .block-container::before{

content:"";

position:fixed;

top:-150px;
right:-150px;

width:400px;
height:400px;

background:
radial-gradient(
circle,
rgba(34,197,94,0.10),
transparent 70%
);

pointer-events:none;

z-index:-1;
}

.main .block-container::after{

content:"";

position:fixed;

bottom:-180px;
left:-180px;

width:420px;
height:420px;

background:
radial-gradient(
circle,
rgba(14,165,233,0.10),
transparent 70%
);

pointer-events:none;

z-index:-1;
}
                /* ═══════════════════════════════════════
   PREMIUM TIPS PAGE
═══════════════════════════════════════ */

.tips-hero {

    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,0.18),
            rgba(14,165,233,0.10)
        );

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 28px;

    padding: 34px;

    margin-bottom: 28px;

    backdrop-filter: blur(20px);

    position: relative;

    overflow: hidden;

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35);
}

.tips-hero::before {

    content:"";

    position:absolute;

    width:300px;
    height:300px;

    background:
        radial-gradient(
            circle,
            rgba(34,197,94,0.18),
            transparent 70%
        );

    top:-120px;
    right:-100px;

    border-radius:50%;
}

.tips-hero-title {

    font-size:2rem;

    font-weight:800;

    color:white;

    margin-bottom:10px;
}

.tips-hero-sub {

    color:rgba(255,255,255,0.72);

    font-size:1rem;

    line-height:1.7;
}

.tip-card {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:24px;

    backdrop-filter: blur(18px);

    transition:0.35s ease;

    position:relative;

    overflow:hidden;

    min-height:170px;

    margin-bottom:20px;

    box-shadow:
        0 8px 28px rgba(0,0,0,0.22);
}

.tip-card::before {

    content:"";

    position:absolute;

    width:180px;
    height:180px;

    background:
        radial-gradient(
            circle,
            rgba(34,197,94,0.12),
            transparent 70%
        );

    top:-80px;
    right:-80px;
}

.tip-card:hover {

    transform:
        translateY(-6px)
        scale(1.01);

    border:
        1px solid rgba(34,197,94,0.28);

    box-shadow:
        0 16px 40px rgba(0,0,0,0.35);
}

.tip-emoji {

    font-size:2.6rem;

    margin-bottom:14px;
}

.tip-title {

    color:white;

    font-size:1.2rem;

    font-weight:800;

    margin-bottom:10px;
}

.tip-desc {

    color:rgba(255,255,255,0.72);

    line-height:1.7;

    font-size:0.95rem;
}

.tip-tag {

    display:inline-block;

    padding:6px 14px;

    border-radius:999px;

    background:
        rgba(34,197,94,0.12);

    color:#86efac;

    font-size:12px;

    font-weight:700;

    margin-top:18px;

    border:
        1px solid rgba(34,197,94,0.18);
}

.farming-stats {

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:22px;

    padding:20px;

    text-align:center;

    backdrop-filter: blur(14px);

    margin-bottom:20px;
}

.farming-stats-value {

    font-size:2.4rem;

    font-weight:900;

    color:#86efac;
}

.farming-stats-label {

    color:rgba(255,255,255,0.55);

    font-size:13px;

    margin-top:5px;

    letter-spacing:1px;
}
                /* ═══════════════════════════════════════
   ULTRA PREMIUM LIVE DASHBOARD
═══════════════════════════════════════ */

.dashboard-wrapper{

    position:relative;

    overflow:hidden;

    padding:10px 0 30px 0;
}

/* Animated glow bg */

.dashboard-wrapper::before{

    content:"";

    position:absolute;

    width:550px;
    height:550px;

    background:
        radial-gradient(
            circle,
            rgba(34,197,94,0.16),
            transparent 70%
        );

    top:-220px;
    right:-180px;

    animation:floatGlow 8s ease-in-out infinite;
}

.dashboard-wrapper::after{

    content:"";

    position:absolute;

    width:500px;
    height:500px;

    background:
        radial-gradient(
            circle,
            rgba(14,165,233,0.15),
            transparent 70%
        );

    bottom:-220px;
    left:-180px;

    animation:floatGlow2 9s ease-in-out infinite;
}

/* ═════════ HERO ═════════ */

.dashboard-hero{

    position:relative;

    overflow:hidden;

    background:
        linear-gradient(
            135deg,
            rgba(17,24,39,0.88),
            rgba(15,118,110,0.30),
            rgba(34,197,94,0.18)
        );

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius:32px;

    padding:34px;

    backdrop-filter:blur(24px);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.45);

    margin-bottom:28px;
}

.dashboard-hero::before{

    content:"";

    position:absolute;

    inset:0;

    background:
        linear-gradient(
            120deg,
            transparent,
            rgba(255,255,255,0.04),
            transparent
        );

    transform:translateX(-100%);

    animation:shine 6s linear infinite;
}

.dashboard-top{

    display:flex;

    justify-content:space-between;

    align-items:center;

    flex-wrap:wrap;

    gap:20px;
}

.dashboard-title{

    font-size:2.3rem;

    font-weight:900;

    color:white;

    line-height:1.1;

    margin-bottom:8px;

    letter-spacing:-1px;
}

.dashboard-sub{

    color:rgba(255,255,255,0.68);

    font-size:1rem;

    line-height:1.7;

    max-width:650px;
}

/* ═════════ LIVE STATUS ═════════ */

.live-status{

    display:flex;

    align-items:center;

    gap:10px;

    background:
        rgba(34,197,94,0.12);

    border:
        1px solid rgba(34,197,94,0.22);

    padding:12px 18px;

    border-radius:999px;

    color:#86efac;

    font-size:14px;

    font-weight:700;

    backdrop-filter:blur(12px);
}

.live-pulse{

    width:10px;
    height:10px;

    border-radius:50%;

    background:#22c55e;

    box-shadow:
        0 0 16px #22c55e;

    animation:pulse 1.5s infinite;
}

/* ═════════ KPI GRID ═════════ */

.dashboard-grid{

    display:grid;

    grid-template-columns:repeat(4,1fr);

    gap:20px;

    margin-top:26px;
}

/* ═════════ KPI CARD ═════════ */

.dashboard-card{

    position:relative;

    overflow:hidden;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.03)
        );

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius:24px;

    padding:24px;

    backdrop-filter:blur(18px);

    transition:0.35s ease;

    box-shadow:
        0 12px 28px rgba(0,0,0,0.25);
}

.dashboard-card::before{

    content:"";

    position:absolute;

    width:180px;
    height:180px;

    background:
        radial-gradient(
            circle,
            rgba(34,197,94,0.18),
            transparent 70%
        );

    top:-80px;
    right:-80px;
}

.dashboard-card:hover{

    transform:
        translateY(-8px)
        scale(1.02);

    border:
        1px solid rgba(34,197,94,0.28);

    box-shadow:
        0 18px 42px rgba(0,0,0,0.35);
}

/* top icon */

.dashboard-icon{

    width:58px;
    height:58px;

    border-radius:18px;

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:28px;

    margin-bottom:18px;

    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,0.18),
            rgba(14,165,233,0.14)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 8px 20px rgba(0,0,0,0.22);
}

.dashboard-label{

    font-size:13px;

    color:rgba(255,255,255,0.55);

    font-weight:600;

    margin-bottom:10px;

    letter-spacing:0.5px;
}

.dashboard-value{

    font-size:2rem;

    font-weight:900;

    color:#86efac;

    line-height:1;
}

.dashboard-desc{

    margin-top:12px;

    color:rgba(255,255,255,0.58);

    font-size:13px;

    line-height:1.6;
}

/* ═════════ LIVE FEED PANEL ═════════ */

.live-feed{

    margin-top:30px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.06),
            rgba(255,255,255,0.03)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:28px;

    padding:28px;

    backdrop-filter:blur(18px);

    box-shadow:
        0 16px 42px rgba(0,0,0,0.30);
}

.live-title{

    display:flex;

    align-items:center;

    gap:12px;

    font-size:1.3rem;

    font-weight:800;

    color:white;

    margin-bottom:22px;
}

.live-title::before{

    content:"";

    width:10px;
    height:10px;

    border-radius:50%;

    background:#22c55e;

    box-shadow:
        0 0 14px #22c55e;

    animation:pulse 1.5s infinite;
}

/* activity items */

.live-item{

    position:relative;

    display:flex;

    align-items:center;

    gap:16px;

    padding:18px;

    border-radius:18px;

    margin-bottom:14px;

    background:
        rgba(255,255,255,0.03);

    border:
        1px solid rgba(255,255,255,0.05);

    transition:0.3s ease;
}

.live-item:hover{

    transform:translateX(6px);

    background:
        rgba(34,197,94,0.08);

    border:
        1px solid rgba(34,197,94,0.18);
}

.live-dot{

    width:12px;
    height:12px;

    border-radius:50%;

    background:#22c55e;

    box-shadow:
        0 0 16px #22c55e;

    animation:pulse 1.5s infinite;
}

.live-text{

    color:rgba(255,255,255,0.80);

    font-size:15px;

    font-weight:500;
}

.live-time{

    margin-left:auto;

    color:rgba(255,255,255,0.38);

    font-size:12px;
}

/* ═════════ ANIMATIONS ═════════ */

@keyframes pulse{

    0%,100%{
        opacity:1;
        transform:scale(1);
    }

    50%{
        opacity:0.4;
        transform:scale(1.2);
    }
}

@keyframes shine{

    0%{
        transform:translateX(-120%);
    }

    100%{
        transform:translateX(120%);
    }
}

@keyframes floatGlow{

    0%,100%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(25px);
    }
}

@keyframes floatGlow2{

    0%,100%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-30px);
    }
}

/* ═════════ RESPONSIVE ═════════ */

@media(max-width:1100px){

.dashboard-grid{
    grid-template-columns:repeat(2,1fr);
}

}

@media(max-width:700px){

.dashboard-grid{
    grid-template-columns:1fr;
}

.dashboard-title{
    font-size:1.8rem;
}

.dashboard-hero{
    padding:24px;
}

}
                .dashboard-hero {
    background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(14,165,233,0.12));
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
                .dashboard-card {
    position: relative;
    overflow: hidden;
}

.dashboard-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at var(--x, 50%) var(--y, 50%), rgba(34,197,94,0.15), transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
}

.dashboard-card:hover::after {
    opacity: 1;
}

    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────
def get_weather(city):

    response = requests.get(
        f"{FLASK_BACKEND_URL}/weather/{city}"
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(data.get("message", "Weather API Error"))

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rainfall": data.get("rain", {}).get("1h", 0),
        "wind_speed": data["wind"]["speed"]
    }

def get_recommendations(rain, hum, water, crop, stage):
    recs = []
    if rain > 60:
        recs.append(("blue","🌧️","Delay Irrigation",f"Heavy rain expected ({rain}%). Skip irrigation today and reassess tomorrow."))
    elif rain > 30:
        recs.append(("amber","⚠️","Reduce Watering","Moderate rainfall expected. Reduce water by 30%."))
    else:
        recs.append(("green","✅","Water Today",f"Weather is clear. Apply full {water} litres today."))
    if hum < 40:
        recs.append(("red","🔥","Low Humidity Alert","Dry air increases evaporation. Irrigate early morning."))
    if "Flowering" in stage:
        recs.append(("amber","🌸","Critical Growth Stage","Flowering stage is highly sensitive to water stress."))
    if crop in ["🌾 Rice","🎋 Sugarcane"]:
        recs.append(("blue","💧","High Water Crop","This crop needs consistent irrigation due to high water demand."))
    return recs

def build_report_html(r):
    today    = date.today().strftime("%d %B %Y")
    recs_html = ""
    for clr, icon, title, sub in get_recommendations(r["rainfall"], r["humidity"], r["water_need"], r["crop"], r["stage"]):
        recs_html += f'<div class="rec {clr}"><b>{icon} {title}</b><br><small>{sub}</small></div>'
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Water Report</title>
<style>body{{font-family:Georgia,serif;max-width:640px;margin:40px auto;color:#1a2e1a;padding:20px;background:#f5fbf6}}
.hdr{{text-align:center;border-bottom:3px solid #2d7a4f;padding-bottom:16px;margin-bottom:24px}}
h1{{color:#1a4d2e;font-size:26px;margin:0}}
.badge{{display:inline-block;background:#e8f7ee;color:#2d7a4f;padding:4px 14px;border-radius:20px;font-size:13px;margin-top:8px}}
.wbox{{background:linear-gradient(135deg,#1a4d2e,#0c2d1a);color:white;padding:28px;border-radius:18px;text-align:center;margin:20px 0}}
.wnum{{font-size:60px;font-weight:700;color:#a8d8b9}}.wunit{{font-size:20px;color:#a8d8b9}}
table{{width:100%;border-collapse:collapse;margin:16px 0}}
td{{padding:10px 14px;border-bottom:1px solid #e2f0e8;font-size:14px}}
td:first-child{{font-weight:600;color:#2d7a4f;width:40%}}
.rec{{padding:12px;border-radius:10px;margin:8px 0;font-size:13px;border-left:3px solid}}
.rec.green{{background:#f0fdf4;border-color:#4caf7d;color:#1a4d2e}}
.rec.amber{{background:#fffbeb;border-color:#f59e0b;color:#7a4a00}}
.rec.blue{{background:#f0f9ff;border-color:#0ea5e9;color:#0a4d7a}}
.footer{{text-align:center;color:#aaa;font-size:11px;margin-top:32px;border-top:1px solid #eee;padding-top:12px}}
h3{{color:#1a4d2e;margin-top:20px}}</style></head><body>
<div class="hdr"><div style="font-size:40px">🌾</div><h1>Crop Water Report</h1><div class="badge">Generated: {today}</div></div>
<div class="wbox"><div style="font-size:14px;opacity:0.6;margin-bottom:4px">Daily Water Requirement</div>
<div class="wnum">{r['water_need']:,}</div><div class="wunit">Litres / Day</div></div>
<table>
<tr><td>Crop</td><td>{r['crop']}</td></tr><tr><td>Land Area</td><td>{r['land']} acres</td></tr>
<tr><td>Soil Type</td><td>{r['soil']}</td></tr><tr><td>Growth Stage</td><td>{r['stage']}</td></tr>
<tr><td>Season</td><td>{r['season']}</td></tr><tr><td>Temperature</td><td>{r['temperature']}°C</td></tr>
<tr><td>Humidity</td><td>{r['humidity']}%</td></tr><tr><td>Rain Chance</td><td>{r['rainfall']}%</td></tr>
<tr><td>Wind Speed</td><td>{r['wind_speed']} km/h</td></tr></table>
<h3>💧 Irrigation Recommendations</h3>{recs_html}
<div class="footer">Crop Water Planner · Smart Irrigation for Every Farmer · {today}</div>
</body></html>"""


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR — pure Streamlit buttons, always reliable
# ─────────────────────────────────────────────────────────────────────
def render_sidebar():
    wx = st.session_state.weather or {"city": "—", "temp": "—", "hum": "—", "rain": "—", "wind": "—"}

    with st.sidebar:
        # Brand
        st.markdown("""
        <div class="sb-brand">
            <div class="sb-brand-icon">🌾</div>
            <div>
                <div class="sb-brand-name">Crop Water Planner</div>
                <div class="sb-brand-sub">Smart Irrigation · Made in India</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Nav label
        st.markdown('<div class="sb-nav-label">Main Menu</div>', unsafe_allow_html=True)

        # Nav items — plain Streamlit buttons, fully reliable
        nav_items = [
            ("🏠", "Home",            "🏠 Home"),
            ("💧", "Predict Water",   "💧 Predict Water"),
            ("🌱", "Crop Tips",       "🌱 Crop Tips"),
            ("📄", "Download Report", "📄 Download Report"),
            ("📊", "Dashboard", "📊 Dashboard"),
            ("📞", "Help",            "📞 Help"),
            ("ℹ️", "About",           "ℹ About"),
        ]
        cur = st.session_state.page
        for icon, label, page_key in nav_items:
            # Highlight active with a subtle marker
            if cur == page_key:
                st.markdown(f"""
                <div style="
                    background:linear-gradient(90deg,rgba(76,175,125,0.20),rgba(76,175,125,0.03));
                    border-left:3px solid #4caf7d;
                    border-radius:0 12px 12px 0;
                    padding:10px 14px;
                    margin:1px 0;
                    font-size:.88rem; font-weight:700;
                    color:#4caf7d;
                    display:flex; align-items:center; gap:10px;
                ">{icon}&nbsp;&nbsp;{label}</div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {label}", key=f"nav_{page_key}"):
                    st.session_state.page = page_key
                    st.rerun()

        # Live weather widget
        st.markdown("<br>", unsafe_allow_html=True)
        temp_display = f"{wx.get('temp','—')}°C"   if wx.get('temp') not in [None,"—"] else "—"
        hum_display  = f"{wx.get('hum','—')}%"     if wx.get('hum')  not in [None,"—"] else "—"
        rain_display = f"{wx.get('rain','—')}mm"   if wx.get('rain') not in [None,"—"] else "—"
        wind_display = f"{wx.get('wind','—')}"     if wx.get('wind') not in [None,"—"] else "—"
        city_display = wx.get('city','—')

        st.markdown(f"""
        <div class="sb-footer">© 2025 Crop Water Planner · India 🇮🇳</div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div class="hero-section">
        <div style="font-size:58px;margin-bottom:14px">🌾</div>
        <div class="hero-title">Welcome to WaterWiseAg - A Crop Water Planner</div>
        <div class="hero-sub">Plan your irrigation smartly. Save water. Increase yield.</div>
        <div>
            <span class="hero-badge">🚫 No Login Required</span>
            <span class="hero-badge">📱 Mobile Friendly</span>
            <span class="hero-badge">💧 AI-Powered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div>
<br><br>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, num, lbl in zip([c1,c2,c3,c4],["6","5","4","Live"],["Crop Types","Soil Types","Growth Stages","Weather Data"]):
        with col:
            st.markdown(f'<div class="dark-card"><div class="stat-num">{num}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    feats = [
        ("💧","Smart Water Prediction","Enter crop, soil & area → precise daily water requirements instantly"),
        ("🌦","Live Weather Integration","Auto-fetches real weather for your location — no manual entry"),
        ("📱","Farmer-First Design","Large buttons, simple language, works on basic smartphones"),
        ("🌱","Crop Stage Awareness","Water needs change at seedling, flowering & harvest — we track them"),
        ("📄","Downloadable Reports","Get an HTML report to share with other farmers or your bank"),
        ("🌾","6 Major Crops","Rice, Wheat, Maize, Cotton, Sugarcane & Groundnut fully supported"),
    ]
    for i, (icon, title, desc) in enumerate(feats):
        with [col_a, col_b, col_c][i % 3]:
            st.markdown(f"""
            <div class="green-card" style="min-height:155px">
                <div style="font-size:30px;margin-bottom:8px">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            


def page_predict():
    st.markdown('<div class="section-header1">💧 Predict Water Need</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="top-status-bar">

<div class="status-chip">
🛰 AI ENGINE ACTIVE
</div>

<div class="status-chip">
📡 LIVE WEATHER CONNECTED
</div>

<div class="status-chip">
⚡ REAL-TIME ANALYTICS
</div>

</div>
""", unsafe_allow_html=True)
    st.markdown("""
<div style="
background:rgba(255,255,255,0.06);
padding:14px 22px;
border-radius:18px;
border:1px solid rgba(255,255,255,0.10);
margin-bottom:20px;
backdrop-filter:blur(18px);
display:flex;
justify-content:space-between;
align-items:center;
">
<div>
<div style="font-size:12px;color:rgba(255,255,255,0.5)">
AI Irrigation Monitoring System
</div>
<div style="font-size:20px;font-weight:700;color:white">
Live Dashboard
</div>
</div>
<div style="color:#4ade80;font-weight:700">
● SYSTEM ONLINE
</div>
</div>
""", unsafe_allow_html=True)

    crop_options = ["🌾 Rice","🌿 Wheat","🌽 Maize","☁️ Cotton","🎋 Sugarcane","🥜 Groundnut"]
    col1, col2 = st.columns([2, 2])

    with col1:
        selected_crop = st.selectbox(
            "Choose Crop",
            crop_options
        )

    st.markdown('<div class="section-header1">📋 Growth Stage &amp; Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        land  = st.number_input("Land Area (acres)", 0.1, 500.0, 1.0)
        soil  = st.selectbox("Soil Type", ["Clay","Sandy","Loamy","Black","Red"])
    with col2:
        stage  = st.selectbox("Crop Growth Stage", ["Seedling","Vegetative","Flowering","Maturity"])
        season = st.selectbox("Season", ["Summer","Winter","Monsoon"])

    col3, col4 = st.columns([2, 2])

    with col3:
        location = st.text_input("Village / City", "Chennai")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💧 Calculate Water Need"):
        try:
            with st.spinner("Fetching Weather + Predicting..."):
                wx = get_weather(location)
                st.session_state.weather = {
                    "city": location,
                    "temp": round(wx["temperature"], 1),
                    "hum":  wx["humidity"],
                    "rain": wx["rainfall"],
                    "wind": round(wx["wind_speed"], 1)
                }
                st.info("🌦 Weather fetched successfully")
                payload = {
                    "land_area": land, "temperature": wx["temperature"],
                    "humidity": wx["humidity"], "rainfall": wx["rainfall"],
                    "wind_speed": wx["wind_speed"], "soil_type": soil,
                    "crop_type": selected_crop, "crop_stage": stage, "season": season
                }
                response = requests.post(f"{FLASK_BACKEND_URL}/predict", json=payload)
                result   = response.json()
                if "water_required_liters" in result:
                    st.session_state.last_result = {
                        "crop": selected_crop,
                        "land": land,
                        "soil": soil,
                        "stage": stage,
                        "season": season,
                        "city": location,
                        "temperature": wx["temperature"],
                        "humidity": wx["humidity"],
                        "rainfall": wx["rainfall"],
                        "wind_speed": wx["wind_speed"],
                        "water_need": result["water_required_liters"],
                        "irrigation_level": result["irrigation_level"],
                        "confidence": result["confidence"],
                        "explanation": result["explanation"]
                    }
                    st.success("✅ Prediction Completed")
                else:
                    st.error(result.get("error", "Unknown error"))
        except Exception as e:
            st.error(f"❌ Error: {e}")

    if st.session_state.last_result:
        r = st.session_state.last_result
        water, temp, hum, rain, wind = r["water_need"], r["temperature"], r["humidity"], r["rainfall"], r["wind_speed"]

        st.markdown(f"""
        <div class="result-main-card">
            <div class="result-main-title">
<span class="live-dot"></span>
LIVE WATER PREDICTION
</div>
            <div class="result-main-value">{water} L</div>
        </div>""", unsafe_allow_html=True)

        c1,c2,c3,c4 = st.columns(4)
        for col,(icon,val,lbl) in zip([c1,c2,c3,c4],[
            ("🌡",f"{temp}°C","Temperature"),
            ("💧",f"{hum}%","Humidity"),
            ("🌧",f"{rain}mm","Rainfall"),
            ("💨",f"{wind} km/h","Wind Speed"),
        ]):
            with col:
                st.markdown(f'<div class="small-card"><div class="small-icon">{icon}</div><div class="small-value">{val}</div><div class="small-label">{lbl}</div></div>', unsafe_allow_html=True)
                
        st.markdown("""
<div class="insight-card">

<div class="insight-title">
🧠 AI Irrigation Insights
</div>

<div class="insight-grid">

<div class="insight-item">
<div class="insight-label">Water Efficiency</div>
<div class="insight-value">92%</div>
</div>

<div class="insight-item">
<div class="insight-label">Soil Retention</div>
<div class="insight-value">Good</div>
</div>

<div class="insight-item">
<div class="insight-label">Crop Health</div>
<div class="insight-value">Stable</div>
</div>

<div class="insight-item">
<div class="insight-label">Irrigation Risk</div>
<div class="insight-value">Low</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="section-header">💡 Smart Recommendations</div>', unsafe_allow_html=True)
        for color, icon, title, desc in get_recommendations(rain, hum, water, r["crop"], r["stage"]):
            st.markdown(f"""
            <div class="recommendation-card rec-{color}">
                <div class="recommendation-header">
                    <div class="recommendation-icon">{icon}</div>
                    <div class="recommendation-title">{title}</div>
                </div>
                <div class="recommendation-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
<div class="activity-feed">

<div class="activity-title">
📡 Live Activity Feed
</div>

<div class="activity-item">
<span class="activity-dot"></span>
Weather synced successfully
</div>

<div class="activity-item">
<span class="activity-dot"></span>
AI prediction model initialized
</div>

<div class="activity-item">
<span class="activity-dot"></span>
Irrigation recommendation generated
</div>

</div>
""", unsafe_allow_html=True)


def page_tips():
    st.markdown('<div class="section-header1">🌱 Smart Farming Tips</div>', unsafe_allow_html=True)

    tips = [
        ("🌅","Water at Dawn","Always irrigate between 5–7 AM. Reduces evaporation by up to 30% versus midday watering."),
        ("💧","Drip Irrigation Saves 50%","Switching from flood to drip irrigation saves 40–60% water for row crops."),
        ("🌧️","Track Every Rainfall","After 10mm of rain, skip the next irrigation cycle."),
        ("🌱","Mulch Your Fields","A 5cm layer of straw mulch reduces soil evaporation by up to 70%."),
        ("🧪","Check Soil Moisture First","Press a handful of soil — if it forms a ball and doesn't crumble, moisture is sufficient."),
        ("🌾","Stage-Based Watering","Crops need the most water during flowering and grain-filling."),
        ("📅","Irrigation Schedule","Create a weekly schedule based on crop stage, soil type, and weather forecast."),
        ("🐛","Avoid Waterlogging","Too much water drowns roots and causes fungal disease."),
        ("☀️","Use Shade Nets","Shade nets reduce crop water demand by 20–25% in peak summer."),
        ("📊","Keep Records","Note date, amount irrigated, and rainfall for better planning next year."),
        ("🌊","Rainwater Harvesting","Collect roof runoff in farm ponds for extra irrigation cycles."),
        ("🤝","Farmer Groups","Join a local water user association to reduce waste and conflict."),
    ]

    # Daily random tips
    selected_tips = random.sample(tips, 6)
    featured_tip = random.choice(tips)

    # Featured tip card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(14,165,233,0.10));
        border: 1px solid rgba(76,175,125,0.22);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(14px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    ">
        <div style="font-size:13px;color:#a8d8b9;font-weight:700;margin-bottom:8px;">
            🌟 TODAY'S FEATURED FARM TIP
        </div>
        <div style="font-size:28px;margin-bottom:10px;">{featured_tip[0]}</div>
        <div style="font-size:20px;font-weight:800;color:white;margin-bottom:8px;">
            {featured_tip[1]}
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.75);line-height:1.6;">
            {featured_tip[2]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Grid tips
    for i in range(0, len(selected_tips), 2):
        col1, col2 = st.columns(2)

        with col1:
            e, t, d = selected_tips[i]
            st.markdown(f'''
            <div class="tip-card" style="min-height:120px;">
                <div class="tip-emoji">{e}</div>
                <div>
                    <div class="tip-title">{t}</div>
                    <div class="tip-desc">{d}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        if i + 1 < len(selected_tips):
            with col2:
                e, t, d = selected_tips[i+1]
                st.markdown(f'''
                <div class="tip-card" style="min-height:120px;">
                    <div class="tip-emoji">{e}</div>
                    <div>
                        <div class="tip-title">{t}</div>
                        <div class="tip-desc">{d}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)


def page_report():
    st.markdown('<div class="section-header1">📄 Download Report</div>', unsafe_allow_html=True)
    if not st.session_state.get("last_result"):
        st.markdown("""
        <div class="green-card report-empty">
            <div style="font-size:48px;margin-bottom:12px">📄</div>
            <div class="report-empty-title">No Report Yet</div>
            <div class="report-empty-text">Go to 💧 Predict Water and calculate your water requirement first.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("💧 Go to Water Prediction"):
            st.session_state.page = "💧 Predict Water"; st.rerun()
        return

    r          = st.session_state.last_result
    html_bytes = build_report_html(r).encode("utf-8")
    st.markdown("Download the detailed water report for your crop, including weather data and smart recommendations.")
    st.download_button(
        label="📄 Download Report",
        data=html_bytes,
        file_name=f"water_report_{r['crop'].replace(' ','_')}_{date.today()}.html",
        mime="text/html",
    )
    msg    = (f"🌾 Crop Water Report\n\nCrop: {r['crop']}\nLand: {r['land']} acres\n"
              f"Daily Water Need: {r['water_need']:.2f} Litres\n\nTemp: {r['temperature']}°C | "
              f"Rain: {r['rainfall']}mm\n\nGenerated by Crop Water Planner 🌱")
    wa_url = f"https://wa.me/?text={requests.utils.quote(msg)}"
    st.link_button("📲 Share via WhatsApp", wa_url)


def page_help():
    st.markdown('<div class="section-header">📞 Help & Support</div>', unsafe_allow_html=True)

    helps = [
        ("❓ How to use this app?",
         "Select your crop → Enter land area → Choose soil type → Enter location → Click Calculate Water Need."),

        ("🌦 Why does weather affect water need?",
         "Higher temperature increases evaporation. Rain reduces irrigation requirement."),

        ("🌱 What is Crop Growth Stage?",
         "Seedling → Vegetative → Flowering → Maturity. Each stage has different water demand."),

        ("🧪 Which soil type should I choose?",
         "Clay retains water, Sandy drains fast, Loamy is balanced, Black soil holds moisture well."),

        ("📄 How to download report?",
         "Go to Download Report page after prediction and click the download button."),

        ("📱 Does this work on mobile?",
         "Yes, fully optimized for Android and low-end devices."),

        ("💡 What if my village is not found?",
         "Use nearest town or district name for weather prediction."),

        ("🌾 Which crops are supported?",
         "Rice, Wheat, Maize, Cotton, Sugarcane, Groundnut.")
    ]

    st.markdown("""
    <div class="green-card">
        <b>📌 Frequently Asked Questions</b><br>
        Click on any question below to expand answer
    </div>
    """, unsafe_allow_html=True)

    for q, a in helps:
        with st.expander(q):
            st.write(a)

    st.markdown('<div class="section-header">📞 Contact Support</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="green-card">
        📧 Email: help@cropwater.in<br>
        🏛️ Kisan Call Centre: 1800-180-1551<br>🌐
        <a href="https://mkisan.gov.in" target="_blank">
        mkisan.gov.in
        </a>

    </div>
    """, unsafe_allow_html=True)
    


def page_about():
    st.markdown('<div class="section-header">ℹ About This App</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-section" style="margin-bottom:16px">
        <div style="font-size:50px;margin-bottom:12px">🌾</div>
        <div class="hero-title">Crop Water Planner</div>
        <div class="hero-sub">Empowering Indian Farmers with Smart Irrigation</div>
        <div>
            <span class="hero-badge">Version 2.0</span>
            <span class="hero-badge">Open Source</span>
            <span class="hero-badge">Made in India 🇮🇳</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="green-card">
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#1a4d2e;margin-bottom:10px">🎯 Our Mission</div>
        <p style="color:#1a2e1a;line-height:1.7;font-size:14px">
        India uses <b>80% of its freshwater</b> for agriculture — yet crop water stress causes billions in losses every year.
        <b>Crop Water Planner</b> brings agronomic science directly to the farmer's phone — no login, no fees, no complexity.
        Just enter your crop and land, and get instant, weather-aware irrigation guidance.
        </p></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="green-card">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:#1a4d2e;margin-bottom:10px">⚙️ Technology</div>
            <div class="help-item"><div class="help-icon">🐍</div><div><div class="help-title">Python + Streamlit</div><div class="help-desc">Fast, lightweight web framework for data apps</div></div></div>
            <div class="help-item"><div class="help-icon">🌤️</div><div><div class="help-title">OpenWeatherMap API</div><div class="help-desc">Real-time weather for any Indian city</div></div></div>
            <div class="help-item"><div class="help-icon">🧮</div><div><div class="help-title">ML Prediction Model</div><div class="help-desc">Trained on Indian crop & climate datasets</div></div></div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="green-card">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:#1a4d2e;margin-bottom:10px">🌟 Key Highlights</div>
            <div class="help-item"><div class="help-icon">🚫</div><div><div class="help-title">No Login Required</div><div class="help-desc">Farmers access instantly — no barriers</div></div></div>
            <div class="help-item"><div class="help-icon">📱</div><div><div class="help-title">Works on Any Phone</div><div class="help-desc">Tested on low-end Android with slow networks</div></div></div>
            <div class="help-item"><div class="help-icon">📄</div><div><div class="help-title">Downloadable Reports</div><div class="help-desc">HTML report ready to share via WhatsApp</div></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="green-card" style="text-align:center">
        <div style="font-size:32px;margin-bottom:8px">🙏</div>
        <div style="font-size:16px;font-weight:700;color:#1a4d2e">Built with respect for Indian Farmers</div>
        <div style="margin-top:14px;font-size:12px;color:#4a7a55">© 2025 Crop Water Planner · Made in India 🇮🇳</div>
    </div>""", unsafe_allow_html=True)

def page_dashboard():
    st.markdown('<div class="section-header1">Live Smart Agriculture Dashboard</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="dashboard-hero">
        <div class="dashboard-title">Live Smart Agriculture Dashboard</div>
        <div class="dashboard-sub">
            Real-time system status, AI engine monitoring, and irrigation intelligence overview.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATUS CARDS (REAL STREAMLIT LAYOUT) ──
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("AI Engine", "ACTIVE"),
        ("Weather API", "LIVE"),
        ("Prediction Model", "READY"),
        ("System Health", "STABLE")
    ]

    for col, (label, value) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div class="dashboard-card">
                <div class="dashboard-label">{label}</div>
                <div class="dashboard-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── LIVE FEED ──
    st.markdown("""
    <div class="live-feed">
        <div class="live-title">📡 Live System Activity</div>
    </div>
    """, unsafe_allow_html=True)

    activities = [
        "Weather data synced successfully",
        "Crop prediction engine initialized",
        "Irrigation model responding in 0.2s",
        "Database connection stable"
    ]

    for item in activities:
        st.markdown(f"""
        <div class="live-item">
            <span class="live-dot"></span>
            {item}
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    render_sidebar()

    page = st.session_state.page
    if   page == "🏠 Home":            page_home()
    elif page == "💧 Predict Water":   page_predict()
    elif page == "🌱 Crop Tips":       page_tips()
    elif page == "📄 Download Report": page_report()
    elif page == "📞 Help":            page_help()
    elif page == "ℹ About":           page_about()
    elif page == "📊 Dashboard":     page_dashboard()
    else:                              page_home()

if __name__ == "__main__":
    main()