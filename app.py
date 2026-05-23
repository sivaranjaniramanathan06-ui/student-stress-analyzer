import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Student Stress Level Analyzer")

# Upload CSV file
uploaded_file = st.file_uploader("Upload Student CSV File", type=["csv"])

if uploaded_file is not None:

    # Read CSV
    data = pd.read_csv(uploaded_file)

    st.subheader("Student Dataset")
    st.write(data)

    # Stress calculation function
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

    # Solution function
    def give_solution(row):

        if row['StressLevel'] == 'High':
            return "Take breaks, sleep more, reduce screen time, and exercise."

        elif row['StressLevel'] == 'Medium':
            return "Maintain a balanced routine and relax regularly."

        else:
            return "Keep maintaining your healthy lifestyle."

    # Apply stress analysis
    data['StressLevel'] = data.apply(calculate_stress, axis=1)

    # Apply solutions
    data['Solution'] = data.apply(give_solution, axis=1)

    # Display result
    st.subheader("Stress Analysis Result")
    st.write(data)

    # Count stress levels
    stress_count = data['StressLevel'].value_counts()

    # Bar chart
    st.subheader("Stress Level Chart")

    fig, ax = plt.subplots()

    ax.bar(stress_count.index, stress_count.values)

    ax.set_xlabel("Stress Level")
    ax.set_ylabel("Number of Students")

    st.pyplot(fig)