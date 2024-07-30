from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, HealthForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

headings = ("First Name", "Last Name", "Email", "Current or Previous Allergies", "Current or Previous Diseases",
             "Current Symptoms", "Current or Previous Medication", "Drugs Consumed in the Last Year", "Extra Information")

headings_Doctor = ("Doctor Speciality","First Name", "Last Name", "Email")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):               
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                
                userD1 = User.query.filter_by(id=current_user.id).first()
                if userD1.isDoctor == False:
                    userD2 = HealthForm.query.filter_by(user_id=current_user.id).first()
                    data = (userD1.first_name, userD1.last_name, userD1.email, userD2.allergies, userD2.disease, userD2.symptoms, userD2.medication, userD2.drugs, userD2.extrainfo)
                    return render_template("home.html", user_id=current_user, headings=headings, data=data)
                else:
                    data = ( 
                    "Dr",userD1.first_name, userD1.last_name, userD1.email
                    )
                    return render_template("home_doctor.html", user_id=current_user, headings=headings_Doctor, data=data)
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash("Email is incorrect or does not exist, try again or Sign Up.", category='error')
        
    return render_template("loginPage/login.html", user_id=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists in system.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 3:
            flash('First Name must be greater or equal to 3 characters.', category='error')
        elif len(lastName) < 3:
            flash('Last Name must be greater or equal to 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName,isDoctor=False, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created with Health Sync! Thank You for Joining.', category='success')
            return redirect(url_for('auth.medical_info'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/sign-up-doctor', methods=['GET', 'POST'])
def sign_up_doctor():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        speciality = request.form.get('speciality')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists in system.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 3:
            flash('First Name must be greater or equal to 3 characters.', category='error')
        elif len(lastName) < 3:
            flash('Last Name must be greater or equal to 3 characters.', category='error')
        elif len(speciality) < 3:
            flash('Speciality must be greater or equal to 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName,speciality=speciality, isDoctor=True, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created with Health Sync! Thank You for Joining.', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up_doctor.html", user=current_user)


@auth.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    data = User.query.filter_by(id=current_user.id).first()

    if data.isDoctor:
        if request.method == 'POST':
            emailUser = request.form.get('email')
            firstNameUser = request.form.get('firstName')
            lastNameUser = request.form.get('lastName')
            user = User.query.filter_by(email=emailUser, first_name=firstNameUser, last_name=lastNameUser ).first()
            if user:
                user.primary_id = data.id
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Information Given, Doctor not Added', category='error')
        return render_template("add_user.html", user=current_user)
    else:
        if request.method == 'POST':
            emailUser = request.form.get('email')
            firstNameUser = request.form.get('firstName')
            lastNameUser = request.form.get('lastName')
            user = User.query.filter_by(email=emailUser, first_name=firstNameUser, last_name=lastNameUser, isDoctor=True).first()
            if user:
                data.primary_id = user.id
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Information Given, Doctor not Added', category='error')
        return render_template("add_doctor.html", user=current_user)

@auth.route('/find-user', methods=['GET', 'POST'])
@login_required
def find_user():
    patients = User.query.filter_by(primary_id=current_user.id).all()
    if request.method == 'POST':
        user_id = request.form.get('id')
        user = User.query.filter_by(id=user_id).first()
        if user:
            return redirect(url_for('.edit_user', user_id=user_id))
        else:
            flash('Wrong Information Given, User not found', category='error')
    return render_template("find_user.html", user=current_user, patients=patients)

@auth.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edit_user():
    user_id = request.args['user_id'] 
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        allergies = request.form.get('allergies')
        disease = request.form.get('disease')
        symptoms = request.form.get('symptoms')
        medication = request.form.get('medication')
        drugs = request.form.get('drugs')
        extrainfo = request.form.get('extrainfo')
        new_data = HealthForm(user_id=user.id, allergies=allergies, disease=disease, symptoms=symptoms, medication=medication, drugs=drugs, extrainfo=extrainfo)
        user = HealthForm.query.filter_by(user_id=user.id).first()
        if user:
            db.session.delete(user)
            db.session.add(new_data)
            db.session.commit()
        else:
            db.session.add(new_data)
            db.session.commit()
        flash('Medical Info Added with Health Sync! Thank You for Entering.', category='success')  
        return redirect(url_for('views.home'))
    return render_template("edit_user.html", user=user)



    


@auth.route('/medical-info', methods=['GET', 'POST'])
@login_required
def medical_info():
    if request.method == 'POST':
        allergies = request.form.get('allergies')
        disease = request.form.get('disease')
        symptoms = request.form.get('symptoms')
        medication = request.form.get('medication')
        drugs = request.form.get('drugs')
        extrainfo = request.form.get('extrainfo')
        new_data = HealthForm(user_id=current_user.id, allergies=allergies, disease=disease, symptoms=symptoms, medication=medication, drugs=drugs, extrainfo=extrainfo)
        user = HealthForm.query.filter_by(user_id=current_user.id).first()
        if user:
            db.session.delete(user)
            db.session.add(new_data)
            db.session.commit()
        else:
            db.session.add(new_data)
            db.session.commit()
        flash('Medical Info Added with Health Sync! Thank You for Entering.', category='success')  
        return redirect(url_for('views.home'))
    return render_template("medical_info.html", user=current_user)

