import requests
from random import randint
import collections
import itertools
import json
from time import sleep

# Find your API key as described in the readme. 
api_key = [YOUR_API_KEY_HERE]

params = {
        "version":"1.2.1",
        "_format":"for_explore_search_web",
        "items_per_grid": 310,
        "experiences_per_grid":20,
        "guidebooks_per_grid":20,
        "fetch_filters":True,
        "supports_for_you_v3":True,
        "screen_size":"large",
        "timezone_offset":-240,
        "auto_ib":True,
        "guest_from_sem_traffic":False,
        "selected_tab_id":"home_tab",
        "location":"Vermont, United States",
        "_intents":"p1",
        "key":api_key,
        "currency":"USD",
        "locale":"en",
        "search_by_map":True,
        "zoom":7
}

Point = collections.namedtuple('Point', ['lat', 'lng'])
Box = collections.namedtuple('Box', ['ne', 'sw'])


def get_listings(box, **kwargs):
        sleep(randint(0,3))
        headers = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
        url = "https://www.airbnb.com/api/v2/explore_tabs"

        params.update(kwargs)
        params.update({
                'ne_lat': box.ne.lat,
                'ne_lng': box.ne.lng,
                'sw_lat': box.sw.lat,
                'sw_lng': box.sw.lng,
        })

        r = requests.get(url, headers=headers, params=params)

        response = r.json()
        is_max = response["explore_tabs"][0]['home_tab_metadata']['pagination']['result_count'] == 300
        listings = response['explore_tabs'][0]['sections'][0]['listings']
        if is_max:
                print "Recursing for", box
                return list(itertools.chain.from_iterable(
                        get_listings(sub, **kwargs) for sub in get_subdivisions(box)))
        print "returning",len(listings)
        with open("output/ne%s-%s-sw-%s-%s.json" % (box.ne.lat, box.ne.lng, box.sw.lat, box.sw.lng), "w") as f:
            f.write(json.dumps(listings, sort_keys=True, indent=4))

        return listings
    
    
def get_subdivisions(box):
        lat_mid = (box.ne.lat + box.sw.lat) / 2.
        lng_mid = (box.ne.lng + box.sw.lng) / 2.

        return [
              # Upper right
              Box(ne=box.ne,
                  sw=Point(lat=lat_mid, lng=lng_mid)),
              # Upper left
              Box(ne=Point(lat=box.ne.lat, lng=lng_mid),
                  sw=Point(lat=lat_mid, lng=box.sw.lng)),
              # Lower left
              Box(ne=Point(lat=lat_mid, lng=lng_mid),
                  sw=box.sw),
              # Lower right
              Box(ne=Point(lat=lat_mid, lng=box.ne.lng),
                  sw=Point(lat=box.sw.lat, lng=lng_mid)),
        ]

# Here's where you specify the top left and bottom right points of your 
# desired geographical boundaries.
b = Box(ne=Point(lat=42.80564, lng=-73.2000),
        sw=Point(lat=42.697843, lng=-73.479597))


listings = get_listings(b)

with open("output/all.json", "w") as f:
    f.write(json.dumps(listings, sort_keys=True, indent=4))
