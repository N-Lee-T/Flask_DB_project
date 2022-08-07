
-- -----------------------------------------------------
-- Table Schools
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Schools (
  school_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(75) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  enrollment INT NULL,
  city VARCHAR(30) NOT NULL,
  PRIMARY KEY (school_id),
  UNIQUE INDEX school_id_UNIQUE (school_id ASC) VISIBLE);

-- -----------------------------------------------------
-- Table Students
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Students (
  student_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  grade INT NOT NULL,
  phone VARCHAR(15) NULL,
  email VARCHAR(250) NULL,
  school INT NULL,
  PRIMARY KEY (student_id),
  UNIQUE INDEX student_id_UNIQUE (student_id ASC) VISIBLE,
  INDEX fk_Students_school_id_idx (school ASC) VISIBLE,
  CONSTRAINT fk_Students_school_id
    FOREIGN KEY (school)
    REFERENCES Schools (school_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Staff
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Staff (
  staff_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  school INT NULL,
  hire_date DATE NULL,
  email VARCHAR(250) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  role VARCHAR(50) NOT NULL,
  PRIMARY KEY (staff_id),
  UNIQUE INDEX staff_id_UNIQUE (staff_id ASC) VISIBLE,
  INDEX fk_Staff_school_id_idx (school ASC) VISIBLE,
  CONSTRAINT fk_Staff_school_id
    FOREIGN KEY (school)
    REFERENCES Schools (school_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Courses
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Courses (
  course_id INT NOT NULL AUTO_INCREMENT,
  subject VARCHAR(30) NULL,
  school INT,
  max_class_size INT NULL,
  enrollment INT NULL,
  PRIMARY KEY (course_id),
  UNIQUE INDEX course_id_UNIQUE (course_id ASC) VISIBLE,
  INDEX fk_Courses_school_id_idx (school ASC) VISIBLE,
  CONSTRAINT fk_Courses_school_id
    FOREIGN KEY (school)
    REFERENCES Schools (school_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Course_Staff_Relationship
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Course_Staff_Relationship (
  course_staff_id INT NOT NULL AUTO_INCREMENT,
  course_id INT NOT NULL,
  staff_id INT NOT NULL,
  INDEX fk_staff_id_idx (staff_id ASC) VISIBLE,
  INDEX fk_course_id_idx (course_id ASC) VISIBLE,
  PRIMARY KEY (course_staff_id),
  UNIQUE INDEX course_staff_id_UNIQUE (course_staff_id ASC) VISIBLE,
  CONSTRAINT fk_staff_id
    FOREIGN KEY (staff_id)
    REFERENCES Staff (staff_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_course_id
    FOREIGN KEY (course_id)
    REFERENCES Courses (course_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Course_Student_Relationship
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Course_Student_Relationship (
  course_student_id INT NOT NULL AUTO_INCREMENT,
  course_id INT NOT NULL,
  student_id INT,
  INDEX fk_course_id_idx (course_id ASC) VISIBLE,
  INDEX fk_student_id_idx (student_id ASC) VISIBLE,
  PRIMARY KEY (course_student_id),
  UNIQUE INDEX course_student_id_UNIQUE (course_student_id ASC) VISIBLE,
  CONSTRAINT fk_student_id
    FOREIGN KEY (student_id)
    REFERENCES Students (student_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk1_course_id
    FOREIGN KEY (course_id)
    REFERENCES Courses (course_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- INSERT SAMPLE DATA

--  Insert schools
INSERT INTO Schools (name, phone, enrollment, city)
VALUES
('MiddleBrook Elementary School',	'847-261-7789',  237, 'Hillsboro'), 
('Second Elementary', '513-567-2891', 349, 'Rylander'),
('The Middle School', '513-222-5489', 789, 'Beaverton'),
('A High School', '513-492-2928', 1183, 'Springfield');


--  Insert staff 
INSERT INTO Staff (first_name, last_name, school, hire_date, email, phone, role)
VALUES 
('Dallon','Shaxby',1,'2018-07-18','jshaxby0@apple.com','639-188-9732','P'),
('Kellby','Lars',1,'2019-12-31','vlars1@go.com','461-660-9660','TZ'),
('Carmencita','Stafford',2,'2014-11-07','mstafford3@microsoft.com','456-679-8456','P'),
('Dorena','Fitchet',2,'2017-05-11','ofitchet4@hostgator.com','665-577-7540','J'),
('Gerhardine','Piscot',3,'2012-12-01','gpiscot5@alexa.com','379-400-6370','Z'),
('Iver','Cummins',3,'2018-09-30','bcummins6@4shared.com','385-606-5703','T'),
('Marylou','McKain',4,'2021-05-24','jmckain7@comcast.net','505-206-0935','T'),
('Siobhan','Avramov',4,'2016-06-04','mavramov8@creativecommons.org','416-613-6973','PZ');


--  Insert students 
INSERT INTO Students (first_name,last_name,school,grade,email,phone)
VALUES 
('Virgie','Scad',1,4,'scadi@intel.com','872-658-5065'),
('Granville','Yousef',1,1,'yousefj@cocolog-nifty.com','757-991-3356'),
('Wynny','Oki',2,6,'oki5@auda.org.au','721-912-7090'),
('Clyde','Copins',2,6,'copins6@comcast.net','919-159-1942'),
('Pamela','Delamaine',3,11,'delamainem@unc.edu','449-609-2944'),
('Zacharias','Littleproud',3,12,'littleproudn@japanpost.jp','933-866-0813'),
('Roxane','Steed',4,12,'steedd@behance.net','715-842-5403'),
('Rachelle','Beard',4,12,'bearde@omniture.com','151-436-8631');

-- Insert courses 
INSERT INTO Courses (`subject`, `school`, `max_class_size`)
VALUES 
('History',1,30),
('Drawing',1,30),
('Social Studies',2,25),
('Science',2,25),
('Algebra 1',3,28) ,
('Graphics & Design',3,20),
('Computer Science',4,30),
('Wood Shop',4,22);

INSERT INTO Course_Staff_Relationship(course_id, staff_id)
VALUES
((SELECT course_id FROM Courses WHERE Courses.course_id = 1), (SELECT staff_id FROM Staff WHERE Staff.staff_id = 1)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 3), (SELECT staff_id FROM Staff WHERE Staff.staff_id = 3)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 5), (SELECT staff_id FROM Staff WHERE Staff.staff_id = 5)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 7), (SELECT staff_id FROM Staff WHERE Staff.staff_id = 7));

INSERT INTO Course_Student_Relationship(course_id, student_id)
VALUES
((SELECT course_id FROM Courses WHERE Courses.course_id = 1), (SELECT student_id FROM Students WHERE Students.student_id = 1)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 3), (SELECT student_id FROM Students WHERE Students.student_id = 3)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 5), (SELECT student_id FROM Students WHERE Students.student_id = 5)),
((SELECT course_id FROM Courses WHERE Courses.course_id = 7), (SELECT student_id FROM Students WHERE Students.student_id = 7));
