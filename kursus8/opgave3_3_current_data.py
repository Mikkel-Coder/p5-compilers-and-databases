# In treelib, the data field is BEST as an object.
class CurrentData():
    def __init__(self, current: list[float]) -> None:
        self.currents = current