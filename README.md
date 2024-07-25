# auto-website-ai

This is a GPT4 Vision API and Puppeteer powered tool that can crawl into Persons google account  and can answer from attached PDF with new unread emails and also cananswer based on screenshot.

## Setup

```code 
git clone git clone https://github.com/maximiliangarmatsch/auto-website-ai.git
cd auto-website-ai
npm install
```
## create .env
```
OPENAI_API_KEY = "Your OpenAI API key here"
PHONE = "Your Phone number for Google 2FA"
EMAIL = "Google Account Gmail"
PASSWORD = "Google Account Passowrd" 
BITWARDEN_EMAIL = "Your email"
BITWARDEN_PASSWORD = "Your bitwarden master password"
```

### Run Gmail Automation Bot
```shell
$ node index.js
```

### Gernal Website automation

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