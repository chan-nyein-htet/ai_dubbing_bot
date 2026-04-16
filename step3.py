import os
import re
import ollama
from deep_translator import GoogleTranslator

def refine_with_ollama(myanmar_text, duration, mode):
    if mode == "3": return myanmar_text # Subtitles သက်သက်ဆိုရင် Google Translate အတိုင်းပဲ ထားမယ်
    
    style = "Casual Burmese 'မင်း/ငါ' Recap style." if mode == "1" else "Natural Burmese Dubbing style."
    prompt = f"Refine this Burmese: '{myanmar_text}' to {style}. Keep it short for {duration:.1f}s. Only output Burmese."
    
    try:
        response = ollama.generate(model='llama3.2', prompt=prompt)
        refined = re.sub(r'[a-zA-Z]', '', response['response']).strip()
        return refined if refined else myanmar_text
    except: return myanmar_text

def process_translation(user_id):
    user_dir = os.path.join("users_workspace", str(user_id))
    t_in = os.path.join(user_dir, "transcription.txt")
    s_out = os.path.join(user_dir, "sync_voiceover_script.txt")

    if not os.path.exists(t_in): return

    print("\n🌐 SELECT MODE:")
    print("1. Recap (Voiceover ပါမယ်)")
    print("2. Dubbing (Voiceover ပါမယ်)")
    print("3. Subtitles Only (Step 4 မလိုပါ - မူရင်းအသံ + စာတန်းထိုး)")
    mode = input("Choice (1, 2, 3): ") or "1"

    translator = GoogleTranslator(source='en', target='my')

    with open(t_in, "r", encoding="utf-8") as f, open(s_out, "w", encoding="utf-8") as out:
        for line in f:
            times = re.findall(r"(\d+\.\d+)", line)
            if len(times) >= 2:
                start, end, content = float(times[0]), float(times[1]), line.split("] ", 1)[1].strip()
                print(f"⌛ Translating {start}s...")
                my_raw = translator.translate(content)
                final_text = refine_with_ollama(my_raw, end-start, mode)
                out.write(f"[{start:.2f}-{end:.2f}]|{end-start:.2f}|{final_text}\n")

    print(f"✅ Step 3 Done! Mode {mode} ကို ရွေးထားတဲ့အတွက် " + ("Step 4 ကို ကျော်ပြီး Step 5 တန်းသွားလို့ရပါပြီ Dude!" if mode == "3" else "Step 4 ကို ဆက်သွားပါ!"))

if __name__ == "__main__":
    u_id = input("Enter User ID: ").strip()
    process_translation(u_id)
