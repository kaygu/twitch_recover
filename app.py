import time
import argparse
from dotenv import load_dotenv
from pathlib import Path

from src.connectors.base import BaseConnector
from src.connectors.twitchtracker import TwitchTrackerConnector
from src.connectors.twitch import TwitchConnector

from twitch.find_vod import generate_vod_path, generate_vod_path_offline, find_vod_host
from utils.ffmpeg_stream import convert_stream_m3u8, rewrite_m3u8
from utils.download import download_vod
from utils.ffmpeg_converter import convert_video
from utils.files import clean_files


# Create the parser
parser = argparse.ArgumentParser(
    description='Process Twitch VODs.',
    epilog='Example: python app.py https://twitchtracker.com/shroud/streams/41466366795 --quality 720p60 --verbose'
)

# Add the arguments
parser.add_argument(
    'url',
    help='The TwitchTracker url of the stream'
)
parser.add_argument( 
    '--timestamp',
    '-t',
    required=False,
    help='Optional. The timestamp of the stream in the format YYYY-MM-DD HH:MM:SS. Required to get the VOD without requesting TwitchTracker directly'
)
parser.add_argument(
    '--quality',
    '-q',
    required=False,
    default='chunked',
    help='Optional. The quality of the stream. Default is "chunked" (source)'
)
parser.add_argument(
    '--output',
    '-o',
    required=False,
    default='output.mp4',
    help='Optional. The output file name. Default is output.mp4'
)
parser.add_argument(
    '--env',
    '-e',
    default='.env',
    help='Optional. The path to the .env file. Default is .env'
)
parser.add_argument(
    "--recover",
    action="store_true",
    help="Use this flag to try to recover the stream or the sound of the video.\n This might not work if the video has been deleted for more than a few hours\nThis flag makes the process slower and takes more space on the dick (during runtime)")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

# Parse the arguments
args = parser.parse_args()

TEMP_FOLDER_PATH = "video" # Warning: Do not name the directory with an existing name or it will be overwritten
TEMP_M3U8_FILE = "temp.m3u8"

def main():
    start_time = time.time()  # Start timing
    env_path = Path(args.env)
    load_dotenv(dotenv_path=env_path) # loads environment variables from .env file

    # TODO: Change connector if link is ttracker or twitch 
    connector = TwitchConnector()
    # if args.timestamp:
    #     vod_path = generate_vod_path_offline(args.url, args.timestamp, args.quality)
    # else:
    #     vod_path = generate_vod_path(args.url, args.quality)


    ## Change connector depending on the URL provided
    vod_path = connector.get_vod_path(args.url, args.quality, args.verbose)
    vod_url = find_vod_host(vod_path, args.verbose)
    print(vod_url)
    if not vod_url:
        print("No VOD was found. Quitting")
        exit()

    if args.recover:
        download_vod(vod_url, TEMP_FOLDER_PATH, args.verbose)
        convert_video(TEMP_FOLDER_PATH, args.output)
    else:
        rewrite_m3u8(vod_url, TEMP_M3U8_FILE)
        convert_stream_m3u8(TEMP_M3U8_FILE, args.output)
    

    end_time = time.time()  # End timing
    if args.verbose:
        print(f"Total time taken: {end_time - start_time:.2f} seconds") 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        # Let program run to clean files
    
    # Clean up files after converting the video
    clean_files(TEMP_FOLDER_PATH, TEMP_M3U8_FILE, args.verbose)


    #TODO: Update progression (percents, time left, etc.) for the download process
    #TODO: Record stats (most used server etc)
    #TODO: Handle 404
    #TODO: Get default VOD name from stream title
    #TODO: Check that VOD name is available before downloading to avoid output override
    #TODO: Record livestream
    #TODO: Create interface for different vod links (twitchtracker, twitch.com, ...)
