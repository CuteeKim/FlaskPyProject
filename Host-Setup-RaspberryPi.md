
# Raspberry Pi Web App Deployment: Todo List API

This documentation describes how to fully configure a Raspberry Pi with Raspberry Pi OS (Debian-based Linux) to host the **FlaskPyProject Todo List API** using Docker. The goal is to enable reproducible setup from a clean operating system image via command-line configuration only.

---

## 📦 Requirements Overview

The Raspberry Pi server must meet the following requirements:

- Static IP address in the local network
- Two local users:
  - `willi`: normal user without sudo rights
  - `fernzugriff`: SSH user with administrative rights
- SSH access enabled for `fernzugriff`
- Web application deployed using Docker (containerized)
- All settings must persist after reboot
- Full configuration performed via the terminal

---

## 🧰 Prerequisites

- A Raspberry Pi (recommended: Raspberry Pi 3 or later)
- A clean installation of **Raspberry Pi OS Lite (64-bit)**
- Monitor, keyboard, or headless SSH setup
- Internet connection for package installation

---

## 🔌 Step 1: Set Static IP Address

Edit the DHCP configuration:

```bash
sudo nano /etc/dhcpcd.conf
```

At the bottom, add the following configuration (adjust IP/subnet/gateway as needed):

```ini
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
```

Then restart networking:

```bash
sudo systemctl restart dhcpcd
```

Confirm with:

```bash
ip a
```

---

## 👤 Step 2: Add Local Users

### Create normal user \`willi\`:

```bash
sudo adduser willi
```

Press Enter to skip optional fields.

### Create \`fernzugriff\` with sudo privileges:

```bash
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff
```

---

## 🔐 Step 3: Enable SSH Access

Enable SSH service:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

Optionally, change SSH port or other settings:

```bash
sudo nano /etc/ssh/sshd_config
```

Allow SSH login for \`fernzugriff\` only:

```
AllowUsers fernzugriff
```

Then restart SSH:

```bash
sudo systemctl restart ssh
```

You can now log in remotely:

```bash
ssh fernzugriff@192.168.1.100
```

---

## 🐳 Step 4: Install Docker & Docker Compose

Install Docker:

```bash
curl -sSL https://get.docker.com | sh
```

Add user to Docker group:

```bash
sudo usermod -aG docker fernzugriff
```

Reboot (to apply group changes):

```bash
sudo reboot
```

Install Docker Compose:

```bash
sudo apt update
sudo apt install -y docker-compose
```

---

## 📁 Step 5: Clone and Deploy the Web App

Log in as \`fernzugriff\` via SSH or terminal, then run:

```bash
mkdir ~/todo-app
cd ~/todo-app
git clone https://github.com/CuteeKim/FlaskPyProject.git
cd FlaskPyProject
```

Ensure that the [entrypoint file](https://github.com/CuteeKim/FlaskPyProject/blob/main/Dockerfile) file is correctly named (e.g. \`index.py\`):
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY src/ /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "index.py"]
```

Make sure [docker-compose.yml](https://github.com/CuteeKim/FlaskPyProject/blob/main/docker-compose.yml) looks like this:

```yaml
version: "3"
services:
  flaskapp:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    restart: unless-stopped
```

Now deploy with:

```bash
docker compose up -d --build
```

Verify that the container is running:

```bash
docker ps
```

The Flask API should now be accessible via:

```
http://192.168.1.100:5000
```

---

## 🧪 Test Persistence

Reboot the Raspberry Pi:

```bash
sudo reboot
```

After reboot, confirm the container auto-started:

```bash
docker ps
```

Your API should still be reachable at \`http://192.168.1.100:5000\`.

---

## 📌 Notes

- This setup assumes no graphical desktop is needed.
- The repository includes all necessary files (\`[Dockerfile](https://github.com/CuteeKim/FlaskPyProject/blob/main/Dockerfile)\`, \`[requirements.txt](https://github.com/CuteeKim/FlaskPyProject/blob/main/src/requirements.txt)\`, \`[docker-compose.yml](https://github.com/CuteeKim/FlaskPyProject/blob/main/docker-compose.yml)\`, and \`[index.py](https://github.com/CuteeKim/FlaskPyProject/blob/main/src/index.py)\`).
- Your Flask application listens on port \`5000\` inside the container.
- SSH access is locked to the \`fernzugriff\` user.
- All settings (static IP, SSH, Docker containers) are persistent after reboot.

---

## ✅ Final Checklist

- [x] Static IP configured
- [x] \`willi\` and \`fernzugriff\` users created
- [x] SSH restricted and enabled
- [x] Docker + Compose installed
- [x] Flask app containerized and deployed
- [x] All settings survive reboot

---

## 📚 Author

Project by [CuteeKim](https://github.com/CuteeKim)  
Deployment guide written for reproducibility and evaluation purposes.
