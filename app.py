import logging
import os
from flask import Flask, render_template, request, send_from_directory, abort
import yt_dlp

app = Flask(__name__, template_folder='templates')

logging.basicConfig(level=logging.INFO)

# Diretório de download (Linux-friendly)
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'musicas')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def my_hook(d):
    if d['status'] == 'downloading':
        pass
    if d['status'] == 'finished':
        app.logger.info("Download finalizado, convertendo...")

def download_audio(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [my_hook],
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # O arquivo final é o .mp3 após conversão
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            return os.path.basename(mp3_filename)
    except Exception as e:
        app.logger.error(f"Erro durante o download: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    filename = download_audio(video_url, DOWNLOAD_DIR)
    if filename is None:
        return "Erro no download, verifique os logs.", 500

    # Envia o arquivo para o cliente baixar
    try:
        return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
