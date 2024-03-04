### ----------------------------------------------------
### File: llm.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from .llm import getLLM
import litellm
from litellm import LiteLLM

import tinydb

# ------------------------------------------------------
# Assistant Management
# ------------------------------------------------------

def updateAssistant(assistantID: str, assistantName: str, desciption: str, model: str, tools: list = [], tempeature: float = 0.7, includeChatHistory: bool = True, includeUserInfo: bool = True, includeUserInstructions: bool = True):
    db = tinydb.TinyDB("../storage/assistants.json")
    assistants = db.table("assistants")

    toolDB = tinydb.TinyDB("../storage/tools.json")
    toolsDB = toolDB.table("tools")

    def checkIfToolsExist(tools: list):
        for tool in tools:
            if not toolsDB.search(tinydb.Query().toolID == tool):
                return False
        return True

    # First check if assistant already exists
    if assistants.search(tinydb.Query().assistantID == assistantID):
        # If it does, modify the existing entry
        if checkIfToolsExist(tools):
            assistants.update({"assistantName": assistantName, "desciption": desciption, "model": model, "tools": tools, "tempeature": tempeature, "includeChatHistory": includeChatHistory, "includeUserInfo": includeUserInfo, "includeUserInstructions": includeUserInstructions}, tinydb.Query().assistantID == assistantID)
            return True, "Assistant updated successfully."
        else: 
            return False, "One or more tools do not exist in the database. Please add the tools first."
    else:
        # If it doesn't, create a new entry
        if checkIfToolsExist(tools):   
            assistants.insert({"assistantID": assistantID, "assistantName": assistantName, "desciption": desciption, "model": model, "tools": tools, "tempeature": tempeature, "includeChatHistory": includeChatHistory, "includeUserInfo": includeUserInfo, "includeUserInstructions": includeUserInstructions})
            return True, "Assistant created successfully."
        else: 
            return False, "One or more tools do not exist in the database. Please add the tools first."

def getAssistant(assistantID: str = None, assistantName: str = None):
    db = tinydb.TinyDB("../storage/assistants.json")
    assistants = db.table("assistants")

    if assistantID != None:
        return assistants.search(tinydb.Query().assistantID == assistantID)
    elif assistantName != None:
        return assistants.search(tinydb.Query().assistantName == assistantName)

def deleteAssistant(assistantID: str):
    db = tinydb.TinyDB("../storage/assistants.json")
    assistants = db.table("assistants")

    assistants.remove(tinydb.Query().assistantID == assistantID)
    
    return True

def listAssistants():
    db = tinydb.TinyDB("../storage/assistants.json")
    assistants = db.table("assistants")

    return assistants.all()

# ------------------------------------------------------
# Assistant Functions
# ------------------------------------------------------

def callAssistant(assistantID: str, messages: dict) -> dict:
    pass