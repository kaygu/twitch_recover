# Look here for petter version, using pipe stream:
# https://stackoverflow.com/questions/70774134/concatenate-multiple-ts-files-byte-or-byte-like-format-to-one-mp4-file

import os
import re
import shutil

import ffmpeg

FILM_NAME = "vod_aleczandxr_40380647193"
INPUT_DIR = f"./{FILM_NAME}/"
OUTPUT_NAME = f"{FILM_NAME}.mp4"

def num_sort(name):
    """
    Sort list elements by numbers present in them 
    """
    # return list(map(int, re.findall(r'\d+', test_string)))[-1] # Always sort by last number
    return int("".join(re.findall(r'\d+', name)))

if __name__ == '__main__':
    files = os.listdir(INPUT_DIR)
    files.sort(key=num_sort)
    print(files) #debug
    with open('tmp.ts', 'wb') as output:
        for file_name in files:
           with open(INPUT_DIR + file_name, 'rb') as input_file:
              output.write(input_file.read())

    (
    ffmpeg
    .input('tmp.ts')
    .output(OUTPUT_NAME)
    .overwrite_output()
    .run()
    )
    # Clean files
    if os.path.isfile("tmp.ts"):
        os.remove("tmp.ts")
    if os.path.exists(INPUT_DIR):
        shutil.rmtree(INPUT_DIR)