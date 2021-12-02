from flask import Flask
from flask import render_template
import json
from threading import Thread
import time
from icmplib import ping


def thread_fn():
    while True:
        for device in config["devices"]:
            host = ping(device["ip"], count=4, interval=1, timeout=2)
            device["online"] = host.is_alive
            if host.is_alive:
                device["online_ts"] = int(time.time())
        time.sleep(10)


app = Flask(__name__)


@app.route("/index.html")
@app.route("/")
def index():
    return render_template("index.html", devices=config["devices"])


@app.route("/status", methods=["GET", "POST"])
def status():
    return json.dumps([{
        "id": device["id"],
        "online": device.get("online"),
        "online_ts": device.get("online_ts")
    } for device in config["devices"]])


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    t = Thread(target=thread_fn)
    t.start()

    app.run("0.0.0.0", "8080")
