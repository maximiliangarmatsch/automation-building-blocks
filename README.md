# auto-website-ai

This is a GPT4 Vision API and Puppeteer powered tool that can crawl into Persons google account  and can answer from attached PDF with new unread emails and also cananswer based on screenshot.

## Pre-Setup
brew install python (newest version) 3.1.0

## Setup

```shell
git clone git clone https://github.com/maximiliangarmatsch/auto-website-ai.git
cd auto-website-ai
npm install
pip install pdfminer pdfminer.six python-dotenv undetected_chromedriver python-xlib openai undetected-chromedriver discord.py
create .env (ask Amir)
```

### Start "Python App"
```shell
python app.py

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