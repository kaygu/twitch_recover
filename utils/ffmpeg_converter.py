import subprocess
import os
import re

TMP_TS_TXT_FILE = "ts_files_list.txt"

def num_sort(name):
    """
    Sort list elements by numbers present in them 
    """
    return int("".join(re.findall(r'\d+', name)))

def generate_ts_list(ts_files: str, files_dir: str):
    """
    Generate a list of .ts files in the directory
    param ts_files: List of .ts files
    param files_dir: Directory where the .ts files are located
    """
    ts_files.sort(key=num_sort)
    with open(TMP_TS_TXT_FILE, 'w') as f:
        for ts_file in ts_files:
            f.write(f"file '{files_dir}/{ts_file}'\n")

def combine_ts_to_mp4(output_file):

    # Construct the ffmpeg command to concatenate .ts files
    ffmpeg_cmd = [
        'ffmpeg', 
        '-f', 'concat',  # Use the concat demuxer
        '-safe', '0',    # Allow input files with different paths
        '-i', TMP_TS_TXT_FILE,  # Input file list
        '-c', 'copy',    # Copy the streams without re-encoding
        '-bsf:a', 'aac_adtstoasc',  # Convert AAC codec
        '-movflags', 'faststart',    # Move moov atom to the beginning
        '-y',            # Overwrite output file if it exists
        output_file      # Output file name
    ]

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_cmd)

    # Remove the temporary generated ts list
    os.remove(TMP_TS_TXT_FILE)


def convert_video(vid_dir:str, output_file: str):
    '''
    Convert .ts files into a single .mp4 file
    param vid_dir: Directory where the .ts files are located
    param output_file: Name of the output .mp4 file
    '''
    files = os.listdir(vid_dir)
    generate_ts_list(files, vid_dir)

    # Combine .ts files into .mp4
    combine_ts_to_mp4(output_file)
