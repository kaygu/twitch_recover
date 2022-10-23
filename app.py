import requests

from utils.find_vod import find_vod_path, find_vod_host
from utils.m3u8 import has_muted, count_muted_segments

headers = {"User-Agent": "Mozilla/5.0"}

if __name__ == '__main__':
    TT = "https://twitchtracker.com/aleczandxr/streams/40195889945"
    vod_path = find_vod_path(TT)
    vod_url = find_vod_host(vod_path)
    print(vod_url)
    r = requests.get(vod_url, headers=headers)
    m3u8 = r.text
    print(m3u8[:100])
    if has_muted(m3u8):
        print(f'VOD has {count_muted_segments(m3u8)} muted segments')
    else:
        print('VOD has no muted content')