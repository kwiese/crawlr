"""
Authors: Sean Donohoe and Kyle Wiese

An implementation to collect place data based on specified user constraints from the googlemaps API
"""


import datetime
import asyncio
import logging
import traceback
import googlemaps
import time

from data_collection.keys import KeyManager

km = KeyManager()
event_loop = asyncio.get_event_loop()

def collectData(user_data):
    all_data = {}
    try:
        place_data = event_loop.run_until_complete(collectUserData(user_data))
        distance_data = event_loop.run_until_complete(collectMapData(place_data))

        all_data["user_data"] = user_data
        all_data["place_data"] = place_data
        all_data["distance_data"] = distance_data
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        return all_data

#async def generateMapData(origins, destinations, j, frm, to, maps_key):
def generateMapData(origins, destinations, names, maps_key):
    client = googlemaps.Client(key=maps_key)
    d_data = {}
    dest_data = client.distance_matrix(
        origins,
        destinations,
        mode="walking",
    )
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
                d_data[(fromName, toName)] = 30 + dest_data["rows"][i]["elements"][j]["duration"]["value"]
    return d_data

async def collectMapData(place_data):
    distance_data = {}

    glob_place_data = [ place_data[k] for k in place_data ]
    glob_place_data = [ (item["name"], item["address"], item["geo_loc"]) for row in glob_place_data for item in row ]
    glob_place_data.sort(key=lambda tup: tup[0])
    print("found {} places".format(len(glob_place_data)))

    origins = [ a for n, a, l in glob_place_data ]
    destinations = [ a for n, a, l in glob_place_data ] 
    names = [ (n, a) for (n, a, l) in glob_place_data ]

    placedata = []
    loop = asyncio.get_event_loop()
    for i in range(0, len(origins), 10):
        for j in range(0, len(origins), 10):
            print(len(origins[i:min(i+10, len(origins))]))
            placedata.append(loop.run_in_executor(
                None,
                generateMapData,
                origins[i:min(i+10, len(origins))], 
                destinations[j:min(j+10, len(origins))],
                names,
                km.get_maps_key(),
            ))
#    for n in asyncio.as_completed(placedata):
    for n in placedata:
        res = await n
        for k in res:
            distance_data[k] = res[k] 
    return distance_data

#async def generateUserData(p, current_day, key_weight, user_data, maps_key, places_key):
def generateUserData(p, current_day, key_weight, user_data, maps_key, places_key):
    maps_client = googlemaps.Client(key=maps_key)
    places_client = googlemaps.Client(key=places_key)
    
    place_grab = time.time()
    placeStats = places_client.place(p["place_id"])
    print("place grab: {}".format((time.time() - place_grab)))
		
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
                if (day["close"]["time"] is not None):
                    closing = int(day["close"]["time"]) 
                trange = (opening, closing)
                break
    except KeyError:
        pass
    timeOk = True
            
    if (trange[1] is not None):
        n = datetime.datetime.now().time()
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

    geocode_grab = time.time()
    geocode = maps_client.geocode(placeStats["result"]["formatted_address"])
    print("geocode grab: {}".format((time.time() - geocode_grab)))

    if (len(geocode) > 0 and timeOk):
        geo_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])
        newItem = {
            'name':  p["name"]+" ("+placeStats["result"]["formatted_address"].replace(",", "")+")",
            'opening_hours':  trange,
            'price_level':  p["price_level"],
            'rating': rating,
            'original_rating': orig_rating,
            'address': placeStats["result"]["formatted_address"],
            'geo_loc': geo_tup,
            'website': website,
        }
        return newItem
    return None

async def collectUserData(user_data):
    current_day = datetime.datetime.today().weekday()
    if current_day == 6:
        current_day = 0
    else:
        current_day += 1
    
    places = {keyword: [] for keyword in user_data['keywords'] + ["HOME"]}


    geocode = km.geocode(user_data['start_address'])
    print(geocode)
    
    geocode_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])
    da = km.reverse_geocode(geocode_tup)
    home_addr = da[0]["formatted_address"]
    homeItem = {
        'name':  "HOME",
        'opening_hours':  (0, 2359),
        'price_level':  0,
        'rating': 0,
        'original_rating': 0,
        'address': home_addr,
        'geo_loc': geocode_tup,
        'website': None,
    }
    places["HOME"].append(homeItem)

    seen_places = []

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
        """
        placedata = [ generateUserData(p, current_day, key_weight, user_data, km.get_maps_key(), km.get_places_key()) for p in data["results"] ]
        for n in asyncio.as_completed(placedata):
            res = await n
            if res and (res["name"], res["address"]) not in seen_places:
                places[keyword].append(res)
                seen_places.append((res["name"], res["address"]))
        """
        loop = asyncio.get_event_loop()
        placedata = [
            loop.run_in_executor(None, generateUserData, p, current_day, key_weight, user_data, km.get_maps_key(), km.get_places_key())
            for p in data["results"]
        ]
        for n in placedata:
            res = await n
            if res and (res["name"], res["address"]) not in seen_places:
                places[keyword].append(res)
                seen_places.append((res["name"], res["address"]))
    return places
