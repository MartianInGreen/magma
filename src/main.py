### ----------------------------------------------------
### File: main.py
### Authors: Hannah Renners
### ----------------------------------------------------


# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from flask import Flask, render_template, send_file, request, redirect, url_for, make_response, send_from_directory
from flask_htmx import HTMX
from markupsafe import escape
from PIL import Image

import os, re

from api.users import createUser, getUser, updateUser, getUserByToken
from aiTooling.assistants import getAssistant, callAssistant, listAssistants, updateAssistant, deleteAssistant
from aiTooling.llm import getLLM, deleteLLM, listLLMs, updateLLM

from aiTooling.standardTools import wolframAlpha

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
    if request.cookies.get('token') != None and request.cookies.get('email') != None:
        try:
            userID = getUserByToken(request.cookies.get('token'))['userID']
            return redirect(f'/notes/{userID}')
        except Exception as e:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If method is GET, return the login page
    print(request.method)

    if request.method == 'GET':
        # Try to get email and token from cookies
        try:
            tokenInput = request.cookies.get('token')
            userEmail = request.cookies.get('email')

            print(tokenInput)
            print(userEmail)

            # Check if the token is valid
            user = getUserByToken(tokenInput)
            userID = user['userID']
            # Check if the email is valid
            if user['userEmail'] != userEmail:
                return render_template('login.html', error="Invalid email or token", title="Login")
            return redirect(f'/notes/{userID}')
        except Exception as e:
            print(e)
            pass

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
            
            response = make_response(redirect(f'/notes/{userID}'))
            response.set_cookie('token', tokenInput)
            response.set_cookie('email', userEmail)
            response.set_cookie('theme', 'dark')
            return response
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
            response = make_response(redirect(f'/login'))
            response.set_cookie('token', token)
            response.set_cookie('email', userEmail)
            return response
        # If the user was not created, return an error
        else:
            return render_template('sign-up.html', error="Error creating user", title="Sign Up")

@app.route('/notes')
def notesRedirect():
    # Get cookies from request
    tokenInput = request.cookies.get('token')
    userEmail = request.cookies.get('email')

    try:
        # Check if the token is valid
        user = getUserByToken(tokenInput)
        userID = user['userID']
        # Check if the email is valid
        if user['userEmail'] != userEmail:
            return redirect('/login')
    except Exception as e:
        return redirect('/login')

    return redirect(f'/notes/{userID}')

@app.route('/notes/<userid>')
def notes(userid):
    # Get cookies from request
    tokenInput = request.cookies.get('token')
    userEmail = request.cookies.get('email')

    try:
        # Check if the token is valid
        user = getUserByToken(tokenInput)
        # Check if the email is valid
        if user['userEmail'] != userEmail:
            return redirect('/login')
    except Exception as e:
        return redirect('/login')
    
    params = {'title': "Notes", 'userName': user['userName'], 'displayName': user['userDisplayName'],'userId': user['userID']}

    # Check if the user has an icon
    try:
        userIcon = user['userIcon']
        params['avatarIcon'] = userIcon
    except Exception as e:
        pass

    print(params)

    return render_template('notes.html', **params)

# ------------------------------------------------------
# Views
# ------------------------------------------------------

@app.route('/views/<view>')
def views(view):
    if htmx:
        try:
            return render_template(f'views/{escape(view)}.html')
        except Exception as e:
            print("Template not found")
            return "401"
    else: 
        return "401"
        
@app.route('/settings/<part>')
def settings(part):
    if htmx:
        try:
            params = {}

            if part == "account": 
                try: 
                    # Get cookies from request
                    tokenInput = request.cookies.get('token')
                    userEmail = request.cookies.get('email')

                    # Check if the token is valid
                    user = getUserByToken(tokenInput)
                    # Check if the email is valid
                    if user['userEmail'] != userEmail:
                        return redirect('/login')

                    # Get the user's information
                    params['userName'] = user['userName']
                    params['userDisplayName'] = user['userDisplayName']
                    params['userEmail'] = user['userEmail']
                    params['userId'] = user['userID']
                    params['avatarIcon'] = user['userIcon']
                    params['tokens'] = user['tokens']
                except Exception as e:
                    return redirect('/login')

            return render_template(f'settings/{escape(part)}.html', **params)
        except Exception as e:
            print("Template not found")
            return "Setting not found"
    else: 
        return "401"

