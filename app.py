from flask import Flask, render_template, request
from pytube import YouTube
from tqdm import tqdm

app = Flask(__name__, template_folder='templates')

class TqdmUpTo(tqdm):
    def update_to(self, stream, chunk, bytes_remaining):
        if self.total is None:
            self.total = bytes_remaining
        self.update(len(chunk))

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        with TqdmUpTo(unit='bytes', unit_scale=True, desc=stream.title) as progress_bar:
            yt.register_on_progress_callback(progress_bar.update_to)
            stream.download(output_path)
        return "Download concluido"
    except Exception as e:
        return f"Erro: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    download_path = r'C:\Users\paulo\Downloads'
    message = download_video(video_url, download_path)
    return message

if __name__ == "__main__":
    app.run(debug=True)