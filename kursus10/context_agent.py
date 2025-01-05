from __future__ import annotations # Not important. Just used for ContextAgent type hint
from typing import Any # Not important. Just used for type notation
from multiprocessing import Process, Pipe # So that the Context agent can communication with "main.py"
import sqlite3 # Every context agent has their own SQL database

from random_data_maker import RandDataMaker # Object that generates data to mimic temperature for example
from utils import flatten # Not important. Just used to send "clean" data via pipes


class ContextAgent(Process):
    """
    A Context Agent extends from an OS process. 
    
    The Context Agent each have their own database and RandomDataMaker Thread.
    You can check for a process tree by "pstree" in GNU/Linux.
    """
    def __init__(self, context_agents: list[ContextAgent], name: str = None):
        # Each Context Agent knows every other context agent
        self.context_agents: list[ContextAgent] = context_agents

        # And the context agent communicates with it random data maker via a pipe
        self._parent_conn, self.child_conn = Pipe()
        self.datamaker = RandDataMaker(self.child_conn) # Give it the other "end" (child)
        Process.__init__(self) # Class the run() method

    def run(self):
        # Lets start the DATAMAKER!!
        self.datamaker.start()

        # The persistance is not important, just use RAM memory
        with sqlite3.connect(':memory:') as conn:
            cur = conn.cursor()

            # We have on table with _id (required), and the random values as an integer
            cur.execute("""
                CREATE TABLE DataTable (
                    _id INTEGER PRIMARY KEY,
                    value INTEGER
                )
            """)

            # We should forever lat ready to process a request
            while True:
                message: dict = self._parent_conn.recv()

                # We got a message. Now process it via the parse_message method
                data: list[Any] | None = self.parse_message(message, conn)

                # Only if we have something to send, then send it back
                if data:
                    self._parent_conn.send(data)

    def parse_message(self, m: dict, conn: sqlite3.Connection) -> list[Any] | None:
        """
        Parse a message request according to the `spec.md` file.

        Args:
            m (dict): The message to be parsed.
            conn (sqlite3.Connection): Our own database so that we can communicate
        Returns:
            list[any]
        """

        cur = conn.cursor()
        data: list[Any] = []

        # We should be able to "proxy" request from other ContextAgents and sent it back. 
        # We do this by checking if we should propagate the received message.
        # (only do this in the scope is present and set to "network")
        if 'scope' in m and m['scope'] == 'network':
            # Remember to change scope to host so that the message does not 
            # Propagate forever in the network
            m['scope'] = 'host'

            # Every agent expect ourself shall receive the message
            # (our protocol does not have unicast)
            for agent in self.context_agents:
                if agent == self:
                    continue

                # Send the message and await a their response
                agent.child_conn.send(m)
                data.append(agent.child_conn.recv())

        match m['method']:
            case "get": # Hente data
                # Give them (only one integer) data back
                data.append(cur.execute("""
                    SELECT value FROM DataTable ORDER BY _id DESC
                """).fetchone())
            case "post": # Tilføje data
                # Insert the provided value
                # We do not check for sql injection!!
                cur.execute(f"""
                    INSERT INTO DataTable (value)
                    VALUES ({m['value']})
                """)
                conn.commit()
            case "delete": # Slette data
                # Just delete some random data
                cur.execute("""
                    DELETE FROM DataTable
                    WHERE _id = (SELECT MAX(_id) FROM DataTable)
                """)
                conn.commit()

        # Depending on the request type, return noting or the request data
        # (flatten remove the extra tuple)
        # (We made it like so, so that we could have implemented more values,
        #  but we did not)
        return flatten(data) if len(data) else None
    