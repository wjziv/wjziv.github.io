---
title: Squid Proxy Server Setup
date: 2020-01-03
description: How to set up a Squid Proxy on Google Cloud Platform.
tags:
    - gcp
    - squid
    - how-to
---

These instructions assume you have successfully completed the following:
1. Opened a GCP account.
2. Set up a VM with a static IP address and open HTTP/HTTPS ports.

The goal of these instrctions is to create a functional proxy VM on GCP.

___
Setting up the port rules:

With you VM already created and tagged correctly, navigate to `VPC Network` > `Firewall Rules`. Here, a number of networking rules have been created. We will be editing the HTTP/S port rules.

- default-allow-http
- default-allow-https

Within both of these  rules, add `3128` to the `tcp` and `udp` port lists.

___
Setting up the VM:

Within CentOS 8, Squid comes with the basic repositories. Beyond the amount of RAM you provide your server (and therefore your users), there are no dependencies to consider. Squid is already a part of the basic Repositories which come with the OS.

Start by updating the repositories within the yum installer:
```bash
sudo yum -y update
```

Next, install and initialize Squid:
```bash
sudo yum -y install squid
sudo systemctl start squid
sudo systemctl enable squid
```

Check that the service is running with the following command:
```bash
sudo systemctl status squid
```
The result should look like this:
```bash
● squid.service - Squid caching proxy
   Loaded: loaded (/usr/lib/systemd/system/squid.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2019-12-06 17:38:04 UTC; 5min ago
 Main PID: 2062 (squid)
    Tasks: 3 (limit: 3517)
   Memory: 20.5M
   CGroup: /system.slice/squid.service
           ├─2062 /usr/sbin/squid -f /etc/squid/squid.conf
           ├─2064 (squid-1) --kid squid-1 -f /etc/squid/squid.conf
           └─2065 (logfile-daemon) /var/log/squid/access.log

Dec 06 17:38:04 alx-vm001 systemd[1]: Starting Squid caching proxy...
Dec 06 17:38:04 alx-vm001 systemd[1]: Started Squid caching proxy.
Dec 06 17:38:04 alx-vm001 squid[2062]: Squid Parent: will start 1 kids
Dec 06 17:38:04 alx-vm001 squid[2062]: Squid Parent: (squid-1) process 2064 started
```

For future reference, note the following important files and locations:

- Squid configuration file: `/etc/squid/squid.conf`
- Squid Access log: `/var/log/squid/access.log`
- Squid Cache log: `/var/log/squid/cache.log`

Technically, Squid is up and running right now! Congrats.

However, nobody is able to access it quite yet. While one may specifically allow particular IP addresses to access their proxy, we would like to autenticate using user/pass.

To enable Client Authentication, install httpd-tools:
```bash
sudo yum -y install httpd-tools
```

And create a place to store user credentials, allow Squid's default username to access/own this file:
```bash
sudo touch /etc/squid/passwd
sudo chown squid: /etc/squid/passwd
```

Now create your first user (here, it's called `proxyusername`):
```bash
sudo htpasswd /etc/squid/passwd proxyusername

New password:
Re-type new password:
Adding password for user proxyusername
```
Now that a user/password account is created, let Squid know this iswhat it should be looking for in a user. Open the config file and add the following:
```bash
sudo vim /etc/squid/squid.conf
```
When adding items to the config file, locate the line: 
`INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS`

Add the following beneath any ACL permissions you've created.
```bash
## Enable Client Authenication
## These definitions require authentication every 2 hours per user.
## There are 100 active authenticators.
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 100
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users

## Allow more than one user to access the proxy
## provided the same credentials, simultaneously.
authenticate_ip_ttl 3 seconds # Remember the user's IP address for 3s
acl max_user max_user_ip -s 10000 # Allow 10000 distinct IP addresses to one account.
```

Finally, restart Squid.
```bash
sudo systemctl restart squid
sudo service squid restart
```

Finally, to use your new proxy service:
```python
import requests
proxies = {
    'http':f'http://{user}:{passwd}@{static_ip}:3128',
    'https':f'https://{user}:{passwd}@{static_ip}:3128'
}
requests.get(url,proxies=proxies).json()
```

Reference:

- https://www.tecmint.com/install-squid-http-proxy-on-centos-7/
___
Check usage/access:

Are you concerned that your proxy is in use by nefarious hackers?

1. Log into GCP and navigate to GCE/VMs.
2. SSH into the sftp/proxy server.
3.  `sudo vim /var/log/squid/access.log`

Ideally, the only rows which contain a "/2xx" response or evidence that they were able to log in using the "data2-proxy" username were valid requests from SellUP devices (likely GCP VMs or developers debugging a rigid ETL). If unsure, the most one may do in this scenario is lookup the public IP origin online.

References:

- http://www.squid-cache.org/Doc/config/access_log/
- https://wiki.squid-cache.org/SquidFaq/SquidLogs



Squid Guide:
https://www.tecmint.com/install-squid-http-proxy-on-centos-7/

SFTP Guides:
https://thelinuxcode.com/enable-configure-sftp-centos-7/
https://medium.com/@biancalorenpadilla/sftp-google-cloud-storage-d559fd16e074
** Note that the restrictions made in the thelinuxcode.com link are great for security.