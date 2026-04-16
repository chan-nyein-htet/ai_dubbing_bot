import os
import shutil
import subprocess

def process_input(user_input, user_id):
    user_dir = os.path.join("users_workspace", str(user_id))
    if not os.path.exists(user_dir): os.makedirs(user_dir)
    
    video_path = os.path.join(user_dir, "original_video.mp4")
    audio_path = os.path.join(user_dir, "original_audio.mp3")

    if os.path.exists(video_path): os.remove(video_path)

    if user_input.startswith(("http", "www")):
        print(f"\n🌐 [User: {user_id}] Attempting Download...")
        
        # Stealth Download Attempt
        yt_cmd = [
            "yt-dlp", "--no-check-certificates",
            "--extractor-args", "youtube:player_client=android,web",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4", 
            "--output", video_path, 
            user_input
        ]
        
        result = subprocess.run(yt_cmd)

        if result.returncode != 0:
            print("\n" + "!"*50)
            print("❌ ယခု Video ကို တိုက်ရိုက် Download လုပ်၍မရနိုင်ပါ။")
            print("💡 YouTube က IP Block ထားသောကြောင့် အောက်ပါ Resources များသုံး၍")
            print("   Video ကို Manual Download ဆွဲပြီး File ကို ပြန်ပို့ပေးပါ Dude!")
            print("-" * 50)
            print("🚀 Recommended Download Tools:")
            print("1. SnapSave / SaveFrom.net (Websites)")
            print("2. Seal / YTDLnis (Android Apps)")
            print("3. IDM (PC)")
            print("-" * 50)
            print("!"*50 + "\n")
            return

    elif os.path.exists(user_input):
        print(f"📁 Processing local file for User {user_id}...")
        shutil.copy(user_input, video_path)
    else:
        print("❌ အမှားအယွင်းရှိနေပါသည်။ File Path သို့မဟုတ် Link ကို ပြန်စစ်ပါ။")
        return

    # Success Path
    if os.path.exists(video_path):
        print("🎙️ Extracting Audio...")
        subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", audio_path, "-y"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Step 1 Success! Video အဆင်သင့်ဖြစ်ပါပြီ။")

if __name__ == "__main__":
    u_id = input("User ID: ")
    target = input("Link သို့မဟုတ် File Path ထည့်ပါ: ")
    process_input(target, u_id)
