# All blocks
```json
{
    "blockID": "id",
    "blockOwner": "Either user/userID or assistant/assistantID"
}
```

# Individual
**Markdown**
Display Markdown Text
```json
{
    "text": "Markdown Text"
}
```

**Image**
Render image content
```json
{
    "imageLocation": "path",
    "imageCaption": false # Can also be a string
}
```

**Audio**
Audio content
```json
{
    "audioPath": "path",
    "audioTranscript": false # Can also be a string
}
```