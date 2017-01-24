import pickledb

def getGeoCode(db, address):
    return db.get(address)

def insertGeoCode(db, address, geocode):
    db.set(address, geocode)

def initialize_cache():
    return db.load("cache.db", False)
