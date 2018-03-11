#!/usr/bin/env python3
"""convert csv to sqlite3 database"""
import argparse
import csv
import os
import sqlite3
import sys


def main():
    """main entry point for this script"""
    print(args)

    input_filepath = os.path.abspath(args.input)

    if os.path.isfile(input_filepath):
        with open(input_filepath, 'rt') as f:
            header = f.readline().strip()
        print(f'header: {header}')
    else:
        print(f'input file `{input_filepath}` does not exist. exiting.')
        sys.exit(1)

    output_filepath = os.path.abspath(args.output)

    if os.path.isfile(output_filepath):
        print(
            f'output file `{output_filepath}` already exists. delete or move '
            'this file before proceeding. exiting.'
        )
        sys.exit(2)

    con = sqlite3.connect(output_filepath)

    if 'precipitation' in header:
        convert_weatherdata(con, input_filepath)
    elif 'Bike Id' in header:
        convert_cycledata(con, input_filepath)


def convert_weatherdata(con: sqlite3.Connection, input_filepath: str):
    """convert the weather csv file"""
    # create the table
    con.execute(
        """
        CREATE TABLE weather (
            id INTEGER PRIMARY KEY,
            datetime TEXT,
            temperature REAL,
            humidity INTEGER,
            wind_speed REAL,
            precipitation REAL,
            condition TEXT,
            fog INTEGER,
            rain INTEGER,
            snow INTEGER,
            hail INTEGER,
            thunder INTEGER
        )
        """
    )

    # for an `n` item list, there are `n-1` splits
    # in order to merge the first two fields, split from the right and
    # leave out the final split, i.e., have `n-1-1` splits

    with con, open(input_filepath, 'rt') as f:
        # skip the header and determine the number of splits
        split_len = len(next(f).split(',')) - 2

        for i, line in enumerate(f, start=1):
            # make datetime a single field
            line = [l.replace(',', ' ') for l in line.rsplit(',', maxsplit=split_len)]
            # replace empty string with NULL
            line = [l if l != '' else None for l in line]

            con.execute(
                "INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (i, *line),
            )

    con.close()


def convert_cycledata(con: sqlite3.Connection, input_filepath: str):
    """convert the cycledata csv file"""
    # create the table
    con.execute(
        """
        CREATE TABLE journey (
            id INTEGER PRIMARY KEY,
            rental_id INTEGER,
            duration INTEGER,
            bike_id INTEGER,
            end_datetime TEXT,
            end_station_id INTEGER,
            end_station_name TEXT,
            start_datetime TEXT,
            start_station_id INTEGER,
            start_station_name TEXT
        )
        """
    )

    with con, open(input_filepath, 'rt') as f:
        next(f)  # skip the header
        r = csv.reader(f)

        for idx, line in enumerate(r, start=1):
            # convert timestamps from `dd/mm/yyyy hh:mm` to `yyyy-mm-dd hh:mm`
            if len(line[3]) == 16 and len(line[6]) == 16:
                for i in (3, 6):
                    line[i] = f'{line[i][6:10]}-{line[i][3:5]}-{line[i][:2]} {line[i][-5:]}'
            line = [l.replace(' ,', ',') for l in line]  # remove leading spaces from commas

            # replace empty strings with NULL
            line = [l if l != '' else None for l in line]

            con.execute(
                "INSERT INTO journey VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (idx, *line),
            )

    con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="convert csv to sqlite",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('input', help='input filename')
    parser.add_argument('output', help='output filename')
    args = parser.parse_args()
    main()
