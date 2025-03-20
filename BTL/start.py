#import serial
import numpy as np
import joblib
from scipy.interpolate import interp1d
import os

# === 1. Cấu hình cổng Serial ===
#SERIAL_PORT = "/dev/ttyUSB0"  # Thay bằng cổng Serial thực tế (Windows: COM3, Linux: /dev/ttyUSB0)
#BAUD_RATE = 115200

# === 2. Tải mô hình AI ===
MODEL_PATH = "/content/drive/My Drive/model_123456.pkl"
CLASSES_PATH = "/content/drive/My Drive/classes_123456.pkl"
clf = joblib.load(MODEL_PATH)
classes = joblib.load(CLASSES_PATH)

# === 3. Định dạng dữ liệu ===
FIXED_ROWS = 50  # Số dòng cố định
NUM_COLUMNS = 16  # Số cột cố định

# === 4. Đọc dữ liệu từ thiết bị ngoại vi ===
def read_sensor_data(ser):
    data_list = []
    while len(data_list) < FIXED_ROWS:
        try:
            line = ser.readline().decode().strip()
            values = list(map(float, line.split(',')))
            if len(values) == NUM_COLUMNS:
                data_list.append(values)
        except:
            continue
    return np.array(data_list)

# === 5. Xử lý và dự đoán ===
def preprocess_and_predict(data):
    current_rows = data.shape[0]
    if current_rows < FIXED_ROWS:
        x_old = np.linspace(0, 1, current_rows)
        x_new = np.linspace(0, 1, FIXED_ROWS)
        data_interp = np.array([interp1d(x_old, data[:, i], fill_value="extrapolate")(x_new) for i in range(NUM_COLUMNS)]).T
    else:
        data_interp = data[:FIXED_ROWS, :]
    
    sample = data_interp.flatten().reshape(1, -1)
    prediction = clf.predict(sample)
    return classes[prediction[0]]

# === 6. Chạy chương trình chính ===
if __name__ == "__main__":
    mode = input("Chọn chế độ (1: Thiết bị ngoại vi, 2: File có sẵn): ")
    
    if mode == "1":
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("📡 Đang đọc dữ liệu từ thiết bị...")
        while True:
            sensor_data = read_sensor_data(ser)
            predicted_label = preprocess_and_predict(sensor_data)
            print(f"📌 Dự đoán: {predicted_label}")
            ser.write(predicted_label.encode() + b'\n')
    
    elif mode == "2":
        file_path = input("Nhập đường dẫn file dữ liệu: ")
        if os.path.exists(file_path):
            data = np.loadtxt(file_path)
            if data.shape[1] != NUM_COLUMNS:
                print("⚠️ File không hợp lệ (không đủ số cột)")
            else:
                predicted_label = preprocess_and_predict(data)
                print(f"📌 Dự đoán từ file: {predicted_label}")
        else:
            print("❌ File không tồn tại!")
