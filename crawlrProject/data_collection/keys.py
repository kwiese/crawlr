"""
Authors: Sean Donohoe and Kyle Wiese
"""


import googlemaps
import datetime
import os
import redis
import json
from log import log

class KeyManager:

    def __init__(self):
        self.maps_keys = [
            'AIzaSyCPzQ7BurH64jXtsgwP7c7VQBK8LQPF5MY',
            'AIzaSyCPLE1prImwt1JXgbdtwfomzfiqr5bO1us',
            'AIzaSyC-FkHdIYrMklmF2VwKJUgJU5xVoJEd0nw',
            'AIzaSyDwa9wQN2Co8owZX6VaLRm9L9B7XQj6Svk',
            'AIzaSyCeRAPsVxCpJsUzWfJMxLAagpe4VeoL-8Y',
            'AIzaSyDW3rShVk6rPbo8CzZ3UbJ5NJEAu2hVz-k',
            'AIzaSyAWR52HC7ZOTkkXW0Clpzm0dT_NXo4g1vs',
            'AIzaSyAp2R3_jPn_So3xm8ljiZUMSqbFCCMClYo',
            'AIzaSyBWhJMWEILQ6mr7MG176O0vGPR8P0Rk7uU',
            'AIzaSyDcN3BM3Uc0RC2fzDJtyxxFSMEHRptjSmI',
            'AIzaSyBuzO_bX-T9oKcBK-4Xx2RqsFbd7vOnM5o',
            'AIzaSyAh9SgzoSax0WpEJkN0qnC6meNDEhRRJ2Q',
            'AIzaSyAlr4gcZFLIj0x9WcruWU9Zf8wQrvL9Vfs',
            'AIzaSyApBWdLAOodXICjW29IKIC0RkUHU4vrSH8',
#            ' AIzaSyDCwMldgD3o7cr3FE0Y-be-y150xLkk_cw',
        ]
        
        

        self.maps_keys = [ (k, True) for k in self.maps_keys ]

         
        self.places_keys = [
            'AIzaSyDg1qhBCO1I7heUbEfXKM4OSNO_EG7P-mw',
            'AIzaSyBD5fNjnMJ2vo_jWsz1x3fWXrcRb4TOAJ0',
        ]

        self.places_keys = [ (k, True) for k in self.places_keys ]

        self.maps_rr = 0
        self.places_rr = 0
        self.instance_ip = os.environ["HOSTIP"]
        self.geo_cache = redis.StrictRedis(host=self.instance_ip, port=6379, db=0)
        self.place_cache = redis.StrictRedis(host=self.instance_ip, port=6379, db=1)

    def distance_matrix(self, origins, destinations):
        maps_key, valid = self.maps_keys[self.maps_rr]
        print("maps_key #{}".format(self.maps_rr))

        self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)
        client = googlemaps.Client(key=maps_key)
        return client.distance_matrix(origins, destinations, mode="walking")

    def get_maps_key(self):
        i = self.maps_rr
        self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)
        return self.maps_keys[i][0]

    def get_places_key(self):
        i = self.places_rr
        self.places_rr = (self.places_rr + 1) % len(self.places_keys)
        return self.places_keys[i][0]

    def geocode(self, address):
        x = self.geo_cache.get(address)
        if x:
            d = json.loads(x.decode('utf-8'))
            return d
        else:
            maps_key, valid = self.maps_keys[self.maps_rr]
            self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)
            client = googlemaps.Client(key=maps_key)
            data = client.geocode(address)

            s = json.dumps(data)
            self.geo_cache.set(address, s)
            return data

    def reverse_geocode(self, geocode_val):
        maps_key, valid = self.maps_keys[self.maps_rr]

        self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)

        client = googlemaps.Client(key=maps_key)
        return client.reverse_geocode(geocode_val)

    def places_nearby(self, geocode_val, min_price=0, max_price=4, type="", open_now=True, radius=0):
        places_key, valid = self.places_keys[self.places_rr]

        self.places_rr = (self.places_rr + 1) % len(self.places_keys)

        client = googlemaps.Client(key=places_key)
        return client.places_nearby(
            geocode_val,
            min_price=min_price,
            max_price=max_price,
            type=type,
            open_now=open_now,
            radius=radius,
        )

    def place(self, pid):
        x = self.place_cache.get(pid)
        if x:
            d = json.loads(x.decode('utf-8'))
            return d
        else:
            places_key, valid = self.places_keys[self.places_rr]
            self.places_rr = (self.places_rr + 1) % len(self.places_keys)
            client = googlemaps.Client(key=places_key)
            data = client.place(pid)

            s = json.dumps(data)
            self.place_cache.set(pid, s)
            return data
