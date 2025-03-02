import asyncio
import logging
from utils.language import get_lang_manager

logger = logging.getLogger('tag')
tagging_active = {}  # Her grup için etiketleme durumunu takip eder

async def command(event, args):
    """
    Command: tag
    Description: Tags all users in the group with a specified message at intervals.
    Usage: !tag <message> [time]
    """
    global tagging_active

    try:
        lang_manager = get_lang_manager()
        
        # Kullanıcıları al
        participants = await event.client.get_participants(event.chat_id)
        
        # Mesaj ve zaman ayarı
        message = ' '.join(args[:-1])  # Son argüman hariç tüm mesaj
        time_interval = int(args[-1]) if args and args[-1].isdigit() else 1  # Varsayılan 1 saniye
        
        # İşlemi başlat
        tagging_active[event.chat_id] = True

        for user in participants:
            if not tagging_active.get(event.chat_id):  # Eğer stop_tag çağrıldıysa dur
                await event.reply("🚫 **Tagging stopped!**")
                return
            
            if user.username:
                await event.reply(f'@{user.username} {message}')
            else:
                await event.reply(f'[{user.first_name}](tg://user?id={user.id}) {message}')
            
            await asyncio.sleep(time_interval)  # Bekleme süresi
        
        return {
            "prefix": "tag",
            "return": "✅ **Users tagged successfully.**"
        }
    except Exception as e:
        logger.error(f"Error in tag command: {str(e)}")
        return {
            "prefix": "tag",
            "return": f"⚠️ **Error:** {str(e)}"
        }

async def stop_tag(event, args):
    """
    Command: stoptag
    Description: Stops the ongoing tagging process.
    Usage: !stoptag
    """
    global tagging_active
    tagging_active[event.chat_id] = False  # Tagging'i durdur
    
    await event.reply("🚫 **Tagging process has been stopped.**")

    return {
        "prefix": "stoptag",
        "return": "Tagging process stopped."
    }
