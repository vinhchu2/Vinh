import os
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import VideoFileClip


def get_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_sec = len(audio) / 1000
    file_size = os.path.getsize(file_path) / (1024 * 1024)

    info = {
        "Tên file": os.path.basename(file_path),
        "Kích thước (MB)": round(file_size, 2),
        "Thời lượng (giây)": round(duration_sec, 2),
        "Kênh âm thanh": audio.channels,
        "Tần số lấy mẫu (Hz)": audio.frame_rate,
        "Độ rộng mẫu (byte)": audio.sample_width,
        "Định dạng": file_path.split('.')[-1]
    }

    return info


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace('.', ',')


def convert_mp4_to_mp3(mp4_path):
    if not os.path.exists(mp4_path):
        print(f"❌ File '{mp4_path}' không tồn tại.")
        return None

    mp3_path = mp4_path.replace(".mp4", ".mp3")
    try:
        video = VideoFileClip(mp4_path)
        if video.audio is None:
            print("❌ Video không có âm thanh.")
            return None
        video.audio.write_audiofile(mp3_path, codec='libmp3lame')
        print(f"🎵 Đã chuyển đổi thành công: {mp3_path}")
        return mp3_path
    except Exception as e:
        print(f"❌ Lỗi khi chuyển MP4 sang MP3: {e}")
        return None


def transcribe_to_vtt(file_path, chunk_ms=120000, language_code="vi-VN"):
    recognizer = sr.Recognizer()

    # Bước 1: Chuyển MP3 sang WAV
    audio = AudioSegment.from_mp3(file_path)
    wav_path = file_path.replace(".mp3", ".wav")
    audio.export(wav_path, format="wav")

    # Bước 2: Cắt thành các đoạn nhỏ
    full_audio = AudioSegment.from_wav(wav_path)
    chunks = [full_audio[i:i + chunk_ms] for i in range(0, len(full_audio), chunk_ms)]

    print(f"Tổng số đoạn cần nhận dạng: {len(chunks)}")

    vtt_lines = ["WEBVTT\n"]

    for i, chunk in enumerate(chunks):
        start_time = i * (chunk_ms / 1000)
        end_time = start_time + (len(chunk) / 1000)

        chunk_filename = f"chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")

        try:
            with sr.AudioFile(chunk_filename) as source:
                audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data, language=language_code, show_all=True)
                if isinstance(text, dict) and "alternative" in text:
                    text = text["alternative"][0].get("transcript", "")
                else:
                    text = "[Không có kết quả rõ ràng]"
                print(f"Đoạn {i + 1}/{len(chunks)}: Nhận dạng thành công.")
            except sr.UnknownValueError:
                text = "[Không hiểu đoạn âm thanh]"
                print(f"Đoạn {i + 1}/{len(chunks)}: Không hiểu.")
            except sr.RequestError as e:
                text = f"[Lỗi khi gửi yêu cầu: {e}]"
                print(f"Đoạn {i + 1}/{len(chunks)}: Lỗi gửi yêu cầu.")
        finally:
            if os.path.exists(chunk_filename):
                try:
                    os.remove(chunk_filename)
                except Exception as e:
                    print(f"⚠️ Không thể xóa file tạm: {chunk_filename} ({e})")

        vtt_lines.append(f"{format_time(start_time)} --> {format_time(end_time)}\n{text}\n")

    if os.path.exists(wav_path):
        try:
            os.remove(wav_path)
        except Exception as e:
            print(f"⚠️ Không thể xóa file WAV: {wav_path} ({e})")

    # Ghi ra file VTT
    vtt_path = file_path.replace(".mp3", ".vtt")
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_lines))

    print(f"\n✅ File phụ đề đã lưu tại: {vtt_path}")


if __name__ == "__main__":
    file_input = input("Nhập tên file MP3 hoặc MP4: ").strip()

    if not os.path.exists(file_input):
        print(f"❌ File '{file_input}' không tồn tại.")
    else:
        if file_input.lower().endswith(".mp4"):
            mp3_file = convert_mp4_to_mp3(file_input)
        elif file_input.lower().endswith(".mp3"):
            mp3_file = file_input
        else:
            print("❌ Chỉ hỗ trợ file .mp3 hoặc .mp4")
            mp3_file = None

        if mp3_file:
            info = get_audio_info(mp3_file)
            print("📊 Thông tin file âm thanh:")
            for key, value in info.items():
                print(f"{key}: {value}")

            print("\n⏳ Bắt đầu chuyển giọng nói thành phụ đề (file .vtt)...")
            transcribe_to_vtt(mp3_file)
