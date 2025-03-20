# Hệ thống Nhận diện Cử chỉ Tay Quân đội bằng Arduino Mega & SVM
<img src="https://github.com/user-attachments/assets/db53adff-8dd4-4b7b-971d-1b189f31d1be" alt="Đại-Nam-University" width="450"/>
<img src="https://github.com/user-attachments/assets/3ba4abb5-fa53-4c90-9775-7b14cc4c36b6" alt="AIOT-LAB" width="450"/>


## 📌 Giới thiệu
Hệ thống nhận diện cử chỉ tay quân đội là một dự án kết hợp giữa phần cứng (Arduino Mega, MPU6050, cảm biến flex) và phần mềm (Python, Scikit-learn) để phân loại cử chỉ tay theo thời gian thực. Dữ liệu từ cảm biến được truyền tới máy tính để huấn luyện mô hình SVM nhằm phân loại chính xác các cử chỉ.  
<p align="center">
<img src="https://github.com/user-attachments/assets/1e674d67-e7d2-4ba0-b727-83eb47f93ffa" alt="Cử chỉ tay" width="450"/>
</p> 

## 🏗️ Hệ thống
### 📂 Cấu trúc dự án
📦 Project
├── 📂 Data # Thư mục chứa dữ liệu cảm biến đã thu thập  
├── 📂 Model # Lưu trữ mô hình đã huấn luyện  
├── train_svm.py # Huấn luyện mô hình SVM với dữ liệu thu thập  
├── classify_gesture.py # Nhận diện cử chỉ tay theo thời gian thực  
└── README.md # Hướng dẫn cài đặt và sử dụng

## ⚙️ Yêu cầu hệ thống
### 🔌 Phần cứng


- **Arduino Mega 2560** - Xử lý tín hiệu từ nhiều cảm biến
- **MPU6050** - Cảm biến IMU đo chuyển động tay
- **Cảm biến flex x7** - Đo độ cong của ngón tay
- **Điện trở & Breadboard** - Hỗ trợ kết nối mạch

### Hướng dẫn lắp đặt phần cứng
<img src="https://github.com/user-attachments/assets/4aadf77d-4a5e-431b-bd67-e0db7941a7b8" alt="Hướng Dẫn" width="450" />

### 💻 Phần mềm
- **Python 3.x** - Xử lý dữ liệu
- **Google Colab** - Traning model
- **Thư viện Python:** NumPy, Pandas, Scikit-learn, Matplotlib, PySerial

## 🚀 Hướng dẫn cài đặt & chạy
### 1️⃣ Chuẩn bị phần cứng
- Kết nối Arduino Mega với cảm biến MPU6050 & cảm biến flex
- Nạp mã Arduino từ thư mục `ArduinoCode` lên Arduino Mega

### 2️⃣ Cài đặt môi trường Python
```bash
pip install numpy pandas scikit-learn matplotlib pyserial
```
### 4️⃣ Huấn luyện mô hình SVM
```bash
python Scripts/train.py
```
- Tập dữ liệu được tiền xử lý và sử dụng để huấn luyện mô hình SVM
- Mô hình sau khi huấn luyện được lưu vào thư mục `Model`

### 5️⃣ Nhận diện cử chỉ tay
```bash
python Scripts/start.py
```
- Hệ thống sẽ dự đoán cử chỉ tay theo thời gian thực và hiển thị kết quả

## 📈 Cải tiến trong tương lai
- **Tối ưu hóa thuật toán SVM** để cải thiện độ chính xác
- **Tích hợp WiFi (ESP32)** để gửi dữ liệu cảm biến không dây
- **Tăng kích thước tập dữ liệu** để nâng cao khả năng tổng quát hóa

## 🏆 Người đóng góp
- **[Hà Tuấn Điệp]** - Triển khai toàn bộ mã nguồn, kiểm thử, triển khai dự án
- **[Đinh Thị Ngọc Bích]** - Thuyết trình
- **[Giàng A Dụng]** - Thiết kế powerpoint
- **[Nguyễn Gia Thái]** - viết overleaf

## 📜 Giấy phép
Dự án này được cấp phép theo MIT License.

