import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadCapture(QThread):
    new_frame = pyqtSignal(object)

    def __init__(self, video_path):
        super().__init__()
        # self.cap = cv2.VideoCapture(video_path)
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
        self.running = True

    def run(self):
        while self.running and self.cap.isOpened():
            start_time = time.time()
            
            ret, frame = self.cap.read()
            if not ret:
                break

            self.new_frame.emit(frame)
            
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1 / 30) - elapsed_time)  # Đảm bảo không quá 30 FPS
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


"""
tóm tắt luồng hoạt động
- Khởi động thread:
    Khi gọi ThreadCapture.start(), PyQt5 sẽ chạy hàm run() trong luồng riêng
- Xử lý video:
    Mở video bằng cv2.VideoCapture()
    Liên tục đọc từng khung hình
    Gửi khung hình qua new_frame.emit(frame)
    Đảm bảo tốc độ phát không vượt quá 30 FPS bằng cách tính thời gian và sleep
- Dừng thread:
    Khi gọi stop(), đặt self.running = False, thoát vòng lặp, dừng thread
"""
