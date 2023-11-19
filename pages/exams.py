 # exams.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_exams_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT NOT NULL,
            exam_date DATE NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_exam(exam_name, exam_date, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO exams (exam_name, exam_date, user_id) VALUES (?, ?, ?)", (exam_name, exam_date, user_id))

    conn.commit()
    conn.close()

def view_exams(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM exams WHERE user_id = ?", (user_id,))
    exams = cursor.fetchall()

    conn.close()
    return exams

def update_exam_date(exam_id, new_exam_date):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE exams SET exam_date = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_exam_date, exam_id))

    conn.commit()
    conn.close()

def delete_exam(exam_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM exams WHERE id = ?", (exam_id,))

    conn.commit()
    conn.close()

def display_exams_page():
    st.title("Exams")

    # Create exams table if not exists
    create_exams_table()

    user_id = st.session_state.user_id

    # Add exam form
    with st.form("add_exam_form"):
        exam_name = st.text_input("Exam Name:")
        exam_date = st.date_input("Exam Date:", min_value=datetime.today())
        submit_button = st.form_submit_button("Add Exam")

    if submit_button:
        # Add exam to the database
        add_exam(exam_name, exam_date, user_id)
        st.success(f"Exam '{exam_name}' added with date '{exam_date}'.")

    # View exams
    exams = view_exams(user_id)
    if exams:
        st.subheader("Your Exams:")
        for exam in exams:
            st.write(f"Exam: {exam[1]}, Date: {exam[2]}")
            
            # Update date form
            with st.form(key=f"update_exam_{exam[0]}"):
                new_exam_date = st.date_input("New Exam Date:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Exam Date")

            if update_button:
                # Update exam date
                update_exam_date(exam[0], new_exam_date)
                st.success(f"Date for '{exam[1]}' updated to '{new_exam_date}'.")
            
            # Delete exam button
            if st.button(f"Delete {exam[1]}"):
                # Delete exam
                delete_exam(exam[0])
                st.success(f"Exam '{exam[1]}' deleted.")

    else:
        st.info("No exams found.")
