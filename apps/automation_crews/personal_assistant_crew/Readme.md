# start Only Personal Assistant Crew

## Steps to Run
**Navigate to the Project Directory:**
```shell
cd apps/automation_crews/personal_assistant_crew
```
Change to the directory where the `setup.sh`, `run_crew.py`, `requirements.txt` files are located. For example:


### 1. Run the Setup File
Make the setup.sh Script Executable (if necessary):
On Linux or macOS, you might need to make the setup.sh script executable:
```shell
chmod +x setup.sh
```

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