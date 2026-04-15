from faster_whisper import WhisperModel
import os
import time

# audio_file အပြင် user_dir ကိုပါ လက်ခံနိုင်အောင် parameter တိုးလိုက်တယ်
def transcribe_audio(audio_file, user_dir):
    # transcription.txt ကို user_dir ထဲမှာ သိမ်းဖို့ လမ်းကြောင်းသတ်မှတ်မယ်
    transcript_path = os.path.join(user_dir, "transcription.txt")
    
    if not os.path.exists(audio_file):
        print(f"❌ {audio_file} ကို ရှာမတွေ့ပါဘူး။ Step 1 ကို အရင် run ပါ။")
        return

    print("🧠 AI Model (Faster-Whisper) ကို Load လုပ်နေတယ်...")
    try:
        # aarch64 (ARM) အတွက် int8 quantization က အမြန်ဆုံးပဲ
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        
        print(f"🎙️ စာသားပြောင်းနေပြီ: {audio_file}")
        start_time = time.time()
        
        segments, info = model.transcribe(audio_file, beam_size=5)
        
        print("\n--- Transcription Result (With Timestamps) ---")
        
        # ဒီနေရာမှာ transcription.txt ကို user_dir အောက်မှာ သိမ်းသွားမှာပါ
        with open(transcript_path, "w", encoding="utf-8") as f:
            for segment in segments:
                output = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
                print(output)
                f.write(output + "\n")

        end_time = time.time()
        print("-" * 40)
        print(f"✅ Transcription ပြီးပါပြီ! ကြာချိန်: {end_time - start_time:.2f} seconds")
        print(f"📁 '{transcript_path}' မှာ Timestamps တွေနဲ့ သိမ်းဆည်းပြီးပါပြီ။")

    except Exception as e:
        print(f"❌ Transcription error: {e}")

if __name__ == "__main__":
    # စမ်းသပ်ရန်အတွက် download folder ကို path အဖြစ်ပေးထားမယ်
    test_dir = "downloads"
    audio_path = os.path.join(test_dir, "original_audio.mp3")
    
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        
    transcribe_audio(audio_path, test_dir)

