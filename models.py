from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    roll_number = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    branch = db.Column(db.String(20), nullable=False)

    year = db.Column(db.String(5), nullable=False)   # E1, E2, E3, E4

class Hall(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    rows = db.Column(db.Integer, nullable=False)

    columns = db.Column(db.Integer, nullable=False) 


class Faculty(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(50), nullable=False)