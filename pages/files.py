# files.py
import streamlit as st
import sqlite3

def create_files_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_file(file_name, file_path, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO files (file_name, file_path, user_id) VALUES (?, ?, ?)", (file_name, file_path, user_id))

    conn.commit()
    conn.close()

def view_files(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM files WHERE user_id = ?", (user_id,))
    files = cursor.fetchall()

    conn.close()
    return files

def update_file_path(file_id, new_file_path):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE files SET file_path = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_file_path, file_id))

    conn.commit()
    conn.close()

def delete_file(file_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))

    conn.commit()
    conn.close()

def display_files_page():
    st.title("Files")

    # Create files table if not exists
    create_files_table()

    user_id = st.session_state.user_id

    # Add file form
    with st.form("add_file_form"):
        file_name = st.text_input("File Name:")
        file_path = st.text_input("File Path:")
        submit_button = st.form_submit_button("Add File")

    if submit_button:
        # Add file to the database
        add_file(file_name, file_path, user_id)
        st.success(f"File '{file_name}' added with path '{file_path}'.")

    # View files
    files = view_files(user_id)
    if files:
        st.subheader("Your Files:")
        for file in files:
            st.write(f"File: {file[1]}, Path: {file[2]}")
            
            # Update path form
            with st.form(key=f"update_file_{file[0]}"):
                new_file_path = st.text_input("New File Path:")
                update_button = st.form_submit_button("Update File Path")

            if update_button:
                # Update file path
                update_file_path(file[0], new_file_path)
                st.success(f"Path for '{file[1]}' updated to '{new_file_path}'.")
            
            # Delete file button
            if st.button(f"Delete {file[1]}"):
                # Delete file
                delete_file(file[0])
                st.success(f"File '{file[1]}' deleted.")

    else:
        st.info("No files found.")
