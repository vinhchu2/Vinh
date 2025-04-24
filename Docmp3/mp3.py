from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TDRC

# Đường dẫn tới file MP3
file_path = r"C:\Users\1vinh\Downloads\OnlyLonelyMe-LySupVuPhungTien-6011775.mp3"  # Thay bằng đường dẫn thực tế của bạn

# Tải file MP3
audio = MP3(file_path, ID3=ID3)

# In thông tin cơ bản
print(f"Thời lượng: {audio.info.length:.2f} giây")
print(f"Tốc độ bit: {audio.info.bitrate} bps")
print(f"Tần số mẫu: {audio.info.sample_rate} Hz")
