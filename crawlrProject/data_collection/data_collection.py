"""
Authors: Sean Donohoe and Kyle Wiese

An implementation to collect place data based on specified user constraints from the googlemaps API
"""


import datetime
import asyncio
import traceback
import googlemaps
import time
import unicodedata
import dateutil.parser as dt
import redis
import os
import json

from log import log, perf
from data_collection.keys import KeyManager

km = KeyManager()

def collectData(user_data):
    all_data = {}
    log("Starting Collection")
    log(user_data["timestamp"])
    try:
        event_loop = asyncio.SelectorEventLoop()
        place_data = event_loop.run_until_complete(collectUserData(user_data, event_loop))
        place_data = filterPlaces(place_data)
        distance_data = event_loop.run_until_complete(collectMapData(place_data, event_loop))

        all_data["user_data"] = user_data
        all_data["place_data"] = place_data
        all_data["distance_data"] = distance_data
    except Exception as e:
        log(traceback.format_exc())
    finally:
        return all_data

#async def generateMapData(origins, destinations, j, frm, to, maps_key):
def generateMapData(origins, destinations, names, maps_key):
    client = googlemaps.Client(key=maps_key)
    d_data = {}
    t = time.time()
    dest_data = client.distance_matrix(
        origins,
        destinations,
        mode="walking",
    )
    c_time = (time.time() - t)
    o_names = [ (n, a, False) for n, a in names ]
    d_names = [ (n, a, False) for n, a in names ]

    o_addr = []
    for addr in origins:
        for k in range(len(o_names)):
            n, a, v = o_names[k]
            if a == addr and not v:
                o_addr.append(n)
                o_names[k] = (n, a, True)
                break
    d_addr = []
    for addr in destinations:
        for k in range(len(d_names)):
            n, a, v = d_names[k]
            if a == addr and not v:
                d_addr.append(n)
                d_names[k] = (n, a, True)
                break

    for i in range(len(dest_data["rows"])):
        fromName = o_addr[i]
        for j in range(len(dest_data["rows"][i]["elements"])):
            toName = d_addr[j]
            if fromName != toName:
                dist_obj = dest_data["rows"][i]["elements"][j]
                if "duration" in dist_obj:
                    d_data[(fromName, toName)] = 30 + dest_data["rows"][i]["elements"][j]["duration"]["value"]
                else:
                    d_data[(fromName, toName)] = 30
    return (d_data, c_time)

async def collectMapData(place_data, event_loop):
    distance_data = {}

    glob_place_data = [ place_data[k] for k in place_data ]
    glob_place_data = [ (item["name"], item["address"]) for row in glob_place_data for item in row ]
    glob_place_data.sort(key=lambda tup: tup[0])

    origins = [ a for n, a in glob_place_data ]
    destinations = [ a for n, a in glob_place_data ] 
    names = [ (n, a) for (n, a) in glob_place_data ]

    placedata = []
    for i in range(0, len(origins), 10):
        for j in range(0, len(origins), 10):
            placedata.append(event_loop.run_in_executor(
                None,
                generateMapData,
                origins[i:min(i+10, len(origins))], 
                destinations[j:min(j+10, len(origins))],
                names,
                km.get_maps_key(),
            ))
    times = []
    for n in placedata:
        res, c = await n
        times.append(c)
        for k in res:
            distance_data[k] = res[k]

    if len(times):
        pdata = [("Average map time", (sum(times)/len(times))), ("Total map time", sum(times))]
        perf(pdata)
            
    return distance_data

