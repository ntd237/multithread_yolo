import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from capture_thread import ThreadCapture
from process_thread import ThreadProcess
from stream_thread import ThreadStream

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Khởi tạo các luồng
        self.capture_thread = ThreadCapture(video_path="data/XLBM.CAM.06.avi")
        self.process_thread = ThreadProcess()
        self.stream_thread = ThreadStream(self.video_view, self.fps_label)  

        # Kết nối tín hiệu
        self.capture_thread.new_frame.connect(self.process_thread.process_frame)
        self.process_thread.processed_frame.connect(self.stream_thread.display_frame)

        # Bắt đầu các luồng
        self.capture_thread.start()
        self.process_thread.start()
        self.stream_thread.start()

    def init_ui(self):
        """Khởi tạo giao diện PyQt5"""
        self.setWindowTitle("Multi-threaded Video Processing")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        self.video_view = QGraphicsView(self)  
        
        self.fps_label = QLabel("FPS: 0", self)

        layout = QVBoxLayout()
        layout.addWidget(self.video_view)
        layout.addWidget(self.fps_label)
        self.setLayout(layout)
        
    def closeEvent(self, event):
        """Dừng các luồng khi đóng ứng dụng"""
        self.capture_thread.stop()
        self.process_thread.stop()
        self.stream_thread.running = False
        event.accept() # chấp nhận sự kiện đóng cửa sổ

    def resizeEvent(self, event):
        """Cập nhật kích thước video khi cửa sổ thay đổi"""
        if self.video_view.scene():
            self.video_view.fitInView(self.video_view.scene().sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec_())
