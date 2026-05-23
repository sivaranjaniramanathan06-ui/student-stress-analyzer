import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Stress Analyzer Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# 🌈 UI STYLING (CSS)
# =========================
st.markdown("""
<style>

/* 🌈 Main Background */
.stApp {
    background-color: #f4f6f9;
    color: #111827;
}

/* 📁 Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
}

/* 🔘 Buttons */
.stButton>button {
    background: #4f46e5;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: #4338ca;
}

/* 📦 Metric Cards */
div[data-testid="stMetric"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

/* 🌫 Glass Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

/* 📊 Titles */
h1, h2, h3 {
    color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
# 📊 Student Stress Analyzer Dashboard  
### 🌿 AI-powered wellness insights for students  
""")

st.markdown("Analyze student stress levels and get personalized wellness recommendations.")

st.write("")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📁 Upload Dataset")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

st.sidebar.header("📝 Real-Time Input")

student_name_input = st.sidebar.text_input("Student Name")
study_hours_input = st.sidebar.slider("Study Hours", 0, 15, 6)
sleep_hours_input = st.sidebar.slider("Sleep Hours", 0, 12, 7)
screen_time_input = st.sidebar.slider("Screen Time", 0, 12, 4)
exercise_hours_input = st.sidebar.slider("Exercise Hours", 0, 5, 1)

analyze_button = st.sidebar.button("Analyze Stress")

# =========================
# MAIN DATA LOGIC
# =========================
if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    # Stress calculation
    def calculate_stress(row):
        score = 0
        if row['StudyHours'] > 8:
            score += 30
        if row['SleepHours'] < 6:
            score += 30
        if row['ScreenTime'] > 5:
            score += 20
        if row['ExerciseHours'] == 0:
            score += 20
        return min(score, 100)

    data['StressScore'] = data.apply(calculate_stress, axis=1)

    def stress_level(score):
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        return "Low"

    data['StressLevel'] = data['StressScore'].apply(stress_level)

    def give_solution(row):
        if row['StressLevel'] == "High":
            return "⚠ Reduce stress: Sleep more, exercise, reduce screen time"
        elif row['StressLevel'] == "Medium":
            return "⚡ Maintain balance and relax"
        return "✅ Healthy lifestyle"

    data['Recommendation'] = data.apply(give_solution, axis=1)

    # =========================
    # METRICS
    # =========================
    st.subheader("📌 Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(data))
    col2.metric("Avg Stress", round(data['StressScore'].mean(), 1))
    col3.metric("Avg Study Hours", round(data['StudyHours'].mean(), 1))
    col4.metric("Avg Sleep Hours", round(data['SleepHours'].mean(), 1))

    # =========================
    # QUICK CARDS (GLASS UI)
    # =========================
    st.markdown("## 🌟 Wellness Insights")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
        <h3>📚 Study</h3>
        <p>Keep study hours between 6–8 for balance</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
        <h3>😴 Sleep</h3>
        <p>7–8 hours sleep improves focus</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="glass-card">
        <h3>🏃 Health</h3>
        <p>Exercise reduces stress naturally</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # TABLE
    # =========================
    st.subheader("📄 Dataset")
    st.dataframe(data)

    # =========================
    # HIGH STRESS ALERT
    # =========================
    high_stress = data[data['StressLevel'] == "High"]

    st.subheader("🚨 Alerts")

    if len(high_stress) > 0:

        st.markdown("""
        <div style="
        background-color:#ff4d4d;
        color:white;
        padding:15px;
        border-radius:10px;
        font-weight:bold;
        animation: blink 1s infinite;
        ">
        🚨 HIGH STRESS ALERT DETECTED!
        </div>

        <style>
        @keyframes blink {
            50% {opacity: 0.5;}
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.success("No high stress students detected.")

    # =========================
    # CHARTS
    # =========================
    st.subheader("📊 Insights")

    fig = px.bar(data, x="Student", y="StressScore", color="StressLevel")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# REAL-TIME ANALYSIS
# =========================
if analyze_button:

    score = 0

    if study_hours_input > 8:
        score += 30
    if sleep_hours_input < 6:
        score += 30
    if screen_time_input > 5:
        score += 20
    if exercise_hours_input == 0:
        score += 20

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    st.subheader("🧠 Real-Time Analysis")
    st.write(f"👤 Student: {student_name_input}")
    st.write(f"📊 Stress Score: {score}")
    st.write(f"🚨 Stress Level: {level}")