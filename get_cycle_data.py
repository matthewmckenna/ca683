#!/usr/bin/env python3
import argparse
import os

import requests
from bs4 import BeautifulSoup

from download_utils import simple_threaded_download


def main():
    """main entry point"""
    download_base = 'http://cycling.data.tfl.gov.uk/'
    # http://cycling.data.tfl.gov.uk/usage-stats/11a-Journey-Data-Extract-18Oct15-31Oct15.csv
    listing_url = 'https://s3-eu-west-1.amazonaws.com/cycling.data.tfl.gov.uk/'
    r = requests.get(listing_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = [k.text for k in soup.find_all('key') if '17.csv' in k.text]
    download_urls = [f'{download_base}{u}' for u in urls]

    simple_threaded_download(
        urls=download_urls[:4],
        download_path=os.path.abspath(args.output_directory),
        nthreads=2,
        # chunk_size=32768,
        # sleep=1,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='get london cycle hire data for 2017',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('output-directory', help='directory to save downloaded files')
    args = parser.parse_args()
    main()
