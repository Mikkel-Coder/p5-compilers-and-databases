from threading import Thread
from multiprocessing.connection import Connection
from time import sleep
from random import randint


class RandDataMaker(Thread):
    def __init__(self, conn: Connection):
        self.conn = conn
        Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            sleep(randint(1, 6))
            self.conn.send({
                "method": "post",
                "value": randint(0, 1000)
            })
