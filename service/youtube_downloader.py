import os

from pytubefix import YouTube

from service.audio_service import AudioService


class YouTubeDownloader:
    def __init__(self, folder_name='lector_files'):
        self.audio_service = AudioService()
        self.folder_name = folder_name
        self.folder_path = os.path.join(os.getcwd(), self.folder_name)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def download_youtube_audio(self, url, file_name='lector_audio.mp3'):
        try:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path=self.folder_path, filename=file_name)
            return os.path.join(self.folder_path, file_name)
        except Exception as e:
            print("download youtube audio error:")
            print(e)
            
    def download_youtube_video(self, url, file_name='lector_video.mp4'):
        try:
            yt = YouTube(url)
            video = yt.streams.first()
            video.download(output_path=self.folder_path, filename=file_name)
            return os.path.join(self.folder_path, file_name)
        except Exception as e:
            print("download youtube video error:")
            print(e)

