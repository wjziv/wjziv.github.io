---
title: About This Site
date: 2020-11-28
description: how this site was built
tags: 
    - how-to
    - golang
    - hugo
    - websites
toc: true
draft: false
---

## Summary
Host a personal website on Github using the Hugo site generator. Updates to content will be incorporated into the site via triggered Github Actions.

## My Choices
Originally, I was using Frozen-Flask and FlatPages to build my static site. Flask, as backend tool I was familiar with, was something I was interested in leveraging for this website. Ultimately, it felt like a hodge-podge project, loosely slapped together which could have been executed in a better way.

Outside of wanting to use a "better" static site generator, I wanted to switch to Hugo for two reasons:
- It's written in Go, a language I'm currently acquainting myself with, and I was interested in reading through a project whose function I was actively familiar with.
- I wanted to use something which immediately made it clear to me that all I had to do on a regular basis was push a new markdown file and wipe my hands clean.

The theme I chose to use was [Cupper](https://cupper-hugo-theme.netlify.app/), as it seemed clean, had a dark-mode alternative, and its layout was a style which I'd try to create if tasked with creating one from scratch.

Hosting on Github was a default choice, as it's where I already keep my personal code repositories. I wanted to get practice in using Github Actions as well; the requirement to build the static site upon `push` was a straight-forward task to accomplish.

I'm building this on a browser-based instance of VSCode ([Code-Server](https://github.com/cdr/code-server)) within a Docker Container. Stretching my experience in exposing container ports to a local system and then forwarding those out to my client on the same network was a rigorous practice on its own which deserves its own post.

## Requirements
- [Install Git](https://github.com/git-guides/install-git)
- [Install Go](https://golang.org/doc/install)
- [Install Hugo](https://gohugo.io/getting-started/quick-start/)


## Still TODO
While I'm pleased with the structure of my website for now, there are still changes I'd like to approach in the future. Some may require monkeywrenching hardcoded details from the Cupper Hugo Theme; I'll link to update/change notes here as new tasks completed.

- ~~Include social media tags in the menu bar.~~
- ~~Move the darkmode toggle to the side menu~~ with a smaller button.
- Search bar on the Resources page.
- Change the `post` page to `posts`.
- Add dates/~~descriptions~~ to the post list.
- ~~Remove Disqus support entirely.~~
- ~~Include Hypothes.is support.~~