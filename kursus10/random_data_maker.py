from threading import Thread
from multiprocessing.connection import Connection # only for typehint
from time import sleep
from random import randint


class RandDataMaker(Thread):
    """
    A RandDataMaker is a thread that adds random data to its associated ContextAgent
    """
    def __init__(self, conn: Connection):
        self.conn = conn # The pipe connection from the Context Agent
        Thread.__init__(self, daemon=True) # So that we died together with our ContextAgent

    def run(self):
        while True:
            sleep(randint(1, 6)) # Sleep randomly so that we no not "spam" the database
            self.conn.send({
                "method": "post",
                "value": randint(0, 1000) # Our Random data generator function
            })
