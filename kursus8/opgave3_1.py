import sqlite3
from treelib import Tree

# Connect to our SQLite databse
connection = sqlite3.connect("measurementdata.db")
db_cursor = connection.cursor()

# Format the SQL query
start_topologyID = 1060
res = db_cursor.execute(
    f"SELECT TOPOLOGYELEMENTID, CONNECTIONID FROM topology WHERE TOPOLOGYID = {start_topologyID}"
)

# Run the SQL query
data = res.fetchall()
print(data)
# [(0, 1), (1, 2), (1, 87), (1, 124), (1, 172), (2, 3), (3, 4), ...]

# We create our tree and its root
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