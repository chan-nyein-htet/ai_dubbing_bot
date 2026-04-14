from faster_whisper import WhisperModel
import os
import time

def transcribe_audio(audio_file):
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
        
        with open("transcription.txt", "w", encoding="utf-8") as f:
            for segment in segments:
                output = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
                print(output)
                f.write(output + "\n")

        end_time = time.time()
        print("-" * 40)
        # ဒီနေရာမှာ Syntax Error ဖြစ်သွားတာ၊ အခု ပြင်လိုက်ပြီ
        print(f"✅ Transcription ပြီးပါပြီ! ကြာချိန်: {end_time - start_time:.2f} seconds")
        print("📁 'transcription.txt' မှာ Timestamps တွေနဲ့ သိမ်းဆည်းပြီးပါပြီ။")

    except Exception as e:
        print(f"❌ Transcription error: {e}")

if __name__ == "__main__":
    audio_path = "original_audio.mp3"
    transcribe_audio(audio_path)

