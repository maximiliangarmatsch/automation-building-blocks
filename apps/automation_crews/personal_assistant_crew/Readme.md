# start Only Personal Assistant Crew

## Steps to Run

```shell
cd apps/automation_crews/personal_assistant_crew
```

### 1. Run the Setup File

Linux or macOS

```shell
chmod +x setup.sh
```
Windows

```shell
./setup.sh
```

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