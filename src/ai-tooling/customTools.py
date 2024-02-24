### ----------------------------------------------------
### File: customTools.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ------------------------------------------------------
# Imports
# ------------------------------------------------------
import os
import subprocess

# ------------------------------------------------------
# Custom Tools
# ------------------------------------------------------

def customTool(argDict: list, toolId: str, chatId: str):
    os.makedirs(f"../storage/chats/{chatId}/files/", exist_ok=True)

    fileLocation = os.path.abspath(f"../storage/chats/{chatId}/files/")
    scriptLocation = os.path.abspath(f"../storage/tools/")

    dockerCommand = f"docker run -it -v {fileLocation}:/runtime:rw -v {scriptLocation}:/scripts:ro --rm --name codeapi codeapi"

    fullCommand = dockerCommand + f" python3 ../scripts/{toolId}.py"
    fullCommand = fullCommand.split(" ")
    
    for arg in argDict:
        fullCommand.append(arg)

    output = subprocess.Popen(fullCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = output.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    
    return stdout

if __name__ == "__main__":
    print(customTool(["10"], 123456789, 123456789))