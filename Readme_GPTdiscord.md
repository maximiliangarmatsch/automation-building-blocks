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