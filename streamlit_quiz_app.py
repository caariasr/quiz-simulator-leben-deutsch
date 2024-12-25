import streamlit as st
import pandas as pd
import random

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('./data/questions_dataset.csv')
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
    st.session_state['show_results'] = False

# Quiz instructions
st.write("This quiz simulates 33 questions from the Einbürgerungstest. Answer the questions below and click 'Finish Test' to see your score. Refresh page to have a new random set of 33 questions")

# Display quiz questions
for i, question_data in enumerate(st.session_state['quiz_data']):
    st.write(f"**Question {i + 1}:** {question_data['question']}")
    if st.session_state['show_results']:
        correct = question_data['correct_answer']
        for option in question_data['options']:
            if option == correct:
                st.write(f"✅ **{option}** (Correct)")
            elif option == st.session_state['responses'][i]:
                st.write(f"❌ **{option}** (Your Answer)")
            else:
                st.write(option)
    else:
        st.session_state['responses'][i] = st.radio(
            f"Select an answer for Question {i + 1}:",
            question_data['options'],
            index=0,
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

        if correct_answers > 16:
            st.success("Congratulations, you passed!")
        else:
            st.error("Unfortunately you didn't pass this simulation, keep practicing")

# Show Answers button
if st.button("Show Answers"):
    st.session_state['show_results'] = True
    st.rerun()

# Reset quiz state for new simulation
if st.session_state['show_results'] and st.button("Start a New Quiz"):
    del st.session_state['quiz_data']
    del st.session_state['responses']
    del st.session_state['show_results']
    st.rerun()
