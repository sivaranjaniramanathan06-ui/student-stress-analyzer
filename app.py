import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas

# Page settings
st.set_page_config(
    page_title="AI Student Stress Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI-Powered Student Stress Dashboard")

st.markdown("""
Analyze student stress levels, visualize patterns,
and provide personalized wellness recommendations.
""")

# Sidebar
st.sidebar.header("📁 Upload Student Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# Real-Time Student Input
st.sidebar.header("📝 Real-Time Student Entry")

student_name_input = st.sidebar.text_input(
    "Student Name"
)

study_hours_input = st.sidebar.slider(
    "Study Hours",
    0,
    15,
    6
)

sleep_hours_input = st.sidebar.slider(
    "Sleep Hours",
    0,
    12,
    7
)

screen_time_input = st.sidebar.slider(
    "Screen Time",
    0,
    12,
    4
)

exercise_hours_input = st.sidebar.slider(
    "Exercise Hours",
    0,
    5,
    1
)

exam_score_input = st.sidebar.slider(
    "Exam Score",
    0,
    100,
    75
)

analyze_button = st.sidebar.button(
    "Analyze Stress"
)

if uploaded_file is not None:

    # Read dataset
    data = pd.read_csv(uploaded_file)

    # Stress calculation function
    def calculate_stress(row):

        stress_score = 0

        if row['StudyHours'] > 8:
            stress_score += 30

        if row['SleepHours'] < 6:
            stress_score += 30

        if row['ScreenTime'] > 5:
            stress_score += 20

        if row['ExerciseHours'] == 0:
            stress_score += 20

        return min(stress_score, 100)

    # Apply stress score
    data['StressScore'] = data.apply(
        calculate_stress,
        axis=1
    )

    # Stress level category
    def stress_level(score):

        if score >= 70:
            return "High"

        elif score >= 40:
            return "Medium"

        else:
            return "Low"

    data['StressLevel'] = data['StressScore'].apply(
        stress_level
    )

    # Personalized solutions
    def give_solution(row):

        if row['StressLevel'] == "High":

            return (
                "⚠ High stress detected. "
                "Sleep more, reduce screen time, "
                "exercise daily, and take study breaks."
            )

        elif row['StressLevel'] == "Medium":

            return (
                "⚡ Moderate stress detected. "
                "Maintain balance and practice relaxation."
            )

        else:

            return (
                "✅ Healthy lifestyle maintained."
            )

    data['Recommendation'] = data.apply(
        give_solution,
        axis=1
    )

    # Sidebar search
    st.sidebar.header("🔍 Search & Filter")

    # Student search
    student_name = st.sidebar.text_input(
        "Enter Student Name"
    )

    # Stress level filter
    stress_filter = st.sidebar.selectbox(
        "Filter by Stress Level",
        ["All", "High", "Medium", "Low"]
    )

    # Start with full dataset
    filtered_data = data.copy()

    # Apply student search
    if student_name:

        filtered_data = filtered_data[
            filtered_data['Student'].str.contains(
                student_name,
                case=False
            )
        ]

    # Apply stress filter
    if stress_filter != "All":

        filtered_data = filtered_data[
            filtered_data['StressLevel'] == stress_filter
        ]

    # Metrics
    st.subheader("📌 Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Students",
        len(data)
    )

    col2.metric(
        "Average Stress Score",
        round(data['StressScore'].mean(), 1)
    )

    col3.metric(
        "Average Study Hours",
        round(data['StudyHours'].mean(), 1)
    )

    col4.metric(
        "Average Sleep Hours",
        round(data['SleepHours'].mean(), 1)
    )

    # Dataset display
    st.subheader("📄 Student Stress Dataset")

    st.dataframe(filtered_data)

    # Gauge Meter
    st.subheader("🎯 Average Stress Meter")

    avg_stress = data['StressScore'].mean()

    gauge_fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=avg_stress,

        title={'text': "Average Stress Score"},

        gauge={

            'axis': {'range': [0, 100]},

            'bar': {'color': "red"},

            'steps': [

                {'range': [0, 40], 'color': "green"},

                {'range': [40, 70], 'color': "yellow"},

                {'range': [70, 100], 'color': "red"}

            ]
        }
    ))

    st.plotly_chart(
        gauge_fig,
        use_container_width=True
    )

    # Interactive charts
    st.subheader("📊 Student Wellness Insights")

    chart1, chart2 = st.columns(2)

    # Bar chart
    with chart1:

        bar_fig = px.bar(
            data,
            x='Student',
            y='StressScore',
            color='StressLevel',
            title="Student Stress Scores"
        )

        st.plotly_chart(
            bar_fig,
            use_container_width=True
        )

    # Pie chart
    with chart2:

        pie_fig = px.pie(
            data,
            names='StressLevel',
            title="Stress Level Distribution"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    # Student Comparison Analytics
    st.subheader("📈 Student Comparison Analytics")

    comparison_fig = px.line(
        data,
        x='Student',
        y=[
            'StudyHours',
            'SleepHours',
            'ScreenTime'
        ],
        markers=True,
        title="Student Lifestyle Comparison"
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )

    # High stress alert
    st.subheader("🚨 High Stress Alerts")

    high_stress = data[
        data['StressLevel'] == 'High'
    ]

    if len(high_stress) > 0:

        st.error(
            f"{len(high_stress)} students are under high stress!"
        )

        st.dataframe(
            high_stress[
                [
                    'Student',
                    'StressScore',
                    'Recommendation'
                ]
            ]
        )

    else:

        st.success(
            "No high stress students detected."
        )

    # Download report
    csv = data.to_csv(index=False).encode('utf-8')
    
    # PDF Report Generator
    def create_pdf():

        pdf = canvas.Canvas("stress_report.pdf")

        pdf.setFont("Helvetica-Bold", 16)

        pdf.drawString(
            180,
            800,
            "Student Stress Report"
        )

        y = 760

        pdf.setFont("Helvetica", 12)

        for index, row in data.iterrows():

            text = (
                f"{row['Student']} | "
                f"Stress: {row['StressLevel']} | "
                f"Score: {row['StressScore']}"
            )

            pdf.drawString(50, y, text)

            y -= 20

        pdf.save()

    # Create PDF
    create_pdf()

    # Download PDF
    with open("stress_report.pdf", "rb") as file:

        st.download_button(

            label="📄 Download PDF Report",

            data=file,

            file_name="stress_report.pdf",

            mime="application/pdf"
        )

    st.download_button(
        label="📥 Download Stress Report",
        data=csv,
        file_name='student_stress_report.csv',
        mime='text/csv'
    )

        # Real-Time Analysis
    if analyze_button:

        stress_score = 0

        if study_hours_input > 8:
            stress_score += 30

        if sleep_hours_input < 6:
            stress_score += 30

        if screen_time_input > 5:
            stress_score += 20

        if exercise_hours_input == 0:
            stress_score += 20

        # Stress Level
        if stress_score >= 70:
            stress_level = "High"

        elif stress_score >= 40:
            stress_level = "Medium"

        else:
            stress_level = "Low"

        # Recommendation
        if stress_level == "High":

            recommendation = (
                "⚠ High stress detected. "
                "Sleep more, reduce screen time, "
                "exercise daily, and take breaks."
            )

        elif stress_level == "Medium":

            recommendation = (
                "⚡ Moderate stress detected. "
                "Maintain balance and relax regularly."
            )

        else:

            recommendation = (
                "✅ Healthy lifestyle maintained."
            )

        # Display Results
        st.subheader("🧠 Real-Time Stress Analysis")

        st.write(f"### 👤 Student: {student_name_input}")

        st.write(f"### 📊 Stress Score: {stress_score}")

        st.write(f"### 🚨 Stress Level: {stress_level}")

        st.success(recommendation)

else:

    st.info("📂 Please upload a CSV file to start analysis.")