# ------------------------------------------------------
# Main - API - Files
# ------------------------------------------------------

@app.route('/images/<filename>')
def images(filename):
    try: 
        directory = os.path.abspath(f'../storage/static/images/')
        filename = escape(filename)
        
        # file type 
        file_type = filename.split(".")[::-1][0]

        response = send_from_directory(directory, filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        
        # Set the mimetype
        response.mimetype = f"image/{file_type}"

        return response
    except Exception as e:
        print(e)
        return "401", 401
    
@app.route('/css/<filename>')
def css(filename):
    try: 
        directory = os.path.abspath('../storage/static/css/')
        filename = escape(filename)
        response = send_from_directory(directory, filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception as e:
        print(e)
        return "401"
    
@app.route('/js/<filename>')
def js(filename):
    try: 
        directory = os.path.abspath('../storage/static/js/')
        filename = escape(filename)
        response = send_from_directory(directory, filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception as e:
        print(e)
        return "401"
    
@app.route('/users/<userid>/<filename>')
def users(userid, filename):
    try: 
        directory = os.path.abspath(f'../storage/static/users/{userid}')
        filename = escape(filename)
        response = send_from_directory(directory, filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception as e:
        print(e)
        return "401"

# ------------------------------------------------------
# Main - API - AI
# ------------------------------------------------------
    
@app.route('/api/ai/assistant', methods=['GET', 'POST'])
def assistantAPI():
    pass

# ------------------------------------------------------
# Main - API - User
# ------------------------------------------------------

@app.route('/api/user/updateUser', methods=['POST'])
def updateUserAPI():
    # Get cookies from request
    tokenInput = request.cookies.get('token')
    userEmail = request.cookies.get('email')

    try:
        # Check if the token is valid
        user = getUserByToken(tokenInput)
        # Check if the email is valid
        if user['userEmail'] != userEmail:
            return "401"
    except Exception as e:
        return "401"

    try:
        params = {}

        try:
            json = request.get_json()
            print(json)
        except Exception as e:
            return "401"

        # Get the data
        try:
            userName = json['userName']
            params['userName'] = userName
        except Exception as e:
            pass

        try:
            userDisplayName = json['userDisplayName']
            params['userDisplayName'] = userDisplayName
        except Exception as e:
            pass

        try:
            userEmail = json['userEmail']
            params['userEmail'] = userEmail

            # Check if it's a valid email with a regex (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
            if not re.match(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", userEmail):
                return "401"

        except Exception as e:
            pass

        print(params)

        # Update the user
        updateUser(user['userID'], **params)
        return "200"
    except Exception as e:
        print(e)
        return "401"

@app.route('/api/user/updateAvatar', methods=['POST'])
def updateAvatar():
    # Get cookies from request
    tokenInput = request.cookies.get('token')
    userEmail = request.cookies.get('email')

    try:
        # Check if the token is valid
        user = getUserByToken(tokenInput)
        # Check if the email is valid
        if user['userEmail'] != userEmail:
            return "401"
    except Exception as e:
        return "401"

    try:
        # Get the file
        file = request.files['avatar']

        # Resize the image to 256x256
        
        img = Image.open(file)
        img = img.resize((256, 256))

        # Save the image
        # Make sure the user's directory exists
        if not os.path.exists(f'../storage/static/users/{user["userID"]}'):
            os.makedirs(f'../storage/static/users/{user["userID"]}')

        img.save(f'../storage/static/users/{user["userID"]}/avatar.png')

        # Update the user's icon
        updateUser(user['userID'], userIcon=f'/users/{user["userID"]}/avatar.png')

        # Make response to tell the client to forget the cache
        response = make_response("200")
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        print(e)
        return "401"

# ------------------------------------------------------
# Run
# ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)