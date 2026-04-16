import os
from faster_whisper import WhisperModel

def transcribe_audio(user_id):
    user_dir = os.path.join("users_workspace", str(user_id))
    audio_file = os.path.join(user_dir, "original_audio.mp3")
    transcript_path = os.path.join(user_dir, "transcription.txt")

    if not os.path.exists(audio_file): return

    print(f"🧠 AI Transcription for User {user_id}...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_file, beam_size=5, vad_filter=True)

    with open(transcript_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}\n")
    print(f"✅ Step 2 Done: {transcript_path}")

if __name__ == "__main__":
    u_id = input("User ID: ")
    transcribe_audio(u_id)
