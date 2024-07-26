from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, HealthForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):               
            flash('Logged In Successfully!', category='success')
            login_user(user, remember=True)
            return render_template("home.html", boolean=True, user=current_user)
        elif not user:
            flash("Email is incorrect or does not exist, try again or Sign Up.", category='error')
        else:
                flash('Incorrect Password, try again.', category='error')
        
    return render_template("login.html", user=current_user)


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
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created with Health Sync! Thank You for Joining.', category='success')
            return redirect(url_for('auth.medical_info'))
    return render_template("sign_up.html", user=current_user)

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
            user.allergies = allergies
            user.disease = disease
            user.symptoms = symptoms
            user.medication = medication
            user.drugs = drugs
            user.extrainfo = extrainfo
            db.session.commit()
        else:
            db.session.add(new_data)
            db.session.commit()
        flash('Medical Info Added with Health Sync! Thank You for Entering.', category='success')  
        return redirect(url_for('views.home'))
    return render_template("medical_info.html", user=current_user)
