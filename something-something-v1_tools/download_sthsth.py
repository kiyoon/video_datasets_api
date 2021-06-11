#!/usr/bin/env python3

import argparse
def get_parser():
    parser = argparse.ArgumentParser(description='''Download something-something by parsing the download page html file.
You'll need to download the html page manually because it requires you to log in.
The download links will expire in 1 hour. Simply update the HTML file and run again, then it will resume the downloads.''',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("TwentyBN_html", help="Path to html file to parse download links.")
    parser.add_argument("output_dir", help="Path to output directory.")
    parser.add_argument("--version", type=int, default=1, choices=[1,2], help="Something-Something version to download")
    return parser

parser = get_parser()
args = parser.parse_args()

import os
import sys
import requests
from bs4 import BeautifulSoup
import hashlib

import time
import traceback

TIME_DURATION_UNITS = (
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('min', 60),
    ('sec', 1)
)


def human_time_duration(seconds):
    if seconds == 0:
        return '0 secs'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

# https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def calc_file_md5hash(path):
    with open(path, 'rb') as f:
        data = f.read()
    md5hash = hashlib.md5(data).hexdigest()
    return md5hash

#https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def download_with_progress(link, file_name):
    with open(file_name, "wb") as f:
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            start_time = time.time()
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                elapsed_time = time.time() - start_time
                eta = (elapsed_time * (total_length / dl)) - elapsed_time if dl > 0 else 0
                sys.stdout.write("\r[%s%s] %s / %s ETA: %s          " % ('=' * done, ' ' * (50-done), sizeof_fmt(dl), sizeof_fmt(total_length), human_time_duration(eta)) )
                sys.stdout.flush()
            sys.stdout.write("\r[%s%s] %s / %s Elapsed time: %s          " % ('=' * done, ' ' * (50-done), sizeof_fmt(dl), sizeof_fmt(total_length), human_time_duration(elapsed_time)) )
            sys.stdout.flush()


if __name__ == '__main__':
    with open(args.TwentyBN_html, 'r') as f:
        html = '\n'.join(f.readlines())
    soup = BeautifulSoup(html, 'html.parser')
    search_res = soup.select('#page-top > section.py-5 > div > div > div > div > div > div > div.col-md-8 > a')

    os.makedirs(args.output_dir, exist_ok=True)
    try:
        for link in search_res:
            url = link['href']
            text = link.text.strip()
            if f'20bn-something-something-v{args.version}' in url:
                if text == 'md5':
                    response = requests.get(url, stream=True)
                    md5hash, filename = response.content.decode().strip().split()
                    calced_hash = calc_file_md5hash(os.path.join(args.output_dir, filename))
                    if calced_hash == md5hash:
                        print(f'{filename} checksum OK')
                    else:
                        print(f'{filename} checksum Failed!')
                else:
                    if not os.path.isfile(os.path.join(args.output_dir, text)):
                        print(text)
                        download_with_progress(url, os.path.join(args.output_dir, text))
                    else:
                        print(f'Skipping {text}')
    except Exception as e:
        print("Error occurred. Perhaps the download links have expired. Update the html file and re-run the code, then it will resume.")
        traceback.print_exc()
    else:
        print("Download completed!")
        print("Extract using: `cat 20bn-something-something-v1-?? | tar zx`")

