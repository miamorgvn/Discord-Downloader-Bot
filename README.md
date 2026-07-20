# IchimiwaDL - Premium Media Downloader & Server Moderator

A powerful Python-based Discord bot featuring a high-performance media downloader that bypasses standard restrictions to fetch large files, alongside essential server moderation utilities.

The official repository for this project can be accessed at [GitHub - miamorgvn/IchimiwaDL](https://github.com/miamorgvn/IchimiwaDL.git).

## 🚀 Key Features

* **Monster File Downloads (1GB+)**: Bypasses standard upload restrictions to automatically detect, fetch, and deliver large videos/media (1GB+ and any video type) straight into your chat, even for completely free Discord users.
* **Multi-Platform Support**: Seamlessly extracts high-quality video content from all major social media platforms (Instagram, TikTok, YouTube Shorts, Twitter/X, and more).
* **Universal Link Parser**: Smart automatic detection of media links inside the text channels without needing any repetitive manual trigger words.
* **Server Moderation**: Keeps your community clean and safe using optimized slash commands like `/kick`, `/ban`, and other necessary admin utilities.
* **Session & Cookie Management**: Employs locally managed session configurations to jump platform encryption blocks and download private videos safely.
* **Secure Environment**: Keeps all your important developer keys and Discord bot tokens safe inside an isolated environment variable file (`.env`).

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
pkg install python git clang -y
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
git clone https://github.com/miamorgvn/IchimiwaDL.git your-folder-name
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

--
