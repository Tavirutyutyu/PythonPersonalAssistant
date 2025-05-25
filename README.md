<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running-the-application">Running the application</a></li>
      </ul>
    </li>
    <li><a href="#usage-and-customisation">Usage and Customisation</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
![Python Personal Assistant Screen Shot][screenshot]

This is my pet project. It's a personal assistant written in python. It uses Ollama as an AI, Festival as TTS and the GUI is written with tkinter. 
You can chat with an AI both in text and in voice. There are custom voice-commands. And there is a coding assistant system where you can upload files for the AI to look at.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][python.image]][python-url]
* [![Tkinter][tkinter.image]][tkinter-url]
* [![Ollama][ollama.image]][ollama-url]
* [![Festival][festival.image]][festival-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
This program is only compatible with Linux and Mac YET. 

### Prerequisites
You will need python 3.13 or higher installed.

### Installation

Clone the Python Personal Assistant repo:
```bash
git clone https://github.com/Tavirutyutyu/PythonPersonalAssistant.git
```

Then to create a virtual environment (.venv) and install dependencies run the setup.sh script like this:
```bash
bash setup.sh 
```
Note: For the application to run it will also need an installed Ollama, downloaded AI model and installed Festival to work. 
BUT!!! The application will attempt to install them on its own on the first run. You will be able to see the process in the terminal.
If there is any error with the installation of either ollama or festival only then try to install them manually.

### Running the application
Finally, you can run the project with this command when you are in the project root directory.
```bash
python3 main.py
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage and Customisation
I designed this application in a way so it's easy to add your own voice commands. You just need to know a little bit of python. 
And if you are a little bit bigger of a python master, you could even add your own AI or TTS service.
To add your own command you need to create a json file to hold the keywords that can trigger your command, and sub_options if you have.
For example to run the browser I have keywords like: [browse, open browser, open firefox...] and I have sub-options like: [google, youtube, github...] to open these sites in the browser.
And if your_command.json is in the resources folder you can write the class for it in python. It goes into the commands/commands.py just on the bottom. 
Here is an example:

```python
from commands import Command


class MyCommand(Command):
    def __init__(self):
        super().__init__(name="the name of your command", file_name="your_command.json")

    def execute(self, text: str | None = None):
        """
        Implement your solution here...
        :param text: This is the chosen sub-option
        :type text: str | None
        """
        pass
```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[screenshot]: resources/screenshot.png
[python.image]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[tkinter.image]: https://img.shields.io/badge/Tkinter-ffcc00?style=for-the-badge
[tkinter-url]: https://docs.python.org/3/library/tkinter.html
[ollama.image]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white
[ollama-url]: https://ollama.com/
[festival.image]: https://img.shields.io/badge/Festival_TTS-0a0a23?style=for-the-badge&logo=soundcloud&logoColor=white
[festival-url]: https://www.cstr.ed.ac.uk/projects/festival/