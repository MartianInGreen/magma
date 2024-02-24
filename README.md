# Magma
Magma is an attempt to unify Note-taking and AI applications into a singular, more powerful, experience

> NOTE: Magma is still in **very** early development, features listed below are **not yet** completed. Please look on the roadmap to see what is actually implemented.
>
> Features below are listed as such:
> - [ ] Planned
> - [ ] **In Progress**
> - [x] Implemented

## Key Features 
- Unified note-taking and AI interface experience.
- Take Markdown-like notes with a robust feature set.
- Interact with the latest in AI, with Agents that have Tools and can help you do you work, not just write. 

## Note-taking
Magma is a note taking, knowledge management, and organization tool. Inspired by Obsidian, Reor, and Notion. 
Magma uses "blocks" for notes, the full featureset of Markdown is supported, additionally there are many more blocks than can be helpful in more specialized uses. Magma automatically converts some Markdown elements into their respective blocks.

## Tools
In addition to the AI features, Magma has some useful tools build in. These include a Calculator (using Wolfram|Alpha), a Camera for taking pictures or scanning documents, an Audio recorder with transcription, a Calendar for organisation, a Pomodoro Timer, and some more planned for the future!

## AI Tools
Magma is focused on an equally as good AI experience as note-taking experience, the goal is for you to be able to replace both your current AI application (like ChatGPT) and your current note-taking application with a single more unified one.
As part of that plan we support (custom) Plugins (with many already build in), custom Assistant (like GPTs), a Code Interpreter, chatting with Notes, and much more!

## Roadmap

**Version 0.1.0 - Cinder**
- [ ] Basic note-taking experience
  - [ ] Markdown input & rendering
  - [ ] Text editor
  - [ ] Some specialized blocks
    - [ ] Images
    - [ ] Audio
- [ ] Basic ai experience
  - [ ] Custom Models
  - [x] Integrated Tools
  - [ ] Basic Chat Interface
  - [ ] Basic Notes Copilot
  - [x] Code Interpreter
  - [x] Custom Tools

**Version 0.2.0 - Shield**
- [ ] Expanding blocks
  - [ ] Video
  - [ ] PDFs
  - [ ] Code
  - [ ] Canvas
  - [ ] Diagrams & Mindmaps
  - [ ] Math
  - [ ] Spreadsheets 
  - [ ] Canvas
- [ ] Tools
  - [ ] Calculator
  - [ ] Pomodor Timer
- [ ] AI Expansion
  - [ ] Management Interface
  - [ ] Upgraded Chat
  - [ ] Upgraded Copilot
  - [ ] (Custom) Assistants
  - [ ] Tools interface

**Version 0.3.0 - Fissure**
- [ ] Expanding blocks
  - [ ] Presentation
  - [ ] Tables / Table Databases / Boards
  - [ ] Webpage Embed
  - [ ] Tasks
- [ ] Note taking features
  - [ ] Tags
  - [ ] Task Overview
  - [ ] Calendar
  - [ ] Daily Notes
- [ ] Tools
  - [ ] Audio recorder
  - [ ] Camera

**Version 0.4.0 - Dome**
...

**Version 1.0 - Strato**
...

# Instructions

## Reporting Bugs and Requesting Features
If you find a bug or want to request a feature, please use the GitHub Issues. The Issues are located [here](https://github.com/MartianInGreen/magma/issues) and file an issue.

## Contributing
If you want to contribute to the project, please read the CONTRUBUTING.md file in the root of this repository.

## Support
If you need support please open an issue.

## System Requirements

This project is build using Python, you will also need Docker installed on your machine. 

## Installation

> Currently installation under Windows is not supported, you can use WSL. Not yet deployment ready.

Install [Python 3.11](https://www.python.org/) and [Docker](https://www.docker.com/).

Clone this repository: 
```bash
git clone https://github.com/MartianInGreen/magma.git
cd magma
```

Copy the `.env.example`file and change what you need to change.

```bash
cp .env.example .env
```

If you want to add additional Python or System packages (apt) for the Code Interpreter modify the respective files in the `codeapi` folder first. Only works when bulding image from source!

> Note: The install script creates a python env, installs python packages, and builds (which can take several minutes) or downloads the codeapi docker image 
> The Docker image is quite large > 2 GB, this is due to the needed Python and NodeJS installation (~850 MB Download)

Run the install script:
```bash
chmod +x tooling/install.sh
chmod +x tooling/run.sh
./tooling/install.sh
```

## Usage

> Coming soon...