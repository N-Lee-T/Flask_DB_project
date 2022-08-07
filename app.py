# Citation for the following functions: courses(), delete_course(), schools(), delete_school, students(), edit_student(),delete_student(), CourseStaff(), delete_course_staff(), CourseStudent(), edit_course_student(), delete_course_student(), staff(), edit_staff(), delete_staff()
      # Date: 8/5/22
      # Copied from /OR/ Adapted from /OR/ Based on: bsg_people_app/app.py
      # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

# Sample Flask application 

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os


app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_xxxxxx"
app.config["MYSQL_PASSWORD"] = "xxxx"
app.config["MYSQL_DB"] = "cs340_xxxxxx"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route("/")
def home():
    return render_template("/index.j2")


# -------Courses Routes------------- 

@app.route("/courses", methods=["POST", "GET"])
def courses():

# Create Course --------------------------
    if request.method == "POST":
        # fire off if user presses the Add School button
        if request.form.get("Add_Course"):
            # grab user form inputs
            subject = request.form["subject"]
            school = request.form["school"]
            max_class_size = request.form["max_class_size"]
            enrollment = request.form["enrollment"] 

            # accounts for null subject
            if subject == "":
                query = "INSERT INTO Courses (school, max_class_size, enrollment) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (school, max_class_size, enrollment))
                mysql.connection.commit()

            # accounts for null max_class_size
            elif max_class_size == "":
                query = "INSERT INTO Courses (subject, school, enrollment) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (subject, school, enrollment))
                mysql.connection.commit()

            # accounts for null enrollment
            elif enrollment == "":
                query = "INSERT INTO Courses (subject, school, max_class_size) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (subject, school, max_class_size))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Courses (subject, school, max_class_size, enrollment) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (subject, school, max_class_size, enrollment))
                mysql.connection.commit()

            # redirect back to courses page
            return redirect("/courses")

# Read Courses -------------------
    if request.method == "GET":
        # mySQL query to grab all the courses 

        query = "SELECT Courses.course_id, Courses.subject as Subject, Schools.name AS School, Courses.max_class_size as 'Max Size', Courses.enrollment as Enrollment FROM Courses LEFT OUTER JOIN Schools on School = Schools.school_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Select schools from dropdown
        query_schools = "SELECT school_id, name FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query_schools)
        school_list = cur.fetchall()

        return render_template("courses.j2", data=data, schools=school_list)

# Delete Courses ------------------------------------
@app.route("/delete_course/<int:id>")
def delete_course(id): 
    query = "DELETE FROM Courses WHERE course_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/courses")


# --------- Schools Routes ----------

@app.route("/schools", methods=["POST", "GET"])
def schools():
  
# Create School ---------------
    if request.method == "POST":

        if request.form.get("Add_School"):
            # grab user form inputs
            name = request.form["name"]
            phone = request.form["phone"]
            enrollment = request.form["enrollment"]
            city = request.form["city"]

            # accounts for null enrollment. enrollment = 'None' in UI, 'Null' in DB  ---
            if enrollment == "":
                query = "INSERT INTO Schools (name, phone, city) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, city))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Schools (name, phone, enrollment, city) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, enrollment, city))
                mysql.connection.commit()

            # redirect back to schools page
            return redirect("/schools")

# Read Schools ------------------------------------
    if request.method == "GET":
        # mySQL query to grab all Schools
        query = "SELECT school_id, name as Name, phone as Phone, enrollment as Enrollment, city as City FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("schools.j2", data=data)

# Delete Schools ------------------------------------
@app.route("/delete_school/<int:id>")
def delete_school(id): 
    query = "DELETE FROM Schools WHERE school_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/schools")


# --------- Students Routes ----------

@app.route("/students", methods=['POST', 'GET'])
def students():
    if request.method == "GET":
        query_students = "SELECT student_id, first_name AS First, last_name AS Last, grade AS Grade, Students.phone AS Phone, email AS Email, Schools.name AS School \
                          FROM Students \
                          LEFT OUTER JOIN Schools \
                          ON Students.school = Schools.school_id" 
        cur = mysql.connection.cursor()
        cur.execute(query_students)
        student_data = cur.fetchall()

        # Select schools from dropdown
        query_schools = "SELECT school_id, name FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query_schools)
        school_list = cur.fetchall()

        return render_template("students.j2", data=student_data, schools=school_list)

    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        grade = request.form['grade'] 
        phone = request.form['phone']
        email = request.form['email'] 
        if request.form["school"] == '0':
            school = None
        else:
            school = request.form["school"]

        query = "INSERT INTO Students(first_name, last_name, grade, phone, email, school) VALUES (%s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor() 
        # execute the SQL statement w/ request.form values subbed for VALUES attributes
        cur.execute(query, (first_name, last_name, grade, phone, email, school))
        mysql.connection.commit()

        return redirect("/students")

