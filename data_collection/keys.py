"""
Authors: Sean Donohoe and Kyle Wiese
"""


import googlemaps
import datetime
from data_collection.cache import *

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
		]

		self.maps_keys = [ (k, True) for k in self.maps_keys ]

		self.places_keys = [
			
			'AIzaSyDg1qhBCO1I7heUbEfXKM4OSNO_EG7P-mw',
			'AIzaSyBD5fNjnMJ2vo_jWsz1x3fWXrcRb4TOAJ0',
		]

		self.places_keys = [ (k, True) for k in self.places_keys ]

		self.maps_rr = 0
		self.places_rr = 0
                self.db = initialize_cache()

	def distance_matrix(self, origins, destinations):
		maps_key, valid = self.maps_keys[self.maps_rr]
		print("maps_key #{}".format(self.maps_rr))
		
		"""
		if not valid:
			found = False
			origin = self.maps_rr
			self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)
			while self.maps_rr != origin:
				maps_key, valid = self.maps_keys[self.maps_rr]
				if valid:
					found = True
					break
				self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)

			if not found:
				raise ValueError("out of maps keys!")
		"""

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
                g = getGeoCode(self.db, address)
                if not g:
	            maps_key, valid = self.maps_keys[self.maps_rr]

		    self.maps_rr = (self.maps_rr + 1) % len(self.maps_keys)

		    client = googlemaps.Client(key=maps_key)
		    g = client.geocode(address)
                    insertGeoCode(self.db, address, g)
                return g

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
		places_key, valid = self.places_keys[self.places_rr]

		self.places_rr = (self.places_rr + 1) % len(self.places_keys)

		client = googlemaps.Client(key=places_key)
		return client.place(pid)
