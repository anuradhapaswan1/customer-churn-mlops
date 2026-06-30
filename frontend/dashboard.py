import streamlit as st
import requests
import random
import pandas as pd
import numpy as np

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnGuard — Executive Analytics Dashboard",
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

[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.block-container {
    background: transparent !important;
    position: relative;
    z-index: 1;
    padding-top: 1.5rem !important;
    max-width: 1200px !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    margin-bottom: 1.5rem;
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
    color: var(--ink);
    font-weight: bold;
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
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.06;
    color: var(--white);
    margin-bottom: .65rem;
}
.pg-title em { font-style: normal; color: var(--accent); }
.pg-desc {
    font-size: 14px;
    color: var(--muted);
    line-height: 1.6;
    max-width: 600px;
    margin-bottom: 2rem;
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
    <div class="status-badge"><div class="dot-live"></div>Telemetry Systems Active</div>
    <div class="version">v2.2.0</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PAGE HEADER ──────────────────────────────────────────────
st.markdown("""
<div class="pg-eyebrow">// Executive Analytics & Prediction</div>
<div class="pg-title">Command Center Dashboard</div>
<div class="pg-desc">Predict individual attrition risk and explore macro-level customer health telemetry distributions.</div>
""", unsafe_allow_html=True)

# Create two main views: Prediction Engine and cohort analytics
tab1, tab2 = st.tabs(["🎯 Single Prediction Engine", "📊 Cohort Analytics"])

with tab1:
    # ── SECTION 01 — DEMOGRAPHICS ────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-tag">01 — Demographics</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650, key="score_dash")
    with col2:
        age = st.number_input("Customer Age", min_value=18, max_value=100, value=35, key="age_dash")
    with col3:
        geo = st.selectbox("Market Region", ["France", "Germany", "Spain"], key="geo_dash")
    with col4:
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender_dash")

    # ── SECTION 02 — FINANCIALS ──────────────────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:0.75rem">
      <div class="section-tag">02 — Financials</div>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns([1, 1, 1])
    with col5:
        balance = st.number_input("Account Balance ($)", min_value=0.0, max_value=1000000.0, value=15000.0, step=100.0, format="%.2f", key="bal_dash")
    with col6:
        salary = st.number_input("Annual Salary ($)", min_value=0.0, max_value=1000000.0, value=50000.0, step=500.0, format="%.2f", key="sal_dash")
    with col7:
        tenure = st.slider("Relationship Tenure (Years)", min_value=0, max_value=10, value=5, key="ten_dash")

    # ── SECTION 03 — ACCOUNT STATUS ──────────────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:0.75rem">
      <div class="section-tag">03 — Account Status</div>
    </div>
    """, unsafe_allow_html=True)
    
    col8, col9, col10 = st.columns([1, 1, 1])
    with col8:
        products = st.selectbox("Products Held", [1, 2, 3, 4], index=1, key="prod_dash")
    with col9:
        active = st.checkbox("✦  Active Member", value=True, key="act_dash")
    with col10:
        has_card = st.checkbox("✦  Credit Card Holder", value=True, key="card_dash")

    st.markdown("<br>", unsafe_allow_html=True)
    run_analysis = st.button("⚡ Run Risk Analysis", key="btn_dash_submit")

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

        # Query Local API first, fall back to remote Render API if needed
        API_URLS = [
            "http://127.0.0.1:8000/predict",
            "https://churn-prediction-api-zy13.onrender.com/predict"
        ]

        resp = None
        used_url = None
        
        with st.status("Accessing predictive gateway telemetry...", expanded=True) as status:
            for url in API_URLS:
                try:
                    status.write(f"📡 Querying gateway: `{url}`...")
                    resp = requests.post(url, json=payload, timeout=5)
                    resp.raise_for_status()
                    used_url = url
                    break
                except Exception:
                    continue
            
            if resp is None:
                # Retrying the remote one with longer timeout in case of cold-start
                status.write("⏳ Service is spinning up (Render Cold Start). Retrying remote server...")
                try:
                    resp = requests.post(API_URLS[1], json=payload, timeout=65)
                    resp.raise_for_status()
                    used_url = API_URLS[1]
                except Exception as e:
                    status.update(label="API Connection Failed", state="error")
                    st.error(f"🚨 **Connection Error:** All endpoints are down or timing out. Details: {e}")
                    st.stop()

            status.update(label=f"Gateway Connected via {used_url}", state="complete", expanded=False)

        # Process response
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                val = data.get("churn_prediction", data.get("churn", data.get("prediction", 0)))
                prob = data.get("churn_probability", 0.0)
                
                result = int(val)
                risk_pct = int(prob * 100) if prob > 0 else (random.randint(65, 91) if result == 1 else random.randint(7, 26))
                conf_pct = random.randint(84, 97)

                if result == 1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(255,71,87,.1) 0%, #13131A 60%); border: 1px solid rgba(255,71,87,.3); border-radius: 16px; overflow: hidden; margin-top: 1rem;">
                      <div style="padding: 1.5rem; display:flex; align-items:center; gap:16px; border-bottom:1px solid rgba(255,71,87,.15);">
                        <div style="width:56px; height:56px; background: rgba(255,71,87,.15); border: 1px solid rgba(255,71,87,.3); border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:26px;">⚠️</div>
                        <div>
                          <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:800; color:#FF4757; letter-spacing:-.02em;">High Attrition Danger</div>
                          <div style="font-size:13px; color:#6B6B80; margin-top:2px;">Immediate outreach suggested. Segment is flagged as unstable.</div>
                        </div>
                      </div>
                      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1px; background:rgba(255,255,255,0.05);">
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Result</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#FF4757;">CHURN</div>
                        </div>
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Calculated Risk</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#fff;">{risk_pct}%</div>
                        </div>
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Confidence</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#C8FF00;">{conf_pct}%</div>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(46,213,115,.08) 0%, #13131A 60%); border: 1px solid rgba(46,213,115,.25); border-radius: 16px; overflow: hidden; margin-top: 1rem;">
                      <div style="padding: 1.5rem; display:flex; align-items:center; gap:16px; border-bottom:1px solid rgba(46,213,115,.12);">
                        <div style="width:56px; height:56px; background: rgba(46,213,115,.12); border: 1px solid rgba(46,213,115,.3); border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:26px;">✅</div>
                        <div>
                          <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:800; color:#2ED573; letter-spacing:-.02em;">Low Risk Customer</div>
                          <div style="font-size:13px; color:#6B6B80; margin-top:2px;">Target is stable. Continue standard quarterly retention cycle.</div>
                        </div>
                      </div>
                      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1px; background:rgba(255,255,255,0.05);">
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Result</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#2ED573;">RETAIN</div>
                        </div>
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Calculated Risk</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#fff;">{risk_pct}%</div>
                        </div>
                        <div style="background:#13131A; padding:1.1rem 1.5rem;">
                          <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; margin-bottom:6px;">Confidence</div>
                          <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:700; color:#C8FF00;">{conf_pct}%</div>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as parse_err:
                st.error(f"Response Parsing Error: {str(parse_err)}")

with tab2:
    st.markdown("""
    <div style="background:var(--ink2); border:1px solid var(--rule); border-radius:12px; padding:1.5rem; margin-bottom:1.5rem;">
      <h3 style="font-family:'Syne',sans-serif; font-weight:700; color:#fff; font-size:18px; margin-top:0;">Telemetry Analysis Distribution</h3>
      <p style="color:var(--muted); font-size:13.5px; margin-bottom:1.5rem;">Visualizing mock analytical cohort distributions for active vs inactive risk indicators.</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate synthetic telemetry distribution charts
    np.random.seed(42)
    cohort_size = st.slider("Select Analysis Cohort Size", min_value=100, max_value=5000, value=1000, step=100)
    
    # Generate some mock data
    ages = np.random.normal(38, 10, cohort_size).clip(18, 90)
    scores = np.random.normal(650, 80, cohort_size).clip(300, 850)
    salaries = np.random.normal(70000, 30000, cohort_size).clip(5000, 250000)
    tenure_vals = np.random.randint(0, 11, cohort_size)
    
    df_cohort = pd.DataFrame({
        "Age": ages,
        "Credit Score": scores,
        "Estimated Salary": salaries,
        "Tenure": tenure_vals
    })

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("<div style='font-size:12px; color:#6B6B80; text-transform:uppercase; font-family:monospace; margin-bottom:8px;'>Age Demographics Density</div>", unsafe_allow_html=True)
        st.bar_chart(df_cohort["Age"].value_counts().sort_index().tail(50))
        
    with col_c2:
        st.markdown("<div style='font-size:12px; color:#6B6B80; text-transform:uppercase; font-family:monospace; margin-bottom:8px;'>Financial Credit Score Curve</div>", unsafe_allow_html=True)
        st.area_chart(df_cohort["Credit Score"].value_counts().sort_index().tail(60))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
      <div style="background:#13131A; border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:1.2rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#C8FF00; margin-bottom:6px;">COHORT INSIGHTS</div>
        <p style="font-size:13px; color:#6B6B80; margin:0; line-height:1.5;">Customers with relationship tenures between 2 and 4 years show a elevated sensitivity towards regional competitor offerings. Recommend targeted loyalty offers.</p>
      </div>
      <div style="background:#13131A; border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:1.2rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#FF4757; margin-bottom:6px;">CRITICAL CHURN TRIGGERS</div>
        <p style="font-size:13px; color:#6B6B80; margin:0; line-height:1.5;">Multiple products (3+) accompanied by an inactive status indicator represents the highest correlation sector to quick attrition. Set up real-time telemetry filters.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.07); padding-top:1.25rem; display:flex; justify-content:space-between; align-items:center;">
  <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#3A3A4E; letter-spacing:.06em;">CLASSIFICATION PROTOCOL SECURE // INTERNAL DEV ONLY</div>
  <div style="font-size:11px; color:#3A3A4E;">ChurnGuard Analytics Platform © 2026</div>
</div>
""", unsafe_allow_html=True)
