from queue import Queue
import sqlite3
# DOCS: https://treelib.readthedocs.io/en/stable/pyapi.html
from treelib import (
    Tree,
    Node,
)

from opgave3_3_current_data import CurrentData


def main() -> None:
    # 1. Connect to DB
    # 2. Get the topology of the electrical grid
    # 3. Convert the topology to a tree
    # 4. Remove redundant nodes
    # 5. Reverse walk the tree from each leaf to the root, noting each branch
    # 6.    Also Fix off by one error (Rasmus)
    # 7. Get the currents from the known leafs in the electrical topology (leaves)
    # 8. For each branch (bottom up) append the children's to the branch node recursively

    # 1. CONNECT TO DB
    # Connect to our SQLite databse
    connection = sqlite3.connect("measurementdata_v3.db")
    db_cursor = connection.cursor()

    # Format the SQL query
    topology_id: int = 1124
    res: sqlite3.Cursor = db_cursor.execute(
        f"""
        SELECT
            TOPOLOGYELEMENTID,
            CONNECTIONID
        FROM
            topology
        WHERE
            TOPOLOGYID = {topology_id}
            AND ID < 10000
        """
    )

    # 2. GET THE TOPOLOGY OF THE ELECTRICAL GRID
    # Run the SQL query
    data: list[tuple[int, int]] = res.fetchall()

    # 3. CONVERT THE TOPOLOGY TO A TREE
    # We create our tree and its root
    tree = Tree()
    tree.create_node(tag=0, identifier=0, data=CurrentData([0.0, 0.0, 0.0]))

    # Now loop over each row
    # We make the tree from the top
    for row in data:
        # Skip null nodes that are connected to leaves
        if row[1] == 0:
            continue

        # Else append a new node
        tree.create_node(
            tag=row[1],
            identifier=row[1],
            parent=row[0],
            data=CurrentData([0.0, 0.0, 0.0]),
        )

    # 4. REMOVE REDUNDANT NODES
    # Remove redundant nodes that are not important for kirchoffs law
    # For every path from the root to each leaf, we must check if
    # a node can be removed (has only one child)
    for path in tree.paths_to_leaves():
        for node_id in path:

            # If the current node_id has been remove from the path
            if node_id is None:
                # Then skip it
                continue

            # Get the current node as an object
            current_node: Node = tree.get_node(node_id)

            # Skip root node as we cannot remove it
            if current_node.is_root():
                continue

            # If the current node only has one child
            children: list[Node] = tree.is_branch(current_node.identifier)
            if len(children) == 1:
                # Then replace the current node with the child,
                # and remove the current node
                tree.link_past_node(current_node.identifier)

    # 5. REVERSE WALK THE TREE FROM EACH LEAF TO THE ROOT, NOTING EACH BRANCH
    # Walk bottom up fixing off by 1 error and assembling nodes to work on after we have data
    # AKA: We are fixing the tree (topology)
    known_leaves: list[int] = []  # Used for Database SQL query
    work_queue = Queue()  # Used later for calculation currents for all branches
    seen_branch_nodes: list[int] = []

    # For each leaf in the tree
    for leaf in tree.leaves():
        # 6. ALSO FIX OFF BY ONE ERROR (RASMUS)
        # Fix off by 1 errors
        # NOTE FROM RASMUS: "The leaf nodes in the database is off by +1"
        known_leaves.append(leaf.tag + 1)

        # For each node in the path from a leaf to root
        for node_id in tree.rsearch(leaf.identifier):

            # Skip if we already known about the node
            if node_id in seen_branch_nodes:
                continue

            # Otherwise add the node to the work queue (to be calculate later)
            # for finding its currents according to kirchoffs law
            # NOTE: a leaf is a node with no children
            child_ids: list[int] = tree.is_branch(node_id)
            if len(child_ids) > 0:
                work_queue.put((node_id, child_ids))
                seen_branch_nodes.append(node_id)

    print(known_leaves)
    # [5, 8, 10, 12]

    # 7. GET THE CURRENTS FROM THE KNOWN LEAFS IN THE ELECTRICAL TOPOLOGY (LEAVES)
    # Get the currents for the leaves in the database
    # NOTE: Map is here to make them into strings
    topologyelementid_sql: str = ", ".join(map(str, known_leaves))
    res: sqlite3.Cursor = db_cursor.execute(
        f"""
        SELECT
            TOPOLOGYELEMENTID,
            C_L1,
            C_L2,
            C_L3
        FROM
            measurements
        WHERE
            TOPOLOGYID = {topology_id}
            AND TOPOLOGYELEMENTID IN ({topologyelementid_sql})
            AND ID < 10000
            AND time = 0;
        """
    )
    # Run the SQL query
    data: list[int, float, float, float] = res.fetchall()

    # Append the current (in Amps) to the known nodes (leaves)
    for node_id, c_l1, c_l2, c_l3 in data:
        node: Node = tree.get_node(node_id - 1)  # The database if off by -1
        node.data.currents = [c_l1, c_l2, c_l3]

    # 8. FOR EACH BRANCH (BOTTOM UP) APPEND THE CHILDREN'S TO THE BRANCH NODE RECURSIVELY
    # Add the current to each branch bottom up (implemented by the work_queue)
    # AKA: Do the work
    while not work_queue.empty():
        # Get the current branch's node_id and its children's ids
        node_id, child_ids = work_queue.get()
        node: Node = tree.get_node(node_id)

        # For each child
        for child_id in child_ids:
            # Get the child as a node object
            child: Node = tree.get_node(child_id)

            # Accumulate each phase current (c_l1, c_l2, c_l3) from the child
            # to parent (aka the current node that is a branch)
            for i, current_line in enumerate(child.data.currents):
                node.data.currents[i] += current_line

    # Print the tree
    print(tree.show(stdout=False, data_property="currents", idhidden=False))
    # NOTE: Remember that the database is off by 1 for each leaf
    # [1.3830969800774222, -1.7124229534248472, 3.21691834766456][0]
    # └── [1.3830969800774222, -1.7124229534248472, 3.21691834766456][1]
    #     ├── [0.15212638714044344, -0.6217535962351239, 0.6105817290372278][4]
    #     ├── [0.10697479186012085, -0.6669051915154466, 0.5654301337569053][7]
    #     ├── [0.6596985427374489, -0.11418144063811853, 1.1181538846342334][9]
    #     └── [0.46429725833940905, -0.30958272503615836, 0.9227526002361934][11]

    # Remember to close the connection to the database
    connection.close()


if __name__ == "__main__":
    main()