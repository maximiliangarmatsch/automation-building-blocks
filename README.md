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


### Start ONLY "Financial Crew"
#### Requires ./src/fincancial_crew/assets/Bank-of-America-Bank-Statement-TemplateLab.com_.pdf to exist
#### fix some imports
#### replace the keys in pyautogui.gmail

```shell
python3 ./apps/automation_crews/financial_crew/run_crew.py
      OR
python ./apps/automation_crews/financial_crew/run_crew.py

```

### Start "Website automation" with Puppeteer

```shell
npm install
cd ./apps/automation_crews
node index.js
```

## Other

### Stop "venv"

```shell
$ deactivate
```

### Start Only "Dev Crew"
```shell
source venv/bin/activate
cd apps/automation_crews/dev_crew
python app.py
```
Example prompt "an ecommerce website for drawings"
- Output directory is in `apps/automation_crews/dev_crew/generated_src`
- `allow_code_excecution` is activated in file "...". It allows crewAI to "test" code on the fly

# start Only Personal Assistant Crew

## Steps to Run
**Navigate to the Project Directory:**
Change to the directory where the `setup.sh`, `run_crew.py`, `requirements.txt` files are located. For example:
```shell
cd path/to/project/directory
```

### 1. Run the Setup File
Make the setup.sh Script Executable (if necessary):
On Linux or macOS, you might need to make the setup.sh script executable:
```shell
chmod +x setup.sh
```
Execute the setup.sh script to set up the environment, install dependencies, login to composio and 
add necessary tools:
```shell
./setup.sh
```
Now, Fill in the .env file with your secrets.

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
### 2. Run the python script
```shell
python run_crew.py
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

## Steps to Run any GPTdiscord

### 1. Setup

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

### 2. Naviagte to project directory

```shell
cd apps
cd GPTdiscord
```
### 3. Run the python script
```shell
python run_discordGPT.py
```
### 4. Text generation 

```
!gpt your message here
```

### 5. Image analysis or insights

```
!analyze your message here
```

### 6. Image generation

```
!generate Image details
```
**Note**
Image generation use dalle-3 which cost around $0.04 per image.  

### 7. Refresh chat history

```
!refresh 
```
## See /docs for more
