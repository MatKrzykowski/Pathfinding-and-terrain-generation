"""path.py"""


class Path:
    def __init__(self, coord, parent=None) -> None:
        self.coord = coord
        self.parent = parent

    def get_path(self):
        path = []
        while self:
            path.append(self.coord)
            self = self.parent
        return path
