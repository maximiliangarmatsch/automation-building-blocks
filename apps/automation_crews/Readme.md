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
