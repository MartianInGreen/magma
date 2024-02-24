### ----------------------------------------------------
### File: main.py
### Authors: Hannah Renners
### ----------------------------------------------------


# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from flask import Flask, render_template, send_file, request
from flask_htmx import HTMX
from markupsafe import escape

import os

from api.users import createUser, getUser, updateUser, getUserByToken

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
        return render_template('login.html')
    # If method is POST, check the login credentials
    elif request.method == 'POST':
        tokenInput = request.form['token']
        userEmail = request.form['email']
        # Check if one of the fields is empty
        if tokenInput == "" or userEmail == "":
            return render_template('login.html', error="Please fill out all fields")

        # Check if the token is valid
        try:
            user = getUserByToken(tokenInput)
            print(user)
            userID = user['userID']
            # Check if the email is valid
            if user['userEmail'] != userEmail:
                return render_template('login.html', error="Invalid email or token")
            return f"200 {userID}"
        except Exception as e:
            return render_template('login.html', error="Invalid email or token")

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    # If method is GET, return the sign-up page
    if request.method == 'GET':
        return render_template('sign-up.html')
    # If method is POST, create the user
    elif request.method == 'POST':
        userEmail = request.form['email']
        userName = request.form['name']
        userDisplayName = request.form['displayName']
        # Check if one of the fields is empty
        if userEmail == "" or userName == "" or userDisplayName == "":
            return render_template('sign-up.html', error="Please fill out all fields")

        # Create the user
        success, userID, token = createUser(userEmail, userName, userDisplayName)
        # If the user was created, return the user's token
        if success:
            return f"200 {userID} {token}"
        # If the user was not created, return an error
        else:
            return render_template('sign-up.html', error="Error creating user")

@app.route('/notes/<userid>')
def notes(userid):
    return render_template('notes.html')

@app.route('/settings/<userid>')
def settings(userid):
    return render_template('settings.html')

# ------------------------------------------------------
# Main - API
# ------------------------------------------------------

@app.route('/images/<filename>')
def images(filename):
    file = os.path.abspath(f'../storage/static/images/{escape(filename)}')
    
    # Check what file type it is
    if filename.endswith(".jpg"):
        return send_file(file, mimetype='image/jpg')
    elif filename.endswith(".png"):
        return send_file(file, mimetype='image/png')
    elif filename.endswith(".ico"):
        return send_file(file, mimetype='image/ico')

if __name__ == '__main__':
    app.run(debug=True)