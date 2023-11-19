# schedule.py
import streamlit as st
import sqlite3

def view_schedule(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    # You can customize the query based on your table structure
    cursor.execute("SELECT * FROM classes WHERE user_id = ?", (user_id,))
    classes = cursor.fetchall()

    cursor.execute("SELECT * FROM assignments WHERE user_id = ?", (user_id,))
    assignments = cursor.fetchall()

    cursor.execute("SELECT * FROM exams WHERE user_id = ?", (user_id,))
    exams = cursor.fetchall()

    cursor.execute("SELECT * FROM meetings WHERE user_id = ?", (user_id,))
    meetings = cursor.fetchall()

    cursor.execute("SELECT * FROM internship WHERE user_id = ?", (user_id,))
    internships = cursor.fetchall()

    cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user_id,))
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM quiz WHERE user_id = ?", (user_id,))
    quizzes = cursor.fetchall()

    cursor.execute("SELECT * FROM todo WHERE user_id = ?", (user_id,))
    todos = cursor.fetchall()

    cursor.execute("SELECT * FROM files WHERE user_id = ?", (user_id,))
    files = cursor.fetchall()

    conn.close()

    return classes, assignments, exams, meetings, internships, projects, quizzes, todos, files

def display_schedule_page():
    st.title("Schedule")

    user_id = st.session_state.user_id

    # View schedule
    classes, assignments, exams, meetings, internships, projects, quizzes, todos, files = view_schedule(user_id)

    st.subheader("Your Schedule:")
    
    # Display classes
    if classes:
        st.subheader("Classes:")
        for class_info in classes:
            st.write(f"Class: {class_info[1]}, Time: {class_info[2]} - {class_info[3]}")

    # Display assignments
    if assignments:
        st.subheader("Assignments:")
        for assignment in assignments:
            st.write(f"Assignment: {assignment[1]}, Deadline: {assignment[2]}")

    # Display exams
    if exams:
        st.subheader("Exams:")
        for exam in exams:
            st.write(f"Exam: {exam[1]}, Date: {exam[2]}")

    # Display meetings
    if meetings:
        st.subheader("Meetings:")
        for meeting in meetings:
            st.write(f"Meeting: {meeting[1]}, Date: {meeting[2]}")

    # Display internships
    if internships:
        st.subheader("Internships:")
        for internship in internships:
            st.write(f"Internship: {internship[1]}, Start Date: {internship[2]}, End Date: {internship[3]}")

    # Display projects
    if projects:
        st.subheader("Projects:")
        for project in projects:
            st.write(f"Project: {project[1]}, Deadline: {project[2]}")

    # Display quizzes
    if quizzes:
        st.subheader("Quizzes:")
        for quiz in quizzes:
            st.write(f"Quiz: {quiz[1]}, Date: {quiz[2]}")

    # Display todos
    if todos:
        st.subheader("Todos:")
        for todo in todos:
            st.write(f"Todo: {todo[1]}, Deadline: {todo[2]}")

    # Display files
    if files:
        st.subheader("Files:")
        for file_info in files:
            st.write(f"File: {file_info[1]}, Path: {file_info[2]}")
