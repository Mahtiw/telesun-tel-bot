Installation Guide for Telegram Bot with Docker

## 1. Installing Docker and Docker Compose

### Installing Docker
To install Docker, run the following commands:

```bash
sudo apt update
sudo apt install docker.io
```

To verify Docker is installed correctly:

```bash
sudo docker --version
```

### Installing Docker Compose
To install Docker Compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

To verify the installation:

```bash
docker-compose --version
```

## 2. Cloning the Project from GitHub
To download the project from GitHub, clone it using the following:

```bash
git clone https://github.com/Mahtiw/telesun-tel-bot.git
cd telesun-tel-bot
```

## 3. Entering Bot Token and Panel Addresses
Configure these settings in the `login.py` file.

### Editing the `login.py` File
To edit `login.py`, you can use various text editors. Here are some common methods:

#### 1. Editing with `nano` (Linux)
If you’re on a Linux server, enter:

```bash
nano login.py
```

After editing, press `CTRL + O` to save changes, `Enter` to confirm, and `CTRL + X` to exit.

#### 2. Editing with `vim` (Linux)
If `vim` is installed, you can use:

```bash
vim login.py
```

Press `i` to enter edit mode. After editing, press `ESC`, type `:wq`, and hit `Enter` to save and exit.

#### 3. Editing with Notepad (Windows)
If the file is on your Windows system, you can use Notepad or another text editor:
- Open `login.py`.
- Make necessary edits and save.

**Note:** After editing, make sure to upload the updated file back to the server.

### Setting the Bot Token
In `login.py`, replace `'YOUR_BOT_TOKEN_HERE'` with your actual bot token:

```python
# Bot token
TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

### Configuring Panel Information
Update the panel URLs and login credentials as follows:

```python
# Panel information
panels = [
    {"url": "http://s1.example.com:1111/", "username": "user1", "password": "admin1"},
    {"url": "http://s1.example.com:2222/", "username": "user2", "password": "admin2"},
    {"url": "http://s1.example.com:3333/", "username": "user3", "password": "admin3"},
]
```

Where:
- `url`: Panel URL
- `username`: Panel username
- `password`: Panel password

## 4. Running Docker Compose
To start the bot with Docker Compose, run:

```bash
docker-compose up -d
```

This command launches all necessary services and runs the bot in the background.

## 5. Checking Container Status
To view running containers, use:

```bash
docker ps
```

This displays a list of active containers.

## 6. Stopping or Restarting Containers
To stop running containers:

```bash
docker-compose down
```

To restart containers:

```bash
docker-compose up -d
```

## Additional Notes
- If your server restarts, Docker Compose will automatically bring up the bot again.
- Ensure the bot token and panel information are configured correctly for proper operation.
