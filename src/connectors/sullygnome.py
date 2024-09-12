
import calendar
import hashlib
import re
from typing import List, Iterable
import requests
import time

from connectors.base import BaseConnector
from utils.enums import HTTPStatusCode

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106"}


class SullygnomeConnector(BaseConnector):
    SULLYGNOME_STREAMS_URL = 'https://sullygnome.com/channel/{STREAMER_NAME}/60/streams'
    SULLYGNAME_STREAMS_API = 'https://sullygnome.com/api/tables/channeltables/streams/60/{SULLYGNOME_ID}/%20/1/1/desc/0/100'

    def get_past_vods(self, streamer: str, verbose: bool = False) -> Iterable[tuple]:
        req = requests.get(self.SULLYGNOME_STREAMS_URL.format(STREAMER_NAME=streamer), headers=header)
        if req.status_code == HTTPStatusCode.OK:
            result = re.search('var PageInfo = {.+\"id\":(\d+)', req.text)
            if not result or result.group(1) == '0':
                raise Exception(f'Could not find Sullygnome ID for {streamer}')
            if verbose:
                print(f'Streamer ID for {streamer}: {result.group(1)}')
        elif req.status_code == HTTPStatusCode.NOT_FOUND:
            raise Exception(f'404 Sullygname page not found for URL {self.SULLYGNOME_STREAMS_URL.format(STREAMER_NAME=streamer)}')
        else:
            raise Exception('Sullygnome returned status code', req.status_code, req.headers)
        req = requests.get(self.SULLYGNAME_STREAMS_API.format(SULLYGNOME_ID=result.group(1)), headers=header)
        try:
            stream_data = req.json().get('data')
        except:
            print(f'request content:\n{req}')
            raise Exception('Error decoding the sullygnome data returned')
        for stream in stream_data:
            if verbose:
                print(stream)
            stream_id = stream.get('streamId')
            start_datetime = stream.get('startDateTime')
            start_time = stream.get('starttime')
            end_time = stream.get('endtime')
            yield stream_id, start_datetime, start_time, end_time