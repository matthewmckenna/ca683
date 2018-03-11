#!/usr/bin/env python3
import os
from queue import Queue
import threading
import time
from typing import List

import requests


def simple_threaded_download(
    urls: List[str],
    download_path: str,
    *,
    nthreads: int = 2,
    chunk_size: int = 32*1024,
    sleep: int = 1,
) -> None:
    """a simple threaded download helper"""
    threads = []
    q = Queue()

    options = {
        'chunk_size': chunk_size,
        'download_dir': download_path,
        'sleep': sleep,
    }
    print(f'using options={options}')

    for _ in range(nthreads):
        t = threading.Thread(target=simple_download, args=(q,), kwargs=options)
        t.start()
        threads.append(t)

    for u in urls:
        q.put(u)

    for _ in range(nthreads):
        q.put(None)

    for t in threads:
        t.join()


def simple_download(
    q,
    *,
    chunk_size: int = 32*1024,
    download_dir: str = os.path.expanduser('~'),
    sleep: int = 1,
):
    """download a csv file."""
    while True:
        url = q.get()

        if url is None:
            return

        fname = url.rsplit('/')[-1]
        path = os.path.join(download_dir, fname)

        with open(path, 'wb') as f:
            r = requests.get(url)
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

        time.sleep(sleep)
