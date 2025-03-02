import os
import sys
import importlib
import traceback
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from loguru import logger
from utils.language import get_lang_manager
from flask import Flask
import threading

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Telegram UserBot is running!'

def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def main():
    try:
        # Configure logging (Render için çıktıyı stderr'e yönlendiriyoruz)
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        
        # Initialize language manager
        lang_manager = get_lang_manager()

        class UserBot:
            def __init__(self):
                # Check for required environment variables
                self.api_id = os.getenv('API_ID')
                self.api_hash = os.getenv('API_HASH')
                self.session_string = os.getenv('SESSION_STRING')
                
                if not all([self.api_id, self.api_hash, self.session_string]):
                    raise ValueError(
                        "API_ID, API_HASH, and SESSION_STRING must be set in environment variables"
                    )
                
                self.prefix = os.getenv('COMMAND_PREFIX', '!')
                self.commands_dir = os.getenv('COMMANDS_DIR', 'commands')
                
                # Initialize client with string session
                self.client = TelegramClient(
                    StringSession(self.session_string),
                    self.api_id,
                    self.api_hash
                )
                
                # Command storage
                self.commands = {}
                
                # Load commands
                self.load_commands()
                
                # Register message handler
                self.client.add_event_handler(self.command_handler, events.NewMessage)
            
            async def set_owner(self):
                """Bot'un çalıştığı hesabın ID'sini al."""
                self.owner_id = (await self.client.get_me()).id
                logger.info(f"UserBot owner ID set to: {self.owner_id}")
            
            def load_commands(self):
                """Load all commands from the commands directory."""
                try:
                    if not os.path.exists(self.commands_dir):
                        os.makedirs(self.commands_dir)
                    
                    self.commands = {}
                    
                    if self.commands_dir in sys.path:
                        sys.path.remove(self.commands_dir)
                    sys.path.insert(0, self.commands_dir)
                    
                    for filename in os.listdir(self.commands_dir):
                        if filename.endswith('.py') and not filename.startswith('_'):
                            module_name = filename[:-3]
                            try:
                                if module_name in sys.modules:
                                    del sys.modules[module_name]
                                module = importlib.import_module(module_name)
                                if hasattr(module, 'command'):
                                    self.commands[module_name] = module.command
                            except Exception as e:
                                logger.error(f"Failed to load command {module_name}: {e}")
                except Exception as e:
                    logger.error(f"Error in load_commands: {e}")
            
            async def command_handler(self, event):
                try:
                    if event.sender_id != self.owner_id:
                        logger.warning(f"Unauthorized user tried to use command: {event.sender_id}")
                        return  # Sadece botun sahibi komut kullanabilir
                    
                    if event.message.text and event.message.text.startswith(self.prefix):
                        command_text = event.message.text[len(self.prefix):]
                        command_name = command_text.split()[0].lower()
                        args = command_text.split()[1:] if len(command_text.split()) > 1 else []
                        
                        if command_name == "cmd":
                            self.load_commands()
                        
                        if command_name in self.commands:
                            try:
                                result = await self.commands[command_name](event, args)
                                if isinstance(result, dict):
                                    prefix = result.get('prefix', '')
                                    message = result.get('return', 'Command executed successfully')
                                    if prefix:
                                        message = f"[{prefix}] {message}"
                                    await event.reply(f"{message} \n 🇫​🇴​🇱​🇺​🇳​🇹​🇪​🇩​ ®")
                            except Exception as e:
                                logger.error(f"Error executing command {command_name}: {e}")
                                await event.reply(f"Error executing command: {e}")
                except Exception as e:
                    logger.error(f"Error in command handler: {e}")
            
            async def start(self):
                logger.info("Starting userbot...")
                await self.client.connect()
                await self.client.get_me()  # Bağlantıyı doğrulamak için Telegram'a ping at
                
                if not await self.client.is_user_authorized():
                    logger.error("Session is invalid! Please regenerate SESSION_STRING.")
                    sys.exit(1)
                
                await self.set_owner()
                logger.info("Userbot is running...")
                await self.client.run_until_disconnected()

        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        bot = UserBot()
        bot.client.loop.run_until_complete(bot.start())
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


