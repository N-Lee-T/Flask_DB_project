# Flask_DB_project
A CRUD app using Flask to interact with a database. This was a project for CS340 at Oregon State University.

For this project, I worked with one other person to design and implement a simple database using MySQL. Our project theme was a school district, and the end result is the DB and its app-based UI.

After editing our schema, we populated the DB with sample data and tested various transaction types. This helped us make edits to the FK restraints and cascading operations. 

Next, we created a UI for this database through a Flask app. There are template pages for each table in the DB, as well as edit pages and a home page. Full CRUD functionality is available for several entities, and one table can be filtered by a certain attribute (Students, by School). 

# Future project: re-write and re-organize this project to add complexity. 
* Modify Flask structure to use the 'app factory' model (using Todd Birchard's awesome explainer here: https://hackersandslackers.com/flask-application-factory/)
* Create full CRUD for every entity, as well as filtering capability for each
* Use either a different RDB (Postgres?) or try using a NoSQL model like MongoDB
