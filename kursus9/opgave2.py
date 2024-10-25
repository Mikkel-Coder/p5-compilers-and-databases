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
#     "_id": "6708cfc38a4383c3518b8002",
#     "event": {
#         "gold": 60,
#         "play_id": "439a9a50-75dd-43ea-a1f8-0fe4d92f39b1",
#         "playtime": 3451,
#     }
# }

# Now we create our pipeline
pipeline = [
    # 1. First groupe by the players id, gold and playtime
    {
        "$group": {
            "_id": "$event.play_id",
            "gold": {
                "$max": "$event.gold"
            },
            "playtime": {
                "$max": "$event.playtime"
            }
                
        }
    },
    # 2. Match where there is a cheater!
    # A player is a cheater when they have more than 20K gold
    # and has played less than 1000
    {
        "$match": {
            "gold": {
                "$gte": 20_000
            },
            "playtime": {
                "$lte": 1_000
            }
        }
    }
]

print()

# Print all the cheaters
cheaters = event_collection.aggregate(pipeline=pipeline)
for i, cheater in enumerate(cheaters, 1):
    print(f"player_id: {cheater["_id"]}, gold: {cheater["gold"]}, playtime: {cheater["playtime"]}")
    # player_id: f3a06b42-c749-4c03-888a-20e26468bb47, gold: 28599, playtime: 756
    # player_id: 0a1d2ebf-92d2-48c5-b18b-8b2314ab37d6, gold: 97319, playtime: 411

print(f"Found {i} cheater(s)")
# Found 2 cheater(s)

# We drop the database as we do not want to store it on disk
client.drop_database(db)

# Remember to close the connection to the mongodb
client.close()
