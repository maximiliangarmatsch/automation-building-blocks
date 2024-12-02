# Automation Building Blocks

## Tools & functions

- GPT4 Vision API
- Gemini vision API
- Puppeteer

## Use Cases

- Crawl google accounts
- Read unread emails and attached PDFs
- Respond based on screenshot

## Pre-Setup

Install Python (newest version, currently 3.11.0)

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

## Setup for Python

```shell
python3 -m venv venv
       OR
python -m venv venv
source venv/bin/activate
pip install -r apps/automation_crews/requirements.txt
```

### Create ./.env file

```
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
CHANNEL_ID = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
GROQ_API_KEY = ""
```
```

### Start "Python App"

```shell
python3 start_discord.py
      OR
python start_discord.py

```

## Steps to Run any crew with "!"command

### 1. Navigate to the Project Directory

Change to the to automation_crews:
```shell
cd apps/automation_crews
```

### 2. Run the python script
```shell
python start_discord.py
```
### 3. Ask to assitant crew from discord

```
!assistant_crew your message here
```

### 4. Ask to financial crew from discord

```
!financial_crew your message here
```

### 5. Connect to dev_crew for development support

```
!dev_crew Project description here (Which you want to develop)
```
## See /docs for more
