# Look here for petter version, using pipe stream:
# https://stackoverflow.com/questions/70774134/concatenate-multiple-ts-files-byte-or-byte-like-format-to-one-mp4-file

import os

import ffmpeg

FILM_NAME = "Vertiacal Sailing Greenland Trailer"
INPUT_DIR = f"./{FILM_NAME}/"
OUTPUT_NAME = f"{FILM_NAME}.mp4"

if __name__ == '__main__':
    with open('tmp.ts', 'wb') as output:
        for file_name in os.listdir(INPUT_DIR):
           with open(INPUT_DIR + file_name, 'rb') as input_file:
              output.write(input_file.read())

    (
    ffmpeg
    .input('tmp.ts')
    .output(OUTPUT_NAME)
    .overwrite_output()
    .run()
    )