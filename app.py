from flask import Flask, render_template, request, jsonify, send_file
from yt_dlp import YoutubeDL
from io import BytesIO

app = Flask(__name__)

# Función para descargar el video usando yt-dlp y devolverlo como BytesIO
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '-'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = f"{info['title']}.{info['ext']}"
        ydl.download([url])

        # Enviar el archivo en memoria
        video_file = BytesIO()
        with open(filename, 'rb') as f:
            video_file.write(f.read())
        video_file.seek(0)
        return video_file, filename

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
        video_file, filename = download_video(url)
        return send_file(video_file, download_name=filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
