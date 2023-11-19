# quiz.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_quiz_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_name TEXT NOT NULL,
            quiz_date DATE NOT NULL,
            num_questions INTEGER,
            correct_answers INTEGER,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_quiz(quiz_name, quiz_date, num_questions, correct_answers, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    query = ''' 
            CREATE PROCEDURE add_quiz_procedure(
                IN quiz_name_param TEXT,
                IN quiz_date_param DATE,
                IN num_questions_param INT,
                IN correct_answers_param INT,
                IN user_id_param INT
            )
            BEGIN
                INSERT INTO quiz (quiz_name, quiz_date, num_questions, correct_answers, user_id)
                VALUES (quiz_name_param, quiz_date_param, num_questions_param, correct_answers_param, user_id_param);
            END;
            
            '''

    cursor.execute("INSERT INTO quiz (quiz_name, quiz_date, num_questions, correct_answers, user_id) VALUES (?, ?, ?, ?, ?)", 
                   (quiz_name, quiz_date, num_questions, correct_answers, user_id))

    conn.commit()
    conn.close()
    return query

def view_quizzes(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quiz WHERE user_id = ?", (user_id,))
    quizzes = cursor.fetchall()

    conn.close()
    return quizzes

def update_quiz_date(quiz_id, new_quiz_date):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE quiz SET quiz_date = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_quiz_date, quiz_id))

    conn.commit()
    conn.close()

def delete_quiz(quiz_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM quiz WHERE id = ?", (quiz_id,))

    conn.commit()
    conn.close()

def display_quiz_page():
    st.title("Quiz")

    # Create quiz table if not exists
    create_quiz_table()

    user_id = st.session_state.user_id

    # Add quiz form
    with st.form("add_quiz_form"):
        quiz_name = st.text_input("Quiz Name:")
        quiz_date = st.date_input("Quiz Date:", min_value=datetime.today())
        num_questions = st.number_input("Number of Questions:", min_value=0, step=1, value=0)
        correct_answers = st.number_input("Correct Answers:", min_value=0, step=1, value=0)
        submit_button = st.form_submit_button("Add Quiz")

    if submit_button:
        # Add quiz to the database
        add_quiz(quiz_name, quiz_date, num_questions, correct_answers, user_id)
        st.success(f"Quiz '{quiz_name}' added on '{quiz_date}' with {num_questions} questions and {correct_answers} correct answers.")

    # View quizzes
    quizzes = view_quizzes(user_id)
    if quizzes:
        st.subheader("Your Quizzes:")
        for quiz in quizzes:
            st.write(f"Quiz: {quiz[1]}, Date: {quiz[2]}, Questions: {quiz[3]}, Correct Answers: {quiz[4]}")
            
            # Update date form
            with st.form(key=f"update_quiz_{quiz[0]}"):
                new_quiz_date = st.date_input("New Quiz Date:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Quiz Date")

            if update_button:
                # Update quiz date
                update_quiz_date(quiz[0], new_quiz_date)
                st.success(f"Date for '{quiz[1]}' updated to '{new_quiz_date}'.")
            
            # Delete quiz button
            if st.button(f"Delete {quiz[1]}"):
                # Delete quiz
                delete_quiz(quiz[0])
                st.success(f"Quiz '{quiz[1]}' deleted.")

    else:
        st.info("No quizzes found.")
