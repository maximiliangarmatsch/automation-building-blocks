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

## Setup Python, Database, Requirements

```shell
python3 -m venv venv
       OR
python -m venv venv
source venv/bin/activate
pip install -r apps/automation_crews/requirements.txt
```

### Start Discord-Server

```shell
cd apps/automation_crews

[MAC] 
python3 start_discord.py

[LINUX/Windows]
python start_discord.py

```

### Compose.io Login (in Browser)
10000 actions/month free
```shell

composio login
[login via browser]
[copy CLI key]
[paste in terminal]

```


## Run any crew with "!"command

### Assistant-Crew

```
!assistant_crew your message here
```

### Financial-Crew

```
!financial_crew your message here
```

### Dev-Crew

```
!dev_crew Project description here (Which you want to develop)
```
