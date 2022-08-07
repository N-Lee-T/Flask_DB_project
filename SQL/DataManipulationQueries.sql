-- -----------------------------------------------------
-- CRUD Operations for app.py
-- -----------------------------------------------------

-- ------ Courses CREATE -------
-- null subject:
INSERT INTO Courses (school, max_class_size, enrollment) VALUES (%s, %s, %s)
-- null max_class_size
INSERT INTO Courses (subject, school, enrollment) VALUES (%s, %s, %s)
-- null enrollment
INSERT INTO Courses (subject, school, max_class_size) VALUES (%s, %s, %s)
-- no null inputs:
INSERT INTO Courses (subject, school, max_class_size, enrollment) VALUES (%s, %s,%s,%s)

-- ------ Courses READ -------
-- Courses - Display in template
SELECT Courses.course_id, Courses.subject as Subject, Schools.name AS School, Courses.max_class_size as 'Max Size', Courses.enrollment as Enrollment 
	FROM Courses 
	LEFT OUTER JOIN Schools 
	ON School = Schools.school_id

-- ------ Courses DELETE -------
-- Courses - Deletes a course
DELETE FROM Courses WHERE course_id = '%s'



-- ------ Schools CREATE -------
-- null enrollment:
INSERT INTO Schools (name, phone, city) VALUES (%s, %s, %s)
-- no null inputs:
INSERT INTO Schools (name, phone, enrollment, city) VALUES (%s, %s,%s,%s)

-- ------ Schools READ -------
-- Schools - Display in template
SELECT school_id, name as Name, phone as Phone, enrollment as Enrollment, city as City 
	FROM Schools
-- Schools - Displays schools for dropdown menu - Used several times throughout app
SELECT school_id, name FROM Schools

-- ------ Schools DELETE -------
-- Schools - Deletes a school
DELETE FROM Schools WHERE school_id = '%s'



-- ------ Students CREATE -------
-- Students
INSERT INTO Students(first_name, last_name, grade, phone, email, school) VALUES (%s, %s, %s, %s, %s, %s)

-- ------ Students READ -------
-- Students - Display in template 
SELECT student_id, first_name AS First, last_name AS Last, grade AS Grade, Students.phone AS Phone, email AS Email, Schools.name AS School 
            FROM Students 
            LEFT OUTER JOIN Schools 
            ON Students.school = Schools.school_id
                        
-- ------ Students UPDATE -------
-- Students - (POST)
UPDATE Students SET Students.first_name = %s, Students.last_name = %s, Students.grade = %s, Students.phone = %s, Students.email = %s, Students.school = %s
		WHERE Students.student_id = %s
-- Students - (GET)
SELECT * FROM Students WHERE student_id = %s  % (id)

-- ------ Students DELETE -------
DELETE FROM Students WHERE student_id = '%s'

-- ------ Students FILTER -------
-- filter student 
SELECT student_id, first_name AS First, last_name AS Last, grade AS Grade, Students.phone AS Phone, email AS Email 
              FROM Students 
              WHERE Students.school = '%s'



-- ------ Staff CREATE -------
INSERT INTO Staff(first_name, last_name, school, hire_date, email, phone, role) VALUES (%s, %s, %s, %s, %s, %s, %s)

-- ------ Staff READ -------
SELECT staff_id, first_name AS First, last_name AS Last, Schools.name AS School, hire_date AS Hired, email AS Email, Staff.phone AS Phone, role AS Role 
             FROM Staff 
             LEFT OUTER JOIN Schools 
             ON Staff.school = Schools.school_id
                          
-- ------ Staff UPDATE -------
-- Staff - (POST)
UPDATE Staff SET Staff.first_name = %s, Staff.last_name = %s, Staff.school = %s, Staff.hire_date = %s, Staff.email = %s, Staff.phone = %s, Staff.role = %s 
		WHERE Staff.staff_id = %s
-- Staff - (GET)
SELECT * FROM Staff WHERE staff_id = %s  % (staff_id)

-- ------ Staff DELETE -------
DELETE FROM Staff WHERE staff_id = '%s'



-- ------ CourseStaff CREATE -------
-- no null inputs:
INSERT INTO Course_Staff_Relationship (course_id, staff_id) VALUES (%s, %s)

-- ------ CourseStaff READ -------
SELECT course_staff_id, CONCAT(Staff.first_name, ' ', Staff.last_name) AS Name, Courses.subject AS Class 
	FROM Course_Staff_Relationship 
	LEFT JOIN Staff ON Course_Staff_Relationship.staff_id = Staff.staff_id 
	LEFT JOIN Courses ON Course_Staff_Relationship.course_id = Courses.course_id
	
-- Selects Staff from dropdown
SELECT staff_id, CONCAT(first_name, ' ', last_name) AS name FROM Staff
	
-- Selects Course from dropdown
SELECT course_id, subject FROM Courses
	
-- ------ CourseStaff DELETE -------
DELETE FROM Course_Staff_Relationship WHERE course_staff_id = '%s'



-- ------ CourseStudent CREATE -------
-- null student_id input:
INSERT INTO Course_Student_Relationship (course_id) VALUES (%s)
-- no null inputs:
INSERT INTO Course_Student_Relationship (course_id, student_id) VALUES (%s, %s)

-- ------ CourseStudent READ -------
SELECT course_student_id, CONCAT(Students.first_name, ' ', Students.last_name) AS Name, Courses.subject AS Class 
	FROM Course_Student_Relationship 
	LEFT JOIN Students ON Course_Student_Relationship.student_id = Students.student_id 
	LEFT JOIN Courses ON Course_Student_Relationship.course_id = Courses.course_id

-- Selects Student from dropdown
SELECT student_id, CONCAT(first_name, ' ', last_name) AS name FROM Students

-- Selects Course from dropdown
SELECT course_id, subject FROM Courses

-- ------ CourseStudent UPDATE -------
-- CourseStudent - (POST)
UPDATE Course_Student_Relationship \
         SET Course_Student_Relationship.course_id = %s, Course_Student_Relationship.student_id = %s \
         WHERE Course_Student_Relationship.course_student_id = %s
	 
-- CourseStudent - (GET)
SELECT * FROM Course_Student_Relationship WHERE course_student_id = '%s'  % (id)

-- Selects Student from dropdown
SELECT student_id, CONCAT(Students.first_name, ' ', Students.last_name) AS name FROM Students

-- Selects Course from dropdown
SELECT course_id, subject FROM Courses
 
-- ------ CourseStaff DELETE -------
DELETE FROM Course_Student_Relationship WHERE course_student_id = '%s';
	 
