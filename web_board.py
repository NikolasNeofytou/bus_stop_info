import os
from flask import Flask, jsonify, render_template
from display_board import fetch_feed, get_arrivals

app = Flask(__name__)
STOP_ID = os.environ.get("STOP_ID", "1234")

@app.route("/arrivals")
def arrivals():
    feed = fetch_feed()
    arrs = get_arrivals(feed, STOP_ID)
    minutes = [sec // 60 for sec in arrs]
    return jsonify(arrivals=minutes)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
