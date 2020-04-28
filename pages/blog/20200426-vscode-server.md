title: VSCode on the Cloud
date: 2020-04-26
hero:
description: Run VSCode on an external server
tags:
    - How-to
    - VSCode
    - IDE
    - Cloud

### Goal
Using Google Cloud Platform, host an instance of VSCode to access via the browser for ~$25-$50/month.
More specifically, we'll be hosting an instance of [Code-Server](https://github.com/cdr/code-server) on GCP in a constantly-running VM.

This works as an alternative to the cloud-development environments which may limit the developer in some way:
- Number of private repositories
- Working Hours in a given period
- Number of projects
- Repository integration.

### Requirements
This tutorial assumes you have already set up a GCP account and enabled billing.

### Short Description:
- Make GCP VM
- Install Code-Server.
- Set up SSL Certificate via Certbot.
- Write start-up script, scheduled by Crontab.
- Associate with a subomain.

### How To
Head over to GCP and create your VM (GCP > GCE > Create VM). Design your instance as you'd like. My preference is for E2 (2 Cores, 4GB RAM) running Debian 10 Buster with 10GB storage. This set-up costs ~$25/month at the time of writing. Note that E2 cores are not entirely reserved, hence the cheaper price. In my case, this is a personal development machine. This said, I have not experienced any signs of poorer performance. Run an N1/N2 machine to reserve your cores at a higher cost (~$50/month). Finally, make sure to enable HTTP/HTTPS access.

Press "Create Instance" and wait for it to finish building. Once complete, press the SSH button.

Copy and paste the following to update and install any dependencies we'll be needing shortly.

`sudo apt update && sudo apt upgrade && sudo apt -y install wget curl certbot screen`

A note on the dependencies we're installing:
- `wget`: A common HTTP/HTTPS/FTP client for retriving data from servers.
- `curl`: Another client for communicating with servers, for a larger number of protocols.
- `certbot`: A tool for retreiving SSL certificates; only necessary if you intend to connect to your VM over HTTPS.
- `screen`: Tool for running orphaned programs, in that they are not tethered to any specific terminal instance.

Use the following bash commands to download the lastest release of VSCode for the browser (hosted on coder/code-server) and extract it to your VM's home directory. Feel free to copy/paste the whole script:

```bash
curl -s https://api.github.com/repos/cdr/code-server/releases/latest | grep "browser_download_url" | grep "linux-x86_64" | cut -d '"' -f4 | wget -qi - -O code-server.tar.gz && mkdir code-server && tar -xzf code-server.tar.gz -C code-server --strip-components 1 && rm code-server.tar.gz
```

