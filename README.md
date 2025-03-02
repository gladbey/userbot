# Telegram UserBot

A modular Telegram UserBot built with Telethon, designed for easy extensibility and command management.

## Features

- Modular command system
- Easy command installation
- Secure session management
- Logging system
- Environment-based configuration

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials:
   - Get your `API_ID` and `API_HASH` from https://my.telegram.org
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your credentials

## Running the Bot

```bash
python bot.py
```

## Creating Custom Commands

1. Create a new Python file in the `commands` directory
2. Follow this template:
```python
async def command(event, args):
    """
    Command: your_command_name
    Description: What your command does
    Usage: !your_command <args>
    """
    return {
        "prefix": "your_command_name",
        "return": "Your command's response"
    }
```

## Available Commands

- `!ping` - Check if the bot is responsive
- `!echo <message>` - Repeats the given message

## Deployment

This bot is designed to be deployed on Render. Follow these steps:

1. Push your code to a Git repository
2. Create a new Web Service on Render
3. Set your environment variables in Render's dashboard
4. Deploy!
