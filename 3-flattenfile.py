import json
import pprint

airbnb = open("output/all_withstate.json", "r")
airbnb = json.loads(airbnb.read())

airbnb_flat = []

for listing in airbnb:
    listing_flat = {}
    listing_flat["county"] = listing["county"]
    listing_flat["state"] = listing["state"]
    listing_flat["beds"] = listing["listing"]["beds"]
    listing_flat["id"] = listing["listing"]["id"]
    listing_flat["is_new_listing"] = listing["listing"]["is_new_listing"]
    listing_flat["lat"] = listing["listing"]["lat"]
    listing_flat["lng"] = listing["listing"]["lng"]
    listing_flat["localized_city"] = listing["listing"]["localized_city"]
    listing_flat["town"] = listing["town"]
    listing_flat["name"] = listing["listing"]["name"]
    listing_flat["person_capacity"] = listing["listing"]["person_capacity"]
    listing_flat["room_type"] = listing["listing"]["room_type"]
    listing_flat["space_type"] = listing["listing"]["space_type"]
    listing_flat["star_rating"] = listing["listing"]["star_rating"]
    listing_flat["tier_id"] = listing["listing"]["tier_id"]
    listing_flat["reviews_count"] = listing["listing"]["reviews_count"]
    listing_flat["price"] = listing["pricing_quote"]["rate"]["amount"]
    listing_flat["currency"] = listing["pricing_quote"]["rate"]["currency"]
    listing_flat["rate_type"] = listing["pricing_quote"]["rate_type"]
    listing_flat["rate_with_service_fee"] = listing["pricing_quote"]["rate_with_service_fee"]["amount"]
    listing_flat["monthly_price_factor"] = listing["pricing_quote"]["monthly_price_factor"]
    listing_flat["weekly_price_factor"] = listing["pricing_quote"]["weekly_price_factor"]
    listing_flat["can_instant_book"] = listing["pricing_quote"]["can_instant_book"]

    airbnb_flat.append(listing_flat)

with open("output/airbnb_flat.json", "w") as f:
    f.write(json.dumps(airbnb_flat))
    print "Done"