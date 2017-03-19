# from https://pythonhosted.org/watchdog/quickstart.html#quickstart
# Adapted heavily

import json
import sys
import time
import logging
import requests
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


def build_json_message(message_type, path):
    message = {'message_type': message_type, 'path': path}
    return json.dumps(message)

class Watchmen(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_created(self, event):
        if isinstance(event, watchdog.events.FileCreatedEvent):p
        print event.src_path + " Created"
        print build_json_message("created",event.src_path)

    def on_deleted(self, event):
        print type(event)
        print event.src_path
        if isinstance(event, watchdog.events.FileDeletedEvent):
            print event.src_path + " Deleted"
            print build_json_message("deleted",event.src_path)

    def on_modified(self, event):
        print type(event)
        print event.src_path
        if isinstance(event, watchdog.events.FileModifiedEvent):
            print event.src_path + " Modified"
            print build_json_message("modified",event.src_path)

    def on_moved(self, event):
        print type(event)
        print event.src_path
        if isinstance(event, watchdog.events.FileMovedEvent):
            print event.src_path + " Moved"
            print build_json_message("moved",event.src_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.schedule(Watchmen(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
