# 🎧 Video Subtitle Generator (MP4 to VTT)

Một công cụ Python giúp bạn:

- Chuyển đổi video `.mp4` thành `.mp3`
- Tách giọng nói thành văn bản
- Tạo file phụ đề `.vtt`
- Phát lại video kèm phụ đề trong trình duyệt

## ⚙️ Tính năng chính

✅ Phân tích thông tin âm thanh: tên file, kích thước, thời lượng, tần số...  
✅ Tự động chuyển `.mp4` → `.mp3` → `.wav` để nhận dạng giọng nói  
✅ Chia nhỏ âm thanh thành các đoạn (mặc định: 2 phút mỗi đoạn)  
✅ Tạo file phụ đề `.vtt` tương thích với HTML5  
✅ Tự động mở trình duyệt để phát lại video có phụ đề

## 🧱 Cài đặt thư viện

```bash
pip install pydub speechrecognition moviepy
```

> **Yêu cầu:**  
> - `ffmpeg` bắt buộc để `pydub` và `moviepy` hoạt động đúng. Tải tại: https://ffmpeg.org  
> - Sau khi cài, hãy đảm bảo `ffmpeg` nằm trong biến môi trường `PATH`.

## ▶️ Cách sử dụng

1. Chạy chương trình:

```bash
python script.py
```

2. Khi được hỏi, nhập vào đường dẫn tới file `.mp4` hoặc `.mp3`

3. Chương trình sẽ:
   - Nếu là `.mp4`: chuyển thành `.mp3`
   - Phân tích file âm thanh
   - Tách giọng nói và tạo file `.vtt`
   - Xóa file `.mp3` trung gian (nếu cần)
   - Mở trình duyệt tại `http://localhost:8000/index.html` để phát video kèm phụ đề

## 📁 Cấu trúc đầu ra

Giả sử đầu vào là `video.mp4`, chương trình sẽ tạo:

- `video.mp3`: âm thanh tách ra (tạm thời)
- `video.vtt`: phụ đề được tạo
- Mã HTML riêng (`index.html`) để phát video kèm phụ đề

## 🌐 Phát video kèm phụ đề

Tạo một file `index.html` như sau:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Phát Video</title>
</head>
<body>
  <video controls width="800">
    <source src="video.mp4" type="video/mp4">
    <track src="video.vtt" kind="subtitles" srclang="vi" label="Tiếng Việt" default>
    Trình duyệt không hỗ trợ video.
  </video>
</body>
</html>
```

Khởi chạy máy chủ tĩnh:

```bash
python -m http.server 8000
```

## 📝 Ghi chú

- Hệ thống sử dụng Google Speech Recognition API miễn phí (giới hạn truy vấn)
- Nếu không có âm thanh trong file MP4, quá trình sẽ dừng
- Mặc định nhận diện tiếng Việt (`vi-VN`). Có thể thay đổi nếu cần

## 📄 Giấy phép

Mã nguồn này được phân phối theo [MIT License](https://opensource.org/licenses/MIT)
