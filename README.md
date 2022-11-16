# Twitch VOD Recovery

This tool was developped to recover deleted twitch videos and recover videos with muted segments. It can also be used to bypass sub only vods

Note that deleted videos will only be recoverable in a short time frame after the deletion. If it has been more than 8 hours after the deletion or muted segments this tool will not work

## Requirements

```cmd
ffmpeg
```

## Installation

```cmd
git clone git@github.com:kaygu/projekt.git
cd projekt
pip install -r requirements.txt 
```

## Usage

Edit TwitchTracker url in *app.py* (ex: `TT = "https://twitchtracker.com/shroud/streams/41466366795"`)

```cmd
py app.py
```

Once the video has been downloaded, use *convert_video.py* to transform downloaded vod into mp4 format
Edit the variable `FILM_NAME =` with the directory where the video segments are stored

```cmd
py convert_video.py
```

Note: This script is not yet optimized, might take hours depending of the length of the video