# auto-website-ai

This is a GPT4 Vision API and Puppeteer powered tool that can crawl into Persons google account  and can answer from attached PDF with new unread emails and also cananswer based on screenshot.

## Setup

```code 
git clone git clone https://github.com/maximiliangarmatsch/auto-website-ai.git
cd auto-website-ai
npm install
cat requirements.txt | xargs npm install -g
```
## create .env
```
OPENAI_API_KEY = "Your OpenAI API key here"
PHONE = "Your Phone number for Google 2FA"
EMAIL = "Google Account Gmail"
PASSWORD = "Google Account Passowrd" 

```

### Gmail Automation
```shell
$ node index.js
```

### Gernal Website automation

```shell
$ node vision_crawl.js
```
## Gmail Examples

You can ask stuff like this,
1. Vision based crawling & response.
```
Go to the URL and tell me the number of sent emails  URL:https://accounts.google.com/AccountChooser?service=mail&continue=https://google.com&hl=en
```

2. Open Unread Emails and reponse from attached emails.
```
Go to the URL and give me the summary of attached PDF  URL:https://accounts.google.com/AccountChooser?service=mail&continue=https://google.com&hl=en. Action:email
```

## General Website Examples.

```
Go to the URL and give me the Public Holidays list URL: https://mukabbirnew.pixelpk.com/. If ask for login Email: Your Email Here and Password: Your password here.
```