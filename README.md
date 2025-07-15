# Bus Stop Info

This repository provides a simple script to display live bus arrival times for a stop in Cyprus using a GTFS-realtime feed.

## Requirements
- Python 3
- `requests`
- `gtfs-realtime-bindings`
- `flask`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage
Set the following environment variables:

- `API_URL` – URL to the GTFS-realtime TripUpdates feed provided by Cyprus Public Transport.
- `API_KEY` – API key if required (optional).
- `STOP_ID` – ID of the stop to monitor.

Run the script:

```bash
python display_board.py
```

The script prints the next few arrival times in minutes. If the network request
fails, it falls back to reading `sample_trip_update.pb`. Modify `update_board` in
`display_board.py` to send the information to your hardware display.

## Web Front End

To preview how the board might look, run the small web server and open a
browser to `http://localhost:8000`:

```bash
python web_board.py
```

The page refreshes automatically every 30 seconds and shows the upcoming bus
arrivals.

