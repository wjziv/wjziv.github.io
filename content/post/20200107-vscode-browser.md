---
title: Run VSCode in the Browser
date: 2020-01-07
tags:
    - how-to
    - vscode
    - ide
---

As a ChromeOS user, it's not uncommon to find that most Linux programs don't run as smoothly as one would hope. If there's a version that runs in the browser, it's likely to be a better experience.

Enter [code-server](https://github.com/cdr/code-server). While its primary intention is to be run on the cloud as a server-based IDE, they provide builds which you can run locally.

Releases: https://github.com/cdr/code-server/releases

Move tar file to the linux container.

In terminal, enter: `tar -xf filename.tar.gz`

That's it! 

In terminal, enter `./path/to/unzip/location/code-server` to execute the shell script inside and run the IDE on localhost. It'll provide a url like `https://localhost:8080`. Copy and paste it into the browser.