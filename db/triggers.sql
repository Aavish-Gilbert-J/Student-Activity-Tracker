-- triggers.sql

-- Trigger to update the last modified timestamp when a user is updated
CREATE TRIGGER user_update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a class is updated
CREATE TRIGGER class_update_timestamp
BEFORE UPDATE ON classes
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when an assignment is updated
CREATE TRIGGER assignment_update_timestamp
BEFORE UPDATE ON assignments
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when an exam is updated
CREATE TRIGGER exam_update_timestamp
BEFORE UPDATE ON exams
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a todo is updated
CREATE TRIGGER todo_update_timestamp
BEFORE UPDATE ON todo
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a project is updated
CREATE TRIGGER project_update_timestamp
BEFORE UPDATE ON projects
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when an internship is updated
CREATE TRIGGER internship_update_timestamp
BEFORE UPDATE ON internship
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a meeting is updated
CREATE TRIGGER meeting_update_timestamp
BEFORE UPDATE ON meetings
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a file is updated
CREATE TRIGGER file_update_timestamp
BEFORE UPDATE ON files
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;

-- Trigger to update the last modified timestamp when a quiz is updated
CREATE TRIGGER quiz_update_timestamp
BEFORE UPDATE ON quiz
FOR EACH ROW
SET NEW.last_modified = CURRENT_TIMESTAMP;
