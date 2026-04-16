import dropbox
import asyncio
import sys
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

# Permanent Settings from your old file
APP_KEY = 'tibtq1z9y3wvst3'
APP_SECRET = '65clbwssd237058'
REFRESH_TOKEN = 'eB1Hd3_y_vsAAAAAAAAAAaf1SkXncbLF7XXONa8v1NNwH-F88acg1h7sBvyktCfu'

# .env ထဲက Token ကို သုံးမယ် (မရှိရင် အဟောင်းထဲကဟာ သုံးမယ်)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "7837477611:AAEO0DMXAI8uuwMYWl4zFgox4Y_yMGfbrEM"

async def upload_and_share(user_id, chat_id):
    # User အလိုက် path တွေကို ခွဲလိုက်ပြီ
    local_path = f"users_workspace/{user_id}/final_ready.mp4"
    dropbox_path = f"/{user_id}/final_ready.mp4"

    try:
        dbx = dropbox.Dropbox(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            oauth2_refresh_token=REFRESH_TOKEN
        )
        bot = Bot(token=TELEGRAM_TOKEN)

        if not os.path.exists(local_path):
            print(f"❌ Error: {local_path} မရှိပါဘူး Dude!")
            return

        print(f"🚀 User {user_id} ရဲ့ ဗီဒီယိုကို Dropbox ပေါ်တင်နေပြီ...")
        
        with open(local_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

        print("🔗 Download Link ထုတ်ယူနေတယ်...")
        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
            raw_url = shared_link_metadata.url
        except:
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links
            raw_url = links[0].url

        download_url = raw_url.replace("?dl=0", "?dl=1")

        print(f"📱 Telegram (Chat ID: {chat_id}) ဆီ ပို့နေပြီ...")
        text = f"🎥 ဗီဒီယိုအဆင်သင့်ဖြစ်ပါပြီ Dude!\n\nဒီမှာဒေါင်းလိုက်တော့:\n{download_url}"
        await bot.send_message(chat_id=chat_id, text=text)
        print("✅ MISSION ACCOMPLISHED!")

    except Exception as e:
        print(f"❌ Dropbox Error: {e}")

if __name__ == "__main__":
    # Terminal ကနေဖြစ်ဖြစ်၊ တခြား script ကနေဖြစ်ဖြစ် လှမ်းခေါ်ရင် parameter ယူမယ်
    if len(sys.argv) > 2:
        u_id = sys.argv[1]
        c_id = sys.argv[2]
        asyncio.run(upload_and_share(u_id, c_id))
    else:
        print("⚠️ Usage: python dropbox_send.py <user_id> <chat_id>")
