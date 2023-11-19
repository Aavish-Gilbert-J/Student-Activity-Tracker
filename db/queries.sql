-- queries.sql

-- Select all users
SELECT * FROM users;

-- Select all classes for a specific user
SELECT * FROM classes WHERE user_id = 1;

-- Insert a new assignment
INSERT INTO assignments (assignment_name, deadline, user_id) VALUES ('New Assignment', '2023-12-31', 1);

-- Update a project deadline
UPDATE projects SET deadline = '2023-11-30' WHERE id = 1;

-- Delete a meeting
DELETE FROM meetings WHERE id = 1;

-- Nested query: Select users with upcoming exams
SELECT * FROM users WHERE id IN (SELECT user_id FROM exams WHERE exam_date > CURDATE());

-- Join query: Select users and their corresponding classes
SELECT users.username, classes.class_name
FROM users
LEFT JOIN classes ON users.id = classes.user_id;

-- Aggregate query: Count the number of completed todo tasks for each user
SELECT user_id, COUNT(*) AS completed_tasks
FROM todo
WHERE completion_date IS NOT NULL
GROUP BY user_id;
