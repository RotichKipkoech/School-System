from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('parent', 'Parent'), ('finance', 'Finance')], validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    subject = StringField('Subject')  # For teachers
    child_name = StringField('Child Name')  # For parents
    department = StringField('Department')  # For finance
    submit = SubmitField('Create User')

class AddMarksForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    marks = FloatField('Marks', validators=[DataRequired()])
    submit = SubmitField('Add Marks')

class FeesUpdateForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    fee_balance = FloatField('Fee Balance', validators=[DataRequired()])
    submit = SubmitField('Update Fees')