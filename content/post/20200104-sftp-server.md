---
title: SFTP Server Setup
date: 2020-01-04
description: How to set up a SFTP Server on Google Cloud Platform.
tags:
    - gcp
    - sftp
    - how-to
---


Assuming the user has already created a VM with a static IP address open to HTTP/S traffic...

## Creating An SFTP Account
SSH into the VM which you'd like to turn into a SFTP server.

Create a new account which you'd like to provide to users to deposit files:
```bash
sudo adduser username
sudo passwd username
```

Create the sftp directory and limit the user's access and permissions. Change the `username` appropriately:
```bash
sudo mkdir -p /var/sftp/uploads
sudo chown root:root /var/sftp
sudo chmod 755 /var/sftp
sudo chown username:username /var/sftp/uploads
```

Enable client authentication in the ssh config file:
```bash
sudo vim /etc/ssh/sshd_config
```

At the bottom, include the following, and appropriately change the `username`:
```bash
Match User username
ForceCommand internal-sftp
PasswordAuthentication yes
ChrootDirectory /var/sftp
PermitTunnel no
AllowAgentForwarding no
AllowTcpForwarding no
X11Forwarding no
```

## Restarting
Finally, reset the ssh service:
```bash
sudo systemctl restart sshd
```

Access this SFTP directory at `/uploads/` within your chosen SFTP client.

## References
As always, there's always reason to read documentation and other takes on how to do things!

- https://medium.com/@biancalorenpadilla/sftp-google-cloud-storage-d559fd16e074
- https://thelinuxcode.com/enable-configure-sftp-centos-7/

## Further Reading

More detail on allowing GROUPS of users:
- https://www.howtoforge.com/tutorial/how-to-setup-an-sftp-server-on-centos/