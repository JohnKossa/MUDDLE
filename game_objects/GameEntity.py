import uuid


class GameEntity:
    def __init__(self):
        super().__init__()
        self.guid = uuid.uuid4()