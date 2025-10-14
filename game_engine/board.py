from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Board:

    def __init__(self):
        self.grid = {}

    def place_tile(self, x, y, tile):
        if (x, y) not in self.grid.keys():
            self.grid[(x, y)] = tile
        else:
            if self.grid[(x, y)] == tile:
                return 0
            else:
                raise Exception("Tile already exists")

        return 0

    def get_tile(self, x, y):
        """
        Returns the tile at position (x, y) in the board

        param x: coordinate x
        param y: coordinate y
        return: tile at position (x, y), None if no tile
        """
        if (x, y) in self.grid.keys():
            return self.grid[(x, y)]
        else:
            return None

    def get_board_bounds(self):
        """
        Returns the board bounds

        return: minX, maxX, minY, maxY
        """
        if not self.grid:
            return 0, 0, 0, 0
        xs = [x for x, _ in self.grid.keys()]
        ys = [y for _, y in self.grid.keys()]
        return min(xs), max(xs), min(ys), max(ys)

    def place_word(self, x: int, y: int, orientation: Orientation, word: str):
        if orientation == Orientation.HORIZONTAL:
            for i, letter in enumerate(word):
                self.place_tile(x + i, y, letter)
        elif orientation == Orientation.VERTICAL:
            for i, letter in enumerate(word):
                self.place_tile(x, y + i, letter)
        else:
            raise Exception("Invalid orientation")
        return 0


board = Board()
