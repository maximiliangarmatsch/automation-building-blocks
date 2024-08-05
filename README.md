# auto-website-ai

This is a GPT4 Vision API and Puppeteer powered tool that can crawl into Persons google account  and can answer from attached PDF with new unread emails and also cananswer based on screenshot.

## Pre-Setup
Install Python (newest version, currently 3.11.0)
- https://www.python.org/downloads/

## Setupt for Python
```shell
git clone git clone https://github.com/maximiliangarmatsch/auto-website-ai.git
cd auto-website-ai
python3 -m venv venv 
       OR
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Start "Python App"
```shell
python3 app.py
      OR
python app.py

```

## Setup for Javscript 

```shell
git clone git clone https://github.com/maximiliangarmatsch/auto-website-ai.git
cd auto-website-ai
npm install
```

### Start "Website automation"

```shell
$ node ./utils/vision_crew_ai.js
```

## Gmail Examples
You can ask stuff like this,
1. Vision based crawling & response.
```
Summarize the email and PDF attachment Action:email
```

## General Website Examples.
```
Go to the URL and give me the {Your action or query} URL: Your URL. If ask for login Email: Your Email Here and Password: Your password here.
```