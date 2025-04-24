from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TDRC

def read_mp3_info(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)

        print(f"\n==> Đọc thông tin từ: {file_path}")
        print(f"Thời lượng: {audio.info.length:.2f} giây")
        print(f"Tốc độ bit: {audio.info.bitrate} bps")
        print(f"Tần số mẫu: {audio.info.sample_rate} Hz")

        tags = audio.tags
        if tags:
            print("------ Thông tin ID3 ------")
            print("Tên bài hát:", tags.get("TIT2", "Không có"))
            print("Ca sĩ:", tags.get("TPE1", "Không có"))
            print("Album:", tags.get("TALB", "Không có"))
            print("Track:", tags.get("TRCK", "Không có"))
            print("Năm:", tags.get("TDRC", "Không có"))
        else:
            print("Không có thẻ ID3 trong file.")

    except Exception as e:
        print(" Lỗi khi đọc file MP3:", e)

# Nhập đường dẫn sau khi chạy
if __name__ == "__main__":
    file_path = input("Nhập tên file MP3: ")
    read_mp3_info(file_path)
