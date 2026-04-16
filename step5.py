import os
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip, ImageClip
import moviepy.video.fx as vfx

def assemble_video(user_id):
    user_dir = f"users_workspace/{user_id}"
    vid_in = f"{user_dir}/original_video.mp4"
    script_in = f"{user_dir}/sync_voiceover_script.txt"
    audio_dir = f"{user_dir}/audio_segments"
    out_file = f"{user_dir}/final_ready.mp4"
    user_logo = f"{user_dir}/logo.png"

    if not os.path.exists(vid_in):
        print(f"❌ Error: {vid_in} missing.")
        return

    try:
        print("\n" + "="*50)
        print(f"🎬  ULTRA-QUALITY STUDIO (V16) - USER: {user_id}")
        print("="*50)

        clip = VideoFileClip(vid_in)

        # [1] Aspect Ratio & Smart Blur Background (No Scipy Required)
        print("\n[Select Aspect Ratio]")
        print("1. 9:16 (Vertical), 2. 16:9 (Horizontal), 3. 1:1 (Square), 4. Original")
        ar_choice = input("Choice (Default 4): ") or "4"
        
        target_size = None
        if ar_choice == "1": target_size = (1080, 1920)
        elif ar_choice == "2": target_size = (1920, 1080)
        elif ar_choice == "3": target_size = (1080, 1080)

        if target_size and ar_choice != "4":
            print(f"✨ Adding High-Res Blur Background (Smart Logic)...")
            
            # Smart Blur Trick: Resize down and then back up to create natural blur without extra modules
            # ဒါက Termux မှာ GaussianBlur error တက်တာကို ကျော်နိုင်တဲ့ အကောင်းဆုံးနည်းပဲ
            bg_clip = clip.resized(width=100) # အရင်သေးလိုက်မယ်
            bg_clip = bg_clip.resized(width=target_size[0] * 1.2) # ပြီးမှ ပြန်ကြီးလိုက်ရင် blur ဖြစ်သွားမယ်
            bg_clip = bg_clip.with_effects([vfx.MultiplyColor(0.4)]) # နည်းနည်း မှောင်ပေးမယ်
            bg_clip = bg_clip.cropped(x_center=bg_clip.w/2, y_center=bg_clip.h/2, width=target_size[0], height=target_size[1])
            
            v_ratio, t_ratio = clip.w/clip.h, target_size[0]/target_size[1]
            fg_clip = clip.resized(width=target_size[0]) if v_ratio > t_ratio else clip.resized(height=target_size[1])
            video = CompositeVideoClip([bg_clip, fg_clip.with_position("center")], size=target_size)
        else:
            video = clip

        # [2] Font Selection
        font_dir = "fonts"
        font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))] if os.path.exists(font_dir) else []
        selected_font = None
        if font_files:
            print("\n[Select Font]")
            for i, f in enumerate(font_files): print(f"{i+1}. {f}")
            f_idx = int(input("Font No (Default 1): ") or 1) - 1
            selected_font = os.path.join(font_dir, font_files[f_idx])

        # [3] Subtitles (Manual Size)
        if os.path.exists(script_in) and input("\n💬 Add Subtitles? (y/n): ").lower() == 'y':
            sub_size = int(input(f"Subtitle Size (Default {int(video.h*0.045)}): ") or int(video.h*0.045))
            sub_list = []
            with open(script_in, "r", encoding="utf-8") as f:
                for line in f:
                    p = line.strip().split("|")
                    if len(p) >= 3:
                        tr, txt = p[0].strip("[]").split("-"), p[2]
                        sub = TextClip(text=txt, font_size=sub_size, color='white', font=selected_font,
                                      bg_color='black', size=(int(video.w*0.85), None), method='caption'
                                      ).with_start(float(tr[0])).with_end(float(tr[1])).with_position(('center', int(video.h*0.85)))
                        sub_list.append(sub)
            video = CompositeVideoClip([video] + sub_list)

        # [4] Logo logic
        if input("\n🖼️ Add Logo? (y/n): ").lower() == 'y':
            if os.path.exists(user_logo):
                logo = (ImageClip(user_logo).resized(height=int(video.h * 0.08)).with_opacity(0.8)
                        .with_duration(video.duration).with_position(("right", "top")))
                video = CompositeVideoClip([video, logo])
            else:
                print("\n⚠️ ALERT: Logo မတွေ့ပါဘူး Dude! Telegram message box ကနေ ပို့ပေးထားပါ။")

        # [5] Manual Copyright Shield
        print("\n[🛡️ Copyright Shield]")
        if input("1. Mirror Flip? (y/n): ").lower() == 'y': video = video.with_effects([vfx.MirrorX()])
        if input("2. Zoom (1.08x)? (y/n): ").lower() == 'y': video = video.resized(1.08)
        if input("3. Color Boost? (y/n): ").lower() == 'y': video = video.with_effects([vfx.MultiplyColor(1.06)])

        # [6] Audio Logic (Syncing...)
        if os.path.exists(audio_dir):
            # ... audio processing logic ...
            pass

        # [7] Final High-Res Rendering (Optimized for Speed)
        print(f"\n🚀 Rendering High-Res Asset... 00K စက်ရုံ Full Power သုံးနေပြီ!")
        
        # Threads ကို ၈ ထိ တိုးလိုက်မယ် (မင်းဖုန်းက core များရင် အများကြီး ပိုမြန်မယ်)
        video.write_videofile(out_file, 
                             codec="libx264", 
                             audio_codec="aac", 
                             fps=24, 
                             preset="ultrafast", 
                             threads=8, 
                             logger='bar')
        
        print(f"\n✅ SUCCESS: {out_file}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    u_id = input("Enter User ID: ").strip()
    assemble_video(u_id)
