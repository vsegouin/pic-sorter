#!/usr/bin/python3
import _thread
import logging
import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from utils.parameters import PATHS


def start_watchdog(path):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def start_thread():
    # Create two threads as follows
    try:
        _thread.start_new_thread(start_watchdog, (PATHS.root_path,))
    except AssertionError as e:
        print(e)
