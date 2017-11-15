import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import random

filename = "output/airbnb_flat.json"


def getUser(link):
    try:
        r = requests.get(link)
        time.sleep(2)

        soup = BeautifulSoup(r.content, "html5lib")

        result = soup.find(
            "script", {'data-hypernova-key': 'p3show_marketplacebundlejs'})

        result = result.text.split('<!--')[1]
        result = result.split('-->')[0]

        result_json = json.loads(result)
        hostid = "https://www.airbnb.com" + \
            result_json["bootstrapData"]["reduxData"]["marketplacePdp"]["listingInfo"]["listing"]["primary_host"]["profile_path"]
        hostname = result_json["bootstrapData"]["reduxData"]["marketplacePdp"]["listingInfo"]["listing"]["primary_host"]["host_name"]

        return [hostname, hostid]

    except Exception as e:
        print e


def getList(filename):
    airbnb_list = []
    i = 0

    airbnb = open(filename, "r")
    airbnb = json.loads(airbnb.read())

    for listing in airbnb:
        print "working on %s" % i
        i += 1

        if listing.get("hostname") == None:
            link = "https://www.airbnb.com/rooms/%s" % listing["id"]
            randtime = random.randint(1, 4)
            time.sleep(randtime)
            host = getUser(link)
            try:
                listing["hostname"] = host[0]
                listing["hostid"] = host[1]
            except Exception as e:
                print "skipped"
        else:
            print listing["hostname"]

    with open(filename, "wb") as f:
        f.write(json.dumps(airbnb))

getList(filename)
