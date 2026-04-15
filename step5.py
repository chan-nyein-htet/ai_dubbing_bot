import os
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip, ImageClip
import moviepy.video.fx as vfx

def assemble_video():
    user_dir = "downloads"
    vid_in = os.path.join(user_dir, "old_video.mp4")
    script_in = os.path.join(user_dir, "sync_voiceover_script.txt")
    audio_segments_dir = os.path.join(user_dir, "audio_segments")
    logo_in = os.path.join(user_dir, "logo.png")
    out_file = os.path.join(user_dir, "final_ready.mp4")

    if not os.path.exists(vid_in):
        print(f"❌ Error: {vid_in} missing.")
        return

    try:
        print("\n" + "="*50)
        print("🎬  PROFESSIONAL VIDEO EDITOR (BUSINESS MODE)")
        print("="*50)

        video = VideoFileClip(vid_in)
        
        # --- [1] Font Selection ---
        font_dir = "fonts"
        font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
        print("\n[1] Select Font:")
        for i, f in enumerate(font_files):
            print(f"{i+1}. {f}")
        font_choice = int(input("Font နံပါတ်ရွေးပါ: ") or 1) - 1
        selected_font = os.path.join(font_dir, font_files[font_choice])

        # --- [2] Ratio & Style ---
        print("\n[2] Select Video Format:")
        print("1. Original Ratio")
        print("2. 9:16 (TikTok/Reels - Blurred Background)")
        print("3. 16:9 (YouTube - Standard Wide)")
        ratio_choice = input("Choice (1, 2, 3): ") or "1"

        if ratio_choice == "2":
            target_w, target_h = 1080, 1920
            # v2.0 stable: Blur effect ကို ခဏဖယ်ပြီး formatting ကို အရင်ညှိမယ်
            bg = video.resized(height=target_h)
            bg = bg.cropped(x_center=bg.w/2, y_center=bg.h/2, width=target_w, height=target_h)
            fg = video.resized(width=target_w)
            video = CompositeVideoClip([bg, fg.with_position("center")], size=(target_w, target_h))
        elif ratio_choice == "3":
            video = video.resized(width=1280) if video.w < video.h else video

        # --- [3] Copyright Shield (Integer Bug Fix) ---
        shield = input("\n🛡️ Apply Mirror + Zoom (Copyright Shield)? (y/n): ").lower() == 'y'
        if shield:
            # v2.0 မှာ integer height/width ပဲ လက်ခံလို့ round လုပ်ပေးရတယ် Dude
            new_w = int(video.w * 1.08)
            video = video.with_effects([vfx.MirrorX()]).resized(width=new_w)

        layers = [video]

        # --- [4] Audio & Subtitles Logic ---
        has_audio = os.path.exists(audio_segments_dir) and len(os.listdir(audio_segments_dir)) > 0
        
        if has_audio:
            print("\n🎙️ Status: AI Dubbing detected.")
            add_subs = input("Dubbing အပေါ်မှာ Subtitles ပါ ထပ်ထည့်မလား? (y/n): ").lower() == 'y'
            
            audio_clips = []
            with open(script_in, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    parts = line.strip().split("|")
                    if len(parts) < 3: continue
                    start_t = float(parts[0].replace("[", "").replace("]", "").split("-")[0])
                    seg_path = os.path.join(audio_segments_dir, f"segment_{i}.mp3")
                    if os.path.exists(seg_path):
                        audio_clips.append(AudioFileClip(seg_path).with_start(start_t))
            
            video = video.with_audio(CompositeAudioClip(audio_clips))
            layers[0] = video # Base layer update

            if add_subs:
                with open(script_in, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) < 3: continue
                        t_range = parts[0].replace("[", "").replace("]", "").split("-")
                        txt = TextClip(text=parts[2], font_size=32, color='white', font=selected_font,
                                       bg_color='black', size=(int(video.w*0.8), None), method='caption'
                                       ).with_start(float(t_range[0])).with_end(float(t_range[1])).with_position(('center', int(video.h*0.82)))
                        layers.append(txt)
        else:
            print("\n💬 Status: Subtitles Only Mode.")
            with open(script_in, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) < 3: continue
                    t_range = parts[0].replace("[", "").replace("]", "").split("-")
                    txt = TextClip(text=parts[2], font_size=34, color='white', font=selected_font,
                                   bg_color='black', size=(int(video.w*0.8), None), method='caption'
                                   ).with_start(float(t_range[0])).with_end(float(t_range[1])).with_position(('center', int(video.h*0.82)))
                    layers.append(txt)

        # --- [5] Logo Overlay ---
        if os.path.exists(logo_in):
            print("🖼️ Logo detected. Adding overlay...")
            logo = ImageClip(logo_in).with_duration(video.duration).resized(height=int(video.h*0.1)).with_opacity(0.8)
            layers.append(logo.with_position(("right", "top"), margin=30))

        # Final Render
        print(f"\n💾 Rendering Final Output...")
        final_video = CompositeVideoClip(layers, size=video.size)
        final_video.write_videofile(out_file, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", threads=4)
        print(f"\n✅ Done: {out_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    assemble_video()

