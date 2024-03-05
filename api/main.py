### ----------------------------------------------------
### File: main.py
### Authors: Hannah Renners
### ----------------------------------------------------


# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from flask import Flask, render_template, send_file, request, redirect, url_for, make_response, send_from_directory
from flask_cors import CORS
from markupsafe import escape
from PIL import Image

import os, re, uuid

from api.users import createUser, getUser, updateUser, getUserByToken
from aiTooling.assistants import getAssistant, callAssistant, listAssistants, updateAssistant, deleteAssistant
from aiTooling.llm import getLLM, deleteLLM, listLLMs, updateLLM

from aiTooling.standardTools import wolframAlpha

# ------------------------------------------------------
# Constants
# ------------------------------------------------------

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/*', methods=['OPTIONS'])
def options():
    # Preflight request. Reply successfully:
    response = app.make_default_options_response()
    return response

# ------------------------------------------------------
# Main - API - Auth
# ------------------------------------------------------

@app.route('/api/auth/login', methods=['POST'])
def loginAPI():
    try: 
        # Get the data
        json = request.get_json()
        userEmail = json['email']
        userToken= json['token']

        # Get the user
        user = getUserByToken(userToken)

        # Check if the password is correct
        if user['userEmail'] == userEmail:
            # Make a response
            response = make_response("200")
            return response
        else:
            return {'error': 'Unauthorized'}, 401
    except Exception as e:
        print(e)
        return {'error': 'Error'}, 500

@app.route('/api/auth/register', methods=['POST'])
def registerAPI():
    pass 

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
        return {'error': 'Error'}, 500
    
@app.route('/users/<userid>/<filename>')
def users(userid, filename):
    try: 
        directory = os.path.abspath(f'../storage/users/{userid}')
        filename = escape(filename)
        response = send_from_directory(directory, filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception as e:
        print(e)
        return {'error': 'Error'}, 500

# ------------------------------------------------------
# Main - API - AI
# ------------------------------------------------------
    
@app.route('/api/ai/assistant', methods=['GET', 'POST'])
def assistantAPI():
    pass

# ------------------------------------------------------
# Main - API - User
# ------------------------------------------------------

@app.route('/api/user/getUser', methods=['GET'])
def getUserAPI():
    try: 
        auth = request.headers['Authorization']
        userToken = auth.split(" ")[1]
        
        user = getUserByToken(userToken)
        return user, 200
    except Exception as e:
        print(e)
        return {'error': 'Error'}, 500

@app.route('/api/user/updateUser', methods=['POST'])
def updateUserAPI():
    try:
        auth = request.headers['Authorization']
        tokenInput = auth.split(" ")[1]

        # Check if the token is valid
        user = getUserByToken(tokenInput)
        # Check if the email is valid
    except Exception as e:
        return {'error': 'Error'}, 400

    try:
        params = {}

        try:
            json = request.get_json()
            print(json)
        except Exception as e:
            return {'error': 'Error'}, 400

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
                return {'error': 'Error, Invalid email.'}, 400

        except Exception as e:
            pass

        print(params)

        # Update the user
        updateUser(user['userID'], **params)
        return "200"
    except Exception as e:
        print(e)
        return {'error': 'Error'}, 401

@app.route('/api/user/createUser', methods=['POST'])
def createUserAPI():
    try:
        # Get the data
        json = request.get_json()

        print(json)

        userName = json['userName']
        userDisplayName = json['userDisplayName']
        userEmail = json['userEmail']
        userEmail = userEmail.lower()

        print(userEmail)

        # Check if it's a valid email with a regex (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
        if not re.match(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", userEmail):
                print('Email did not match regex: ' + userEmail)
                return {'error': 'Error, Invalid email.'}, 400
        
        # Create the user
        status, userID, userToken = createUser(userEmail=userEmail, userDisplayName=userDisplayName, userName=userName)
        if status:
            user = getUserByToken(userToken)
            return user, 200
        else:
            return {'error': 'Error, could not create user.'}, 400
    except Exception as e:
        print(e)
        return {'error': 'Error'}, 500

@app.route('/api/user/updateAvatar', methods=['POST'])
def updateAvatar():
    # Get cookies from request
    auth = request.headers['Authorization']
    tokenInput = auth.split(" ")[1]

    try:
        # Check if the token is valid
        print(tokenInput)
        user = getUserByToken(tokenInput)
        print(user)
        # Check if the email is valid
        if tokenInput not in user['tokens']:
            return {'error': 'Error'}, 401
    except Exception as e:
        return {'error': 'Error, failed Validation.'}, 401

    try:
        # Get the file
        print(request)
        file = request.files['avatar']

        # Resize the image to 256x256
        
        img = Image.open(file)
        img = img.resize((256, 256))

        # Save the image
        # Make sure the user's directory exists
        if not os.path.exists(f'../storage/users/{user["userID"]}'):
            os.makedirs(f'../storage/users/{user["userID"]}')

        # Delete old avatars
        for file in os.listdir(f'../storage/users/{user["userID"]}'):
            if file.startswith('avatar-'):
                os.remove(f'../storage/users/{user["userID"]}/{file}')

        avatarID = uuid.uuid4().hex

        img.save(f'../storage/users/{user["userID"]}/avatar-{avatarID}.png')

        # Update the user's icon
        updateUser(user['userID'], userIcon=f'/users/{user["userID"]}/avatar-{avatarID}.png')

        # Make response to tell the client to forget the cache
        response = make_response("200")
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        print(e)
        return {'error': 'Error, failed to update image.'}, 500

# ------------------------------------------------------
# Run
# ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)