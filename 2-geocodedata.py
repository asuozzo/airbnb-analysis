import requests
import json
from time import sleep
from random import randint

api_key = [GOOGLE_MAPS_API_KEY]

def get_geo(lat, lng):

    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&key={api_key}".format(
        lat=lat,
        lon=lng,
        api_key=api_key
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url).json()
    if response["status"] == "OK" and response["results"][1]:
        placedata = response["results"][0]["address_components"]
        town = "none"
        county = "none"
        state = "none"
        for item in placedata:
            if item["types"][0] == "locality":
                town = item["long_name"]
            elif item["types"][0] == "administrative_area_level_2":
                county = item["long_name"]
            elif item["types"][0] == "administrative_area_level_1":
                state = item["long_name"]
        return town, county, state
    else:
        return "none","none","none"

def load_file(file, n):
    f = open(file, "r")
    listings = json.loads(f.read())

    for listing in listings:
        sleep(randint(0,1))

        n+=1

        town,county,state = get_geo(listing["listing"]["lat"], listing["listing"]["lng"])
        print "Item %s: %s, %s, %s" % (n,town, county, state)

        listing["state"] = state
        listing["county"] = county
        listing["town"] = town

    return listings

def get_missing_geo(lat, lng):

    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&key={api_key}".format(
        lat=lat,
        lon=lng,
        api_key=api_key
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url).json()
    if response["status"] == "OK" and response["results"][1]:
        placedata = response["results"][0]["address_components"]
        for i in placedata:
            if i["types"][0] == "neighborhood":
                return i["long_name"]



def fill_missing_towns(file, n):
    f = open(file, "r")
    listings = json.loads(f.read())

    for listing in listings:
        if listing["state"] == "Vermont" and listing["town"] == "none":
            print listing["listing"]["name"]
            town = get_missing_geo(listing["listing"]["lat"], listing["listing"]["lng"])
            print town
            listing["town"] = town

    return listings


listings = load_file("output/all.json", 0)
# listings = fill_missing_towns("output/all_withstate.json", 0)

with open("output/all_withstate.json", "w") as f:
    f.write(json.dumps(listings))
