import logging
import os
from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__, template_folder='templates')

# Configuração do logger
logging.basicConfig(level=logging.INFO)

# Caminho do diretório de download
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads\musicas')

# Caminho do ffmpeg.exe
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # <<< MUITO IMPORTANTE: coloque o caminho correto aqui

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
            'ffmpeg_location': FFMPEG_PATH,  # <<< Aqui está passando o caminho do ffmpeg
            'progress_hooks': [my_hook],
            'noplaylist': True,
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        app.logger.info("Download de áudio concluído")
    except Exception as e:
        app.logger.error(f"Erro durante o download: {e}")

def my_hook(d):
    if d['status'] == 'downloading':
        pass
    if d['status'] == 'finished':
        app.logger.info("Download finalizado, convertendo...")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    download_audio(video_url, DOWNLOAD_DIR)
    return "O download está em andamento. Verifique os logs para obter o progresso."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
