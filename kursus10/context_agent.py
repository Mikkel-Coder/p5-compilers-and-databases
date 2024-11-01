from __future__ import annotations
from typing import Any
from multiprocessing import Process, Pipe
import sqlite3

from random_data_maker import RandDataMaker
from utils import flatten


class ContextAgent(Process):
    def __init__(self, context_agents: list[ContextAgent], name: str = None):
        self.context_agents: list[ContextAgent] = context_agents
        self._parent_conn, self.child_conn = Pipe()
        self.datamaker = RandDataMaker(self.child_conn)
        Process.__init__(self)

    def parse_message(self, m: dict, conn: sqlite3.Connection) -> list[Any] | None:
        cur = conn.cursor()
        data: list[Any] = []

        if 'scope' in m and m['scope'] == 'network':
            m['scope'] = 'host'
            for agent in self.context_agents:
                if agent == self:
                    continue

                agent.child_conn.send(m)
                data.append(agent.child_conn.recv())

        match m['method']:
            case "get":
                data.append(cur.execute("""
                    SELECT value FROM DataTable ORDER BY _id DESC
                """).fetchone())
            case "post":
                cur.execute(f"""
                    INSERT INTO DataTable (value)
                    VALUES ({m['value']})
                """)
                conn.commit()
            case "delete":
                cur.execute("""
                    DELETE FROM DataTable
                    WHERE _id = (SELECT MAX(_id) FROM DataTable)
                """)
                conn.commit()

        return flatten(data) if len(data) else None

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
                message: dict = self._parent_conn.recv()

                data: list[Any] | None = self.parse_message(message, conn)

                if data:
                    self._parent_conn.send(data)
