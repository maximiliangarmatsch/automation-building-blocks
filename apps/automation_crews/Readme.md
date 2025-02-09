## Tools & functions

- GPT4 Vision API
- Gemini vision API
- Puppeteer
- CrewAI
- Discord
- `GPTdiscord`: Integrates GPT into Discord
- `financial_crew`: Conduct financial research
- `personal_assistant_crew`: Automate tasks like updating gCalendar and gSheet events or sending emails
- `dev_crew`: Multi-agnets based Web/App dvelopment tool

## Use Cases

- Access user accounts using Password manager Like.  
- Manage emails and Create drafts.  
- Conduct Financial research  
- Create Website or app complete code base  
- Perform any task on gSheet, gCalender.  
  - Insert or delete data in gSheet  
  - Create Salary Slip or financial reports
  - Monthly summary report from gSheet   
  - Send salary slip or financial report via Gmail attachment  
  - Create, Update, Delete gCalender event  

## Install Python

Install Python (newest version, currently 3.11.0, ~Nov 2024)

- https://www.python.org/downloads/


## (MacOS Only) Pre-Setup

```shell
#General Fixes:
export HNSWLIB_NO_NATIVE=1

#For Certificates
/Applications/Python\ 3.12/Install\ Certificates.command
pip install --upgrade certifi

#For pyAutoGui
brew install --cask xquartz
```


## Create .apps/automations_crews/.env file
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
CHANNEL_ID = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
GROQ_API_KEY = ""
HISTORYLENGTH=12
CHANNEL_IDS=1233073621849866352 //Garmatsch-Server: "ai-testing"
REGISTERED_CHANNEL_IDS = [1233073621849866352] //Garmatsch-Server: "ai-testing"
MAX_TOKENS=5000
MAX_TOKENS_RANDOM=100
MODEL_CHAT=gpt-4o-mini

## Setup Python, Database, Requirements

```shell
python3 -m venv venv
       OR
python -m venv venv
source venv/bin/activate
pip install -r apps/automation_crews/requirements.txt
```


### Login to Compose.io (in Browser)
10000 actions/month free
```shell

composio login
[login via browser]
[copy CLI key]
[paste in terminal]
composio add googlesheets

```

### Start Discord-Server

```shell
cd apps/automation_crews

[MAC] 
python3 start_discord.py

[LINUX/Windows]
python start_discord.py

```


## Run Assistant-Crew

```
!assistant_crew your message here
```

## Run Financial-Crew

```
!financial_crew your message here
```

## Run Dev-Crew

```
!dev_crew Project description here (Which you want to develop)
```
## 1. GPTdiscord bot

### Setup

```shell
pip install -r apps/automation_crews/requirements.txt
```
Create .env inside automation-building-blocks and put secrets below
```shell
OPENAI_API_KEY = ""
DISCORD_TOKEN = ""
HISTORYLENGTH=12
CHANNEL_IDS=1233073621849866352, 1245390947395698711 
REGISTERED_CHANNEL_IDS = [1233073621849866352, 1245390947395698711]
MAX_TOKENS=5000
MAX_TOKENS_RANDOM=100
MODEL_CHAT=gpt-4o-mini
```

### Naviagte to project directory

```shell
cd apps
cd automation_crews
```
### Run the python script
```shell
python start_discord.py
```
### Text generation 

```
!gpt your message here
```

### Image analysis or insights

```
!analyze your message here
```

### Image generation

```
!generate Image details
```
**Note**
Image generation use dalle-3 which cost around $0.04 per image.  

### Refresh chat history

```
!refresh 
```
## 2. ProActiveDiscord Bot

A Discord bot that creates custom invite links and sends personalized welcome messages to new members when they join using those links.

### Features

- Creates single-use invite links with custom user data
- Tracks invite usage
- Sends personalized welcome messages
- REST API endpoint for invite generation

### Prerequisites

- Python 3.10+
- Discord Bot Token
- Discord Developer Portal Access

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install discord.py flask python-dotenv quart_cors quart
```
3. Create a `.env` file:
```env
DISCORD_TOKEN=your_bot_token_here
```

### Discord Developer configuration

1. Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable required intents:
   - Server Members Intent
   - Message Content Intent
   - Presence Intent
3. Invite bot to your server with required permissions:
   - Manage Server
   - Create Instant Invite
   - Send Messages
   - View Channels

### Usage

1. Start the bot:
```bash
python flask_discord_server.py.py
```

2. Generate invite via API:
```bash
curl -X POST http://localhost:5000/join-discord \
  -H "Content-Type: application/json" \
  -d '{"username": "user123", "server_name": "Your Server", "channel_name": "general", "user_id": "123"}'
```

### API Endpoint

`POST /join-discord`
```json
{
  "username": "string",
  "server_name": "string",
  "channel_name": "string",
  "user_id": "string"
}
```
## 3. Personal Assistant Crew

### Run the Setup File

Linux or macOS

```shell
chmod +x setup.sh
```
Windows

```shell
./setup.sh
```

### Update ./.env file

```
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
CHANNEL_ID = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
MODEL = gpt-4o-mini
```
### Run the python script
```shell
python run_crew.py
```

## 4. Financial Crew

### /.env file

```
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
CHANNEL_ID = ""
DISCORD_TOKEN = ""
MODEL = gpt-4o-mini
```

```shell
python3 ./apps/automation_crews/financial_crew/run_crew.py
      OR
python ./apps/automation_crews/financial_crew/run_crew.py

```
### 5. Dev Crew
```shell
source venv/bin/activate
cd apps/automation_crews/dev_crew
python app.py
```
Example prompt "an ecommerce website for drawings"
- Output directory is in `apps/automation_crews/dev_crew/generated_src`
- `allow_code_excecution` is activated in file "...". It allows crewAI to "test" code on the fly
