from pathlib import Path
from yt_dlp import YoutubeDL


YTDL_PARAMS = {
    "format": "b[ext=mp4]",
    "getcomments": True,
}


def download(url: str, workspace: str) -> (Path, dict):
    params = YTDL_PARAMS | {"outtmpl": f'{workspace}/%(title)s.%(ext)s'}

    with YoutubeDL(params) as yd:
        info_dict = yd.extract_info(url, download=True)
        filename = yd.prepare_filename(info_dict)

    return Path(filename), info_dict
