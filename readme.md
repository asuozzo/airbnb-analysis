## Scrape Airbnb data

Before you start, head to any Airbnb search page and load it while looking at network requests in your browser. Filter by XHR, and you should see a few urls that look like API calls. Find one that contains the "key" param, copy that key.

Also, create an `output` folder in the main directory where your scripts can save files.

### Get the data
Next, open `1-scrapedata.py`. This script will get you a json file of all locations within two northeast/southwest points you specify. Enter the key you found as your `api_key`, then scroll down to the definition for `b` near the bottom. Pick northeast and southwest points that form a rectangle around the area you'd like to get data for, then run the script.

This script will grab information from the search API that Airbnb uses to send information to your browser. The API will only return a maximum of 300 results for any area, so if the API returns 300 results, the script will divide the search area into four quadrants and make an API request with the narrower geographical location. It'll keep subdividing until the API returns a result with fewer than 300 items.

Each individual search result will dump to a file in the output folder, and all results are concatenated in `output/all.json`. You can get rid of the individual results once the script has run, but this will at least let you see how far the script got if it errors out.

### Reverse geocode the data
Now we've got a truckload of Airbnb data, but ideally each Airbnb listing should have a city, county and state attached to it. The API returns the town that the host listed, which is not always correct — sometimes people list a nearby popular town so the listing shows up in searches. But we've also got a lat/lng point for each listing, which means we can reverse geocode the points using Google's geocode API. These points are jittered to protect the host's privacy, but unless the listing is right on a border it should get us the correct city, state and county.

Before you run this script, head to the Google API console and get yourself an API key ([instructions here](https://developers.google.com/maps/documentation/geocoding/get-api-key)). Pop it into the `api_key` variable in `2-geocodedata.py`.

Run the file, and you'll get a file of listings with geographic information in `output/all_withstate.json`. This doesn't always get all the listings. If you end up with a bunch of un-geocoded listings, comment out the `load_file` function and run the `fill_missing_towns` function on the geocoded file instead.

### Flatten file
Great, you've got a massive json file now. The problem? It's nested and has a ton of excess stuff that we just don't need. If you don't want to those headaches, run `3-flattenfile` to get a simpler json file of all the listings.

### Get host info for each listing
This one is optional; if you've got a really massive dataset, you may want to run this script on a smaller file, as it involves loading each page and using Beautiful Soup to parse the information on that page. If you don't get all the hosts the first time around, you can re-run the script and it will try to fill in the blanks.

### Now for the fun part
Run `jupyter notebook` from your command line (or pip install first, if you don't have it set up yet). In the browser window that pops up, navigate to `notebook/explore-airbnb-data.ipynb`. Then start exploring your data!