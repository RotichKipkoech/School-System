from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Roles: 'admin', 'teacher', 'parent', 'finance'
    name = db.Column(db.String(150), nullable=False, server_default='Default Name')

    # Method to set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Teacher model
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('teacher', uselist=False))

    def __repr__(self):
        return f'<Teacher {self.name}, Subject: {self.subject}>'

# Parent model
class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    child_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('parent', uselist=False))

    def __repr__(self):
        return f'<Parent {self.name}, Child: {self.child_name}>'

# Finance model
class Finance(db.Model):
    __tablename__ = 'finance'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('finance', uselist=False))

    def __repr__(self):
        return f'<Finance {self.name}, Department: {self.department}>'

# Student Mark model
class StudentMark(db.Model):
    __tablename__ = 'student_marks'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    # Relationship to Teacher
    teacher = db.relationship('Teacher', backref=db.backref('marks', lazy=True))

    def __repr__(self):
        return f'<StudentMark {self.student_name}, Marks: {self.marks}>'

# Student Fee model
class StudentFee(db.Model):
    __tablename__ = 'student_fees'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    fee_balance = db.Column(db.Float, nullable=False)
    finance_id = db.Column(db.Integer, db.ForeignKey('finance.id'), nullable=False)

    # Relationship to Finance
    finance = db.relationship('Finance', backref=db.backref('fees', lazy=True))

    def __repr__(self):
        return f'<StudentFee {self.student_name}, Fee Balance: {self.fee_balance}>'
