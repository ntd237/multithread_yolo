import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadCapture(QThread):
    new_frame = pyqtSignal(object)

    def __init__(self, video_path="data/video2.mp4"):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
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



