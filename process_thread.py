import cv2
import time
import torch
import queue
from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO
from utils import draw_results

class ThreadProcess(QThread):
    processed_frame = pyqtSignal(object, float)
    video_saved = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = YOLO("models/yolov8m.pt")
        self.running = True
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.frame_queue = queue.Queue(maxsize=5)  # Giới hạn queue để tránh tràn bộ nhớ
        self.video_writer = None
        self.fps_target = 30  # FPS mong muốn

    def process_frame(self, frame):
        if not self.running:
            return
        
        # Đưa frame vào queue để xử lý
        if not self.frame_queue.full():
            self.frame_queue.put(frame)
        
    def run(self):
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                start_time = time.time()
                
                with torch.inference_mode():  # Giảm tải tính toán
                    results = self.model(frame, device=self.device)
                
                fps = 1.0 / (time.time() - start_time)
                processed_frame = draw_results(frame, results, fps)
                
                # Ghi frame vào file video
                if self.video_writer is None:
                    height, width, _ = frame.shape
                    self.video_writer = cv2.VideoWriter('results/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps_target, (width, height))
                self.video_writer.write(processed_frame)
                
                self.processed_frame.emit(processed_frame, fps)
                
                # Điều chỉnh tốc độ xử lý
                elapsed = time.time() - start_time
                sleep_time = max(0, (1.0 / self.fps_target) - elapsed)
                time.sleep(sleep_time)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
            self.video_saved.emit()

"""
Tóm tắt luồng hoạt động
- Nhận frame từ capture_thread:
    Frame được đưa vào hàng đợi (self.frame_queue)
- Xử lý với YOLOv8:
    Lấy frame ra khỏi hàng đợi
    Dự đoán đối tượng trong frame
    Vẽ kết quả lên frame
    Tính toán FPS
- Ghi video & gửi frame đã xử lý:
    Nếu chưa có video_writer, tạo mới
    Lưu frame vào video output.mp4
    Gửi frame và FPS đến giao diện chính
- Điều chỉnh tốc độ xử lý:
    Đảm bảo video chạy đúng tốc độ (30 FPS)
- Dừng thread:
    Dừng vòng lặp xử lý khi stop() được gọi
    Giải phóng bộ nhớ và kết thúc ghi video
"""