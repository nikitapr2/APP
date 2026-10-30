import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Hospital Queue Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root / Dark Theme ── */
:root {
    --bg-primary:   #0a0f1e;
    --bg-card:      #111827;
    --bg-card2:     #1a2235;
    --accent-blue:  #3b82f6;
    --accent-cyan:  #06b6d4;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red:   #ef4444;
    --accent-purple:#8b5cf6;
    --text-primary: #f1f5f9;
    --text-muted:   #94a3b8;
    --border:       #1e293b;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary);
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background-color: #0d1424 !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Hide default header ── */
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Metric cards ── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform .18s, box-shadow .18s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(0,0,0,.4); }
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
}
.kpi-blue::before   { background: var(--accent-blue); }
.kpi-cyan::before   { background: var(--accent-cyan); }
.kpi-green::before  { background: var(--accent-green); }
.kpi-amber::before  { background: var(--accent-amber); }
.kpi-red::before    { background: var(--accent-red); }
.kpi-purple::before { background: var(--accent-purple); }

.kpi-label {
    font-size: .75rem; font-weight: 600; letter-spacing: .08em;
    color: var(--text-muted); margin-bottom: .5rem;
    text-transform: uppercase;
}
.kpi-value {
    font-size: 2.2rem; font-weight: 700;
    color: var(--text-primary); line-height: 1;
}
.kpi-sub {
    font-size: .78rem; color: var(--text-muted); margin-top: .4rem;
}
.kpi-icon {
    position: absolute; top: 1.2rem; right: 1.4rem;
    font-size: 1.8rem; opacity: .25;
}

/* ── Section headings ── */
.section-heading {
    font-size: 1.15rem; font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
    padding-bottom: .6rem; margin-bottom: 1rem;
}

