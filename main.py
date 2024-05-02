from pytube import YouTube
from tqdm import tqdm

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
        print("Download completed!")
    except Exception as e:
        print("Error: ", e)

if __name__ == "__main__":
    video_url = input("URL do video: ")
    download_path = r'C:\Users\paulo\Downloads' # set at folder destiny
    download_video(video_url, download_path)