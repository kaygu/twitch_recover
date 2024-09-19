import datetime
import re
import requests
import tempfile

from utils.enums import HTTPStatusCode
from utils.transport_stream import does_exist, is_downloadable

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106"}


class M3U8:
    def __init__(self, url: str, verbose: bool = False):
        self.verbose = verbose
        self.url = url
        r = requests.get(self.url, headers=header)
        if r.status_code == HTTPStatusCode.OK:
            self.content = r.text
            self.playlist = self.content.strip().splitlines()
        else:
            raise Exception(f'Could not download m3u8 file from url "{self.url}"')
        self.base_url = self.url.rpartition('/')[0]

        timestamp_int = int(self.url.split('/')[-3].split('_')[-1])
        self.timestamp = datetime.datetime.fromtimestamp(timestamp_int, tz=datetime.timezone.utc)

    def download(self, **kwargs) -> None:
        '''
        Downloads the segments and store them in a temp folder
        Suported kwargs: start (timestamp), end (tiemstamp), whole (bool)
        '''
        with tempfile.TemporaryDirectory() as tempdir:
            if self.verbose:
                print(f'Temporary dir has been created: {tempdir}')
            if kwargs.get('start') and kwargs.get('end'):
                # Find what segment are included in this timeframe
                start_in_x_seconds, end_in_x_seconds = self._find_segments_in_timeframe(kwargs.get('start'), kwargs.get('end'))
                seconds_passed = 0
                previous_line = ''
                for line in self.playlist:
                    if '.ts' in line:
                        match = re.search(r'#EXTINF:(\d+\.\d+)', previous_line)
                        seconds_passed += float(match.group(1))
                        if start_in_x_seconds <= seconds_passed and seconds_passed <= end_in_x_seconds:
                            print(f'download segment {line}')
                    previous_line = line


        # Create temp dir & temp txt file
        # Download all the .ts files
        # 
        pass
    
    def _find_segments_in_timeframe(self, start, end) -> tuple[float, float]:
        '''
        Checks if some part of the vod are out fo the timeframe
        '''
        seconds_after_start = 0
        seconds_before_end = 0
        # start = start.toPyDateTime().replace(tzinfo=datetime.timezone.utc)
        # end = end.toPyDateTime().replace(tzinfo=datetime.timezone.utc)
        if start > self.timestamp:
            # How many seconds after the start of te vod
            seconds_after_start = (start - self.timestamp).total_seconds()
        if end < (self.timestamp + datetime.timedelta(seconds=self.get_length())):
            # How many seconds before the end of the vod
            seconds_before_end = (end - (self.timestamp + datetime.timedelta(seconds=self.get_length()))).total_seconds()
            
        print(f'seconds to skip at start {seconds_after_start}')
        print(f'seconds to skip at end {seconds_before_end}')
        return seconds_after_start, seconds_before_end

    def _download_ts_file(self, url: str, path: str) -> bool:
        '''
        Download .ts file if it doesnt exist
        '''
        # Check if it exists
        if not does_exist(path):
            r = requests.get(url)
            if is_downloadable(r):
                with open(path, 'wb') as download:
                    download.write(r.content)
                    return True
            else:
                if r.status_code != HTTPStatusCode.FORBIDDEN:
                    raise Exception(f'{url} could not be downloaded\nstatus code: {r.status_code}\n{r.headers}')
        return False

    def has_muted_segments(self) -> bool:
        '''
        Check if a portion of the vod is muted
        '''
        if '-unmuted.ts' in self.conent:
            if self.verbose:
                print(f'VOD has muted segments')
            return True
        return False
    
    def count_muted_seconds(self) -> float:
        '''
        Returns the amount of muted seconds present in the vod
        '''
        total_seconds = 0.0
        previous_line = None
        for line in self.playlist:
            if 'unmuted' in line and previous_line:
                match = re.search(r'#EXTINF:(\d+\.\d+)', previous_line)
                total_seconds += float(match.group(1))
            previous_line = line
        if self.verbose:
            print(f'VOD has {total_seconds} muted seconds')
        return total_seconds
    
    def count_muted_segements(self) -> int:
        '''
        Count the number of muted segements in a vod
        '''
        segments = 0
        is_previous_segment_muted = False
        for line in self.playlist:
            if not line.startswith('#'):
                if 'unmuted' in line and not is_previous_segment_muted:
                    segments += 1
                    is_previous_segment_muted = True
                if not 'unmuted' in line:
                    is_previous_segment_muted = False
        if self.verbose:
            print(f'VOD has {segments} muted segments')
        return segments


    def get_length(self) -> float:
        '''
        Returns the length of the vod in seconds
        '''
        match = re.search(r'#EXT-X-TWITCH-TOTAL-SECS:(\d+\.\d+)', self.content)
        length = float(match.group(1))
        if self.verbose:
            print(f'VOD has a length of {length} seconds')
        return length