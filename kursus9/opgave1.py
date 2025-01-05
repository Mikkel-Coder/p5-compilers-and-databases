"""
Opgave A

Find ud af hvilke tre spillere af spillet har spillet i længst tid?
"""

from os import listdir, path    # Used to get all the json databases from the os
from pprint import pprint       # Used to print document so they look good
import json                     # Used to read in the json database files
import pymongo                  # Our database program interface

# Create the mongo client
client = pymongo.MongoClient(host="localhost", port=27017)
db = client["database"]
event_collection = db["data"]

# Read in the databases from the json file
json_directory = "slay-the-data-subset-80MB/slay-the-data-subset-mini/"

for filename in listdir(json_directory):
    file_path = path.join(json_directory, filename)
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        event_collection.insert_many(json_data)

# We print a single document to see what it looks like
pprint(event_collection.find_one())
# For what we need it looks like this...
# {
#     "_id": "6707cd8b6b91435d8977a52b",
#     "event": {
#         "playtime": 5,
#         "play_id": "2eebda8a-6486-4fed-b32e-306c66ce5b52",
#     }
# }

# Note that the document is an "event", which does not equal a player!

# Now we want to find, groupe and sort after the players with the most playtime
pipeline = [
    # 1. Groupe by the maximum playtime per player
    {
        "$group": {
            "_id": "$event.play_id", 
            "playtime": {
                "$max": "$event.playtime"
            }
        }
    },
    # 2. Sort each playtime by descending
    {
        "$sort": {
            "playtime": pymongo.DESCENDING
        }
    },
    # 3. Limit to only top 3 players
    {
        "$limit": 3
    },
]

# Run the aggregation via our pipeline
top_players = event_collection.aggregate(pipeline=pipeline)
for player in top_players:
    print(f"play_id: {player["_id"]}   playtime: {player["playtime"]}")
    # play_id: 7557b2c1-7ac6-4cdf-8a8c-0086d2953e7a   playtime: 252560
    # play_id: 93c6e89c-3c70-4a24-9c46-169e8a1033a4   playtime: 108472
    # play_id: 877ae757-33a9-4448-879a-7d85d121ffcd   playtime: 107772

# We drop the database as we do not want to store it on disk
client.drop_database(db)

# Remember to close the connection to the mongodb
client.close()
