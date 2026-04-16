import dropbox
import asyncio
import sys
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

# --- Configurations ---
APP_KEY = 'tibtq1z9y3wvst3'
APP_SECRET = '65clbwssd237058'
REFRESH_TOKEN = 'eB1Hd3_y_vsAAAAAAAAAAaf1SkXncbLF7XXONa8v1NNwH-F88acg1h7sBvyktCfu'

# .env ထဲက Token ကိုသုံးမယ်
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# မင်းရဲ့ Chat ID ကို ဒီမှာ အသေသတ်မှတ်ထားလိုက်မယ်
FIXED_CHAT_ID = "5768501788"

async def upload_and_send_link(user_id, chat_id):
    local_file = f"users_workspace/{user_id}/final_ready.mp4"
    dropbox_path = f"/{user_id}/final_video_{user_id}.mp4"

    if not os.path.exists(local_file):
        print(f"❌ Error: {local_file} ကို ရှာမတွေ့ပါ!")
        return

    try:
        dbx = dropbox.Dropbox(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            oauth2_refresh_token=REFRESH_TOKEN
        )
        bot = Bot(token=TELEGRAM_TOKEN)

        print(f"🚀 Dropbox ပေါ်တင်နေပြီ Dude... (User: {user_id})")
        with open(local_file, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

        print("🔗 Link ထုတ်ယူနေတယ်...")
        try:
            shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
            raw_url = shared_link.url
        except:
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links
            raw_url = links[0].url

        download_url = raw_url.replace("?dl=0", "?dl=1")

        print(f"📱 Telegram (Chat ID: {chat_id}) ဆီ ပို့နေပြီ...")
        caption = f"🎥 ဗီဒီယိုအဆင်သင့်ဖြစ်ပါပြီ Dude!\n\n🔗 Download Link:\n{download_url}"
        
        await bot.send_message(chat_id=chat_id, text=caption)
        print("✅ MISSION ACCOMPLISHED!")

    except Exception as e:
        print(f"❌ Step 6 Error: {e}")

if __name__ == "__main__":
    # User ID တစ်ခုပဲ တောင်းမယ်၊ Chat ID က အပေါ်က fixed ID ကို ယူသုံးမယ်
    if len(sys.argv) > 1:
        u_id = sys.argv[1]
        # Chat ID ပါလာရင် ယူမယ်၊ မပါရင် FIXED_CHAT_ID ကို သုံးမယ်
        c_id = sys.argv[2] if len(sys.argv) > 2 else FIXED_CHAT_ID
        asyncio.run(upload_and_send_link(u_id, c_id))
    else:
        print("💡 အသုံးပြုပုံ: python step6.py <user_id>")
