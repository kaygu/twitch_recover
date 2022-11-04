import requests

from utils.find_vod import find_vod_path, find_vod_host
from utils.m3u8 import has_muted, count_muted_segments
from utils.download_vod import create_dir, download_transport_stream

if __name__ == '__main__':
    TT = "https://twitchtracker.com/targamas1/streams/46112643356"
    vod_path = find_vod_path(TT)
    vod_url = find_vod_host(vod_path)
    print(vod_url)
    r = requests.get(vod_url)
    base_url = vod_url.rpartition('/')[0]
    m3u8 = r.text
    vod_name = "vod_" + TT.rsplit('/')[-3] + "_" + TT.rsplit('/')[-1] # streamer name + vod ID
    create_dir(vod_name)
    if has_muted(m3u8):
        print(f'VOD has {count_muted_segments(m3u8)} muted segments')
    else:
        print('VOD has no muted content')
    
    # Download muted segments first if aviable, else download in order
    for record in m3u8.splitlines():
        if not record.startswith('#') and record != '':
            if '-unmuted.ts' in record:
                record_name = record.replace('-unmuted.ts', '.ts')
                record_muted = record.replace('-unmuted.ts', '-muted.ts')
                print(f'Downloading muted record {record_name}')
                download_transport_stream(vod_name + '/' + record_name, base_url + '/' + record_name) #download original file (recover)
                download_transport_stream(vod_name + '/' + record_name, base_url + '/' + record_muted) #download muted file (backup)
            else:
                download_transport_stream(vod_name + '/' + record, base_url + '/' + record)