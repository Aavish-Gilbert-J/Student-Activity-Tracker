# files.py
import streamlit as st
import sqlite3
import os
from datetime import datetime

def create_files_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_data BLOB,
            file_size INTEGER,
            upload_time TIMESTAMP,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create file_logs table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_description TEXT NOT NULL,
            event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create trigger for after_insert_file
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_insert_file
        AFTER INSERT ON files
        BEGIN
            INSERT INTO file_logs (event_type, event_description, event_timestamp)
            VALUES ('INSERT', 'New file added', CURRENT_TIMESTAMP);
        END;
    ''')

    conn.commit()
    conn.close()

def add_file(file_name, file_data, file_size, upload_time, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO files (file_name, file_data, file_size, upload_time, user_id) VALUES (?, ?, ?, ?, ?)", 
                   (file_name, file_data, file_size, upload_time, user_id))

    # Get the file_id and event_timestamp after inserting
    cursor.execute("SELECT last_insert_rowid(), (SELECT event_timestamp FROM file_logs ORDER BY id DESC LIMIT 1)")
    result = cursor.fetchone()

    conn.commit()
    conn.close()

    return result  # Return file_id and event_timestamp

def view_files(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM files WHERE user_id = ?", (user_id,))
    files = cursor.fetchall()

    conn.close()
    return files

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
        uploaded_file = st.file_uploader("Drag and drop your file here, or browse for it:", 
                                         type=["csv", "xlsx", "xls", "txt", "pdf", "png", "jpg", "jpeg", "gif", "mp4", "mp3", "wav"])
        submit_button = st.form_submit_button("Add File")

    if submit_button:
        # Check if a file was uploaded
        if uploaded_file is not None:
            # Get file details
            file_data = uploaded_file.read()
            file_size = len(file_data)
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add file to the database
            file_id, event_timestamp = add_file(file_name, file_data, file_size, upload_time, user_id)
            st.success(f"File '{file_name}' added with size {file_size} bytes.")
            st.info(f"File ID: {file_id}, Event Timestamp: {event_timestamp}")

        else:
            st.warning("Please upload a valid file.")

    # View files
    files = view_files(user_id)
    if files:
        st.subheader("Your Files:")
        for file in files:
            st.write(f"File: {file[1]}, Upload Time: {file[3]} ms")

            # Download button
            download_button = st.download_button(
                label=f"Download {file[1]}",
                key=f"download_button_{file[0]}",
                data=file[2],
                file_name=file[1]
            )

            # Delete file button
            if st.button(f"Delete {file[1]}"):
                # Delete file
                delete_file(file[0])
                st.success(f"File '{file[1]}' deleted.")

    else:
        st.info("No files found.")