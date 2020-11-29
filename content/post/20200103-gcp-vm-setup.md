---
title: GCP VM Setup for Squid Proxy and SFTP
date: 2020-01-03
tags: 
    - gcp
    - sftp
    - squid
    - how-to
draft: false
---

Assuming the user has already opened a GCP Account and enabled billing...

The goal of this tutorial is to create a server which will be responsive to external HTTP requests for the purpose of serving external users a FTP server to drop files, or operate as an authenticated proxy.

Open Compute Engine > VM Instances. Createa new Instance. (NOTE. If you would like to create a template from which more instances can be made, perform the following steps from `Instance Templates`.)

1. Name your VM/Instance/Template as you like.
2. Select your pertinent Region.
3. Select your machine.
    - Our recommendation is the cheapest/free option: Series N1, Machine f1-micro.
    - Not much RAM is required for SFTP or proxies.
4. Select your OS
    - To follow along with the following tutorials, we chose the CentOS 8 Boot Image.
5. Check both options within `Firewall`:
    - Allow HTTP traffic.
    - Allow HTTPS traffic.
6. In the drop down, select  `Networking` and enter the following into `Network tags`:
    - http-server
    - https-sever
7. Hit the `Create` button at the bottom.
8. If you have opted to create a template first, enter `VM Instances` and create a VM from your new template.
___
Setting up a Static IP:

Navigate to `VPC Network` > `External IP addresses`. Find you newly created VM and under `Type`, select `Static`. The `External IP Address` shown in the table will be the way we communicate with this VM from now on.