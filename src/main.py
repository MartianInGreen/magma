### ----------------------------------------------------
### File: main.py
### Authors: Hannah Renners
### ----------------------------------------------------


# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from flask import Flask, render_template, send_file, request, redirect, url_for
from flask_htmx import HTMX
from markupsafe import escape

import os

from api.users import createUser, getUser, updateUser, getUserByToken
from aiTooling.assistants import getAssistant, callAssistant, listAssistants, updateAssistant, deleteAssistant
from aiTooling.llm import getLLM, deleteLLM, listLLMs, updateLLM

# ------------------------------------------------------
# Constants
# ------------------------------------------------------

# ------------------------------------------------------
# Main - UI
# ------------------------------------------------------

app = Flask(__name__)
htmx = HTMX(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If method is GET, return the login page
    print(request.method)
    if request.method == 'GET':
        return render_template('login.html', title="Login")
    # If method is POST, check the login credentials
    elif request.method == 'POST':
        tokenInput = request.form['token']
        userEmail = request.form['email']
        # Check if one of the fields is empty
        if tokenInput == "" or userEmail == "":
            return render_template('login.html', error="Please fill out all fields", title="Login")

        # Check if the token is valid
        try:
            user = getUserByToken(tokenInput)
            print(user)
            userID = user['userID']
            # Check if the email is valid
            if user['userEmail'] != userEmail:
                return render_template('login.html', error="Invalid email or token", title="Login")
            return redirect(f'/notes/{userID}')
        except Exception as e:
            print(e)
            return render_template('login.html', error="Invalid email or token", title="Login")

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    # If method is GET, return the sign-up page
    if request.method == 'GET':
        return render_template('sign-up.html', title="Sign Up")
    # If method is POST, create the user
    elif request.method == 'POST':
        userEmail = request.form['email']
        userName = request.form['name']
        userDisplayName = request.form['displayName']
        # Check if one of the fields is empty
        if userEmail == "" or userName == "" or userDisplayName == "":
            return render_template('sign-up.html', error="Please fill out all fields", title="Sign Up")

        # Create the user
        success, userID, token = createUser(userEmail, userName, userDisplayName)
        # If the user was created, return the user's token
        if success:
            return redirect(f'/login?token={token}&email={userEmail}')
        # If the user was not created, return an error
        else:
            return render_template('sign-up.html', error="Error creating user", title="Sign Up")

@app.route('/notes/<userid>')
def notes(userid):
    return render_template('notes.html', title="Notes")

@app.route('/notes/<userid>/<noteid>')
def note(userid, noteid):
    return render_template('notes.html', title="Note: " + noteid)

@app.route('/settings/<userid>')
def settings(userid):
    return render_template('settings.html', title="Settings")

# ------------------------------------------------------
# Main - API
# ------------------------------------------------------

@app.route('/images/<filename>')
def images(filename):
    try: 
        file = os.path.abspath(f'../storage/static/images/{escape(filename)}')
        
        # file type 
        file_type = filename.split(".")[::-1][0]

        return send_file(file, mimetype=f'image/{file_type}')
    except Exception as e:
        print(e)
        return "401"

# ------------------------------------------------------
# Run
# ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)