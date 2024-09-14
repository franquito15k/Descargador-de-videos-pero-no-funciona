from flask import Flask, render_template, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Configura la ruta de descarga temporal
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Función para descargar el video usando yt-dlp
def download_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# Ruta principal que devuelve la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para recibir la URL por POST y devolver el archivo descargado
@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No se proporcionó una URL"}), 400

    try:
        filename = download_video(url)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
