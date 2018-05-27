##### 1. Add the following line to /etc/ssh/sshd_config (I just added it at the very end) on your remote SSH server to allow remote port forwarding:
```bash
GatewayPorts yes
```
##### 2. Save the file and apply the changes with:
```bash
sudo restart ssh
```
##### 3. On your local development machine, make sure the localhost web server is running then type the command:
```bash
ssh user@www.myremotehost.com -R 8000:localhost:8000
```
An even better command is this:
```bash
ssh user@www.myremotehost.com -nNT -o ServerAliveInterval=30 -R 8000:localhost:8000
```