def generateUserData(p, current_day, key_weight, user_data, maps_key, places_key, ):
    place_cache = redis.StrictRedis(host=os.environ["HOSTIP"], port=6379, db=1)
    dobj = dt.parse(user_data["timestamp"])
    
    place_grab = time.time()
    x = place_cache.get(p["place_id"])
    if x:
        placeStats = json.loads(x.decode('utf-8'))
    else:
        places_client = googlemaps.Client(key=places_key)
        placeStats = places_client.place(p["place_id"])
        s = json.dumps(placeStats)
        place_cache.set(p["place_id"], s)

    placeTime = (time.time() - place_grab)
    rating = None 
    orig_rating = None
    website = None
    try:
        rating = placeStats["result"]["rating"]
        orig_rating = rating
        rating = rating * key_weight
    except KeyError:
        rating = 1
        orig_rating = 0
    try:
        website = placeStats["result"]["website"]
    except KeyError:
        website = None
    trange = (0, None)
    try:
        opening_hours = placeStats["result"]["opening_hours"]["periods"]
        for day in opening_hours:
            if day["open"]["day"] == current_day:
                opening = int(day["open"]["time"])
                closing = None
                if "close" in day:
                    if (day["close"]["time"] is not None):
                        closing = int(day["close"]["time"]) 
                trange = (opening, closing)
                break
    except Exception as e:
        raise e
    timeOk = True
            
    if (trange[1] is not None):
        n = dobj.time()
        nowTime = (n.hour*100) +  n.minute
        dur = user_data["time"]
        durHour = dur / 3600
        durMin = (dur - (durHour * 3600)) / 60
        durr = (durHour * 100) + durMin
        if trange[1] < trange[0]:
            if (nowTime + durr) >= 2400:
                durr = (nowTime + durr) % 2400
                if durr > trange[1]:
                    timeOk = False
        else:   
            timeOk = ((nowTime + durr) <= trange[1])


    if (timeOk):
        n = p["name"]+" ("+placeStats["result"]["formatted_address"].replace(",", "")+")"
        newItem = {
            "name":  scrub(n),
            "opening_hours":  trange,
            "price_level":  p["price_level"],
            "rating": rating,
            "original_rating": orig_rating,
            "address": scrub(placeStats["result"]["formatted_address"]),
            "website": website,
        }
        return (newItem, placeTime)
    return None

def scrub(s):
    better = "".join(c for c in s if unicodedata.category(c)[0] != "C")
    return better.replace("&", "and")

async def collectUserData(user_data, event_loop):
    current_day = datetime.datetime.today().weekday()
    if current_day == 6:
        current_day = 0
    else:
        current_day += 1
    
    places = {keyword: [] for keyword in user_data['keywords'] + ["HOME"]}


    geocode = km.geocode(user_data['start_address'])
    
    geocode_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])
    da = km.reverse_geocode(geocode_tup)
    home_addr = da[0]["formatted_address"]
    homeItem = {
        "name":  "HOME",
        "opening_hours":  (0, 2359),
        "price_level":  0,
        "rating": 0,
        "original_rating": 0,
        "address": home_addr,
        "website": None,
    }
    places["HOME"].append(homeItem)

    seen_places = []
    placeTimes = []
    pdata = []
    
    for keyword in user_data['keywords']:
        key_weight = user_data["weights"][keyword]
        data = km.places_nearby(
            geocode_tup,
            min_price=0,
            max_price=4,
            type=keyword,
            open_now=True,
            radius=user_data['radius'],
        )
        placedata = [
            event_loop.run_in_executor(None, generateUserData, p, current_day, key_weight, user_data, km.get_maps_key(), km.get_places_key())
            for p in data["results"]
        ]
        for n in placedata:
            res = await n
            if res and (res[0]["name"], res[0]["address"]) not in seen_places:
                places[keyword].append(res[0])
                seen_places.append((res[0]["name"], res[0]["address"]))
                placeTimes.append(res[1])
    pdata.append(("Total place grab time", sum(placeTimes)))
    if len(placeTimes) > 0:
        pdata.append(("Number of place times", len(placeTimes)))
        pdata.append(("Average place grab time", (sum(placeTimes)/len(placeTimes))))
    pdata.append(("Requesting time", (str(dt.parse(user_data["timestamp"])))))
    perf(pdata)
    return places

def filterPlaces(place_data):
    filtered_places = {k: [] for k in place_data}
    filtered_places["HOME"] = place_data["HOME"]

    glob_place_data = [ place_data[k] for k in place_data ]
    ratings = [ item["rating"] for row in glob_place_data for item in row ]
    ratings.sort()
    threshold = int(len(ratings)/4)
    min_rating = ratings[threshold]
    
    for k in place_data:
        if k != "HOME":
            for place in place_data[k]:
                if place["rating"] >= min_rating:
                    filtered_places[k].append(place)

    return filtered_places    
