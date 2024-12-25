import streamlit as st
import pandas as pd
import random

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('/mnt/data/questions_dataset.csv')
    grouped = data.groupby("question_number").apply(lambda df: {
        "question_number": df.iloc[0]["question_number"],
        "question": df.iloc[0]["question"],
        "options": df["option"].tolist(),
        "correct_answer": df[df["is_correct"] == "Yes"]["option"].iloc[0] if not df[df["is_correct"] == "Yes"].empty else None  # Handle empty DataFrame
    }).tolist()
    return grouped

# Function to generate a random quiz
def generate_quiz(data, num_questions=33):
    return random.sample(data, num_questions)

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
for i, question_data in enumerate(st.session_state['quiz_data']):
    st.write(f"**Question {i + 1}:** {question_data['question']}")
    st.session_state['responses'][i] = st.radio(
        f"Select an answer for Question {i + 1}:",
        question_data['options'],
        index=-1 if st.session_state['responses'][i] is None else question_data['options'].index(st.session_state['responses'][i]),
        key=f"q{i}"
    )

# Finish button
if st.button("Finish Test"):
    if None in st.session_state['responses']:
        st.error("Please answer all questions before finishing the test.")
    else:
        correct_answers = 0
        for i, question_data in enumerate(st.session_state['quiz_data']):
            if st.session_state['responses'][i] == question_data['correct_answer']:
                correct_answers += 1
        st.write(f"You scored {correct_answers} out of 33.")

        # Reset quiz state for new simulation
        if st.button("Start a New Quiz"):
            del st.session_state['quiz_data']
            del st.session_state['responses']
            st.experimental_rerun()
