#!/usr/bin/env python3
"""merge weather data files into single CSV file."""
import argparse
import csv
import json
import os
import re
from typing import Dict, Generator, List

CONDITIONS = {
    'clear': {'clear', 'mist', 'haze'},
    'cloudy': {'mostly_cloudy', 'overcast', 'partly_cloudy', 'scattered_clouds'},
    'fog': {'fog', 'patches_of_fog', 'light_freezing_fog'},
    'hail_snow_storm': {
        'hail',
        'hail_showers',
        'light_ice_pellets',
        'light_snow',
        'light_thunderstorms_and_rain',
        'snow_grains',
        'thunderstorm',
        'thunderstorms_and_rain',
    },
    'rain': {
        'drizzle',
        'heavy_rain',
        'light_drizzle',
        'light_rain',
        'light_rain_showers',
        'rain',
    },
}


def main():
    """main entry point"""
    output_fname = args.output
    directory = os.path.abspath(args.directory)
    # look for files in the format YYYYMMDD_XXXX.json, where XXXX is
    # the ICAO airport code (e.g., EGLC for London City Airport (LCY),
    # EGGW for London Luton Airport (LTN), EGLL for London Heathrow
    # Airport(LHR), EIDW for Dublin Airport (DUB))
    pattern = '^\d{8}_[a-zA-Z]{4}.json$'

    fieldnames = get_fieldnames(directory, pattern)
    filenames = sorted(get_matching_filenames(directory, pattern))

    with open(output_fname, 'wt', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for fn in filenames:
            fname = os.path.join(directory, fn)
            writer.writerows(r for r in parse_json_dict(fname))


def get_fieldnames(directory: str, pattern: str) -> List[str]:
    """get the fieldnames for the output file."""
    filenames = get_matching_filenames(directory, pattern)
    row = parse_json_dict(os.path.join(directory, next(filenames)), header=True)
    return next(row).keys()


def get_matching_filenames(directory: str, pattern: str) -> Generator[str, None, None]:
    """get all filenames which match `pattern` in the given directory.

    Args:
        directory: the directory in which to look for files
        pattern: regex of the filename pattern to look for. for
            weather data we look for `YYYYMMDD_XXXX.json`, where
            `XXXX` is the ICAO airport code.
    Yields:
        entry.name: name of file which matches `pattern`
    """
    fname_pattern = re.compile(fr'{pattern}')

    with os.scandir(directory) as it:
        for entry in it:
            if fname_pattern.match(entry.name):
                yield entry.name


def parse_json_dict(fname: str, *, header: bool = False) -> Generator[Dict[str, str], None, None]:
    """get fields of interest from json file and return a dictionary of these.

    Args:
        fname: name of the json file to process
        header: return after the first observation if True. used
            to get the header for the output file.

    Yields:
        d: dictionary with fields of interest
    """
    with open(fname, 'rt') as f:
        data = json.load(f)

    d: Dict[str, str] = {}

    # reverse the `CONDITIONS` lookup
    conditions = {v: key for key, value in CONDITIONS.items() for v in value}

    for o in data['history']['observations']:
        # d['date'] = f"{o['date']['year']}-{o['date']['mon']}-{o['date']['mday']}"
        # d['time'] = f"{o['date']['hour']}:{o['date']['min']}"
        d['datetime'] = get_datetime(o['date'])
        d['temperature'] = o['tempm'] if o['tempm'] != '-9999' else ''  # in degrees Celsius
        d['humidity'] = o['hum'] if o['hum'] != 'N/A' else '' # % humidity
        d['wind_speed'] = o['wspdm']  # in kph
        # d['precipitation'] = o['precipm'] if o['precipm'] != '-9999.00' else '0.0'  # in mm
        condition = o['conds'].replace(' ', '_').lower()
        # d['condition'] = condition if condition != 'unknown' else ''

        d['condition'] = conditions[condition] if condition != 'unknown' else ''

        d['fog'] = o['fog']
        d['rain'] = o['rain']
        d['snow'] = o['snow']
        d['hail'] = o['hail']
        d['thunder'] = o['thunder']

        yield d

        if header:
            # only looking for header so just return one record
            return


def get_datetime(o: Dict[str, str]) -> str:
    """Return a datetime string from the observation dict `o`."""
    return f"{o['year']}-{o['mon']}-{o['mday']} {o['hour']}:{o['min']}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='merge many json files into a csv',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('directory', help='directory containing json files')
    parser.add_argument('-o', '--output', help='output filename', default='weather.csv')
    args = parser.parse_args()
    main()
