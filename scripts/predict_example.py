"""Minimal client showing how to call the running API.

Start the server first (``make run``), then run: ``python scripts/predict_example.py``
"""

from __future__ import annotations

import json
import urllib.request

URL = "http://localhost:8000/predict"

payload = {
    "inputs": [
        {
            "MedInc": 8.3252,
            "HouseAge": 41.0,
            "AveRooms": 6.9841,
            "AveBedrms": 1.0238,
            "Population": 322.0,
            "AveOccup": 2.5556,
            "Latitude": 37.88,
            "Longitude": -122.23,
        }
    ]
}

request = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(request) as response:
    print(json.dumps(json.loads(response.read()), indent=2))
