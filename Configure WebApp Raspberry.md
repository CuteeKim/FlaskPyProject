
## Sample configuration (adjust to local network)

```ini
interface eth0
static ip_address=192.168.178.50/24
static routers=192.168.178.1
static domain_name_servers=192.168.178.1
```
## Apply settings:

```bash
sudo reboot
2. Create Local Users
User "willi" (no admin privileges):
```
```bash
sudo adduser willi
User "fernzugriff" (for SSH access, with sudo):
```
```bash
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff
```
## 3. Enable SSH for Remote Administration
Enable and start SSH:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
Test from another device:
```
```bash
ssh fernzugriff@192.168.178.50
```
## 4. Install Docker and Docker Compose
Install Docker:
```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker fernzugriff
Reboot or logout required for group change to take effect.
```
## Install Docker Compose:
```bash
sudo apt-get install -y python3-pip
sudo pip3 install docker-compose
5. Prepare Project Directory
Install Git and clone the repository:
```
```bash
sudo apt install git -y
git clone <REPO_URL>
cd <REPO_DIRECTORY>
```
## 6. Deploy the Web Application (Todo List Management)
Sample docker-compose.yml:
```yaml
version: "3"
services:
  todoapp:
    build: .
    ports:
      - "8080:80"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```
## Start the container:
```bash
docker-compose up -d
Verify:
Access in browser: http://192.168.178.50:8080
```
## 7. Ensure Persistence After Reboot
If restart: unless-stopped is used, Docker will auto-restart the container.

Optional crontab entry for redundancy:

```bash
sudo crontab -e
Add the following line:
```
```bash
@reboot cd /path/to/project && docker-compose up -d
```
## 8. Summary
After completion:

The server has a static IP address

The web app runs inside a Docker container

Two users are created with appropriate privileges

The user "fernzugriff" can manage the server via SSH

All changes persist after a reboot

Notes
Replace <REPO_URL> and project paths accordingly. The repository must include:

OpenAPI specification

Python implementation

All required files for Docker deployment

This README.md as setup documentation
