import asyncio
import edge_tts
import os
import shutil

async def generate_voice(user_id):
    user_dir = os.path.join("users_workspace", str(user_id))
    script = os.path.join(user_dir, "sync_voiceover_script.txt")
    out_folder = os.path.join(user_dir, "audio_segments")

    if os.path.exists(out_folder): shutil.rmtree(out_folder)
    os.makedirs(out_folder)

    # [1] Voice Selection Logic
    print("\n--- 🎙️ SELECT BURMESE VOICE ---")
    print("1. Male (ThihaNeural)")
    print("2. Female (NilarNeural)")
    v_choice = input("အသံရွေးပါ (1 သို့မဟုတ် 2): ") or "1"
    voice = "my-MM-ThihaNeural" if v_choice == "1" else "my-MM-NilarNeural"

    # [2] Intro Branding
    name_tag = input("\n👤 Intro မှာ နာမည်ထည့်မလား? (ဥပမာ- 'Presented by Chan'): ")
    
    # [3] Speed Selection
    print("\n--- ⚡ SELECT VOICE SPEED ---")
    print("1. Normal (1.0x)")
    print("2. Fast (1.2x - Best for Recaps)")
    print("3. Slow (0.9x)")
    speed_choice = input("အမြန်နှုန်းရွေးပါ (1, 2, 3): ") or "1"
    rate = "+0%" if speed_choice=="1" else "+20%" if speed_choice=="2" else "-10%"

    if not os.path.exists(script):
        print(f"❌ Error: {script} ကို ရှာမတွေ့ပါ။ Step 3 အရင် run ပါ။")
        return

    with open(script, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Intro Branding အသံသွင်းခြင်း
    if name_tag:
        print(f"📣 Branding Intro သွင်းနေသည်...")
        intro_text = f"{name_tag} က တင်ဆက်ပေးလိုက်ပါတယ်။"
        comm = edge_tts.Communicate(intro_text, voice, rate=rate)
        await comm.save(os.path.join(out_folder, "intro_name.mp3"))

    print(f"🎙️ Generating {len(lines)} AI Voice segments...")
    for i, line in enumerate(lines):
        parts = line.strip().split("|")
        if len(parts) >= 3:
            text_to_speak = parts[2]
            # [4] Generate segment
            communicate = edge_tts.Communicate(text_to_speak, voice, rate=rate)
            await communicate.save(os.path.join(out_folder, f"segment_{i}.mp3"))
            print(f"⏳ {i+1}/{len(lines)} segments done...", end="\r")
            
    print(f"\n✅ Step 4 Done! All voices saved in: {out_folder}")

if __name__ == "__main__":
    u_id = input("Enter User ID: ").strip()
    asyncio.run(generate_voice(u_id))
