from __future__ import annotations
from typing import List, Dict, Any
from multiprocessing import Process, Pipe
import sqlite3

from random_data_maker import RandDataMaker


class ContextAgent(Process):
    def __init__(self, context_agents: List[ContextAgent], name: str = None):
        self.context_agents: List[ContextAgent] = context_agents
        self._parent_conn, self.child_conn = Pipe()
        self.datamaker = RandDataMaker(self.child_conn)
        Process.__init__(self)

    def parse_message(self, m: Dict, conn: sqlite3.Connection) -> Any | None:
        cur = conn.cursor()

        match m['method']:
            case "get":
                return cur.execute("""
                    SELECT value FROM DataTable ORDER BY _id DESC
                """).fetchone()
            case "post":
                cur.execute(f"""
                    INSERT INTO DataTable (value)
                    VALUES ({m['value']})
                """)
                conn.commit()
                return None
            case "delete":
                raise Exception("What da F...")

    def run(self):
        self.datamaker.start()
        with sqlite3.connect(':memory:') as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE DataTable (
                    _id INTEGER PRIMARY KEY,
                    value INTEGER
                )
            """)

            while True:
                message: Dict = self._parent_conn.recv()

                data: Any | None = self.parse_message(message, conn)

                if data:
                    self._parent_conn.send(data)
