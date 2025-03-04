from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
import numpy as np
import cv2

class ThreadStream(QThread):
    def __init__(self, video_view, fps_label):
        super().__init__()
        self.video_view = video_view  # Thay video_label bằng video_view
        self.fps_label = fps_label
        self.running = True

        # Tạo QGraphicsScene
        self.scene = QGraphicsScene()
        self.video_view.setScene(self.scene)  # Gán Scene vào QGraphicsView
        self.pixmap_item = QGraphicsPixmapItem()  # Tạo đối tượng QGraphicsPixmapItem
        self.scene.addItem(self.pixmap_item)  # Thêm vào Scene

    def display_frame(self, frame, fps):
        if not self.running:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Cập nhật hình ảnh trong QGraphicsScene
        self.pixmap_item.setPixmap(QPixmap.fromImage(qimg))
        self.video_view.setScene(self.scene)  # Cập nhật scene

        # Cập nhật FPS
        self.fps_label.setText(f"FPS: {fps:.2f}")