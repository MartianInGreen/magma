### ----------------------------------------------------
### File: notes.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import mistune
from markupsafe import escape

# ----------------------------------------------------
# Notes API
# ----------------------------------------------------

def getNoteById(noteId: str):
    pass

# ---------------------------------------------------- 
# Block Functions
# ----------------------------------------------------

def markdownBlock(input: str):
    return convertMarkdownToHtml(input)

def imageBlock(input: str, noteId: str):
    serverImagePath = f"/notes/{escape(noteId)}/images/{escape(input)}"
    return f"<img src='{serverImagePath}' alt='{input}' />"

def audioBlock(input: str):
    pass

def videoBlock(input: str):
    pass

def codeBlock(input: str):
    pass

def canvasBlock(input: str):
    pass

def spreadSheetBlock(input: str):
    pass

def diagramBlock(input: str):
    pass

def mathBlock(input: str):  
    pass

def tableBlock(input: str):
    pass

def presentationBlock(input: str):
    pass

def webPageBlock(input: str):
    pass

def pdfBlock(input: str):
    pass  

def tasksBlock(input: str):
    pass

# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------

def convertMarkdownToHtml(markdown: str):
    converter = mistune.create_markdown(plugins=["strikethrough", "footnotes", "table", "url", 'task_lists', 'abbr', 'mark', 'superscript', 'subscript', 'math', 'spoiler'])
    html = converter(markdown)
    
    return html
