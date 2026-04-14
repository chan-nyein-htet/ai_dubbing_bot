import yt_dlp
import os
import shutil

def process_input(user_input):
    # ၁။ အရင်ရှိနေတဲ့ file တွေကို ရှင်းထုတ်မယ်
    for f in ["original_video.mp4", "original_audio.mp3"]:
        if os.path.exists(f):
            os.remove(f)

    # ၂။ Input က YouTube Link လား၊ Local File လား စစ်မယ်
    if user_input.startswith(("http://", "https://", "www.")):
        print(f"🌐 Link ရှာတွေ့တယ်... YouTube ကနေ ဒေါင်းနေပြီ...")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'original_video.mp4',
        }
        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'original_audio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([user_input])
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([user_input])

    else:
        # Local File ဖြစ်ခဲ့ရင်
        if os.path.exists(user_input):
            print(f"📁 Local File ရှာတွေ့တယ်: {user_input}")
            # Video ကို original_video.mp4 အဖြစ် နာမည်ပြောင်း/ကူးမယ်
            shutil.copy(user_input, "original_video.mp4")
            
            # Transcription အတွက် အသံဖိုင် သီးသန့်ထုတ်မယ် (FFmpeg သုံးမယ်)
            print("🎙️ အသံဖိုင် ခွဲထုတ်နေတယ်...")
            os.system(f"ffmpeg -i {user_input} -q:a 0 -map a original_audio.mp3 -y")
        else:
            print("❌ Error: Link လည်းမဟုတ်၊ File လည်း ရှာမတွေ့ပါ!")
            return

    print("\n✅ Step 1 ပြီးပါပြီ!")
    print("📁 original_video.mp4 နှင့် original_audio.mp3 အဆင်သင့်ရှိပါသည်။")

if __name__ == "__main__":
    path_or_link = input("🔗 YouTube Link သို့မဟုတ် File Path ထည့်ပါ: ").strip()
    # Path ထဲမှာ ' ' (space) ပါရင် ဖယ်ပေးဖို့ strip() သုံးထားတယ်
    process_input(path_or_link)

