# TODO : Count minutes muted

def has_muted(file: str) -> bool:
    '''
    Check if a portion of the stream is muted
    param file: m3u8 file content. Not the file path
    return: bool
    '''
    if '-unmuted.ts' in file:
        return True
    return False

def count_muted_segments(file: str) -> int:
    '''
    Returns the amount of muted segments present in the playlist
    param file: m3u8 file content. Not the file path
    return: muted segments count
    '''
    count = file.count("-unmuted.ts")
    return count

def repair_muted_segments(file: str):
    '''
    Replaces all the muted segments with links that work
    param file: m3u8 file content. Not the file path
    return: modified m3u8 file content
    '''
    newFile = file.replace('-unmuted.ts', '-muted.ts')
    return newFile