#!/usr/bin/env python3
"""get one years worth of weather data for London City Airport."""
import configparser
from datetime import datetime, timedelta
import json
import sys
import time

import requests

BASE_URL = 'http://api.wunderground.com/api'


def main():
    """main entry point for the script."""
    # TODO: can make the script more flexible by accepting arguments for date
    # range and weather station
    start_date = datetime(2016, 12, 25)
    end_date = datetime(2017, 12, 29)
    current = start_date + timedelta(days=0)

    # load API key
    api_key = load_credentials('credentials.ini')
    if api_key == '':
        print(
            'you have not configured your api key. create a file `credentials.ini`'
            ' and add your api key under the section [wunderground]. exiting.'
        )
        sys.exit(1)

    country = 'UK'
    # EGLC: London City Airport
    station = 'EGLC'

    while current < end_date:
        str_date = str(current)
        ymd = get_ymd(str_date)
        # 'http://api.wunderground.com/api/<YOUR_API_KEY>/history_20170101/q/UK/EGLC.json'
        url = f'{BASE_URL}/{api_key}/history_{ymd}/q/{country}/{station}.json'

        print(f'getting data for {ymd}')

        r = requests.get(url)

        if r.status_code == 200:
            pass
        elif r.status_code == 429:
            print('rate limit exceeded. waiting for 60 seconds.')
            time.sleep(60)
        else:
            print(f'status: {r.status_code}. retrying in 20 seconds')
            time.sleep(20)

        with open(f'{ymd}_{station}.json', 'w') as f:
            json.dump(r.json(), f)

        current += timedelta(days=1)
        # we're rate limited to 10 requests per minute
        time.sleep(6)

    print('data collection completed')


def get_ymd(s):
    """get the year, month and day in the format yyyy, mm, dd."""
    return f'{s[:4]}{s[5:7]}{s[8:10]}'


def load_credentials(credentials):
    """load and return an API key."""
    config = configparser.ConfigParser()
    config.read(credentials)
    return config['wunderground']['api_key']


if __name__ == '__main__':
    main()
