import subprocess
import requests
import urllib.parse


def rewrite_m3u8(m3u8_url, output_file):
    output = ""
    r = requests.get(m3u8_url)
    m3u8 = r.text

    for record in m3u8.splitlines():
        if record and not record.startswith("#"):
            record = record.replace("unmuted", "muted")
            record = urllib.parse.urljoin(m3u8_url, record)
        output += record + "\n"

    with open(output_file, 'w') as f:
        f.write(output)

        

def convert_stream_m3u8(m3u8_file, output_file):
    ffmpeg_cmd = [
        'ffmpeg',
        '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
        '-i', m3u8_file,  # Input m3u8 file
        '-c', 'copy',    # Copy the streams without re-encoding
        '-bsf:a', 'aac_adtstoasc',  # Convert AAC codec
        '-movflags', 'faststart',    # Move moov atom to the beginning
        '-y',            # Overwrite output file if it exists
        output_file      # Output file name
    ]

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_cmd)
