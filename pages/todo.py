# todo.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_todo_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            todo_name TEXT NOT NULL,
            deadline DATE NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_todo(todo_name, deadline, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO todo (todo_name, deadline, user_id) VALUES (?, ?, ?)", (todo_name, deadline, user_id))

    conn.commit()
    conn.close()

def view_todos(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM todo WHERE user_id = ?", (user_id,))
    todos = cursor.fetchall()

    conn.close()
    return todos

def update_todo_deadline(todo_id, new_deadline):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE todo SET deadline = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_deadline, todo_id))

    conn.commit()
    conn.close()

def delete_todo(todo_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todo WHERE id = ?", (todo_id,))

    conn.commit()
    conn.close()

def display_todo_page():
    st.title("Todo")

    # Create todo table if not exists
    create_todo_table()

    user_id = st.session_state.user_id

    # Add todo form
    with st.form("add_todo_form"):
        todo_name = st.text_input("Todo Name:")
        deadline = st.date_input("Deadline:", min_value=datetime.today())
        submit_button = st.form_submit_button("Add Todo")

    if submit_button:
        # Add todo to the database
        add_todo(todo_name, deadline, user_id)
        st.success(f"Todo '{todo_name}' added with deadline '{deadline}'.")

    # View todos
    todos = view_todos(user_id)
    if todos:
        st.subheader("Your Todos:")
        for todo in todos:
            st.write(f"Todo: {todo[1]}, Deadline: {todo[2]}")
            
            # Update deadline form
            with st.form(key=f"update_todo_{todo[0]}"):
                new_deadline = st.date_input("New Deadline:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Todo Deadline")

            if update_button:
                # Update todo deadline
                update_todo_deadline(todo[0], new_deadline)
                st.success(f"Deadline for '{todo[1]}' updated to '{new_deadline}'.")
            
            # Delete todo button
            if st.button(f"Delete {todo[1]}"):
                # Delete todo
                delete_todo(todo[0])
                st.success(f"Todo '{todo[1]}' deleted.")

    else:
        st.info("No todos found.")
