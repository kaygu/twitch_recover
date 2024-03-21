from twitch.find_vod import generate_vod_path, generate_vod_path_offline, find_vod_host
from utils.download import download_vod
from utils.ffmpeg_converter import convert_video


TT = "https://twitchtracker.com/aleczandxr/streams/50506622717"
PATH = "video"

if __name__ == '__main__':
    vod_path = generate_vod_path_offline(TT, '2024-02-28 15:07:23', "480p30")
    vod_url = find_vod_host(vod_path)
    print(vod_url)
    if not vod_url:
        print("No VOD was found. Quitting")
        exit()
    download_vod(vod_url, PATH)
    convert_video(PATH, "output.mp4")