# app.py
import streamlit as st
from streamlit_option_menu import option_menu
import st_pages as stp

from pages.user_management import display_user_management_page
from pages.schedule import display_schedule_page
from pages.todo import display_todo_page
from pages.projects import display_projects_page
from pages.quiz import display_quiz_page
from pages.meetings import display_meetings_page
from pages.internship import display_internship_page
from pages.assignments import display_assignments_page
from pages.exams import display_exams_page
from pages.files import display_files_page



# Main Streamlit app
def main():
    
    st.title("Student Tracker App")
    stp.hide_pages(["app", "assignments", "exams", "files", "internship", "meetings", "projects", "quiz", "schedule", "todo", "user_management"])

    # Check if the user is logged in
    if "user_id" not in st.session_state:
        st.session_state.user_id = 5

    # Navigation
    pages = {
      
        "User Management": display_user_management_page,
        "Schedule": display_schedule_page,
        "Todos": display_todo_page,
        "Projects": display_projects_page,
        "Quizzes": display_quiz_page,
        "Meetings": display_meetings_page,
        "Internship": display_internship_page,
        "Assignments": display_assignments_page,
        "Exams": display_exams_page,
        "Files": display_files_page,
    }
    
    with st.sidebar:
        
        selected_page = option_menu("Navigation", list(pages.keys()), icons=['house', 'clipboard', 'calendar', 'clipboard', 'folder', 'briefcase','clipboard', 'file-earmark-text', 'clipboard', 'file-earmark-text'], menu_icon="cast", default_index=0)

    # Check if user is authenticated before accessing certain pages
    if selected_page != "User Management" and not st.session_state.user_id:
        st.warning("Please authenticate before accessing other pages.")
        return

    # Display the selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()
