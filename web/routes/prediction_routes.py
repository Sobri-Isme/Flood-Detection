from flask import Blueprint, jsonify, request
import cv2
import tensorflow as tf
import numpy as np
import base64

prediction_bp = Blueprint('prediction', __name__)

# Load model yang telah dilatih sebelumnya
model = tf.keras.models.load_model('C:/Users/user/PycharmProjects/deteksibanjir/output/deteksibanjirfinal.h5')

# Buka kamera dengan nomor indeks 0
cap = cv2.VideoCapture(0)

# Set ukuran citra masukan pada model
img_size = (150, 150)

# Membuat dictionary untuk label kelas
class_dict = {
    0: 'Normal',
    1: 'Banjir'
}

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    image_data = request.form['imageData']

    # Mengubah data gambar dari string base64 ke array numpy
    _, image_encoded = image_data.split(",")
    image_decoded = base64.b64decode(image_encoded)
    nparr = np.frombuffer(image_decoded, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize citra sesuai dengan ukuran masukan pada model
    img = cv2.resize(image, img_size)

    # Konversi citra menjadi array numpy
    img_array = np.array(img)

    # Normalisasi citra
    img_array = img_array / 255.0

    # Tambahkan dimensi baru pada array citra
    img_array = np.expand_dims(img_array, axis=0)

    # Lakukan prediksi pada citra
    pred = model.predict(img_array)

    # Ambil indeks kelas dengan nilai prediksi tertinggi
    pred_class = np.argmax(pred)

    # Ambil label kelas berdasarkan indeks kelas
    pred_label = class_dict[pred_class]

    # Mengembalikan hasil prediksi dalam format JSON
    return jsonify({'prediction': pred_label})