Let's pick it apart, piece by piece:
- `curl -s https://api.github.com/repos/cdr/code-server/releases/latest`: Make a request for the url provided without providing any output. (The URL provided is the permalink to the latest releases made for the project hosting the software we're isntalling on our VM.)
- `grep "browser_download_url"`: given the response from above, seek out lines which contain the given string.
- `grep "linux-x86_64"`: given the response from above, seek out lines which contain the given string.
- `cut -d '"' -f4`: split the response from above, using `"` as a delimiter. Return the 4th field after splitting.
- `wget -qi - -O code-server.tar.gz`: given the response from above, make a request for the url and rename it. Do this without providing output.
- `mkdir code-server`: make a new folder called "code-server"
- `tar -xzf code-server.tar.gz -C code-server --strip-components 1`: extract the contents of the last file we downloaded into the folder we just made.
- `rm code-server.tar.gz`: delete the compressed file since we've extracted its contents.

For extra notes on the connectors between each command, see this [Stack Overflow](https://unix.stackexchange.com/questions/159489/is-there-a-difference-between-and-and) Q/A.

Optionally, if you'd like to access the server via HTTPS (and if you're planning on accessing this VM through a URL, you'd most likely be in this pool) install and execute certbot: `sudo certbot certonly --standalone`. [Certbot](https://certbot.eff.org/) is a tool provided by the EFF to make handling SSL certificates fast and easy.  They'll take your email address to contact you should there be an emergency regarding access to your machine, but beyond this, consider them your cosigner to prove legitimacy. Take note of where the SSL certificate and key are saved. We'll need them later.

Now let's create a script to execute code-server. Using your favorite code editor, create a file called `run-code-server.sh` and start editing:

```bash
#!/bin/bash
while true
do

sudo PASSWORD=yOur_Pa55w0rd \
        ./code-server/code-server \
                --auth password \
                --port 443 \
                --cert "/etc/your/path/to/cert/fullchain.pem" \
                --cert-key "/etc/your/path/to/certkey/privkey.pem"
sleep 3
done
```

Note the following:
- Code-Server allows the user to set up a password for accessing their coding environment. Provide a custom one by declaring the `PASSWORD` variable on the same line.
- `--port 443`: this is the default port which HTTPS requests use. IF you plan on using a clean URL to access your VM and have no intentions to set up a reverse proxy of some kind, this is necessary. Otherwise, feel free to set it to something else, and navigate to it via `yourwebsite.com:PORT` or `12.34.56.78:PORT`. Take note of your selection, as it will be needed later.
- `--cert "/etc/path..."`: if you have an SSL certificate to provide, enter the path here.
- `--cert-key "/etc/path..."`: if you have an SSL certificate to provide, enter the path here.

Start Crontab to schedule your script to execute upon start-up: `crontab -e`. If this is your first time opening crontab, it will ask you to select a preferred editor, which can be changed at any time. Once inside your crontab file, add the following line: `@reboot screen -m -d sh $HOME/run-code-server.sh`. Save and exit.

Close the SSH terminal and navigate to (GCP > VPC Network > Firewall Rules > Create a new Firewall Rule) to create a new firewall setting. Name it whatever you like and set a priority ~1000. Add your port to the TCP port section. Should you be running applications on extra ports on this VM, it may be worthwhile to add a few others: 8080, 8888, 8443, or whatever is preferred to you.

Navigate to (GCP > VPC Network > External IP Addresses) and find the VM you recently created; under the `Type` column, change the value from "Ephemeral" to "Static". This will keep your external IP address constant, and ease access to it. Take note of this IP address for later.

Restart your VM.

Optionally make your VM accessible through the web via a custom domain which you may already have by performing the following:
- Navigate to your domain admin dashboard
- Add a new Custom resource record
- Type: A
- Name: the subdomain you'd prefer to use for your development VM (if any).
- Data/IP Address: the static IP address of your VM.

Save your settings and wait. It may take a few minutes/hours for your domain to be set up.

This should be all it takes to get your own, custom cloud-hosted development environment up and running for about the price of any other unlimited cloud-dev env!

Navigate to your dev env using:
- Your external IP and port: `12.34.56.78:PORT`.
- Your custom domain and port (with cert): `https://subdomain.yourdomain.com:PORT`
- Your custom domain and port (without cert): `http://subdomain.yourdomain.com:PORT`
- Your custom domain, assuming port 443 (with cert): `http://subdomain.yourdomain.com`

### References and Resources

Note that there are plenty of alternative softwares for a few of these services:

##### Cloud Based IDEs
- [Code-Server](https://github.com/cdr/code-server)
- [SSH-Code](https://github.com/cdr/sshcode)
- [Theia Ecplise](https://theia-ide.org/)

##### Containerized Solutions
- [Code-Server](https://hub.docker.com/r/codercom/code-server)
- [Linux-Server](https://hub.docker.com/r/linuxserver/code-server)

##### Cloud Based Development as a Service
- [Gitpod](https://www.gitpod.io/)
- [Stackblitz](https://stackblitz.com/)
- [CodeSandbox](https://codesandbox.io/)

##### GCP Shell Options
- [Google Cloud Shell](https://cloud.google.com/shell)