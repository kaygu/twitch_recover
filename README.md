# Twitch VOD Recovery

This tool was developped to recover deleted twitch videos and recover videos with muted segments. It can also be used to bypass sub only vods

Note that deleted videos will only be recoverable in a short time frame after the deletion. If it has been more than 8 hours after the deletion or muted segments this tool will most likely not work

## Requirements

```cmd
python >= 3.9
ffmpeg
```

## Installation

```cmd
git clone git@github.com:kaygu/twitch_recover.git
cd twitch_recover
pip install -r requirements.txt 
```

## Usage

Add TwitchTracker url in command
<br>
<br>
Example:

```cmd
python app.py https://twitchtracker.com/shroud/streams/41466366795
```
