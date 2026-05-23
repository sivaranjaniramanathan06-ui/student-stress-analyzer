import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(
    page_title="Student Stress Analyzer",
    layout="wide"
)

# Title
st.title("📊 Student Stress Level Analyzer Dashboard")

st.markdown("Analyze student stress levels and provide wellness suggestions.")

# Sidebar
st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Read dataset
    data = pd.read_csv(uploaded_file)

    # Stress calculation
    def calculate_stress(row):

        stress_score = 0

        if row['StudyHours'] > 8:
            stress_score += 2

        if row['SleepHours'] < 6:
            stress_score += 2

        if row['ScreenTime'] > 5:
            stress_score += 1

        if row['ExerciseHours'] == 0:
            stress_score += 1

        if stress_score >= 5:
            return "High"

        elif stress_score >= 3:
            return "Medium"

        else:
            return "Low"

    # Recommendation function
    def give_solution(row):

        if row['StressLevel'] == 'High':
            return "Sleep more, exercise daily, and reduce screen time."

        elif row['StressLevel'] == 'Medium':
            return "Maintain a balanced schedule and relax regularly."

        else:
            return "Healthy lifestyle maintained."

    # Apply functions
    data['StressLevel'] = data.apply(calculate_stress, axis=1)

    data['Solution'] = data.apply(give_solution, axis=1)

    # Dashboard Metrics
    st.subheader("📌 Dashboard Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", len(data))

    col2.metric(
        "Average Study Hours",
        round(data['StudyHours'].mean(), 2)
    )

    col3.metric(
        "Average Sleep Hours",
        round(data['SleepHours'].mean(), 2)
    )

    # Display Dataset
    st.subheader("📄 Student Dataset")
    st.dataframe(data)

    # Stress Count
    stress_count = data['StressLevel'].value_counts()

    # Charts section
    st.subheader("📊 Stress Visualization")

    chart1, chart2 = st.columns(2)

    # Bar chart
    with chart1:

        fig1, ax1 = plt.subplots()

        ax1.bar(
            stress_count.index,
            stress_count.values
        )

        ax1.set_title("Stress Level Count")

        ax1.set_xlabel("Stress Level")

        ax1.set_ylabel("Number of Students")

        st.pyplot(fig1)

    # Pie chart
    with chart2:

        fig2, ax2 = plt.subplots()

        ax2.pie(
            stress_count.values,
            labels=stress_count.index,
            autopct='%1.1f%%'
        )

        ax2.set_title("Stress Distribution")

        st.pyplot(fig2)

    # High stress students
    st.subheader("⚠ High Stress Students")

    high_stress = data[data['StressLevel'] == 'High']

    st.dataframe(
        high_stress[['Student', 'StressLevel', 'Solution']]
    )

else:

    st.info("Please upload a CSV file to begin analysis.")