from datetime import datetime, timezone
import re

def str_to_datetime(s: str) -> datetime:
    s = re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)
    dt = datetime.strptime(s, "%A %d %B %Y %H:%M")
    dt = dt.replace(tzinfo=timezone.utc)

    return dt

def qdatetime_to_utc_datetime(qdt):
    dt = qdt.dateTime().toPyDateTime()
    dt = dt.replace(tzinfo=timezone.utc)

    return dt

def convert_to_utc_timestamp(date_str: str) -> int:
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    dt = dt.replace(tzinfo=timezone.utc)
    
    return int(dt.timestamp())