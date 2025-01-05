"""
Opgave 3.1

For each cable element, there is a connected element (connectionID) pin pointing
the connection (zero is root node)
• Take a grid e.g. topologyID = 1060 and find the longest ”tree distance” from root to a bottom node. 
  How many nodes are there in between?

"""

import sqlite3 # The "driver" to talk to the db via
from treelib import Tree # For making the tree
from pathlib import Path # Not important for the assignment 

# For sanity, check if the DB exists
database_file = Path("measurementdata.db")
if not database_file.exists():
    print("I cannot find the \"measurementdata.db\" database. Please move the file to here")
    exit(1)

# Connect to our SQLite databse
connection = sqlite3.connect(database_file)
db_cursor = connection.cursor()

# Format the SQL query
# Not that safe to do (SQL injection)
start_topologyID = 1060
res = db_cursor.execute(
    f"SELECT TOPOLOGYELEMENTID, CONNECTIONID FROM topology WHERE TOPOLOGYID = {start_topologyID}"
)

# Run the SQL query
data = res.fetchall()
print(data)
# The first number in the tuple is the topologyelementID used to uniquely identify each "transformer station"
# The seconde number is what the topologyelement is connected to
# [(0, 1), (1, 2), (1, 87), (1, 124), (1, 172), (2, 3), (3, 4), ...]

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

    # Else append a new node
    tree.create_node(f"node-{row[1]}", row[1], parent=row[0])

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

# and the depth
print(tree.depth())
# 23

# Remember to close the connection to the database
connection.close()