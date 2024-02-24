### ----------------------------------------------------
### File: main.py
### Authors: Hannah Renners
### ----------------------------------------------------


# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from flask import Flask, render_template, send_file
from flask_htmx import HTMX
from markupsafe import escape

import os

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign-up')
def signUp():
    return render_template('sign-up.html')

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