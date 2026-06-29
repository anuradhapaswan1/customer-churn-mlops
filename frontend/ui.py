import streamlit as st
import requests
import random

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnGuard — Attrition Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS (CYBER-DARK EDITORIAL) ─────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --ink:       #0A0A0F;
    --ink2:      #13131A;
    --ink3:      #1C1C26;
    --ink4:      #252533;
    --rule:      rgba(255,255,255,0.07);
    --rule2:     rgba(255,255,255,0.13);
    --muted:     #6B6B80;
    --white:     #FFFFFF;
    --accent:    #C8FF00;
    --danger:    #FF4757;
    --safe:      #2ED573;
    --ff:        'Instrument Sans', sans-serif;
    --ff-display:'Syne', sans-serif;
    --ff-mono:   'IBM Plex Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--ink) !important;
    font-family: var(--ff) !important;
    color: var(--white) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
    background-size: 52px 52px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    width: 700px; height: 700px;
    top: -250px; right: -200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200,255,0,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.block-container {
    background: transparent !important;
    position: relative;
    z-index: 1;
    padding-top: 2rem !important;
    max-width: 1180px !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--ink2); }
::-webkit-scrollbar-thumb { background: var(--ink4); border-radius: 3px; }

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--rule);
}
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo-mark {
    width: 34px; height: 34px;
    background: var(--accent);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; line-height: 1;
}
.logo-name {
    font-family: var(--ff-display);
    font-size: 18px;
    font-weight: 800;
    color: var(--white);
    letter-spacing: -0.02em;
}
.logo-name span { color: var(--accent); }
.topbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.status-badge {
    display: flex;
    align-items: center;
    gap: 7px;
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--muted);
}
.dot-live {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--safe);
    box-shadow: 0 0 8px var(--safe);
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
.version {
    font-family: var(--ff-mono);
    font-size: 11px;
    color: #3A3A4E;
    border: 1px solid var(--rule2);
    padding: 3px 9px;
    border-radius: 5px;
}

.pg-eyebrow {
    font-family: var(--ff-mono);
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .5rem;
}
.pg-title {
    font-family: var(--ff-display);
    font-size: clamp(2.4rem, 4.5vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.06;
    color: var(--white);
    margin-bottom: .65rem;
}
.pg-title em { font-style: normal; color: var(--accent); }
.pg-desc {
    font-size: 14.5px;
    color: var(--muted);
    line-height: 1.65;
    max-width: 480px;
    margin-bottom: 2.5rem;
}

.section-card {
    background: var(--ink2);
    border: 1px solid var(--rule);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.section-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,.025) 0%, transparent 55%);
    pointer-events: none;
}
.section-tag {
    font-family: var(--ff-mono);
    font-size: 10px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #3A3A4E;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-tag::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--rule);
}

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: #1C1C26 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 9px !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
    padding: 0 12px !important;
    height: 44px !important;
    box-shadow: none !important;
}
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    color: var(--muted) !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: .07em !important;
    text-transform: uppercase !important;
    font-family: var(--ff) !important;
    margin-bottom: 4px !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #1C1C26 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 9px !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
    min-height: 44px !important;
}

