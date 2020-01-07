title: Installing Python on ChromeOS
date: 2020-01-05
hero:
description: A beginner-friendly approach to installing Python on you Linux-based machine.
tags:
    - ChromeOS
    - Python
    - How-to

The use of each software being installed:

pyenv - install and manage the different versions of python you may need to use

pipenv - manage the different development environments you may need to use in the future. Usecase: you have a project that requires Dependency A v1, and another that required Dep A v2. You can't have both installed onyour device. Use environments. Pipenv makes it easy to use virtual environments and pip together at one time. Enter the pipenv and use pip all you like.

I have a Pixelbook, but this may work for any CrOS computer which has Linux Enabled. Pixelbook comes with Python 3.5, but I don't know if other Linux-enabled Chromebooks come with Python. Probably? Either way, this is written for all ChromeOS Linux-Enabled/Crostini beginners, assuming you have no Python installed at all.
This is done without invoking Developer Mode.

1. Enter Settings, enable Linux Container.
2. Install Linux.
3. Open Terminal.
4. Update current apt-get libraries (sudo apt-get update)
5. Optional: If this is the first time you're doing anything in your ChromeOS linux container, upgrade already-installed libraries (sudo apt-get upgrade)
6. Note the current version of Python, if it is installed. Try the following commands. If you receive '-bash: python: command not found', it is not installed. (python --version, python3 --version) Pixelbook automatically comes with Python 3.5 at the time of writing (9/15/19)
7. If you have the python version you're looking to install, that's great! You're done. If you'd like otherwise, continue.
8. https://realpython.com/intro-to-pyenv/
9. After installation, set the pyenv version to your preferred version: `pyenv global x.x.x`

    See options with `pyenv versions`


Basically, just follow basic instructions for pyenv-installer. More trustworthy documentation:
https://github.com/pyenv/pyenv-installer
https://dev.to/writingcode/the-python-virtual-environment-with-pyenv-pipenv-3mlo
The reason being:
a) It's the easiest way (IMO) to get Python up and running on your machine.
b) It's not conda.
- As a beginner, it does not get you wrapped up deeper and deeper into the conda field (which, while very powerful, may detract from a first-time user's learning experience. Encourage you to become familiar when you are comfortable with vanilla python and pip)
- Relatedly, just use pip as is--use Python as it's intended made (eyes at conda)

Comes with pip and setuptools automatically.
Automatically changes the path for shortcuts to these packages.

install global python libraries

PIPENV
next, install pipenv, for the purpose of creating virtual environments for your python projects. Instructions here.
https://docs.pipenv.org/en/latest/install/#installing-pipenv
Ultimately, done with (pip install --user pipenv)
After the pip install, make sure to add the 'user base binary' to ~/.bashrc. Instructions just under the pip instructions on the link above.

restart shell (exec bash)

Done, pipenv is installed!

Give it some use. Navigate to a local git repo/project you have going on, (or clone one now. Git required.) Once cd'd in, enter this (pipenv --python 3.7.4 [or whatever version you may need]).

If the specified python version was not already installed on your computer, it'll be installed. It'll take some time to create the virtual environment. Once completed, you'll have the opportunity to enter the virtual environment (pipenv shell), install whatever library versions you want with pip, etcetc. To leave, type (exit).