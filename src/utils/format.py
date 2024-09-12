from datetime import datetime
import re

def str_to_datetime(s: str) -> datetime:
    s = re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)
    return datetime.strptime(s, "%A %d %B %Y %H:%M")
