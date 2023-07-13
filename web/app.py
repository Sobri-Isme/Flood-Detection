from flask import Flask, render_template, Response
from routes.prediction_routes import prediction_bp
import cv2
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.register_blueprint(prediction_bp, url_prefix='/prediction')

# Load model yang telah dilatih sebelumnya
model = tf.keras.models.load_model('C:/Users/user/PycharmProjects/deteksibanjir/output/deteksibanjirfinal.h5')

# Set ukuran citra masukan pada model
img_size = (150, 150)

# Membuat dictionary untuk label kelas
class_dict = {
    0: 'Normal',
    1: 'Banjir'
}

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        # Baca setiap frame dari kamera
        ret, frame = cap.read()

        if not ret:
            break

        # Ubah warna citra menjadi RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize citra sesuai dengan ukuran masukan pada model
        img = cv2.resize(img, img_size)

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

        # Tampilkan hasil prediksi pada frame
        cv2.putText(frame, pred_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Konversi frame menjadi format yang dapat ditampilkan di web
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Menghasilkan frame sebagai streaming video
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Jika tombol 'q' ditekan, keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Tutup kamera
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
