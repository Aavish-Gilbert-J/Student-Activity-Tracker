-- procedures.sql

-- Procedure to add a user
DELIMITER //
CREATE PROCEDURE AddUser(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_role ENUM('admin', 'user')
)
BEGIN
    INSERT INTO users (username, password, role) VALUES (p_username, p_password, p_role);
END //
DELIMITER ;

-- Procedure to add a class
DELIMITER //
CREATE PROCEDURE AddClass(
    IN p_class_name VARCHAR(255),
    IN p_class_schedule VARCHAR(255),
    IN p_user_id INT
)
BEGIN
    INSERT INTO classes (class_name, class_schedule, user_id) VALUES (p_class_name, p_class_schedule, p_user_id);
END //
DELIMITER ;

-- Procedure to add an assignment
DELIMITER //
CREATE PROCEDURE AddAssignment(
    IN p_assignment_name VARCHAR(255),
    IN p_deadline DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO assignments (assignment_name, deadline, user_id) VALUES (p_assignment_name, p_deadline, p_user_id);
END //
DELIMITER ;

-- procedures.sql

-- Procedure to add an exam
DELIMITER //
CREATE PROCEDURE AddExam(
    IN p_exam_name VARCHAR(255),
    IN p_exam_date DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO exams (exam_name, exam_date, user_id) VALUES (p_exam_name, p_exam_date, p_user_id);
END //
DELIMITER ;

-- Procedure to add a todo
DELIMITER //
CREATE PROCEDURE AddTodo(
    IN p_task_name VARCHAR(255),
    IN p_completion_date DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO todo (task_name, completion_date, user_id) VALUES (p_task_name, p_completion_date, p_user_id);
END //
DELIMITER ;

-- Procedure to add a project
DELIMITER //
CREATE PROCEDURE AddProject(
    IN p_project_name VARCHAR(255),
    IN p_deadline DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO projects (project_name, deadline, user_id) VALUES (p_project_name, p_deadline, p_user_id);
END //
DELIMITER ;

-- Procedure to add an internship
DELIMITER //
CREATE PROCEDURE AddInternship(
    IN p_company_name VARCHAR(255),
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO internship (company_name, start_date, end_date, user_id) VALUES (p_company_name, p_start_date, p_end_date, p_user_id);
END //
DELIMITER ;

-- Procedure to add a meeting
DELIMITER //
CREATE PROCEDURE AddMeeting(
    IN p_meeting_name VARCHAR(255),
    IN p_meeting_date DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO meetings (meeting_name, meeting_date, user_id) VALUES (p_meeting_name, p_meeting_date, p_user_id);
END //
DELIMITER ;

-- Procedure to add a file
DELIMITER //
CREATE PROCEDURE AddFile(
    IN p_file_name VARCHAR(255),
    IN p_file_path VARCHAR(255),
    IN p_user_id INT
)
BEGIN
    INSERT INTO files (file_name, file_path, user_id) VALUES (p_file_name, p_file_path, p_user_id);
END //
DELIMITER ;

-- Procedure to add a quiz
DELIMITER //
CREATE PROCEDURE AddQuiz(
    IN p_quiz_name VARCHAR(255),
    IN p_quiz_date DATE,
    IN p_user_id INT
)
BEGIN
    INSERT INTO quiz (quiz_name, quiz_date, user_id) VALUES (p_quiz_name, p_quiz_date, p_user_id);
END //
DELIMITER ;

