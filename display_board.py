import os
import time
import requests
from google.transit import gtfs_realtime_pb2

API_URL = os.environ.get('API_URL', 'https://api.example.com/gtfs-rt/TripUpdates')
API_KEY = os.environ.get('API_KEY')

STOP_ID = os.environ.get('STOP_ID', '1234')

HEADERS = {}
if API_KEY:
    HEADERS['Authorization'] = f'Bearer {API_KEY}'


def fetch_feed():
    resp = requests.get(API_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(resp.content)
    return feed


def get_arrivals(feed, stop_id):
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
    for i, seconds in enumerate(arrivals[:5], start=1):
        minutes = seconds // 60
        print(f"Bus {i} arriving in {minutes} min")


def main():
    feed = fetch_feed()
    arrivals = get_arrivals(feed, STOP_ID)
    update_board(arrivals)


if __name__ == '__main__':
    main()
