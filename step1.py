import os
import shutil
import subprocess

def get_unique_filename(base_name, user_dir):
    """ဖိုင်နာမည်တူရှိရင် old_video_1.mp4 စသဖြင့် အော်တို နာမည်ပြောင်းပေးရန် (User Folder ထဲတွင်)"""
    full_path = os.path.join(user_dir, base_name)
    if not os.path.exists(full_path):
        return full_path
    
    name, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(os.path.join(user_dir, f"{name}_{counter}{ext}")):
        counter += 1
    return os.path.join(user_dir, f"{name}_{counter}{ext}")

def process_input(user_input, user_dir):
    # ဖိုင်လမ်းကြောင်းများကို user_dir နှင့် ချိတ်ဆက်ခြင်း
    video_path = os.path.join(user_dir, "original_video.mp4")
    audio_path = os.path.join(user_dir, "original_audio.mp3")

    # ဒေါင်းလုဒ်ဆွဲရန် အကြံပြုချက်များ
    download_tools = [
        "1. Seal (Android - အကြံပြုသည်)",
        "2. VidMate",
        "3. SnapTube",
        "4. Blackhole",
        "5. 1DM (Download Manager)",
        "6. NewPipe",
        "7. Y2Mate (Website)",
        "8. SaveFrom.net (Website)",
        "9. SnapTik (For TikTok)",
        "10. SaveSubs (For Subtitles)"
    ]

    # အရင်ရှိနေတဲ့ ဖိုင်တွေကို Backup လုပ်ပြီး ဖယ်ပေးခြင်း (User Folder ထဲမှာပဲ လုပ်မယ်)
    if os.path.exists(video_path):
        os.rename(video_path, get_unique_filename("old_video.mp4", user_dir))
    if os.path.exists(audio_path):
        os.rename(audio_path, get_unique_filename("old_audio.mp3", user_dir))

    # ၁။ Link ထည့်ခဲ့လျှင်
    if user_input.startswith(("http", "www")):
        print(f"🌐 ဗီဒီယိုနှင့် အသံဖိုင်ကို အွန်လိုင်းမှ ရယူနေပါသည်...")
        
        # TikTok အတွက် Audio ပါအောင် format ကို "best" ဟု ပြောင်းလဲသတ်မှတ်ခြင်း
        yt_cmd = [
            "yt-dlp", 
            "-f", "bestvideo+bestaudio/best", 
            "--merge-output-format", "mp4",
            "--output", video_path, 
            user_input
        ]
        result = subprocess.run(yt_cmd)
        
        # ဒေါင်းလုဒ်ဆွဲ၍ မရခဲ့လျှင်
        if result.returncode != 0:
            print("\n❌ ခွင့်လွှတ်ပါခင်ဗျာ၊ ယခု Link ကို တိုက်ရိုက်ဒေါင်းလုပ်ဆွဲ၍ မရနိုင်ပါ။")
            print("💡 အောက်ပါ Tools တစ်ခုခုကို အသုံးပြု၍ သင့်ဖုန်းထဲသို့ အရင်ဒေါင်းလုဒ်ဆွဲပေးပါ။")
            print("   ပြီးလျှင် ဒေါင်းလုဒ်ဆွဲထားသော ဖိုင်ကို ဤနေရာသို့ Upload တင်ပေးပါခင်ဗျာ:\n")
            for tool in download_tools:
                print(f"   {tool}")
            return
            
    # ၂။ ဖိုင်အမည် တိုက်ရိုက်ရိုက်ထည့်လျှင်
    elif os.path.exists(user_input):
        print(f"📁 ဖိုင်ကို စစ်ဆေးနေပါသည်...")
        shutil.copy(user_input, video_path)
    else:
        print("❌ Error: ဖိုင်အမည် မှားယွင်းနေခြင်း သို့မဟုတ် Link မှားယွင်းနေပါသည်။")
        return

    # ၃။ အသံဖိုင် ခွဲထုတ်ခြင်း
    if os.path.exists(video_path):
        print("🎙️ အသံဖိုင်ကို တိတိကျကျ ခွဲထုတ်နေပါသည်...")
        # FFmpeg အမိန့်ကို ပိုမိုတိကျအောင် ပြန်လည်ပြင်ဆင်ခြင်း
        cmd = [
            "ffmpeg", "-i", video_path, 
            "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", 
            audio_path, "-y"
        ]
        subprocess.run(cmd)
        
        if os.path.exists(audio_path):
            print("\n✅ လုပ်ငန်းစဉ် အပိုင်း (၁) အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
            print(f"📁 ဖိုင်များကို {user_dir} ထဲတွင် သိမ်းဆည်းပြီးပါပြီ။")
        else:
            print("⚠️ Error: အသံဖိုင် ခွဲထုတ်၍ မရပါခင်ဗျာ။ ဗီဒီယိုတွင် အသံပါဝင်မှု ရှိမရှိ ပြန်လည်စစ်ဆေးပေးပါ။")

if __name__ == "__main__":
    # စမ်းသပ်ရန်အတွက် download folder ကို path အဖြစ်ပေးထားမယ်
    test_dir = "downloads"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        
    url = input("🔗 Link သို့မဟုတ် ဖိုင်အမည် ရိုက်ထည့်ပါ: ").strip()
    process_input(url, test_dir)

