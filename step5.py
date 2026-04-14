import os
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip

def assemble_video():
    uid = input("Enter User ID (e.g., 1): ")
    user_dir = f"workspace/user_{uid}"
    
    vid_in = os.path.join(user_dir, "video.mp4")
    aud_in = os.path.join(user_dir, "voice.mp3")
    sub_in = os.path.join(user_dir, "subtitles.txt")
    logo_path = os.path.join(user_dir, "logo.png")
    out_file = os.path.join(user_dir, "final_ready.mp4")

    if not os.path.exists(vid_in) or not os.path.exists(aud_in):
        print(f"❌ Error: {user_dir} ထဲမှာ ဖိုင်မစုံပါဘူး!")
        return

    # --- Font Selection ---
    fonts = sorted([f for f in os.listdir("fonts") if f.endswith(('.ttf', '.otf'))])
    for i, f in enumerate(fonts):
        print(f"{i+1}. {f}")
    selected_font = os.path.join("fonts", fonts[int(input("Font နံပါတ်: ")) - 1])

    # --- Feature Configuration ---
    add_logo = input("Logo ထည့်မလား? (y/n): ").lower() == 'y'
    add_subs = input("Subtitles ထိုးမလား? (y/n): ").lower() == 'y'
    use_copyright = input("Copyright Protection (y/n): ").lower() == 'y'

    try:
        video = VideoFileClip(vid_in)
        audio = AudioFileClip(aud_in)
        video = video.with_duration(round(audio.duration, 2)).with_audio(audio)
        
        main_video = video.resized(1.1) if use_copyright else video
        layers = [main_video]

        # --- Logo Advanced Logic ---
        if add_logo:
            if os.path.exists(logo_path):
                print("\n--- Logo Settings ---")
                pos_choice = input("Position (1: Top-Right / 2: Center / 3: Bottom-Left): ")
                opacity = float(input("Opacity (0.1 to 1.0): ") or 1.0)
                size_p = float(input("Logo Size (0.1 = 10% of height): ") or 0.1)

                logo = ImageClip(logo_path).with_duration(main_video.duration)
                logo = logo.resized(height=int(main_video.h * size_p))
                logo = logo.with_opacity(opacity)

                if pos_choice == "1":
                    logo = logo.with_position(('right', 'top'), margin=20)
                elif pos_choice == "2":
                    logo = logo.with_position('center')
                else:
                    logo = logo.with_position(('left', 'bottom'), margin=20)
                
                layers.append(logo)
                print("✅ Logo configured!")
            else:
                print(f"⚠️ {logo_path} မှာ logo မရှိလို့ ကျော်လိုက်ပါပြီ Dude!")

        # --- Subtitles Fix (Using v2.0 parameters) ---
        if add_subs and os.path.exists(sub_in):
            with open(sub_in, "r", encoding="utf-8") as f:
                content = f.read()
            
            sub_clip = TextClip(
                text=content, font_size=30, color='white',
                font=selected_font, duration=main_video.duration,
                method='caption', size=(int(main_video.w * 0.8), None)
            ).with_position(('center', 'bottom')) # Margin error ကို ဒီမှာ ရှောင်ထားတယ်
            
            layers.append(sub_clip)

        print("\n💾 Rendering... (မင်းရဲ့ $100K ပန်းတိုင်အတွက်!)")
        final = CompositeVideoClip(layers)
        final.write_videofile(out_file, codec="libx264", audio_codec="aac", fps=24)
        
        print(f"✅ အောင်မြင်ပါတယ်။ '{out_file}' ထွက်လာပါပြီ!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    assemble_video()

