### ----------------------------------------------------
### File: llm.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ------------------------------------------------------
# Imports
# ------------------------------------------------------

import tinydb

# ------------------------------------------------------
# LLM Storage Functions
# ------------------------------------------------------

def updateLLM(modelName: str, humanName: str, functionCalling: bool, toolCalling: bool, imageInput: bool, maxTokens: int, maxNewTokens: int, apiKey: str):
    db = tinydb.TinyDB("../storage/models.json")
    models = db.table("models")

    # First check if model already exists
    if models.search(tinydb.Query().modelName == modelName):
        # If it does, modify the existing entry
        models.update({"humanName": humanName, "functionCalling": functionCalling, "toolCalling": toolCalling, "imageInput": imageInput, "maxTokens": maxTokens, "maxNewTokens": maxNewTokens, "apiKey": apiKey}, tinydb.Query().modelName == modelName)
    else:
        # If it doesn't, create a new entry
        models.insert({"modelName": modelName, "humanName": humanName, "functionCalling": functionCalling, "toolCalling": toolCalling, "imageInput": imageInput, "maxTokens": maxTokens, "maxNewTokens": maxNewTokens, "apiKey": apiKey})
        
    return True

def getLLM(modelName: str, humanName: str = None):
    db = tinydb.TinyDB("../storage/models.json")
    models = db.table("models")

    if humanName != None:
        return models.search(tinydb.Query().humanName == humanName)
    else:
        return models.search(tinydb.Query().modelName == modelName)

def deleteLLM(modelName: str):
    db = tinydb.TinyDB("../storage/models.json")
    models = db.table("models")

    models.remove(tinydb.Query().modelName == modelName)

    return True

def listLLMs():
    db = tinydb.TinyDB("../storage/models.json")
    models = db.table("models")

    return models.all()

# ------------------------------------------------------
# LLM Functions
# ------------------------------------------------------


if __name__ == "__main__":
    print(updateLLM("gpt-3", "GPT-3", True, True, True, 2048, 100, "1234"))
    print(getLLM("gpt-3"))