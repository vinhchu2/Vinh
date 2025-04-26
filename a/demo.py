import os
from pydub import AudioSegment
import speech_recognition as sr


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


def transcribe_to_vtt(file_path, chunk_ms=120000, language_code="vi-VN"):  # 2 phút mỗi đoạn
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

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data, language=language_code, show_all=True)  # Hiển thị tất cả kết quả
                print(f"Đoạn {i + 1}/{len(chunks)}: Nhận dạng thành công.")
            except sr.UnknownValueError:
                text = "[Không hiểu đoạn âm thanh]"
                print(f"Đoạn {i + 1}/{len(chunks)}: Không hiểu.")
            except sr.RequestError as e:
                text = f"[Lỗi khi gửi yêu cầu: {e}]"
                print(f"Đoạn {i + 1}/{len(chunks)}: Lỗi gửi yêu cầu.")

            vtt_lines.append(f"{format_time(start_time)} --> {format_time(end_time)}\n{text}\n")

        os.remove(chunk_filename)

    os.remove(wav_path)

    # Ghi ra file VTT
    vtt_path = file_path.replace(".mp3", ".vtt")
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_lines))

    print(f"\n✅ File phụ đề đã lưu tại: {vtt_path}")


if __name__ == "__main__":
    mp3_file = input("Nhập tên file MP3 (có đuôi .mp3): ").strip()

    if not os.path.exists(mp3_file):
        print(f"❌ File '{mp3_file}' không tồn tại.")
    else:
        info = get_audio_info(mp3_file)
        print("📊 Thông tin file âm thanh:")
        for key, value in info.items():
            print(f"{key}: {value}")

        print("\n⏳ Bắt đầu chuyển giọng nói thành phụ đề (file .vtt)...")
        transcribe_to_vtt(mp3_file)
