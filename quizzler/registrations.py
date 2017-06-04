import collections
import csv
import functools
import io
import os
import zipfile

from .env import ROOT_DIR_PATH


__all__ = ['get_registrations']


def generate_info():
    with zipfile.ZipFile(str(ROOT_DIR_PATH.joinpath('tickets.zip'))) as zf:
        for name in zf.namelist():
            stem, ext = os.path.splitext(name)
            if ext != '.csv':
                continue
            with zf.open(name) as f:
                # Zipfile only opens file in binary mode, but csv only accepts
                # text files, so we need to wrap this.
                # See <https://stackoverflow.com/questions/5627954>.
                textfile = io.TextIOWrapper(f, encoding='utf8', newline='')
                for row in csv.DictReader(textfile):
                    yield row


@functools.lru_cache(maxsize=1)
def get_info_map():
    info_map = collections.defaultdict(list)
    for info in generate_info():
        key = info['聯絡人 Email'].strip()
        info_map[key].append(info)
    return info_map


def get_registrations(*, email):
    return list(get_info_map()[email.strip()])