/* ── Token badge ── */
.token-badge {
    display: inline-block;
    background: linear-gradient(135deg, #3b82f6, #06b6d4);
    color: #fff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.8rem; font-weight: 700;
    padding: .6rem 2rem;
    border-radius: 12px;
    letter-spacing: .05em;
    box-shadow: 0 0 30px rgba(59,130,246,.35);
}

/* ── Queue pill ── */
.queue-pill {
    display: inline-block;
    padding: .22rem .7rem;
    border-radius: 999px;
    font-size: .72rem; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.pill-waiting  { background: rgba(245,158,11,.15);  color: #f59e0b; }
.pill-progress { background: rgba(59,130,246,.15);  color: #3b82f6; }
.pill-done     { background: rgba(16,185,129,.15);  color: #10b981; }

/* ── Form styling ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: .55rem 1.5rem !important;
    transition: opacity .15s !important;
}
.stButton > button:hover { opacity: .88 !important; }

/* ── Table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }
.stDataFrame table { background: var(--bg-card); }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0d1a3a 0%, #0a1628 50%, #06101f 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute; top: -40%; right: -10%;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(59,130,246,.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 1.9rem; font-weight: 700;
    background: linear-gradient(90deg, #f1f5f9, #94a3b8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.2; margin-bottom: .35rem;
}
.hero-tagline {
    font-size: 1rem; color: var(--accent-cyan);
    font-weight: 500; letter-spacing: .03em;
}
.hero-timestamp {
    font-size: .75rem; color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: .7rem;
}

/* ── Sidebar nav items ── */
.nav-item {
    padding: .55rem 1rem;
    border-radius: 8px;
    margin-bottom: .25rem;
    cursor: pointer;
    font-weight: 500;
    font-size: .9rem;
}

/* ── Alert boxes ── */
.alert-success {
    background: rgba(16,185,129,.1);
    border: 1px solid rgba(16,185,129,.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #10b981;
}
.alert-info {
    background: rgba(59,130,246,.1);
    border: 1px solid rgba(59,130,246,.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #3b82f6;
}

/* ── Waiting-time estimate card ── */
.wait-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
}
.wait-time-big {
    font-size: 3rem; font-weight: 700;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Seed & constants ──────────────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

DOCTORS = {
    "Dr. Priya Sharma":    "Cardiology",
    "Dr. Arjun Mehta":     "Orthopedics",
    "Dr. Sunita Verma":    "General Medicine",
    "Dr. Rahul Gupta":     "Neurology",
    "Dr. Kavitha Nair":    "Pediatrics",
    "Dr. Imran Sheikh":    "Dermatology",
}

SYMPTOMS = [
    "Chest pain", "Fever & cough", "Joint pain", "Headache",
    "Skin rash", "Back pain", "Dizziness", "Shortness of breath",
    "Abdominal pain", "Fatigue", "High BP", "Diabetes management",
]

STATUSES = ["Waiting", "In Progress", "Completed"]

# ── Session-state bootstrap ───────────────────────────────────────────────────
def init_state():
    if "patients" not in st.session_state:
        st.session_state.patients = generate_sample_patients()
    if "token_counter" not in st.session_state:
        st.session_state.token_counter = len(st.session_state.patients) + 1
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

# ── Sample data generator ─────────────────────────────────────────────────────
def generate_sample_patients():
    names = [
        "Aarav Singh", "Priya Patel", "Rahul Kumar", "Ananya Mishra",
        "Vikram Rao", "Sneha Joshi", "Arjun Nair", "Divya Sharma",
        "Ravi Verma", "Meera Iyer", "Suresh Gupta", "Pooja Reddy",
        "Karan Malhotra", "Nisha Kapoor", "Deepak Tiwari", "Ankita Das",
        "Mohit Saxena", "Lakshmi Pillai", "Gaurav Agarwal", "Swati Bhatt",
    ]
    doctors = list(DOCTORS.keys())
    patients = []
    base_time = datetime.now() - timedelta(hours=4)

    for i, name in enumerate(names):
        reg_time = base_time + timedelta(minutes=i * 11)
        est_wait = max(5, random.randint(10, 60) - i * 2)
        status = STATUSES[0] if i > 12 else (STATUSES[1] if i > 8 else STATUSES[2])
        patients.append({
            "Token":       f"T{i+1:03d}",
            "Name":        name,
            "Age":         random.randint(18, 80),
            "Gender":      random.choice(["Male", "Female"]),
            "Doctor":      random.choice(doctors),
            "Symptom":     random.choice(SYMPTOMS),
            "Registered":  reg_time.strftime("%I:%M %p"),
            "Est. Wait":   f"{est_wait} min",
            "Status":      status,
            "Priority":    random.choice(["Normal", "Normal", "Normal", "Urgent"]),
        })
    return patients

# ── Daily chart data ──────────────────────────────────────────────────────────
def generate_daily_data():
    days = pd.date_range(end=datetime.today(), periods=14).strftime("%b %d")
    return pd.DataFrame({
        "Date":           days,
        "Total Patients": np.random.randint(80, 200, 14),
        "Avg Wait (min)": np.random.randint(15, 55, 14),
        "Completed":      np.random.randint(60, 180, 14),
    })

# ── KPI card helper ───────────────────────────────────────────────────────────
def kpi(label, value, sub, color_cls, icon):
    st.markdown(f"""
    <div class="kpi-card {color_cls}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(17,24,39,1)"
PAPER_BG  = "rgba(17,24,39,1)"
GRID_COL  = "rgba(30,41,59,1)"
TEXT_COL  = "#94a3b8"

def base_layout(**kw):
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family="Inter", color=TEXT_COL, size=12),
        xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(color=TEXT_COL)),
        yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(color=TEXT_COL)),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COL)),
        **kw,
    )

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 1.5rem;">
          <div style="font-size:2.4rem;">🏥</div>
          <div style="font-weight:700; font-size:1rem; color:#f1f5f9; line-height:1.3;">
            Smart Hospital<br>Queue Management
          </div>
          <div style="font-size:.72rem; color:#06b6d4; margin-top:.3rem; font-weight:500;">
            AI-Powered System
          </div>
        </div>
        """, unsafe_allow_html=True)

        pages = {
            "Dashboard":      "📊",
            "Register Patient": "📝",
            "Patient Queue":  "👥",
            "Analytics":      "📈",
            "Patient Records": "🗂️",
        }
        for page, icon in pages.items():
            active = st.session_state.page == page
            bg = "rgba(59,130,246,.18)" if active else "transparent"
            border = "1px solid rgba(59,130,246,.4)" if active else "1px solid transparent"
            st.markdown(f"""
            <div style="background:{bg}; border:{border}; border-radius:8px;
                        padding:.55rem 1rem; margin-bottom:.25rem; cursor:pointer;
                        font-weight:{'600' if active else '400'}; font-size:.9rem;">
                {icon} &nbsp; {page}
            </div>""", unsafe_allow_html=True)
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:.72rem; color:#475569; text-align:center; padding:.5rem 0;">
          🟢 System Online &nbsp;|&nbsp; {datetime.now().strftime('%d %b %Y')}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    df = pd.DataFrame(st.session_state.patients)
    total     = len(df)
    waiting   = len(df[df["Status"] == "Waiting"])
    in_prog   = len(df[df["Status"] == "In Progress"])
    completed = len(df[df["Status"] == "Completed"])
    urgent    = len(df[df["Priority"] == "Urgent"])

    # Hero
    st.markdown(f"""
    <div class="hero">
      <div class="hero-title">Smart Hospital Queue Management System</div>
      <div class="hero-tagline">✦ Less Waiting. Better Care.</div>
      <div class="hero-timestamp">
        Live dashboard &nbsp;·&nbsp; Updated {datetime.now().strftime('%I:%M %p, %d %b %Y')}
      </div>
    </div>""", unsafe_allow_html=True)

    # KPI row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Total Patients Today", total, "Registered since 8 AM", "kpi-blue", "👥")
    with c2: kpi("Waiting", waiting, "In queue right now", "kpi-amber", "⏳")
    with c3: kpi("In Consultation", in_prog, "With doctor", "kpi-cyan", "🩺")
    with c4: kpi("Completed", completed, "Consultations done", "kpi-green", "✅")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # KPI row 2
    avg_wait = 27
    c5, c6, c7, c8 = st.columns(4)
    with c5: kpi("Avg Wait Time", f"{avg_wait} min", "Down 12% from yesterday", "kpi-purple", "⏱️")
    with c6: kpi("Urgent Cases", urgent, "Prioritised in queue", "kpi-red", "🚨")
    with c7: kpi("Doctors Active", 6, "All departments staffed", "kpi-cyan", "👨‍⚕️")
    with c8: kpi("Satisfaction", "4.6 / 5", "Based on 38 reviews today", "kpi-green", "⭐")

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Charts
    daily = generate_daily_data()
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-heading">Daily Patient Volume — Last 14 Days</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=daily["Date"], y=daily["Total Patients"],
            name="Total", marker_color="#3b82f6",
            marker_line_width=0,
        ))
        fig.add_trace(go.Bar(
            x=daily["Date"], y=daily["Completed"],
            name="Completed", marker_color="#10b981",
            marker_line_width=0,
        ))
        fig.update_layout(**base_layout(title="", barmode="overlay", height=300))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-heading">Average Waiting Time Trend</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=daily["Date"], y=daily["Avg Wait (min)"],
            mode="lines+markers",
            line=dict(color="#f59e0b", width=2.5),
            marker=dict(size=6, color="#f59e0b"),
            fill="tozeroy",
            fillcolor="rgba(245,158,11,.08)",
            name="Avg Wait",
        ))
        fig2.update_layout(**base_layout(height=300))
        st.plotly_chart(fig2, use_container_width=True)

    # Doctor load + status donut
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-heading">Doctor-wise Patient Load</div>', unsafe_allow_html=True)
        doc_counts = df.groupby("Doctor").size().reset_index(name="Patients")
        doc_counts["Short"] = doc_counts["Doctor"].str.extract(r"Dr\. (\w+)")
        fig3 = go.Figure(go.Bar(
            x=doc_counts["Patients"], y=doc_counts["Short"],
            orientation="h",
            marker=dict(
                color=doc_counts["Patients"],
                colorscale=[[0,"#1e40af"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                showscale=False,
            ),
        ))
        fig3.update_layout(**base_layout(height=280))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-heading">Queue Status Distribution</div>', unsafe_allow_html=True)
        fig4 = go.Figure(go.Pie(
            labels=["Waiting", "In Progress", "Completed"],
            values=[waiting, in_prog, completed],
            hole=.55,
            marker=dict(colors=["#f59e0b", "#3b82f6", "#10b981"]),
            textfont=dict(color="#f1f5f9", size=12),
        ))
        fig4.update_layout(
            **base_layout(height=280),
            showlegend=True,
            annotations=[dict(text=f"<b>{total}</b><br>patients",
                              x=.5, y=.5, showarrow=False,
                              font=dict(size=14, color="#f1f5f9"))],
        )
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REGISTER PATIENT
# ══════════════════════════════════════════════════════════════════════════════
def page_register():
    st.markdown("""
    <div class="hero" style="padding:1.6rem 2rem;">
      <div class="hero-title" style="font-size:1.4rem;">Patient Registration</div>
      <div class="hero-tagline" style="font-size:.9rem;">Register a new patient and auto-generate a queue token.</div>
    </div>""", unsafe_allow_html=True)

    col_form, col_info = st.columns([3, 2])

    with col_form:
        st.markdown('<div class="section-heading">Patient Details</div>', unsafe_allow_html=True)

        with st.form("registration_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name    = c1.text_input("Full Name *", placeholder="e.g. Rahul Kumar")
            age     = c2.number_input("Age *", min_value=1, max_value=120, value=30)

            c3, c4 = st.columns(2)
            gender  = c3.selectbox("Gender *", ["Male", "Female", "Other"])
            phone   = c4.text_input("Phone Number", placeholder="+91 98765 43210")

            symptom = st.selectbox("Primary Symptom *", SYMPTOMS)
            doctor  = st.selectbox("Preferred Doctor *", list(DOCTORS.keys()),
                                   format_func=lambda d: f"{d} — {DOCTORS[d]}")
            priority = st.selectbox("Priority", ["Normal", "Urgent"])
            notes   = st.text_area("Additional Notes", placeholder="Any allergies, past conditions…", height=80)

            submitted = st.form_submit_button("🎫 Register & Generate Token", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Please enter the patient's name.")
            else:
                token = f"T{st.session_state.token_counter:03d}"
                st.session_state.token_counter += 1

                # Estimate wait: count waiting patients for that doctor × 8 min avg
                df_tmp = pd.DataFrame(st.session_state.patients)
                doc_waiting = len(df_tmp[(df_tmp["Doctor"] == doctor) &
                                         (df_tmp["Status"] == "Waiting")])
                est_wait = max(5, doc_waiting * 8 + random.randint(3, 10))

                new_patient = {
                    "Token":       token,
                    "Name":        name.strip(),
                    "Age":         age,
                    "Gender":      gender,
                    "Doctor":      doctor,
                    "Symptom":     symptom,
                    "Registered":  datetime.now().strftime("%I:%M %p"),
                    "Est. Wait":   f"{est_wait} min",
                    "Status":      "Waiting",
                    "Priority":    priority,
                }
                st.session_state.patients.append(new_patient)

                st.markdown(f"""
                <div class="alert-success">
                  <div style="font-size:.8rem; font-weight:600; margin-bottom:.4rem;">
                    ✅ Patient Registered Successfully
                  </div>
                  <div style="font-size:.9rem;">
                    <b>{name}</b> has been added to the queue under <b>{doctor}</b>.
                  </div>
                </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="text-align:center; margin-top:1.4rem;">
                  <div style="font-size:.85rem; color:#94a3b8; margin-bottom:.6rem;">
                    Your Queue Token
                  </div>
                  <div class="token-badge">{token}</div>
                  <div style="margin-top:.8rem; color:#f59e0b; font-size:.9rem; font-weight:600;">
                    ⏱ Estimated Wait: {est_wait} minutes
                  </div>
                  <div style="margin-top:.3rem; font-size:.78rem; color:#94a3b8;">
                    Please keep this token number for reference.
                  </div>
                </div>""", unsafe_allow_html=True)

    with col_info:
        st.markdown('<div class="section-heading">Our Specialists</div>', unsafe_allow_html=True)
        for doc, spec in DOCTORS.items():
            short = doc.replace("Dr. ", "")
            df_tmp = pd.DataFrame(st.session_state.patients)
            q = len(df_tmp[(df_tmp["Doctor"] == doc) & (df_tmp["Status"] == "Waiting")])
            st.markdown(f"""
            <div class="kpi-card kpi-blue" style="margin-bottom:.6rem; padding:1rem 1.2rem;">
              <div style="font-weight:600; font-size:.9rem; color:#f1f5f9;">{short}</div>
              <div style="font-size:.75rem; color:#94a3b8;">{spec}</div>
              <div style="font-size:.78rem; color:#f59e0b; margin-top:.3rem;">
                {q} patient{'s' if q != 1 else ''} waiting
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PATIENT QUEUE
# ══════════════════════════════════════════════════════════════════════════════
def page_queue():
    st.markdown("""
    <div class="hero" style="padding:1.4rem 2rem;">
      <div class="hero-title" style="font-size:1.4rem;">Live Patient Queue</div>
      <div class="hero-tagline" style="font-size:.9rem;">Doctor-wise queue with real-time status.</div>
    </div>""", unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.patients)

    # Filter bar
    fc1, fc2, fc3 = st.columns([2, 2, 1])
    sel_doc    = fc1.selectbox("Filter by Doctor", ["All Doctors"] + list(DOCTORS.keys()))
    sel_status = fc2.selectbox("Filter by Status", ["All", "Waiting", "In Progress", "Completed"])
    if fc3.button("🔄 Refresh", use_container_width=True):
        st.rerun()

    fdf = df.copy()
    if sel_doc    != "All Doctors": fdf = fdf[fdf["Doctor"] == sel_doc]
    if sel_status != "All":         fdf = fdf[fdf["Status"] == sel_status]

    st.markdown(f"""
    <div class="alert-info" style="margin-bottom:1rem;">
      Showing <b>{len(fdf)}</b> patient(s) &nbsp;·&nbsp;
      <b>{len(fdf[fdf['Status']=='Waiting'])}</b> waiting &nbsp;·&nbsp;
      <b>{len(fdf[fdf['Priority']=='Urgent'])}</b> urgent
    </div>""", unsafe_allow_html=True)

    # Doctor-wise accordion
    for doc, spec in DOCTORS.items():
        doc_df = fdf[fdf["Doctor"] == doc]
        if sel_doc != "All Doctors" and doc != sel_doc:
            continue
        waiting_n = len(doc_df[doc_df["Status"] == "Waiting"])

        with st.expander(f"🩺 {doc} — {spec}   ({waiting_n} waiting)", expanded=(waiting_n > 0)):
            if doc_df.empty:
                st.caption("No patients in this queue for the selected filter.")
            else:
                for _, row in doc_df.iterrows():
                    pill_cls = {"Waiting": "pill-waiting",
                                "In Progress": "pill-progress",
                                "Completed": "pill-done"}.get(row["Status"], "pill-waiting")
                    urgency = "🚨 " if row["Priority"] == "Urgent" else ""
                    st.markdown(f"""
                    <div class="kpi-card" style="margin-bottom:.5rem; padding:.9rem 1.2rem;">
                      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:.4rem;">
                        <div>
                          <span style="font-family:'JetBrains Mono',monospace; color:#3b82f6;
                                       font-size:.8rem; font-weight:600;">{row['Token']}</span>
                          &nbsp; {urgency}<span style="font-weight:600; color:#f1f5f9;">{row['Name']}</span>
                          <span style="color:#94a3b8; font-size:.8rem;"> · {row['Age']} y · {row['Gender']}</span>
                        </div>
                        <div style="display:flex; gap:.5rem; align-items:center; flex-wrap:wrap;">
                          <span style="font-size:.78rem; color:#94a3b8;">⏱ {row['Est. Wait']}</span>
                          <span class="queue-pill {pill_cls}">{row['Status']}</span>
                        </div>
                      </div>
                      <div style="font-size:.78rem; color:#64748b; margin-top:.3rem;">
                        {row['Symptom']} &nbsp;·&nbsp; Registered {row['Registered']}
                      </div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
def page_analytics():
    st.markdown("""
    <div class="hero" style="padding:1.4rem 2rem;">
      <div class="hero-title" style="font-size:1.4rem;">Analytics & Insights</div>
      <div class="hero-tagline" style="font-size:.9rem;">AI-driven trends and performance metrics.</div>
    </div>""", unsafe_allow_html=True)

    daily = generate_daily_data()
    df    = pd.DataFrame(st.session_state.patients)

    # Line chart — multi-axis
    st.markdown('<div class="section-heading">14-Day Patient & Wait-Time Trends</div>', unsafe_allow_html=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Total Patients"],
        name="Total Patients", mode="lines+markers",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=6),
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Avg Wait (min)"],
        name="Avg Wait (min)", mode="lines+markers",
        line=dict(color="#f59e0b", width=2.5, dash="dot"),
        marker=dict(size=6),
    ), secondary_y=True)
    fig.update_layout(**base_layout(height=320, title=""))
    fig.update_yaxes(title_text="Patients",     secondary_y=False,
                     gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL))
    fig.update_yaxes(title_text="Wait (min)",   secondary_y=True,
                     gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-heading">Symptom Frequency</div>', unsafe_allow_html=True)
        sym_cnt = df["Symptom"].value_counts().reset_index()
        sym_cnt.columns = ["Symptom", "Count"]
        fig2 = px.bar(sym_cnt, x="Count", y="Symptom", orientation="h",
                      color="Count",
                      color_continuous_scale=["#1e3a8a", "#3b82f6", "#06b6d4"])
        fig2.update_layout(**base_layout(height=320), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-heading">Age Distribution of Patients</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Histogram(
            x=df["Age"], nbinsx=10,
            marker=dict(color="#8b5cf6", line=dict(color="#0a0f1e", width=1)),
        ))
        fig3.update_layout(**base_layout(height=320))
        st.plotly_chart(fig3, use_container_width=True)

    # Wait-time estimate table
    st.markdown('<div class="section-heading">Estimated Waiting Time by Doctor</div>', unsafe_allow_html=True)
    rows = []
    for doc, spec in DOCTORS.items():
        doc_df = df[(df["Doctor"] == doc) & (df["Status"] == "Waiting")]
        q = len(doc_df)
        est = q * 8
        rows.append({
            "Doctor": doc,
            "Specialty": spec,
            "Queue Length": q,
            "Est. Wait for Next": f"{est} min" if q else "—",
            "Status": "🟡 Busy" if q > 3 else ("🟢 Available" if q == 0 else "🟠 Moderate"),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Hourly heatmap (simulated)
    st.markdown('<div class="section-heading">Simulated Hourly Queue Density</div>', unsafe_allow_html=True)
    hours = [f"{h:02d}:00" for h in range(8, 20)]
    days_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    z = np.random.randint(5, 60, size=(len(days_week), len(hours)))
    fig4 = go.Figure(go.Heatmap(
        z=z, x=hours, y=days_week,
        colorscale=[[0,"#0f172a"],[0.4,"#1e40af"],[0.7,"#3b82f6"],[1,"#06b6d4"]],
        showscale=True,
    ))
    fig4.update_layout(**base_layout(height=260))
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PATIENT RECORDS
# ══════════════════════════════════════════════════════════════════════════════
def page_records():
    st.markdown("""
    <div class="hero" style="padding:1.4rem 2rem;">
      <div class="hero-title" style="font-size:1.4rem;">Patient Records</div>
      <div class="hero-tagline" style="font-size:.9rem;">Complete dataset with search and filter capabilities.</div>
    </div>""", unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.patients)

    sc1, sc2, sc3 = st.columns([3, 2, 2])
    search   = sc1.text_input("🔍 Search by name or token", placeholder="Type to search…")
    f_status = sc2.selectbox("Status", ["All"] + STATUSES)
    f_gender = sc3.selectbox("Gender", ["All", "Male", "Female", "Other"])

    fdf = df.copy()
    if search:
        mask = (fdf["Name"].str.contains(search, case=False) |
                fdf["Token"].str.contains(search, case=False))
        fdf = fdf[mask]
    if f_status != "All": fdf = fdf[fdf["Status"] == f_status]
    if f_gender != "All": fdf = fdf[fdf["Gender"] == f_gender]

    st.caption(f"{len(fdf)} record(s) found")

    def style_status(val):
        colors = {"Waiting": "#f59e0b", "In Progress": "#3b82f6", "Completed": "#10b981"}
        c = colors.get(val, "#94a3b8")
        return f"color: {c}; font-weight: 600;"

    def style_priority(val):
        return "color: #ef4444; font-weight: 700;" if val == "Urgent" else ""

    styled = fdf.style.applymap(style_status, subset=["Status"]) \
                      .applymap(style_priority, subset=["Priority"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=480)

    st.download_button(
        label="⬇ Download as CSV",
        data=fdf.to_csv(index=False),
        file_name=f"patients_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    init_state()
    sidebar()

    page = st.session_state.page
    if page == "Dashboard":        page_dashboard()
    elif page == "Register Patient": page_register()
    elif page == "Patient Queue":  page_queue()
    elif page == "Analytics":      page_analytics()
    elif page == "Patient Records": page_records()

if __name__ == "__main__":
    main()
