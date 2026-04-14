import asyncio
import edge_tts
import os

async def generate_voiceover():
    script_file = "voiceover_script.txt"
    output_file = "final_voiceover.mp3"

    if not os.path.exists(script_file):
        print(f"❌ {script_file} ကို ရှာမတွေ့ပါ။ Step 3 ကို အရင် run ပါ။")
        return

    with open(script_file, "r", encoding="utf-8") as f:
        text = f.read()

    print("\n" + "="*40)
    print("🎙️  AI VOICE OVER CONFIGURATION & GUIDE")
    print("="*40)
    
    # Voice Selection
    print("\n[1] အသံအမျိုးအစား ရွေးချယ်ပါ:")
    print("1. Thiha (Male - အမျိုးသား)")
    print("2. Nilar (Female - အမျိုးသမီး)")
    voice_choice = input("ရွေးချယ်မှု (Default 1): ") or "1"
    voice = "my-MM-ThihaNeural" if voice_choice == "1" else "my-MM-NilarNeural"

    # Rate Guide & Input
    print("\n[2] အသံအမြန်နှုန်း (Speed Rate) Guide:")
    print("   • -20% (နှေး)  • +0% (Normal)  • +20% (မြန် - Recap အတွက် အကြံပြုသည်)")
    user_rate = input("Enter Rate (e.g. +15%): ") or "+0%"

    # Pitch Guide & Input
    print("\n[3] အသံအနိမ့်အမြင့် (Pitch) Guide:")
    print("   • -10Hz (အသံဩ/နက်)  • +0Hz (Normal)  • +10Hz (အသံစူး/တက်)")
    user_pitch = input("Enter Pitch (e.g. -5Hz): ") or "+0Hz"

    print("\n" + "-"*40)
    print(f"🚀 Processing with {voice}...")
    print(f"📊 Settings: Rate={user_rate}, Pitch={user_pitch}")
    print("-"*40)
    
    try:
        communicate = edge_tts.Communicate(text, voice, rate=user_rate, pitch=user_pitch)
        await communicate.save(output_file)
        print(f"\n✅ အောင်မြင်ပါတယ်! '{output_file}' ထွက်လာပါပြီ။")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())

