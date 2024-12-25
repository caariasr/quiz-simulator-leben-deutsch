import streamlit as st
import pandas as pd
import random

# Load dataset
@st.cache
def load_data():
    return pd.read_csv('/mnt/data/questions_dataset.csv')

# Function to generate a random quiz
def generate_quiz(data, num_questions=33):
    return data.sample(n=num_questions, replace=False).reset_index(drop=True)

# Streamlit app
st.title("Einbürgerungstest Quiz Simulator")

# Load the dataset
data = load_data()

# Session state to manage quiz state
if 'quiz_data' not in st.session_state:
    st.session_state['quiz_data'] = generate_quiz(data)
    st.session_state['responses'] = [None] * 33

# Quiz instructions
st.write("This quiz simulates 33 questions from the Einbürgerungstest. Answer the questions below and click 'Finish Test' to see your score.")

# Display quiz questions
for i, row in st.session_state['quiz_data'].iterrows():
    st.write(f"**Question {i + 1}:** {row['question']}")
    options = [row[f"option_{j}"] for j in range(1, 5) if pd.notna(row[f"option_{j}"])]
    st.session_state['responses'][i] = st.radio(f"Select an answer for Question {i + 1}:", options, index=0 if st.session_state['responses'][i] is None else options.index(st.session_state['responses'][i]), key=f"q{i}")

# Finish button
if st.button("Finish Test"):
    correct_answers = 0
    for i, row in st.session_state['quiz_data'].iterrows():
        if st.session_state['responses'][i] == row['correct_answer']:
            correct_answers += 1
    st.write(f"You scored {correct_answers} out of 33.")

    # Reset quiz state for new simulation
    if st.button("Start a New Quiz"):
        st.session_state['quiz_data'] = generate_quiz(data)
        st.session_state['responses'] = [None] * 33
