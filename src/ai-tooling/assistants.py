### ----------------------------------------------------
### File: llm.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ------------------------------------------------------
# Imports
# ------------------------------------------------------

from llm import getLLM
import litellm
from litellm import LiteLLM

# ------------------------------------------------------
# Assistant Management
# ------------------------------------------------------

def updateAssistant(assistantID: str, assistantName: str, desciption: str, model: str, tools: list = [], tempeature: float = 0.7, includeChatHistory: bool = True, includeUserInfo: bool = True, includeUserInstructions: bool = True):
    pass 

def getAssistant(assistantID: str = None, assistantName: str = None):
    pass

def deleteAssistant(assistantID: str):
    pass

def listAssistants():
    pass

# ------------------------------------------------------
# Assistant Functions
# ------------------------------------------------------

def callAssistant(assistantID: str, messages: dict) -> dict:
    pass