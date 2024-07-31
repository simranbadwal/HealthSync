from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, HealthForm, User
from . import db
import json
import pip._vendor.requests as requests
from pip._vendor.requests import get
views = Blueprint('views', __name__)

headings = ("First Name", "Last Name", "Email", "Current or Previous Allergies", "Current or Previous Diseases",
             "Current Symptoms", "Current or Previous Medication", "Drugs Consumed in the Last Year", "Extra Information")

headings_Doctor = ("Doctor Speciality","First Name", "Last Name", "Email")



def readFromDatabase(query):
    """
    -------------------------------------------------------
    Executes a search query to retrieve data from a database.
    The function constructs a search URL using the provided query,
    sends a GET request to the database, and returns result as string
    Use: result = readFromDatabase('query')
    -------------------------------------------------------
    Parameters:
        query - The search query to be executed (String).
    Returns:
        result - String.
    -------------------------------------------------------
    """
    searchQuery = f'http://15.156.34.180:8020/search-for-a-doctor/{query}'
    result = get(searchQuery).json()['data'].strip()
    return result


@views.route('/')
@views.route('/homeapage')
def landingPage():
    """
    -------------------------------------------------------
    Handles requests to the landing page.
    Routes:
        /         : The root URL of the website.
        /homepage : An alternative URL for the landing page.
    Returns:
        A rendered HTML template for the landing page with provided data.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        A rendered HTML template for the landing page with provided data.
    -------------------------------------------------------
    """
    # dynamic Tilte to webpage
    data={
        'title':"Health-Sync"
    }
    return render_template('homepage/homepage.html',data= data)


@views.route('/searchForAdoctor')
def doctorSearchResults():
    """
    -------------------------------------------------------
    Handles requests to search for a doctor based on a keyword.
    Route:
        /searchForAdoctor : Endpoint for searching doctors.
    Returns:
        A rendered HTML template with search results or a 'no results found' message.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        A rendered HTML template based on the search results:
            - If the keyword is empty, returns "noResultsFound2.html".
            - If no matching results are found, returns "noResultsFound.html".
            - If matching results are found, returns "searchBoxResultItem.html" with the data.
    -------------------------------------------------------
    """
    keyword = request.args.get("keyword")
    if len(keyword)==0:
        return render_template("homepage/components/noResultsFound2.html")
    
    
    data = readFromDatabase(keyword)
    if len(data)==0:
        return render_template("homepage/components/noResultsFound.html")
    
    return render_template("homepage/components/searchBoxResultItem.html",data= data)





# change this to whatever path you want, i want shiffted the landing page to main route
@views.route('/SIMRAN', methods=['GET','POST'])
@login_required
def home():
    
    def redirect_action():
        return redirect(url_for('auth.medical_info'))
    if current_user.isDoctor == False:
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
        return render_template("home.html", user_id=current_user, headings=headings, data=data, )
    else:
        userD1 = User.query.filter_by(id=current_user.id).first()
        data = ( 
        "Dr",userD1.first_name, userD1.last_name, userD1.email
        )
        return render_template("home_doctor.html", user_id=current_user, headings=headings_Doctor, data=data)



    


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    
    return jsonify({})

