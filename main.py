class Game:
    visual = [
        "*───*───*",
        "|   |   |",
        "| *─*─* |",
        "| |   | |",
        "*─*   *─*",
        "| |   | |",
        "| *─*─* |",
        "|   |   |",
        "*───*───*"
    ]

    adjacent = {
        (0, 0): [(2, 0), (0, 2)],
        (2, 0): [(0, 0), (4, 0), (2, 1)],
        (4, 0): [(2, 0), (4, 2)],
        (1, 1): [(2, 1), (1, 2)],
        (2, 1): [(2, 0), (1, 1), (3, 1)],
        (3, 1): [(2, 1), (3, 2)],
        (0, 2): [(0, 0), (0, 4), (1, 2)],
        (1, 2): [(0, 2), (1, 1), (1, 3)],
        (3, 2): [(3, 1), (3, 3), (4, 2)],
        (4, 2): [(4, 0), (4, 4), (3, 2)],
        (1, 3): [(1, 2), (2, 3)],
        (2, 3): [(1, 3), (3, 3), (2, 4)],
        (3, 3): [(3, 2), (2, 3)],
        (0, 4): [(0, 2), (2, 4)],
        (2, 4): [(0, 4), (4, 4), (2, 3)],
        (4, 4): [(2, 4), (4, 2)]
    }

    lines = [
        [(0, 0), (2, 0), (4, 0)],
        [(1, 1), (2, 1), (3, 1)],
        [(1, 3), (2, 3), (3, 3)],
        [(0, 4), (2, 4), (4, 4)],
        [(0, 0), (0, 2), (0, 4)],
        [(1, 1), (1, 2), (1, 3)],
        [(3, 1), (3, 2), (3, 3)],
        [(4, 0), (4, 2), (4, 4)],
    ]

    def __init__(self):
        self.board = [['*' for j in range(5)] for i in range(5)]
        self.player = 'W'
        self.placed = 0
        self.white = 0
        self.black = 0
        self.history = []
        self.game_active = False

    def start(self):
        self.board = [['*' for j in range(5)] for i in range(5)]
        self.player = 'W'
        self.placed = 0
        self.white = 0
        self.black = 0
        self.history = []
        self.game_active = True

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def place(self, x, y):
        if self.placed < 12 and (x, y) in self.adjacent.keys() and self.board[y][x] == '*':
            self.history.append([[self.board[i][j] for j in range(5)] for i in range(5)])
            self.board[y][x] = self.player
            self.placed += 1
            if self.player == 'W':
                self.white += 1
            else:
                self.black += 1
            return True
        return False

    def move(self, x, y, nx, ny):
        if (self.white == 3 and self.black == 3 and (x, y) in self.adjacent.keys() and (nx, ny) in self.adjacent[(x, y)]
                and self.board[y][x] == self.player and self.board[ny][nx] == '*'):
            self.history.append([[self.board[i][j] for j in range(3)] for i in range(3)])
            self.board[y][x] = '*'
            self.board[ny][nx] = self.player
            return True
        return False

    def undo(self):
        if len(self.history) > 0:
            self.board = self.history.pop()
            self.white = sum(1 for row in self.board for cell in row if cell == 'W')
            self.black = sum(1 for row in self.board for cell in row if cell == 'B')
            return True
        return False


def main():
    print("Welcome to the Six Men Morris Solver!")


if __name__ == "__main__":
    main()