# Edit a student
@app.route("/edit_student/<int:id>", methods=["POST", "GET"])
def edit_student(id):

    if request.method == "POST":
        # populate form with pre-existing data
        if request.form.get("edit_student"): 
            id = request.form["student_id"]
            # first_name = None
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            grade = request.form["grade"] 
            phone = request.form["phone"]
            email = request.form["email"]
            if request.form["school"] == '0':
                school = None
            else:
                school = request.form["school"]
        
            query = "UPDATE Students \
                    SET Students.first_name = %s, Students.last_name = %s, Students.grade = %s, Students.phone = %s, Students.email = %s, Students.school = %s \
                    WHERE Students.student_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, grade, phone, email, school, id))
            mysql.connection.commit()
        return redirect("/students")
        
    if request.method == "GET":
        query_students = "SELECT * FROM Students WHERE student_id = %s"  % (id)
        cur = mysql.connection.cursor()
        cur.execute(query_students)
        student_data = cur.fetchall()

        # Select schools from dropdown
        query_schools = "SELECT school_id, name FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query_schools)
        school_list = cur.fetchall()
        
        return render_template("edit_student.j2", data=student_data, schools=school_list)

# Delete a student
@app.route("/delete_student/<int:id>")
def delete_student(id): 
    query = "DELETE FROM Students WHERE student_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/students")
  
# Filter students by school  
@app.route("/students/<int:id>", methods=["GET"])
def filter_students(id):
    if request.method == "GET":
        query_students = "SELECT student_id, first_name AS First, last_name AS Last, grade AS Grade, Students.phone AS Phone, email AS Email \
                            FROM Students \
                            WHERE Students.school = '%s'" 
        cur = mysql.connection.cursor()
        cur.execute(query_students, (id,))
        student_data = cur.fetchall()

        # Select school
        query_schools = "SELECT school_id, name FROM Schools \
                         WHERE Schools.school_id = '%s'"
        cur = mysql.connection.cursor()
        cur.execute(query_schools, (id,))
        the_school = cur.fetchall()

        return render_template("students.j2", data=student_data, the_school=the_school)


# --------- CourseStaff Routes ----------

@app.route("/CourseStaff", methods=["POST", "GET"])
def CourseStaff():

# Create CourseStaff Relationship ---------------
    if request.method == "POST":

        if request.form.get("Add_CourseStaff"):
            # grab user form inputs
            course_id = request.form["course_id"]
            staff_id = request.form["staff_id"]

            query = "INSERT INTO Course_Staff_Relationship (course_id, staff_id) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (course_id, staff_id))
            mysql.connection.commit()

            return redirect("/CourseStaff")

# Read CourseStaff Relationship ------------------------------------
    if request.method == "GET":

        query = "SELECT course_staff_id, CONCAT(Staff.first_name, ' ', Staff.last_name) AS Name, Courses.subject AS Class \
                 FROM Course_Staff_Relationship \
                 LEFT JOIN Staff ON Course_Staff_Relationship.staff_id = Staff.staff_id \
                 LEFT JOIN Courses ON Course_Staff_Relationship.course_id = Courses.course_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Select staff from dropdown
        query_staff = "SELECT staff_id, CONCAT(first_name, ' ', last_name) AS name FROM Staff"
        cur = mysql.connection.cursor()
        cur.execute(query_staff)
        staff_list = cur.fetchall()

        # Select courses from dropdown
        query_courses = "SELECT course_id, subject FROM Courses"
        cur = mysql.connection.cursor()
        cur.execute(query_courses)
        course_list = cur.fetchall()

        return render_template("CourseStaff.j2", data=data, staff=staff_list, courses=course_list)

# Delete a student-staff relationship
@app.route("/delete_course_staff/<int:id>")
def delete_course_staff(id): 
    query = "DELETE FROM Course_Staff_Relationship WHERE course_staff_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/CourseStaff")   

# --------- CourseStudent Routes ----------

@app.route("/CourseStudent", methods=["POST", "GET"])
def CourseStudent():

# Create CourseStudent Relationship ---------------
    if request.method == "POST":

        if request.form.get("Add_CourseStudent"):
            # grab user form inputs
            course_id = request.form["course_id"]
            student_id = request.form["student_id"]

            # accounts for null student_id, Nullable relationship  ---
            if student_id == "":
                query = "INSERT INTO Course_Student_Relationship (course_id) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (course_id))
                mysql.connection.commit()
            
            # no null inputs 
            else:
                query = "INSERT INTO Course_Student_Relationship (course_id, student_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (course_id, student_id))
                mysql.connection.commit()

            return redirect("/CourseStudent")
          
# Read CourseStudent Relationship ------------------------------------
    if request.method == "GET":

        query = "SELECT course_student_id, CONCAT(Students.first_name, ' ', Students.last_name) AS Name, Courses.subject AS Class \
                FROM Course_Student_Relationship \
                LEFT JOIN Students ON Course_Student_Relationship.student_id = Students.student_id \
                LEFT JOIN Courses ON Course_Student_Relationship.course_id = Courses.course_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Select students from dropdown
        query_students = "SELECT student_id, CONCAT(first_name, ' ', last_name) AS name FROM Students"
        cur = mysql.connection.cursor()
        cur.execute(query_students)
        student_list = cur.fetchall()

        # Select courses from dropdown
        query_courses = "SELECT course_id, subject FROM Courses"
        cur = mysql.connection.cursor()
        cur.execute(query_courses)
        course_list = cur.fetchall()

        return render_template("CourseStudent.j2", data=data, students=student_list, courses=course_list)

