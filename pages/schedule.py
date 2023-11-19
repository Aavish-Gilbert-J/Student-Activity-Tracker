# schedule.py
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse', False)
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

def view_data(user_id):
        conn = sqlite3.connect("data/student_tracker.db")
        cursor = conn.cursor()

        # You can customize the query based on your table structure
        cursor.execute("SELECT COUNT(*) FROM classes WHERE user_id = ?", (user_id,))
        class_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id = ?", (user_id,))
        assignment_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM exams WHERE user_id = ?", (user_id,))
        exam_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM meetings WHERE user_id = ?", (user_id,))
        meeting_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM internship WHERE user_id = ?", (user_id,))
        internship_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM projects WHERE user_id = ?", (user_id,))
        project_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM quiz WHERE user_id = ?", (user_id,))
        quiz_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM todo WHERE user_id = ?", (user_id,))
        todo_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM files WHERE user_id = ?", (user_id,))
        file_count = cursor.fetchone()[0]

        conn.close()

        return (
            class_count,
            assignment_count,
            exam_count,
            meeting_count,
            internship_count,
            project_count,
            quiz_count,
            todo_count,
            file_count
        )


def plot_bar_graph(data, numbers):

# Create a DataFrame from the input data
    df = pd.DataFrame(data, columns=['Category', 'Value'])
    
    
    plt.figure(figsize=(8, 3))  # Set the background color to black
    plt.bar(df['Category'], df['Value'])
    
    plt.ylabel('Number of items')

    plt.xticks(rotation=45)

    plt.yticks(np.arange(0, max(numbers) + 1, 1))

    # Display the plot using Streamlit
    st.pyplot()
      


def display_schedule_page():
    
    user_id = st.session_state.user_id
    
    data = [
        "class",
        "assignment",
        "exam",
        "meeting",
        "internship",
        "project",
        "quiz",
        "todo",
        "file"
     ] 
    
    numbers = view_data(user_id)
    # print([(data[i], numbers[i]) for i in range(len(data))])
    # print(numbers)
    # print(data)
    
    # Display counts as comments
    plot_bar_graph(zip(data, numbers), numbers)

   
    st.title("Schedule")

    # View schedule
    classes, assignments, exams, meetings, internships, projects, quizzes, todos, files = view_schedule(user_id)

    
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
            st.write(f"File: {file_info[1]}")
