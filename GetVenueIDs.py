import requests
import csv

headers = {
    'authority': 'api.resy.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'x-origin': 'https://resy.com',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'cache-control': 'no-cache',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://resy.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://resy.com/',
    'accept-language': 'en-US,en;q=0.9',
}

params_list = [
    (('location_id', 'ny'),
    ('collection_id', '14'),
    ('day', '2022-07-04'),
    ('party_size', '2'),
    ('limit', '500'),
    ('offset', '1'),
    ('finder', '4'),),

    (('location_id', 'ny'),
    ('collection_id', '889'),
    ('day', '2022-07-04'),
    ('party_size', '2'),
    ('limit', '500'),
    ('offset', '1'),
    ('finder', '4'),
    ),

    (('location_id', 'ny'),
    ('collection_id', '891'),
    ('day', '2022-07-04'),
    ('party_size', '2'),
    ('limit', '500'),
    ('offset', '1'),
    ('finder', '4'),
    ),
    
    (('location_id', 'ny'),
    ('collection_id', '890'),
    ('day', '2022-07-04'),
    ('party_size', '2'),
    ('limit', '500'),
    ('offset', '1'),
    ('finder', '4'),
    )
]

venue_ids = []

for collection in params_list:
    print(collection)
    response = requests.get('https://api.resy.com/3/collection/venues', headers=headers, params=collection)
    dat = response.json()
    venues = dat['results']['venues']
    for v in venues:
        venue_dict = {}
        venue_info = v.get("venue")
        venue_dict["name"] = venue_info.get("name")
        venue_dict["id"] = venue_info["id"].get("resy")
        venue_dict["food"] = venue_info.get("type")
        venue_dict["price"] = venue_info.get("price_range")
        venue_dict["location"] = venue_info["location"].get("neighborhood")
        venue_dict["avg_rating"] = venue_info.get("rating")
        venue_ids.append(venue_dict)

keys = venue_ids[0].keys()

with open('venue_data.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(venue_ids)


