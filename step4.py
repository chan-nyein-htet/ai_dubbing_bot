import asyncio
import edge_tts
import os

def apply_voice_fix(text):
    """ အသံမသွင်းခင် Recap လေသံ ပြင်မယ် """
    fixes = {
        "ကျွန်ုပ်": "ငါ", "ကျွန်မ": "ငါ", "သင်": "မင်း", "၎င်း": "အဲဒါ",
        "ဖြစ်ပါသည်": "တယ်", "ရှိပါသည်": "ရှိတယ်", "ကျေးဇူးပြုပြီး": "",
        "သို့သော်": "ဒါပေမဲ့", "သည်": "က", "၏": "ရဲ့", "ဖခင်": "အဖေ",
        "မိခင်": "အမေ", "ကောင်းပြီ": "အေးပါ", "ဟုတ်ကဲ့": "အင်း"
    }
    for old, new in fixes.items():
        text = text.replace(old, new)
    return text

def format_rate(val):
    """ 0 ကို +0% ဖြစ်အောင် ပြင်ပေးမယ့် logic """
    val = val.strip().replace("%", "")
    if val == "0" or val == "0%": return "+0%"
    # အကယ်၍ အပေါင်း/အနှုတ် လက္ခဏာ မပါရင် အပေါင်း ထည့်ပေးမယ်
    if not val.startswith("+") and not val.startswith("-"):
        return f"+{val}%"
    return f"{val}%"

def format_pitch(val):
    """ 0 ကို +0Hz ဖြစ်အောင် ပြင်ပေးမယ့် logic """
    val = val.strip().lower().replace("hz", "")
    if val == "0": return "+0Hz"
    if not val.startswith("+") and not val.startswith("-"):
        return f"+{val}Hz"
    return f"{val}Hz"

async def generate_voiceover():
    script_file = "downloads/sync_voiceover_script.txt"
    output_folder = "downloads/audio_segments"
    
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    if not os.path.exists(script_file):
        print(f"❌ {script_file} ကို ရှာမတွေ့ပါ။")
        return

    print("\n" + "="*50)
    print("🎙️  AI VOICE OVER PRO (STABLE MODE)")
    print("="*50)

    print("\n[1] Voice Selection:")
    print("    1. Thiha (Male) | 2. Nilar (Female)")
    voice_choice = input("    ရွေးချယ်မှု (Default 1): ") or "1"
    voice = "my-MM-ThihaNeural" if voice_choice == "1" else "my-MM-NilarNeural"

    print("\n[2] Speed Rate (အသံအမြန်နှုန်း):")
    print("    - 0 (Normal), +20 (Fast), -20 (Slow)")
    rate_raw = input("    Enter Rate: ") or "0"
    user_rate = format_rate(rate_raw)

    print("\n[3] Pitch (အသံအနိမ့်အမြင့်):")
    print("    - 0 (Normal), +10 (High), -10 (Low)")
    pitch_raw = input("    Enter Pitch: ") or "0"
    user_pitch = format_pitch(pitch_raw)

    with open(script_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    print("\n" + "-"*50)
    print(f"🚀 Processing with {voice}")
    print(f"📊 Config: Rate={user_rate}, Pitch={user_pitch}")
    print("-"*50 + "\n")

    for i, line in enumerate(lines):
        try:
            parts = line.strip().split("|")
            if len(parts) < 3: continue
            
            final_text = apply_voice_fix(parts[2])
            segment_path = os.path.join(output_folder, f"segment_{i}.mp3")
            
            communicate = edge_tts.Communicate(final_text, voice, rate=user_rate, pitch=user_pitch)
            await communicate.save(segment_path)
            
            # Progress Bar
            percent = int(((i + 1) / total) * 100)
            bar = '█' * (25 * percent // 100) + '░' * (25 - (25 * percent // 100))
            short_text = final_text[:15] + "..." if len(final_text) > 15 else final_text
            print(f"\rProgress: |{bar}| {percent}% ({i+1}/{total}) > {short_text}", end="")
            
        except Exception as e:
            print(f"\n❌ Error at line {i}: {e} (Rate={user_rate}, Pitch={user_pitch})")

    print(f"\n\n✅ Done! အသံဖိုင်အားလုံး အဆင့်သင့်ဖြစ်ပါပြီ။")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())