# Edit course-student relationship
@app.route("/edit_course_student/<int:id>", methods=["POST", "GET"])
def edit_course_student(id):

    if request.method == "POST":
        # populate form with pre-existing data
        if request.form.get("edit_course_student"): 
            id = request.form["course_student_id"]
            course = request.form["course_id"]
            student = request.form["student_id"]
   
            query = "UPDATE Course_Student_Relationship \
                    SET Course_Student_Relationship.course_id = %s, Course_Student_Relationship.student_id = %s \
                    WHERE Course_Student_Relationship.course_student_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (course, student, id))
            mysql.connection.commit()
        
        return redirect("/CourseStudent")

    if request.method == "GET":
        query_students = "SELECT * FROM Course_Student_Relationship WHERE course_student_id = %s"  % (id)
        cur = mysql.connection.cursor()
        cur.execute(query_students)
        course_student_data = cur.fetchall()

        # Select courses from dropdown
        query_courses = "SELECT course_id, subject FROM Courses"
        cur = mysql.connection.cursor()
        cur.execute(query_courses)
        course_list = cur.fetchall()

        # Select students from dropdown
        query_students = "SELECT student_id, CONCAT(Students.first_name, ' ', Students.last_name) AS name FROM Students"
        cur = mysql.connection.cursor()
        cur.execute(query_students)
        student_list = cur.fetchall()
        
        return render_template("edit_course_student.j2", data=course_student_data, courses=course_list, students=student_list)

# Delete a student-course relationship
@app.route("/delete_course_student/<int:id>")
def delete_course_student(id): 
    query = "DELETE FROM Course_Student_Relationship WHERE course_student_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/CourseStudent")


# --------- Staff Routes ----------

@app.route("/staff", methods=['POST', 'GET'])
def staff():
    # Read Staff ---------------
    if request.method == "GET":
        # if we use an alias for staff_id ('SELECT staff_id AS ID' etc) it won't pass the ID correctly to the route. 
        query_staff = "SELECT staff_id, first_name AS First, last_name AS Last, Schools.name AS School, hire_date AS Hired, email AS Email, Staff.phone AS Phone, role AS Role \
                          FROM Staff \
                          LEFT OUTER JOIN Schools \
                          ON Staff.school = Schools.school_id" 
        cur = mysql.connection.cursor()
        cur.execute(query_staff)
        staff_data = cur.fetchall()

        # Select schools from dropdown
        query_schools = "SELECT school_id, name FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query_schools)
        school_list = cur.fetchall()

        return render_template("staff.j2", data=staff_data, schools=school_list)

    # Create Staff ---------------
    elif request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        if request.form["school"] == '0':
            school = None
        else:
            school = request.form["school"]
        hire_date = request.form['hire_date']
        email = request.form["email"] 
        phone = request.form["phone"]
        role = request.form["role"] 

        query = "INSERT INTO Staff(first_name, last_name, school, hire_date, email, phone, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor() 
        # execute the SQL statement w/ request.form values subbed for VALUES attributes
        cur.execute(query, (first_name, last_name, school, hire_date, email, phone, role))
        mysql.connection.commit()

        return redirect("/staff")

# Update Staff ---------------
@app.route("/edit_staff/<int:staff_id>", methods=["POST", "GET"])
def edit_staff(staff_id): #id

    if request.method == "POST":
        # populate form with pre-existing data
        if request.form.get("edit_staff"): # don't forget to add the name as well as id @ the submit button in edit_staff.j2!!
            id = request.form["staff_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            if request.form["school"] == '0':
                school = None
            else:
                school = request.form["school"]
            hire_date = request.form['hire_date'] 
            email = request.form["email"]
            phone = request.form["phone"]
            role = request.form["role"] 

            query = "UPDATE Staff \
                    SET Staff.first_name = %s, Staff.last_name = %s, Staff.school = %s, Staff.hire_date = %s, Staff.email = %s, Staff.phone = %s, Staff.role = %s \
                    WHERE Staff.staff_id = %s" 
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, school, hire_date, email, phone, role, id))
            mysql.connection.commit()
        
        return redirect("/staff")
        
    if request.method == "GET":
        query_staff = "SELECT * FROM Staff WHERE staff_id = %s"  % (staff_id) #id
        cur = mysql.connection.cursor()
        cur.execute(query_staff)
        staff_data = cur.fetchall()

        # Select schools for dropdown
        query_schools = "SELECT school_id, name FROM Schools"
        cur = mysql.connection.cursor()
        cur.execute(query_schools)
        school_list = cur.fetchall()
        
        return render_template("edit_staff.j2", data=staff_data, schools=school_list)

# Delete Staff ---------------
@app.route("/delete_staff/<int:id>")
def delete_staff(id): 
    query = "DELETE FROM Staff WHERE staff_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/staff")

# Listener
if __name__ == "__main__":
    app.run(port=7779, debug=True)
