from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, HealthForm, User
from . import db
import json

views = Blueprint('views', __name__)

headings = ("First Name", "Last Name", "Email", "Current or Previous Allergies", "Current or Previous Diseases",
             "Current Symptoms", "Current or Previous Medication", "Drugs Consumed in the Last Year", "Extra Information")



@views.route('/', methods=['GET','POST'])
@login_required
def home():
    
    def redirect_action():
        return redirect(url_for('auth.medical_info'))

    if request.method == 'POST':
        note = request.form.get('note')
        

        if len(note) < 1:
            flash('Note for the Doctor is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note is given to Doctor!', category='success')

    userD2 = HealthForm.query.filter_by(user_id=current_user.id).first()
    userD1 = User.query.filter_by(id=current_user.id).first()

    data = ( 
    userD1.first_name, userD1.last_name, userD1.email, userD2.allergies, userD2.disease, userD2.symptoms, userD2.medication, userD2.drugs, userD2.extrainfo
    )
    return render_template("home.html", user_id=current_user, headings=headings, data=data)


@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    
    return jsonify({})
