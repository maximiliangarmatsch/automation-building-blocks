## 2. ProActiveDiscord Bot

A Discord bot that creates custom invite links and sends personalized welcome messages to new members when they join using those links.

### Features

- Creates single-use invite links with custom user data
- Tracks invite usage
- Sends personalized welcome messages
- REST API endpoint for invite generation

### Prerequisites

- Python 3.10+
- Discord Bot Token
- Discord Developer Portal Access

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install discord.py flask python-dotenv quart_cors quart
```
3. Create a `.env` file:
```env
DISCORD_TOKEN=your_bot_token_here
```

### Discord Developer configuration

1. Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable required intents:
   - Server Members Intent
   - Message Content Intent
   - Presence Intent
3. Invite bot to your server with required permissions:
   - Manage Server
   - Create Instant Invite
   - Send Messages
   - View Channels
   

1. Start ProActive Discord Bot
```bash
cd ./apps/automation_crews/ProActiveDiscord
python flask_discord_server.py
```

2. Generate invite via API:
```bash
curl -X POST http://localhost:5000/join-discord \
  -H "Content-Type: application/json" \
  -d '{"username": "user123", "server_name": "Your Server", "channel_name": "general", "user_id": "123"}'
```

### API Endpoint

`POST /join-discord`
```json
{
  "username": "string",
  "server_name": "string",
  "channel_name": "string",
  "user_id": "string"
}
```