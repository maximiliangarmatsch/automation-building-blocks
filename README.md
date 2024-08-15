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
### create .env
Create two .envs in main project folder and inside financial_crew

In project main folder
```
OPENAI_API_KEY = ""
CHANNEL_ID = ""
BITWARDEN_EMAIL = ""
BITWARDEN_PASSWORD = ""
DISCORD_TOKEN = ""
```
In financial crew folder
```
OPENAI_API_KEY = ""
SERPAPI_API_KEY = ""
```
### Start "Python App"

```shell
python3 app.py
      OR
python app.py

```

## Setup for Javascript

```shell
npm install
```

### Start "Website automation"

```shell
$ node ./utils/vision_crew_ai.js
```

### See /docs for more
