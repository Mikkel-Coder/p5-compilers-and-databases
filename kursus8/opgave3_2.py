"""
Opgave 3.2

For each cable element, there is a connected element (connectionID) pin 
pointing the connection (zero is root node)
• Each cable segment (identified with a topologyID) has a resistance 
  that can be summed to find the total resistance. what is the total
  resistance for the longest path?

"""

import sqlite3 # The "driver" to talk to the db via
from treelib import Tree # For making the tree so we can find the longest resistance
from pathlib import Path # Not important for the assignment 

# For sanity, check if the DB exists
database_file = Path("measurementdata.db")
if not database_file.exists():
    print("I cannot find the \"measurementdata.db\" database. Please move the file to here")
    exit(1)

# Connect to our SQLite databse
connection = sqlite3.connect("measurementdata.db")
db_cursor = connection.cursor()

# Format the SQL query
# Not that safe to do (SQL injection)
start_topologyID = 1060
res = db_cursor.execute(
    f"SELECT TOPOLOGYELEMENTID, CONNECTIONID, RESISTIVITY FROM topology WHERE TOPOLOGYID = {start_topologyID}"
)

# Run the SQL query
data = res.fetchall()
print(data)
# The first number in the tuple is the topologyelementID used to uniquely identify each "transformer station"
# The seconde number is what the topologyelement is connected to
# The 3rd is the resistance for the first topologyelementID 
# [(0, 1, 5.116312933119511), (1, 2, 6.318213372549275), (1, 87, 6.318213372549275), ...]

# We create our tree and its root
# You could see the root as the power plant
tree = Tree()
tree.create_node("root", 0)

# Now loop over each row
# We make the tree from the top
for row in data:
    # Skip null nodes that are connected to leaves
    if row[1] == 0:
        continue

    # Else append a new node with its resistivity as data argument
    tree.create_node(f"node-{row[1]}", row[1], parent=row[0], data=row[2])

# Print the tree formatted
print(tree.show(stdout=False))
# root
# └── node-1
#     ├── node-124
#     │   └── node-125
#     │       └── node-126
#     │           ├── node-127
#     │           ├── node-128
#     │           │   └── node-129
# .....

tree_depth = tree.depth()

# Find the longest path (optimized because we know the depth)
longest_path = []
for path in tree.paths_to_leaves():
    if len(path) -1 == tree_depth: # Exclude the root node in the tree depth
        longest_path = path[1:] # Slice off the root node
        break

# Find the sum of all resistances in the longest path
resistance = 0
for node_id in longest_path:
    node = tree.get_node(node_id)
    resistance += node.data

# Print the resistance
print(resistance)
# 115.35495417982489

# Remember to close the connection to the database
connection.close()