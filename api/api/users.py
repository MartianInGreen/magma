### ----------------------------------------------------
### File: users.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import tinydb
import uuid
import secrets

# ----------------------------------------------------
# User Management
# ----------------------------------------------------

def createUser(userEmail: str, userName: str, userDisplayName: str) -> tuple[bool, str, str]:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    userToken = secrets.token_urlsafe(32)

    unique = False
    while not unique:
        userID = str(uuid.uuid4().hex)[:8]

        # Check if userID already exists
        if not users.search(tinydb.Query().userID == userID):
            unique = True

    # First check if user already exists
    if users.search(tinydb.Query().userEmail == userEmail):
        return False, None, None
    else:
        # If it doesn't, create a new entry
        users.insert({"userID": userID, "userEmail": userEmail, "userName": userName, "userDisplayName": userDisplayName, "userInfo": "", "userInstructions": "", "tokens": [userToken]})
        return True, userID, userToken

def getUser(userID: str = None, userEmail: str = None, userName: str = None) -> dict:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    if userID != None:
        return users.search(tinydb.Query().userID == userID)
    elif userEmail != None:
        return users.search(tinydb.Query().userEmail == userEmail)
    elif userName != None:
        return users.search(tinydb.Query().userName == userName)
    else:
        return None

def updateUser(userID: str, userEmail: str = None, userName: str = None, userDisplayName: str = None, userInfo: str = None, userInstructions: str = None, userIcon: str = None) -> bool:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    # First check if user already exists
    if users.search(tinydb.Query().userID == userID):
        # If it does, modify the existing entry
        if userEmail != None:
            users.update({"userEmail": userEmail}, tinydb.Query().userID == userID)
        if userName != None:
            users.update({"userName": userName}, tinydb.Query().userID == userID)
        if userDisplayName != None:
            users.update({"userDisplayName": userDisplayName}, tinydb.Query().userID == userID)
        if userInfo != None:
            users.update({"userInfo": userInfo}, tinydb.Query().userID == userID)
        if userInstructions != None:
            users.update({"userInstructions": userInstructions}, tinydb.Query().userID == userID)
        if userIcon != None:
            users.update({"userIcon": userIcon}, tinydb.Query().userID == userID)

        return True
    else:
        return False

def getUserByToken(token: str) -> dict:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    # Tokens looks something like this: "tokens": ["VN2npha-Zueb3MrKLV3u2gs74eEBD_No8O0sD78CbZU"]
    for user in users.all():
        if token in user['tokens']:
            return user

def generateNewToken(userID: str) -> str:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    userToken = secrets.token_urlsafe(32)

    # First check if user already exists
    if users.search(tinydb.Query().userID == userID):
        # If it does, modify the existing entry
        users.update(tinydb.operations.add("tokens", userToken), tinydb.Query().userID == userID)
        return userToken
    else:
        return None
    
def resetTokens(userID: str) -> str:
    db = tinydb.TinyDB("../storage/users.json")
    users = db.table("users")

    userToken = secrets.token_urlsafe(32)

    # First check if user already exists
    if users.search(tinydb.Query().userID == userID):
        # If it does, modify the existing entry
        users.update(tinydb.operations.set("tokens", [userToken]), tinydb.Query().userID == userID)
        return userToken
    else:
        return None