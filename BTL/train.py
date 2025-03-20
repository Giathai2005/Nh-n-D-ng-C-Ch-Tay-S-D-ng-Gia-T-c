import os
import numpy as np
import joblib  # Dùng thay cho sklearn.externals.joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
from scipy.interpolate import interp1d
from tqdm import tqdm  # Thêm thư viện hiển thị tiến trình

# === 1. Chuẩn bị dữ liệu ===
data_root = "/content/drive/My Drive/data"  # Thư mục chứa dữ liệu
x_data, y_data = [], []
classes = {}
fixed_rows = 50  # Số dòng cố định
num_columns = 16  # Số cột cố định
fixed_size = fixed_rows * num_columns

# Lặp qua tất cả file trong thư mục
def load_data_from_folder(folder_path):
    label_index = 0  # Gán chỉ số nhãn bắt đầu từ 0
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    for filename in tqdm(files, desc="Đang tải dữ liệu", unit="file"):
        path = os.path.join(folder_path, filename)
        data = np.loadtxt(path)
        
        # Kiểm tra số cột hợp lệ
        if data.shape[1] != num_columns:
            print(f"⚠️ Bỏ qua file {filename} do không đủ {num_columns} cột dữ liệu")
            continue
        
        # Xử lý nội suy hoặc cắt bớt dữ liệu để có số dòng cố định
        current_rows = data.shape[0]
        if current_rows < fixed_rows:
            x_old = np.linspace(0, 1, current_rows)
            x_new = np.linspace(0, 1, fixed_rows)
            data_interp = np.array([interp1d(x_old, data[:, i], fill_value="extrapolate")(x_new) for i in range(num_columns)]).T
        else:
            data_interp = data[:fixed_rows, :]
        
        # Chuyển dữ liệu thành mảng 1D
        flat_data = data_interp.flatten()
        x_data.append(flat_data)  # Thêm vào danh sách
        
        # Lấy tên file làm nhãn
        category = filename.split(".")[0]  # Lấy phần trước ".txt"
        if category not in classes.values():
            classes[label_index] = category
            label_index += 1
        
        label = list(classes.keys())[list(classes.values()).index(category)]
        y_data.append(label)

# Đọc dữ liệu từ thư mục chính
load_data_from_folder(data_root)

# Chuyển thành mảng NumPy
x_data = np.array(x_data)
y_data = np.array(y_data)

# === 2. Huấn luyện mô hình ===
print("🔄 Đang huấn luyện mô hình...")
X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=0)
clf = svm.SVC(kernel="rbf", C=1, probability=True)
clf.fit(X_train, Y_train)
print("✅ Huấn luyện xong!")

# Lưu mô hình lên Google Drive
model_path = "/content/drive/My Drive/model_123456.pkl"
classes_path = "/content/drive/My Drive/classes_123456.pkl"
joblib.dump(clf, model_path)
joblib.dump(classes, classes_path)
print(f"🎯 Mô hình đã được lưu tại: {model_path}")

# === 3. Dự đoán trên dữ liệu mẫu ===
print("🔎 Thử nghiệm dự đoán...")
clf = joblib.load(model_path)
classes = joblib.load(classes_path)

# Chọn một file ngẫu nhiên từ dữ liệu để dự đoán
sample_file = next(iter(os.listdir(data_root)))
sample_path = os.path.join(data_root, sample_file)
sample = np.loadtxt(sample_path)

if sample.shape[1] != num_columns:
    print(f"⚠️ Dữ liệu dự đoán {sample_file} không hợp lệ (không đủ {num_columns} cột)")
else:
    current_rows = sample.shape[0]
    if current_rows < fixed_rows:
        x_old = np.linspace(0, 1, current_rows)
        x_new = np.linspace(0, 1, fixed_rows)
        sample_interp = np.array([interp1d(x_old, sample[:, i], fill_value="extrapolate")(x_new) for i in range(num_columns)]).T
    else:
        sample_interp = sample[:fixed_rows, :]
    
    sample = sample_interp.flatten().reshape(1, -1)
    prediction = clf.predict(sample)
    predicted_label = classes[prediction[0]]
    
    print(f"Dự đoán: {predicted_label}")
    print(f"📂 File được sử dụng để dự đoán: {sample_file}")
