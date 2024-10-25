from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Teacher, Parent, Finance, StudentMark, StudentFee
from forms import LoginForm, CreateUserForm, AddMarksForm, FeesUpdateForm  # Ensure your forms are imported
  # Ensure your forms are imported
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_system.db'
app.config['SECRET_KEY'] = 'yoursecretkey'

db.init_app(app)

# Initialize SQLAlchemy and Migrate
migrate = Migrate(app, db)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Example of a protected route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Create admin user function
@app.cli.command('create_admin')
def create_admin_user():
    with app.app_context():
        admin_user = User.query.filter_by(username='Admin').first()
        if not admin_user:
            admin_user = User(username='Admin', role='admin')
            admin_user.set_password('Admin@123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created with username: 'Admin' and password: 'Admin@123'")
        else:
            print("Admin user already exists")

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)  # Log in the user
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for(f"{user.role}_dashboard"))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You are not authorized to view this page.')
        return redirect(url_for('home'))
    
    # Get all users and their related information
    users = User.query.options(
        db.joinedload(User.teacher),  # Load teacher info if role is teacher
        db.joinedload(User.parent),   # Load parent info if role is parent
        db.joinedload(User.finance)   # Load finance info if role is finance
    ).all()  # Get all users for management
    return render_template('admin_dashboard.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))
    
    form = CreateUserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            role=form.role.data,
            name=form.name.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()  # Commit to assign an ID to the new user

        # Create additional user type entries based on role
        if form.role.data == 'teacher':
            new_teacher = Teacher(name=form.name.data, subject=form.subject.data, user_id=new_user.id)
            db.session.add(new_teacher)
        elif form.role.data == 'parent':
            new_parent = Parent(name=form.name.data, child_name=form.child_name.data, user_id=new_user.id)
            db.session.add(new_parent)
        elif form.role.data == 'finance':
            new_finance = Finance(name=form.name.data, department=form.department.data, user_id=new_user.id)
            db.session.add(new_finance)

        db.session.commit()
        flash(f'User {form.username.data} created successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_user.html', form=form)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))
    
    form = CreateUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data
        user.name = form.name.data
        # Update additional user type details
        if user.role == 'teacher':
            teacher = Teacher.query.filter_by(user_id=user.id).first()
            teacher.subject = form.subject.data
        elif user.role == 'parent':
            parent = Parent.query.filter_by(user_id=user.id).first()
            parent.child_name = form.child_name.data
        elif user.role == 'finance':
            finance = Finance.query.filter_by(user_id=user.id).first()
            finance.department = form.department.data

        db.session.commit()
        flash(f'User {user.username} updated successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_user.html', form=form, user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@app.route('/parent_dashboard')
@login_required
def parent_dashboard():
    return render_template('parent_dashboard.html')

@app.route('/finance_dashboard')
@login_required
def finance_dashboard():
    return render_template('finance_dashboard.html')

# Add marks route for teachers
@app.route('/add_marks', methods=['GET', 'POST'])
@login_required
def add_marks():
    if current_user.role != 'teacher':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))
    
    form = AddMarksForm()
    if form.validate_on_submit():
        new_mark = StudentMark(student_name=form.student_name.data, marks=form.marks.data, teacher_id=current_user.teacher.id)
        db.session.add(new_mark)
        db.session.commit()
        flash(f'Marks for {form.student_name.data} added successfully!')
        return redirect(url_for('teacher_dashboard'))

    return render_template('add_marks.html', form=form)

# View marks for parents
@app.route('/view_marks', methods=['GET'])
@login_required
def view_marks():
    if current_user.role != 'parent':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))

    marks = StudentMark.query.filter_by(student_name=current_user.parent.child_name).all()
    return render_template('view_marks.html', marks=marks)

# Update fees route for finance
@app.route('/update_fees', methods=['GET', 'POST'])
@login_required
def update_fees():
    if current_user.role != 'finance':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))

    form = FeesUpdateForm()
    if form.validate_on_submit():
        student_fee = StudentFee(student_name=form.student_name.data, fee_balance=form.fee_balance.data, finance_id=current_user.finance.id)
        db.session.add(student_fee)
        db.session.commit()
        flash(f'Fees for {form.student_name.data} updated successfully!')
        return redirect(url_for('finance_dashboard'))

    return render_template('update_fees.html', form=form)

@app.route('/view_fee_balance', methods=['GET'])
@login_required
def view_fee_balance():
    if current_user.role != 'parent':
        flash('You are not authorized to perform this action.')
        return redirect(url_for('login'))

    # Fetch the fee balance for the parent's child
    fee_balance = StudentFee.query.filter_by(student_name=current_user.parent.child_name).first()

    return render_template('view_fee_balance.html', fee_balance=fee_balance)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