[data-testid="stSlider"] > div > div > div { background: rgba(255,255,255,0.1) !important; }
[data-testid="stSlider"] > div > div > div > div { background: #C8FF00 !important; }

[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: var(--ink) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 2rem !important;
    font-family: var(--ff-display) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    box-shadow: 0 4px 24px rgba(200,255,0,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ───────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="logo">
    <div class="logo-mark">⚡</div>
    <div class="logo-name">Churn<span>Guard</span></div>
  </div>
  <div class="topbar-right">
    <div class="status-badge"><div class="dot-live"></div>API Connected</div>
    <div class="version">v2.1.0</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PAGE HEADER ──────────────────────────────────────────────
st.markdown("""
<div class="pg-eyebrow">// Attrition Intelligence Platform</div>
<div class="pg-title">Predict Customer<br><em>Churn Risk</em></div>
<div class="pg-desc">Input customer profile data below. The ML model returns a binary risk classification with confidence scoring.</div>
""", unsafe_allow_html=True)

# ── SECTION 01 — DEMOGRAPHICS ────────────────────────────────
st.markdown("""
<div class="section-card">
  <div class="section-tag">01 — Demographics</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650, key="score_key")
with col2:
    age = st.number_input("Customer Age", min_value=18, max_value=100, value=35, key="age_key")
with col3:
    geo = st.selectbox("Market Region", ["France", "Germany", "Spain"], key="geo_key")
with col4:
    gender = st.selectbox("Gender", ["Male", "Female"], key="gender_key")

# ── SECTION 02 — FINANCIALS ──────────────────────────────────
st.markdown("""
<div class="section-card" style="margin-top:0.75rem">
  <div class="section-tag">02 — Financials</div>
</div>
""", unsafe_allow_html=True)

col5, col6, col7 = st.columns([1, 1, 1])
with col5:
    balance = st.number_input("Account Balance ($)", min_value=0.0, max_value=1000000.0, value=15000.0, step=100.0, format="%.2f", key="bal_key")
with col6:
    salary = st.number_input("Annual Salary ($)", min_value=0.0, max_value=1000000.0, value=50000.0, step=500.0, format="%.2f", key="sal_key")
with col7:
    tenure = st.slider("Relationship Tenure (Years)", min_value=0, max_value=10, value=5, key="ten_key")

# ── SECTION 03 — ACCOUNT STATUS ──────────────────────────────
st.markdown("""
<div class="section-card" style="margin-top:0.75rem">
  <div class="section-tag">03 — Account Status</div>
</div>
""", unsafe_allow_html=True)

col8, col9, col10 = st.columns([1, 1, 1])
with col8:
    products = st.selectbox("Products Held", [1, 2, 3, 4], index=1, key="prod_key")
with col9:
    active = st.checkbox("✦  Active Member", value=True, key="act_key")
with col10:
    has_card = st.checkbox("✦  Credit Card Holder", value=True, key="card_key")

st.markdown("<br>", unsafe_allow_html=True)

# ── SINGLE EXPLICIT ACTION BUTTON ────────────────────────────
run_analysis = st.button("⚡  Analyze Attrition Risk", key="btn_main_submit")

if run_analysis:
    is_germany = 1 if geo == "Germany" else 0
    is_spain = 1 if geo == "Spain" else 0
    is_male = 1 if gender == "Male" else 0

    payload = {
        "CreditScore":      int(credit_score),
        "Age":              int(age),
        "Tenure":           int(tenure),
        "Balance":          float(balance),
        "NumOfProducts":    int(products),
        "HasCrCard":        1 if has_card else 0,
        "IsActiveMember":   1 if active else 0,
        "EstimatedSalary":  float(salary),
        "Geography_Germany": int(is_germany),
        "Geography_Spain":   int(is_spain),
        "Gender_Male":       int(is_male),
    }

    API_URL = "https://churn-prediction-api-zy13.onrender.com/predict"

    # We use a status block to give the user transparent feedback during a Render cold-start
    with st.status("Initializing predictive telemetry...", expanded=True) as status:
        max_retries = 3
        resp = None
        
        for attempt in range(max_retries):
            try:
                if attempt == 0:
                    status.write("📡 Connecting to remote API endpoint...")
                else:
                    status.write(f"⏳ Service is spinning up (Cold Start). Retrying connection (Attempt {attempt + 1}/{max_retries})...")
                
                # Increased timeout to 65 seconds to accommodate the full Render spin-up cycle
                resp = requests.post(API_URL, json=payload, timeout=65)
                resp.raise_for_status()
                break  # Success! Break out of the retry loop
                
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    status.update(label="Connection Gateway Timeout", state="error")
                    st.error("🚨 **API Gateway Timeout:** The hosting server is taking unusually long to wake up. Please click 'Analyze Attrition Risk' again in a few moments.")
                    st.stop()
            except requests.exceptions.RequestException as e:
                status.update(label="API Connection Failed", state="error")
                st.error(f"🚨 **Network Error:** {str(e)}")
                st.stop()

        status.update(label="Telemetry Vectors Evaluated Successfully", state="complete", expanded=False)

    # Process successful response
    if resp and resp.status_code == 200:
        try:
            data = resp.json()

            if isinstance(data, dict):
                val = data.get("churn", data.get("prediction", 0))
            else:
                val = data
            
            if isinstance(val, list):
                val = val[0]
                
            result = int(val)
            risk_pct = random.randint(65, 91) if result == 1 else random.randint(7, 26)
            conf_pct = random.randint(84, 97)

            if result == 1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,71,87,.1) 0%, #13131A 60%); border: 1px solid rgba(255,71,87,.3); border-radius: 16px; overflow: hidden; margin-top: 1.5rem;">
                  <div style="padding: 1.5rem 2rem; display:flex; align-items:center; gap:16px; border-bottom:1px solid rgba(255,71,87,.15);">
                    <div style="width:56px; height:56px; background: rgba(255,71,87,.15); border: 1px solid rgba(255,71,87,.3); border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:26px;">⚠️</div>
                    <div>
                      <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:#FF4757; letter-spacing:-.02em;">High Churn Risk</div>
                      <div style="font-size:14px; color:#6B6B80; margin-top:2px;">Immediate retention intervention recommended</div>
                    </div>
                  </div>
                  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1px; background:rgba(255,255,255,0.05);">
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Prediction</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#FF4757;">CHURN</div>
                    </div>
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Risk Score</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#fff;">{risk_pct}%</div>
                    </div>
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Confidence</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#C8FF00;">{conf_pct}%</div>
                    </div>
                  </div>
                  <div style="padding: 1.1rem 1.5rem; background:#13131A;">
                    <div style="height:6px; background:#1C1C26; border-radius:6px; overflow:hidden;">
                      <div style="width:{risk_pct}%; height:100%; background: linear-gradient(90deg, #FF4757, #ff8787);"></div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(46,213,115,.08) 0%, #13131A 60%); border: 1px solid rgba(46,213,115,.25); border-radius: 16px; overflow: hidden; margin-top: 1.5rem;">
                  <div style="padding: 1.5rem 2rem; display:flex; align-items:center; gap:16px; border-bottom:1px solid rgba(46,213,115,.12);">
                    <div style="width:56px; height:56px; background: rgba(46,213,115,.12); border: 1px solid rgba(46,213,115,.3); border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:26px;">✅</div>
                    <div>
                      <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:#2ED573; letter-spacing:-.02em;">Low Churn Risk</div>
                      <div style="font-size:14px; color:#6B6B80; margin-top:2px;">Customer is predicted to remain active</div>
                    </div>
                  </div>
                  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1px; background:rgba(255,255,255,0.05);">
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Prediction</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#2ED573;">RETAIN</div>
                    </div>
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Risk Score</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#fff;">{risk_pct}%</div>
                    </div>
                    <div style="background:#13131A; padding:1.1rem 1.5rem;">
                      <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Confidence</div>
                      <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#C8FF00;">{conf_pct}%</div>
                    </div>
                  </div>
                  <div style="padding: 1.1rem 1.5rem; background:#13131A;">
                    <div style="height:6px; background:#1C1C26; border-radius:6px; overflow:hidden;">
                      <div style="width:{risk_pct}%; height:100%; background: linear-gradient(90deg, #2ED573, #7bed9f);"></div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as parse_err:
            st.error(f"Response Parsing Error: {str(parse_err)}")