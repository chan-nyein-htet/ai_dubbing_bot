import os
from deep_translator import GoogleTranslator

def read_transcript():
    lines = []
    if not os.path.exists("transcription.txt"):
        return None
    with open("transcription.txt", "r", encoding="utf-8") as f:
        for line in f:
            if " -> " in line:
                # [0.00s -> 3.92s] text ပုံစံကို ခွဲထုတ်မယ်
                parts = line.split("] ", 1)
                time_part = parts[0] + "]"
                text_part = parts[1].strip()
                lines.append({"time": time_part, "text": text_part})
    return lines

def translate_text(text):
    # deep-translator library ကို သုံးပြီး မြန်မာလို ပြန်မယ်
    return GoogleTranslator(source='auto', target='my').translate(text)

def main():
    data = read_transcript()
    if not data:
        print("❌ transcription.txt ကို ရှာမတွေ့ပါ။ Step 2 ကို အရင် run ပါ။")
        return

    print("\n--- 🤖 Local Processing Menu ---")
    print("1. Translate & Subtitles (မြန်မာစာတန်းထိုး)")
    print("2. Voiceover Script (အသံသွင်းရန်အတွက် - No Timestamps)")
    print("3. Basic Recap (စာသားအကျဉ်းချုပ်)")
    
    choice = input("\nရွေးချယ်ပါ (1/2/3): ")

    if choice == "1":
        print("⏳ ဘာသာပြန်နေပြီ... ခဏစောင့်ပါ။")
        with open("translated_subtitles.txt", "w", encoding="utf-8") as f:
            for item in data:
                translated = translate_text(item['text'])
                output = f"{item['time']} {translated}\n"
                print(output.strip())
                f.write(output)
        print("\n✅ 'translated_subtitles.txt' ရပါပြီ။")

    elif choice == "2":
        print("⏳ Voiceover အတွက် ပြင်ဆင်နေပြီ...")
        with open("voiceover_script.txt", "w", encoding="utf-8") as f:
            # စာသားတွေကို စုပြီး တစ်ကြောင်းချင်း ပြန်မယ်
            for item in data:
                translated = translate_text(item['text'])
                f.write(translated + " ")
        print("\n✅ 'voiceover_script.txt' ရပါပြီ။")

    elif choice == "3":
        print("📝 Generating Basic Recap Plan...")
        # အရှည်ဆုံးနဲ့ အရေးကြီးဆုံး စာကြောင်း ၅ ကြောင်းလောက်ကိုပဲ နမူနာ ယူပြမယ်
        summary_data = data[::len(data)//5] if len(data) > 5 else data
        with open("recap_plan.txt", "w", encoding="utf-8") as f:
            for s in summary_data:
                translated = translate_text(s['text'])
                f.write(f"{s['time']} {translated}\n")
        print("\n✅ 'recap_plan.txt' ရပါပြီ။")

if __name__ == "__main__":
    main()

