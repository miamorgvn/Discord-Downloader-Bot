# Ichimiwa Bot - Universal Discord Downloader & Utility Bot

A versatile Python-based Discord bot designed to manage server greetings and automatically detect, fetch, and download media (videos/photos) from various major social media platforms directly into Discord chat channels. 

The official repository for this project can be accessed at [GitHub - miamorgvn/Ichimiwa-Bot](https://github.com/miamorgvn/Ichimiwa-Bot.git).

## 🚀 Key Features

* **Multi-Platform Support**: Download video and media content from popular platforms (Instagram, TikTok, YouTube Shorts, Twitter/X, etc.).
* **Universal Link Parser**: Smart system that automatically detects media links in chat without needing manual commands.
* **Large File Handling**: Built to process and support high-quality video downloads of **up to 500MB** efficiently.
* **Welcome & Goodbye System**: Automatically greets new members upon joining and sends a departure message when they leave the server.
* **Session & Cookie Management**: Uses local session file management to bypass platform encryption limits and securely download private content.
* **Secure Environment**: Protects sensitive credentials using environment variable encapsulation (`.env`).

## 🛠️ Tech Stack

* **Programming Language**: Python
* **Main Libraries**: Discord.py, Python-dotenv, Requests, Yt-dlp
* **Version Control**: Git & GitHub

## ⚙️ Installation Guide

### Prerequisites

Before setting up the bot, you **MUST** install Python and the necessary system packages for your specific platform.

#### For Termux:
```bash
pkg update && pkg upgrade -y
pkg install python git clang libjpeg-turbo -y
```

#### For Debian/Ubuntu:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git clang -y
```

---

### Step-by-Step Setup (Termux Example)

#### 1. Clone the Repository
Download the bot source code to your environment. You can change `your-folder-name` at the end of the command to any short name you prefer:
```bash
git clone https://github.com/miamorgvn/Ichimiwa-Bot.git your-folder-name
cd your-folder-name
```

#### 2. Install Dependencies
*(Make sure Python is installed from the Prerequisites section before running this command)*  
Install all required Python libraries at once:
```bash
pip install -r requirements.txt
```

#### 3. Set Up Access Token
Create a secure `.env` file to store your Discord bot token:
```bash
nano .env
```
Paste the following text inside (replace with your actual bot token):
```text
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
```
Save and exit by pressing **CTRL + X**, then **Y**, then **Enter**.

#### 4. Run the Bot
Now the bot is ready to start. Run it using the following command:
```bash
python bot.py
```

---

## 🔄 How to Update

If you make manual changes or want to pull the latest updates into your repository, use the following commands:

### Push changes to GitHub (After editing files manually):
```bash
git add .
git commit -m "explain what you changed/updated"
git push origin main
```

### Pull latest updates from GitHub to your device:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```
