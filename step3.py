import os
import re
import time
from deep_translator import GoogleTranslator

def parse_duration(time_str):
    times = re.findall(r"(\d+\.\d+)", time_str)
    if len(times) == 2:
        start, end = float(times[0]), float(times[1])
        return start, end, end - start
    return 0.0, 0.0, 0.0

def read_transcript(user_dir):
    lines = []
    transcript_path = os.path.join(user_dir, "transcription.txt")
    if not os.path.exists(transcript_path):
        return None
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            if " -> " in line:
                parts = line.split("] ", 1)
                time_range = parts[0] + "]"
                text_part = parts[1].strip()
                start, end, duration = parse_duration(time_range)
                lines.append({
                    "time": time_range, 
                    "start": start, 
                    "end": end, 
                    "duration": duration,
                    "text": text_part
                })
    return lines

def translate_text(text):
    return GoogleTranslator(source='auto', target='my').translate(text)

def main_process(user_dir, choice):
    data = read_transcript(user_dir)
    if not data:
        print(f"❌ {user_dir} ထဲမှာ transcription.txt ကို ရှာမတွေ့ပါ။")
        return

    sync_path = os.path.join(user_dir, "sync_voiceover_script.txt")
    total_lines = len(data)
    
    print(f"⏳ စတင်နေပါပြီ... စုစုပေါင်း ({total_lines}) ကြောင်း ရှိပါတယ်။")

    if choice in ["1", "2"]:
        output_file = os.path.join(user_dir, "translated_subtitles.txt" if choice == "1" else "sync_voiceover_script.txt")
        
        with open(output_file, "w", encoding="utf-8") as f:
            for i, item in enumerate(data):
                translated = translate_text(item['text'])
                
                # Percentage calculation for Terminal
                percent = int(((i + 1) / total_lines) * 100)
                bar = '█' * (percent // 10) + '░' * (10 - (percent // 10))
                print(f"\r进度: |{bar}| {percent}% ({i+1}/{total_lines})", end="")
                
                if choice == "1":
                    f.write(f"{item['time']} {translated}\n")
                else:
                    f.write(f"[{item['start']:.2f}-{item['end']:.2f}]|{item['duration']:.2f}|{translated}\n")
        
        print(f"\n✅ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ: {output_file}")

    elif choice == "3":
        print("📝 Generating Recap Plan...")
        recap_path = os.path.join(user_dir, "recap_plan.txt")
        summary_data = data[::len(data)//5] if len(data) > 5 else data
        with open(recap_path, "w", encoding="utf-8") as f:
            for s in summary_data:
                translated = translate_text(s['text'])
                f.write(f"{s['time']} {translated}\n")
        print(f"✅ Recap Plan ရပါပြီ: {recap_path}")

if __name__ == "__main__":
    test_dir = "downloads"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    print("\n--- 🤖 Pro Sync Processing Menu ---")
    print("1. Subtitles (မြန်မာစာတန်းထိုး)")
    print("2. Sync Voiceover (Scene နဲ့ အသံ ညှိရန် - အကြံပြုသည်)")
    print("3. Basic Recap (စာသားအကျဉ်းချုပ်)")
    
    user_choice = input("\nရွေးချယ်ပါ (1/2/3): ")
    main_process(test_dir, user_choice)

