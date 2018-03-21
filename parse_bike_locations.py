#!/usr/bin/env python3
"""get and parse London bike station locations"""
import argparse
from collections import defaultdict
import csv
from datetime import datetime
import json
from operator import itemgetter
import os
from typing import Dict, List

import requests


KEY_MAP = {
    # 'CommonName': 'name',
    # 'TerminalName': 'terminal',
    # 'Installed': 'installed',
    # 'Locked': 'locked',
    'InstallDate': 'install_date',
    'RemovalDate': 'removal_date',
    # 'Temporary': 'temporary',
    # 'NbBikes': 'num_bikes',
    # 'NbEmptyDocks': 'num_empty_docks',
    'NbDocks': 'num_docks',
}


def main():
    """main entry point"""
    # TODO: a little bit messy, but works for now
    filepath = os.path.join(os.path.abspath(args.directory), args.filename)

    # transport for london unified api
    url = 'https://api.tfl.gov.uk/BikePoint'
    r = requests.get(url)

    # get the data if it does not exist
    if not os.path.isfile(filepath):
        bikepoints = r.json()
        with open(filepath, 'wt', encoding='utf-8') as f:
            json.dump(bikepoints, f)
    else:
        with open(filepath, 'rt') as f:
            bikepoints = json.load(f)

    data = extract_station_info(bikepoints)

    create_csv(data, filename=f'{os.path.splitext(filepath)[0]}.csv')


def create_csv(data: defaultdict, filename: str):
    """dump the station information to a CSV file"""
    header = data[next(iter(data.keys()))].keys()

    with open(filename, 'wt', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        writer.writeheader()
        for v in sorted(data.values(), key=itemgetter('id')):
            writer.writerow(v)


def extract_station_info(bikepoints: List[Dict]) -> defaultdict:
    """extract information of interest from the API response"""
    d = defaultdict(dict)
    keys_of_interest = {'InstallDate', 'RemovalDate', 'NbDocks'}

    for point in bikepoints:
        station = int(point['id'].split('_')[-1])

        d[station]['id'] = int(station)
        d[station]['name'] = point['commonName']
        d[station]['lat'] = float(point['lat'])
        d[station]['lon'] = float(point['lon'])

        for prop in point['additionalProperties']:
            if prop['key'] in keys_of_interest:
                k = KEY_MAP[prop['key']]
                d[station][k] = prop['value']

        # replace empty strings with None
        for k, v in d[station].items():
            if v == '':
                d[station][k] = None

        for k in ('install_date', 'removal_date'):
            if d[station][k] is not None:
                d[station][k] = epoch_to_datestr(d[station][k])

        d[station]['num_docks'] = int(d[station]['num_docks'])

    return d


def epoch_to_datestr(timestamp_ms: str) -> str:
    """accepts a timestamp as the number of milliseconds from
    January 1, 1970 and returns a date in the form YYYY-mm-dd"""
    timestamp = int(timestamp_ms) / 1000
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='get London bike stations and extract useful information',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-d', '--directory', help='input and output directory', default='.')
    parser.add_argument('-f', '--filename', help='output filename', default='bikepoints.json')
    args = parser.parse_args()
    main()
