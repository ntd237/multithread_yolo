from ultralytics import YOLO
import os

# Tạo thư mục models nếu chưa có
os.makedirs("models", exist_ok=True)

# Tải lại mô hình từ nguồn chính thức
model = YOLO("yolov8x.pt")

# Kiểm tra xem mô hình có tải đúng không
if os.path.exists("yolov8x.pt"):
    os.rename("yolov8x.pt", "models/yolov8x.pt")
    print("Mô hình đã tải lại thành công!")
else:
    print("Lỗi tải mô hình. Hãy kiểm tra lại kết nối internet.")
