import json
import requests
dummy = {
    "keywords": ["restaurant", "cafe"],
    "start_address": "1521 Pearl St, Boulder, CO",
    "radius": 100,
    "budget": 3,
    "time": 3600,
    "weights": {"restaurant": 1, "cafe": 1},
    "strictness": {},
    "bounds": {"restaurant": 3600, "cafe": 3600},
}
url = "http://127.0.0.1:8002/query"
response = requests.post(url, json=dummy)
print(type(response.json()))
