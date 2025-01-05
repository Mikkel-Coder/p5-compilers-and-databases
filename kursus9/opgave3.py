"""
Opgave C

Giver det mening fra data at danne følgende relation: 
 "En spillers mængde af guld er relateret til antallet af etager der er opnået?”
 (engelsk: “a players amount of gold is related to the amounts of floor reached” 
    - hvorfor/hvorfor ikke? 
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
#         "floor_reached": 0,
#         "gold": 99,
#         "gold_per_flor": [99, 99]
#         "play_id": "2eebda8a-6486-4fed-b32e-306c66ce5b52",
#     }
# }

# Note that the document is an "event", which does not equal a player!

# Now we want to find, groupe and sort to find the player with the most floor reached
pipeline = [
    # 1. Group by player ID, their gold and max gold per floor
    {
        "$group": {
            "_id": "$event.play_id",
            "floor_reached": {
                "$max": "$event.floor_reached"
            },
            "gold": {
                "$max": "$event.gold"
            },
            "gold_per_floor": {
                "$max": "$event.gold_per_floor"
            } 
        }
    },
    # 2. Sort by the players floor reached and then gold in descending order
    {
        "$sort": {
            "floor_reached": pymongo.DESCENDING,
            "gold": pymongo.DESCENDING,
        }
    },
    # 3. Limit to the top player with the most floors
    {
        "$limit": 1
    }
]

print()

# Run the aggregation via our pipeline
top_player = event_collection.aggregate(pipeline=pipeline)
for player in top_player:
    pprint(player)
# {'_id': '83c6f708-07af-49d9-b18f-99acf180555a',
#  'floor_reached': 102,
#  'gold': 146,
#  'gold_per_floor': [999,
#                     1016,
#                     776,
#                     788,
#                     .........
#                     684,
#                     146,
#                     146,
#                     146]}

# Vi bliver spurgt om at “floor_reached” og “gold” har en sammenhæng, 
# men alene ud fra de to ser det ikke ud til at være en sammenhæng imellem de to. 
# Men hvis vi i stedet kiggede på “gold_per_floor” kunne der være en sammenhæng. 
# Det er dog svært at sige siden vi ikke er bekendt med spillet.

# We drop the database as we do not want to store it on disk
client.drop_database(db)

# Remember to close the connection to the mongodb
client.close()
