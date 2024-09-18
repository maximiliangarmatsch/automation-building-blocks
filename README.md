# Automation Building Blocks

## Tools & functions

- GPT4 Vision API
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
pip install -r requirements.txt
```

### Create ./.env file

```
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
CHANNEL_ID = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
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
python3 ./src/financial_crew/run_crew.py
      OR
python ./src/financial_crew/run_crew.py

```

### Start "Website automation" with Puppetee

```shell
npm install
node ./utils/vision_crew_ai.js
```

## Other

### Stop "venv"

```shell
$ deactivate
```

### Start Only "Dev Crew"
```shell
source venv/bin/activate
cd src/dev_crew
python app.py
```
Example prompt "an ecommerce website for drawings"
- Output directory is in `src/dev_crew/generated_src`
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

## See /docs for more
