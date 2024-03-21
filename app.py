import time

from twitch.find_vod import generate_vod_path, generate_vod_path_offline, find_vod_host
# from utils.download import download_vod
# from utils.ffmpeg_converter import convert_video
from utils.ffmpeg_stream import convert_stream_m3u8, rewrite_m3u8


TT = "https://twitchtracker.com/aleczandxr/streams/50678946093"
PATH = "video" # Warning: Do not name the directory with an existing name or it will be overwritten

if __name__ == '__main__':
    vod_path = generate_vod_path_offline(TT, '2024-03-20 13:58:02', "720p60")
    vod_url = find_vod_host(vod_path)
    print(vod_url)
    if not vod_url:
        print("No VOD was found. Quitting")
        exit()
          
    start_time = time.time()  # Start timing
   
    rewrite_m3u8(vod_url, "temp.m3u8")
    convert_stream_m3u8("temp.m3u8", "output.mp4")
    # Delete temporary m3u8 file here

    end_time = time.time()  # End timing
    print(f"Time taken: {end_time - start_time} seconds") 

    #Todo: Add a function to delete the .ts files after conversion
    #Todo: Add command line arguments for the script
    #Todo: Time the download and conversion process
    #Todo: Update progression (precents, time left, etc.) for the download process

    # Time for ffmpeg stream converion: 2045 seconds
    # Time for download and conversion: 3075 seconds