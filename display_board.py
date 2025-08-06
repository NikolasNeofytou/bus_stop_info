import os
import time
import requests
from google.transit import gtfs_realtime_pb2
from requests.exceptions import RequestException
from google.protobuf import text_format

API_URL = os.environ.get('API_URL')
API_KEY = os.environ.get('API_KEY')

STOP_ID = os.environ.get('STOP_ID', '1234')
LOCAL_FEED = os.environ.get('LOCAL_FEED', 'sample_trip_update.pb')

HEADERS = {}
if API_KEY:
    HEADERS['Authorization'] = f'Bearer {API_KEY}'


def fetch_feed():
    """Fetch TripUpdates feed.

    Falls back to reading ``LOCAL_FEED`` if ``API_URL`` is not set or the
    download fails.
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    if not API_URL:
        print(f"API_URL not set. Using local file '{LOCAL_FEED}'.")
        with open(LOCAL_FEED, "rb") as fh:
            data = fh.read()
            try:
                feed.ParseFromString(data)
            except Exception:
                text_format.Parse(data.decode("utf-8"), feed)
        return feed

    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        feed.ParseFromString(resp.content)
    except RequestException as exc:
        print(
            f"Warning: failed to download feed ({exc}). Using local file '{LOCAL_FEED}'."
        )
        with open(LOCAL_FEED, "rb") as fh:
            data = fh.read()
            try:
                feed.ParseFromString(data)
            except Exception:
                text_format.Parse(data.decode("utf-8"), feed)
    return feed


def get_arrivals(feed, stop_id):
    """Return a list of arrival times in seconds from now for ``stop_id``."""
    arrivals = []
    now = int(time.time())
    for entity in feed.entity:
        if not entity.HasField('trip_update'):
            continue
        for stu in entity.trip_update.stop_time_update:
            if stu.stop_id == stop_id and stu.HasField('arrival') and stu.arrival.time >= now:
                arrivals.append(stu.arrival.time)
    arrivals.sort()
    return [t - now for t in arrivals]


def update_board(arrivals):
    """Print arrival information.

    Replace this function with code that updates your physical display.
    """
    for i, seconds in enumerate(arrivals[:5], start=1):
        minutes = seconds // 60
        print(f"Bus {i} arriving in {minutes} min")


def main():
    feed = fetch_feed()
    arrivals = get_arrivals(feed, STOP_ID)
    if arrivals:
        update_board(arrivals)
    else:
        print("No upcoming arrivals found.")


if __name__ == '__main__':
    main()
