## Tools & functions

- GPT4 Vision API
- Gemini vision API
- Puppeteer
- CrewAI
- Discord
- `GPTdiscord`: Integrates GPT into Discord
- `finance_crew`: Conduct financial research
- `invoice_crew`: Update fields in gSheet and trigger gSheet-Script
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


## Create .env file in .apps/automations_crews
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
GROQ_API_KEY = ""
HISTORYLENGTH=12
REGISTERED_CHANNEL_IDS = [1233073621849866352] //Garmatsch-Server: "ai-testing"-Channel
MAX_TOKENS=5000
MAX_TOKENS_RANDOM=100
MODEL_CHAT=gpt-4o-mini

## Install Python Requirements

```shell
python3 -m venv venv
       OR
python -m venv venv
source venv/bin/activate
pip install -r apps/crewcord/requirements.txt
```


## Login to Compose.io (in Browser)
10000 actions/month free
```shell

composio login
[login via browser]
[copy CLI key]
[paste in terminal]
composio add googlesheets

```

## Start Discord-Server locally

```shell
cd apps/crewcord

[MAC] 
python3 start_discord.py

[LINUX/Windows]
python start_discord.py

```


## Run Invoice-Crew from Discord

```
!invoice_crew YOUR_MESSAGE
```

## Run Finance-Crew from Discord

```
!finance_crew YOUR_MESSAGE
```

## Run Dev-Crew from Discord 

```
!dev_crew PROJECT_DESCRIPTION (Which you want developed)
Example PROJECT_DESCRIPTION: !dev_crew "An ecommerce website for drawings"

```


## Usages

### Text generation 
```
!gpt your message here
```

### Image analysis or insights
```
!analyze your message here
```

### Image generation (Uses dalle-3, ~$0.04 per image)
```
!generate Image details
```

### Refresh chat history
```
!refresh 
```


## Run Crews individually 
### 1. Personal Assistant Crew (and Setup Composio)
```shell
cd ./apps/crewcord

[Linux or macOS]
chmod +x setup_composio.sh

[Windows]
./setup_composio.sh

//TODO IS THIS CORRECT?
python run_crew.py 
```


### 2. Finance Crew
```shell
cd ./apps/crewcord/finance_crew
python3 run_crew.py
      OR
python run_crew.py

```


### 3. Dev Crew
```shell
cd apps/crewcord/dev_crew
python app.py
```
Example prompt "an ecommerce website for drawings"
- Output directory is in `apps/crewcord/dev_crew/generated_src`
- `allow_code_excecution` is activated in file "...". It allows crewAI to "test" code on the fly


# Other notes

1. pytest: excluded folder:
  --ignore=apps/dev_crew --ignore=apps/crewcord --ignore=tests