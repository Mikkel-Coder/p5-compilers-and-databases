# In treelib, the data field is BEST as an object.
# DOCS: https://treelib.readthedocs.io/en/stable/pyapi.html
class CurrentData():
    def __init__(self, current: list[float]) -> None:
        self.currents = current