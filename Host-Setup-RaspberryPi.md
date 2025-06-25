
# 🚀 Raspberry Pi Hosting Setup for FlaskPyProject (Docker-Based)

This guide explains how to set up a Raspberry Pi to host the [FlaskPyProject](https://github.com/CuteeKim/FlaskPyProject) using Docker.

---

## 📋 Requirements

- A Raspberry Pi with Raspberry Pi OS (Lite version recommended)
- SSH access (e.g. `ssh pi@raspberrypi.local`)
- Internet connection
- `git` installed
- Docker & Docker Compose installed

---

## 🔌 Step 1: Prepare the Raspberry Pi

### Update the system:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🐳 Step 2: Install Docker and Docker Compose

### Install Docker:

```bash
curl -sSL https://get.docker.com | sh
```

Then add your user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

> 🔁 Log out and back in, or reboot your Pi:

```bash
sudo reboot
```

### Install Docker Compose:

```bash
sudo apt install docker-compose -y
```

---

## 📦 Step 3: Clone the Project

```bash
cd ~
git clone https://github.com/CuteeKim/FlaskPyProject.git
cd FlaskPyProject
```

---

## ⚙️ Step 4: Build and Run the Docker Container

### ✅ Important: Verify the main entry point

Make sure the `Dockerfile` is set to run `index.py` (not `main.py`):

```dockerfile
CMD ["python", "index.py"]
```

> If you're using a `docker-compose.yml`, make sure the same command is reflected there.

### Build and start the container:

```bash
docker compose up -d --build
```

---

## 🌐 Step 5: Access the Web App

Open your browser and go to:

```
http://<YOUR_PI_IP>:5000
```

For example:

```
http://192.168.1.42:5000
```

---

## 🛠 Useful Commands

| Task                        | Command                                   |
|-----------------------------|--------------------------------------------|
| Show container logs         | `docker logs flaskpyproject-flaskapp-1`    |
| List running containers     | `docker ps`                                |
| Stop containers             | `docker compose down`                      |
| Rebuild and restart         | `docker compose up -d --build`            |

---

## ✅ Tested With

- Raspberry Pi 4 Model B
- Raspberry Pi OS Lite (Bookworm)
- Python 3.11
- Docker 24.x
- Flask 3.x

---

## 🧠 Notes

- Flask runs on port `5000` by default.
- Ensure `index.py` is located at `/app/index.py` inside the container.
- If you modify the code, rebuild the container to apply changes:

```bash
docker compose up -d --build
```

---

## 👨‍💻 Author

[github.com/CuteeKim](https://github.com/CuteeKim)
