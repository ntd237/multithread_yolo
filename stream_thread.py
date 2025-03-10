from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
import numpy as np
import cv2

class ThreadStream(QThread):
    def __init__(self, video_view, fps_label):
        super().__init__()
        self.video_view = video_view  
        self.fps_label = fps_label
        self.running = True

        # Tạo QGraphicsScene
        self.scene = QGraphicsScene()
        self.video_view.setScene(self.scene)  
        self.pixmap_item = QGraphicsPixmapItem()  
        self.scene.addItem(self.pixmap_item)  
    def display_frame(self, frame, fps):
        if not self.running:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape # Lấy kích thước hình ảnh
        bytes_per_line = 3 * width # mỗi pixel có 3 kênh màu (RGB)
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Cập nhật hình ảnh trong QGraphicsScene
        self.pixmap_item.setPixmap(QPixmap.fromImage(qimg))
        self.video_view.setScene(self.scene)  

        # Cập nhật FPS
        self.fps_label.setText(f"FPS: {fps:.2f}")

"""
tóm tắt luồng hoạt động
- Nhận frame từ process_thread.py:
    display_frame(frame, fps) được gọi khi có frame mới
- Chuyển đổi frame:
    Chuyển từ BGR (OpenCV) sang RGB (PyQt)
    Tạo QImage để hiển thị
- Cập nhật giao diện:
    Cập nhật hình ảnh trong QGraphicsScene
    Hiển thị FPS
- Lặp lại quá trình này với frame tiếp theo
"""