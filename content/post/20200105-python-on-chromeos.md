---
title: Installing Python on ChromeOS
date: 2020-01-05
description: A beginner-friendly approach to installing Python on you Linux-based machine.
tags:
    - chromeos
    - python
    - how-to
---

Have a Chromebook? Don't have Python installed? Or worse, have Python2 and you'd rather have Python3? Let's fix that!

To start out, I want to share a picture from [XKCD](https://xkcd.com/1987/):

![Python Env](https://imgs.xkcd.com/comics/python_environment.png)

Python is notorious for its ability to lull the developer into a false sense of security before they absentmindedly mis-manage their coding environment. It's unfortunate, and not exactly necessary for a language to require this. Go ahead and search for the `golang python enviroment equivalent`. There is **nothing** like it for Go. Or C. Or Java.

While all of these languages may have their own quirks around the subject, the need for virtual environments is a quirk of Python. Go figure! (It has to do with the [global package management system](https://opensource.com/article/19/4/managing-python-packages) underneath the hood. It's a solid few hours of education if you want to get into it which I recommend!)


## Solution Description
To manage the Python development environments, I'm going to recommend and walk through installing a Python environment/version manager: [Pyenv](https://github.com/pyenv/pyenv-installer).

It'll allow you, the developer, to install different versions of Python at any time, specify when/where to use each one, and limit the reach of your dependencies such that they do not bleed into other projects.

And honestly this tutorial will work for anybody running a Debian or Ubuntu machine; if this describes you and you are not using ChromeOS, you may skip the next section and start installing Pyenv right off the bat.

## Setting Up ChromeOS
Before installing, we need to make sure Linux is installed.
This is done without invoking Developer Mode.

1. Enter Settings, enable Linux Container.
1. Install Linux.
    
    Preferrably, create your container with >=10GB of space, depending on how much you have available.

And just like that, you should have access to a new application called "Terminal". Congrats! You're using Debian ontop of ChromeOS!

## Installing Pyenv
[Pyenv](https://github.com/pyenv/pyenv-installer) has excellent instructions and documentation on their Github repo, but in the interest of keeping basic instructions on one page, I'll summarize here:

1. Open Terminal.
1. Update your device repositories and libraries by entering the following into Terminal (This may take some time if this is the first time you've done this!):
    ```
    $ sudo apt-get update && sudo apt-get upgrade
    ```

    If you have a ChromeOS version >=81 (which includes Debian 10), you probably already have Python3! (Use it by entering on the terminal: `python3`) Still, if you'd like to continue with installing Pyenv and manage your versions and dependencies more clearly, continue.
1. Install required dependencies by entering the following into Terminal:
    ```
    $ sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    ```
1. Install Pyenv from the creators:
    ```
    $ curl https://pyenv.run | bash
    ```
    This should be a quick installation; if you see the following message, you have another task to tend to:

    ```
    WARNING: seems you still have not added 'pyenv' to the load path.

    # Load pyenv automatically by adding
    # the following to ~/.bashrc:

    export PATH="/home/YOURUSERNAMEHERE/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```

    The steps are as simple as following the instructions provided! First, copy the commands Pyenv prompted you with and then enter the `~/.bashrc` file with your text editor of choice:

    ```
    $ vim ~/.bashrc
    ```

    Navigate to the bottom of the file and press `i` to enter `INSERT MODE`. Paste the commands you were prompted with before you entered the `~/.bashrc` file. I like to comment out (using `#`) a label for what I inserted and why.

    When finished, Press `Esc`, then `:wq` to save and exit.

1. Restart the shell with the following command:
    ```
    $ exec $BASH
    ```

    Or, if you prefer, close and open the Terminal. It'll do the same thing.

2. Finally, update Pyenv:
    ```
    $ pyenv update
    ```

Congrats! You have installed Pyenv and now Python version and environment management is very nearly putty in your fingers! We still need to *install* Python, though.

## Installing Python with Pyenv

Pyenv is useful, but it isn't the Python programming language; it's more of a handy-dandy multitool to do all the house-keeping which becomes common in Python development.

Try this:

You'll see a message similar to the following:
```
$ pyenv help
  Usage: pyenv <command> [<args>]

  Some useful pyenv commands are:
  activate    Activate virtual environment
  commands    List all available pyenv commands
  deactivate   Deactivate virtual environment
  doctor      Verify pyenv installation and development tools to build pythons.
  exec        Run an executable with the selected Python version
  global      Set or show the global Python version(s)
  help        Display help for a command
  hooks       List hook scripts for a given pyenv command
  init        Configure the shell environment for pyenv
  install     Install a Python version using python-build
  local       Set or show the local application-specific Python version(s)
  prefix      Display prefix for a Python version
  rehash      Rehash pyenv shims (run this after installing executables)
  root        Display the root directory where versions and shims are kept
  shell       Set or show the shell-specific Python version
  shims       List existing pyenv shims
  uninstall   Uninstall a specific Python version
  --version   Display the version of pyenv
  version     Show the current Python version(s) and its origin
  version-file   Detect the file that sets the current pyenv version
  version-name   Show the current Python version
  version-origin   Explain how the current Python version is set
  versions    List all Python versions available to pyenv
  virtualenv   Create a Python virtualenv using the pyenv-virtualenv plugin
  virtualenv-delete   Uninstall a specific Python virtualenv
  virtualenv-init   Configure the shell environment for pyenv-virtualenv
  virtualenv-prefix   Display real_prefix for a Python virtualenv version
  virtualenvs   List all Python virtualenvs found in `$PYENV_ROOT/versions/*'.
  whence      List all Python versions that contain the given executable
  which       Display the full path to an executable

  See `pyenv help <command>' for information on a specific command.
  For full documentation, see: https://github.com/pyenv/pyenv#readme
```

It's a whole lot of commands to play with which I'm unfortunately not going to explain. Let's get to the nitty gritty. To install a particular version of Python, we're going to use the `pyenv install` command.

To see what versions are available:
```
$ pyenv install --list
  ...
```

It's a long list. Taper it down with `grep` (a regex filter):
```
$ pyenv install --list | grep " 3\.[789]"
  3.7.0
  3.7-dev
  3.7.1
  3.7.2
  3.7.3
  3.7.4
  3.7.5
  3.7.6
  3.7.7
  3.7.8
  3.7.9
  3.8.0
  3.8-dev
  3.8.1
  3.8.2
  3.8.3
  3.8.4
  3.8.5
  3.8.6
  3.9.0
  3.9-dev
```

We have a few options to choose from!

to install a particular version, we're going to call it by the name provided in that list we found. If we want [Python 3.7.1](https://www.python.org/downloads/release/python-371/), we'll call it just as we see above, and let pyenv do the work for us!
```
$ pyenv install 3.7.1
  Downloading Python-3.7.1.tar.xz...
  -> https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tar.xz
  Installing Python-3.7.1...
  Installed Python-3.7.1 to /home/wjziv/.pyenv/versions/3.7.1
```

Looks like it's done; to check all the versions we have installed:
```
$ pyenv versions
  * system (set by /home/wjziv/.pyenv/version)
    3.7.1
```

We may set any version of python to be accessed with the `python` command with the following:
```
$ pyenv global 3.7.1
```

Note the change when we check the `versions` (the "global" star shifts.):
```
$ pyenv versions
    system
  * 3.7.1 (set by /home/wjziv/.pyenv/version)
```

And now we can see it in use immediately by entering the `python` command, plainly!
```
$ python
  Python 3.7.1 (default, Dec  2 2020, 11:27:43) 
  [GCC 8.3.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> 
```

It works! Exit `python` by entering `quit()`.

And of course, to uninstall any given version:
```
$ pyenv uninstall 3.7.1
```

___
Side note, as this is not necessarily *part* of Python, but it's important to notice; `pip` was installed with Pyenv!
```
$ pip

  Usage:   
    pip <command> [options]

  Commands:
    install                     Install packages.
    download                    Download packages.
    uninstall                   Uninstall packages.
    freeze                      Output installed packages in requirements format.
    list                        List installed packages.
    show                        Show information about installed packages.
    check                       Verify installed packages have compatible dependencies.
    config                      Manage local and global configuration.
    search                      Search PyPI for packages.
    wheel                       Build wheels from your requirements.
    hash                        Compute hashes of package archives.
    completion                  A helper command used for command completion.
    help                        Show help for commands.

  General Options:
    -h, --help                  Show help.
    --isolated                  Run pip in an isolated mode, ignoring environment variables and user configuration.
    -v, --verbose               Give more output. Option is additive, and can be used up to 3 times.
    -V, --version               Show version and exit.
    -q, --quiet                 Give less output. Option is additive, and can be used up to 3 times (corresponding to WARNING, ERROR, and CRITICAL logging
                                levels).
    --log <path>                Path to a verbose appending log.
    --proxy <proxy>             Specify a proxy in the form [user:passwd@]proxy.server:port.
    --retries <retries>         Maximum number of retries each connection should attempt (default 5 times).
    --timeout <sec>             Set the socket timeout (default 15 seconds).
    --exists-action <action>    Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup, (a)bort).
    --trusted-host <hostname>   Mark this host as trusted, even though it does not have valid or any HTTPS.
    --cert <path>               Path to alternate CA bundle.
    --client-cert <path>        Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
    --cache-dir <dir>           Store the cache data in <dir>.
    --no-cache-dir              Disable the cache.
    --disable-pip-version-check
                                Don't periodically check PyPI to determine whether a new version of pip is available for download. Implied with --no-index.
    --no-color                  Suppress colored output
```

`pip` is a package installer for Python. You'll be using this to install external packages from [PyPI](https://pypi.org/).

## Creating a Virtual Environment

Do all the playing-around you'd like with Pyenv in the terminal. Download the version(s) of Python you anticipte using. Uninstall and reinstall items. I'm glad you're having fun with it!

However, it may be the case you are not the most comfortable with using the command line; maybe you use an IDE like VSCode and you'd prefer to use a graphical UI wherever possible. Let's get into practical usage of Pyenv now that it's installed.

I mentioned at the top of the article that Pyenv was useful for keeping dependencies in one place, and managing versions. This is where **Virtual Environments** come into play.

To get in the practice of using the VSCode terminal if this is your situation, crack it open and navigate to a project where you'd like to install some dependencies. If you're comfortable with the terminal, stick with what you have and `cd` over to your project.

While working within the directory of your project:
1. Create your environment and give it a name:
    ```
    $ pyenv virtualenv PROJECT_NAME
    ```
1. Tie the environment to the pwd:
    ```
    $ pyenv local PROJET_NAME
    ```
1. Ensure to activate the environment:
    ```
    $ pyenv activate PROJECT_NAME
    ```

And that's it! You can install new versions of python and pin them to a particular project within this virtual environment:
```
$ pyenv install 3.9-dev
$ pyenv local 3.9-dev
```

Using the `python` command within this directory will point to `3.9-dev` in this case, rather than the global bersion found outside this directory.

You can install dependencies with particular versions within this project using a naked `pip` command:
```
$ pip install pandas 1.0.0
```

And this library/version will only exist within the defined project/directory! No more dependency bleeding.

## Closeout

Installing Python and managing environments is simple and easy with Pyenv; even if you aren't comfortable with the command line, most operations are done within the library itself, and with its accessible `help` menu, solving your particular technical problems aren't too far out of reach.