import copy
import math

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
        self.removed_white = 0
        self.removed_black = 0

    def start(self):
        self.board = [['*' for j in range(5)] for i in range(5)]
        self.player = 'W'
        self.placed = 0
        self.white = 0
        self.black = 0
        self.removed_white = 0
        self.removed_black = 0
        self.history = []
        self.game_active = True

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def place(self, x, y):
        if self.placed < 12 and (x, y) in self.adjacent.keys() and self.board[y][x] == '*':
            # Record complete game state
            self.history.append((
                [[self.board[i][j] for j in range(5)] for i in range(5)],
                self.placed,
                self.white,
                self.black,
                self.removed_white,
                self.removed_black
            ))
            self.board[y][x] = self.player
            self.placed += 1
            if self.player == 'W':
                self.white += 1
            else:
                self.black += 1
            return True
        return False

    def move(self, x, y, nx, ny):
        # Check if all pieces are placed
        if self.placed < 12:
            return False
            
        # Check if source position is valid and contains player's piece
        if (x, y) not in self.adjacent.keys() or self.board[y][x] != self.player:
            return False
            
        # Check if destination is empty
        if self.board[ny][nx] != '*':
            return False
            
        # Check if destination is valid
        if (nx, ny) not in self.adjacent.keys():
            return False
            
        # Check movement rules
        if self.get_piece_count(self.player) > 3:
            # Must move to adjacent position
            if (nx, ny) not in self.adjacent[(x, y)]:
                return False
        else:
            # Can move to any empty position
            pass
            
        # Record complete game state
        self.history.append((
            [[self.board[i][j] for j in range(5)] for i in range(5)],
            self.placed,
            self.white,
            self.black,
            self.removed_white,
            self.removed_black
        ))
        self.board[y][x] = '*'
        self.board[ny][nx] = self.player
        return True

    def get_piece_count(self, player):
        """Get the number of pieces on the board for a given player"""
        count = 0
        for row in self.board:
            for cell in row:
                if cell == player:
                    count += 1
        return count

    def check_mill(self, x, y, player):
        """Check if placing/moving a piece at (x,y) forms a mill for the given player"""
        for line in self.lines:
            if (x, y) in line:
                # Check if all positions in this line are occupied by the same player
                all_same = True
                for px, py in line:
                    if self.board[py][px] != player:
                        all_same = False
                        break
                if all_same:
                    return True
        return False

    def get_opponent_pieces(self, player):
        """Get all pieces of the opponent that can be removed"""
        opponent = 'B' if player == 'W' else 'W'
        pieces = []
        
        # Get all opponent pieces
        for y in range(5):
            for x in range(5):
                if self.board[y][x] == opponent:
                    pieces.append((x, y))
        
        # Check if all opponent pieces are in mills
        all_in_mills = True
        for x, y in pieces:
            if not self.check_mill(x, y, opponent):
                all_in_mills = False
                break
        
        # If all pieces are in mills, all can be removed
        if all_in_mills:
            return pieces
        
        # Otherwise, only pieces not in mills can be removed
        removable = []
        for x, y in pieces:
            if not self.check_mill(x, y, opponent):
                removable.append((x, y))
        
        return removable

    def remove_piece(self, x, y, player):
        """Remove an opponent's piece"""
        opponent = 'B' if player == 'W' else 'W'
        
        if self.board[y][x] != opponent:
            return False
            
        # Check if piece can be removed
        removable_pieces = self.get_opponent_pieces(player)
        if (x, y) not in removable_pieces:
            return False
            
        self.board[y][x] = '*'
        if opponent == 'W':
            self.removed_white += 1
            self.white -= 1
        else:
            self.removed_black += 1
            self.black -= 1
        return True

    def check_win(self):
        """Check if current player has won"""
        opponent = 'B' if self.player == 'W' else 'W'
        
        # Check if opponent has 2 or fewer pieces
        if self.placed >= 12 and self.get_piece_count(opponent) <= 2:
            return True
            
        # Check if opponent has no valid moves
        if self.placed >= 12 and not self.has_valid_moves(opponent):
            return True
            
        return False

    def has_valid_moves(self, player):
        """Check if a player has any valid moves"""
        piece_count = self.get_piece_count(player)
        
        if piece_count <= 2:
            return False
            
        # Check if any piece can move
        for y in range(5):
            for x in range(5):
                if self.board[y][x] == player:
                    if piece_count > 3:
                        # Check adjacent moves
                        for nx, ny in self.adjacent.get((x, y), []):
                            if self.board[ny][nx] == '*':
                                return True
                    else:
                        # Can move anywhere
                        for ny_inner in range(5):
                            for nx_inner in range(5):
                                if self.board[ny_inner][nx_inner] == '*' and (nx_inner, ny_inner) in self.adjacent:
                                    return True
        return False

    def undo(self):
        if len(self.history) > 0:
            # Restore complete game state
            state = self.history.pop()
            self.board = state[0]
            self.placed = state[1]
            self.white = state[2]
            self.black = state[3]
            self.removed_white = state[4]
            self.removed_black = state[5]
            return True
        return False

    def display_board(self):
        """Display the current board state using the visual representation"""
        print("\nCurrent Board:")
        
        # Create a copy of the visual board
        visual_board = [line for line in self.visual]
        
        # Map real board coordinates to visual positions
        # The visual board has '*' at positions that correspond to valid board positions
        # We need to replace these '*' with actual pieces
        # Mapping: (real_x, real_y) -> (visual_x, visual_y) where visual = real * 2
        visual_positions = [
            (0, 0), (4, 0), (8, 0),  # Top row - real (0,0), (2,0), (4,0)
            (2, 2), (4, 2), (6, 2),  # Middle row - real (1,1), (2,1), (3,1)
            (0, 4), (2, 4), (6, 4), (8, 4),  # Bottom row - real (0,2), (1,2), (3,2), (4,2)
            (2, 6), (4, 6), (6, 6),  # Middle row - real (1,3), (2,3), (3,3)
            (0, 8), (4, 8), (8, 8)   # Top row - real (0,4), (2,4), (4,4)
        ]
        
        # Real board positions in order (matching the adjacent.keys() order)
        real_positions = [
            (0, 0), (2, 0), (4, 0),
            (1, 1), (2, 1), (3, 1),
            (0, 2), (1, 2), (3, 2), (4, 2),
            (1, 3), (2, 3), (3, 3),
            (0, 4), (2, 4), (4, 4)
        ]
        
        # Create a mapping from visual positions to real positions
        visual_to_real = {}
        for i, (vx, vy) in enumerate(visual_positions):
            if i < len(real_positions):
                visual_to_real[(vx, vy)] = real_positions[i]
        
        # Replace '*' in visual board with actual pieces
        for (vx, vy), (rx, ry) in visual_to_real.items():
            if 0 <= vy < len(visual_board) and 0 <= vx < len(visual_board[vy]):
                piece = self.board[ry][rx]
                visual_board[vy] = visual_board[vy][:vx] + piece + visual_board[vy][vx+1:]
        
        # Display the visual board
        for line in visual_board:
            print(line)
        
        print(f"\nWhite pieces: {self.white} (removed: {self.removed_white})")
        print(f"Black pieces: {self.black} (removed: {self.removed_black})")
        print(f"Current player: {self.player}")
        print(f"Pieces placed: {self.placed}/12")

    def get_unblocked_two_in_a_rows(self, player):
        """Counts the number of unblocked 2-in-a-rows for a player."""
        count = 0
        for line in self.lines:
            player_pieces = 0
            empty_spaces = 0
            for x, y in line:
                if self.board[y][x] == player:
                    player_pieces += 1
                elif self.board[y][x] == '*':
                    empty_spaces += 1
            if player_pieces == 2 and empty_spaces == 1:
                count += 1
        return count

    def evaluate(self):
        """
        Evaluates the current board state.
        - White winning: +infinity
        - Black winning: -infinity
        - White's pieces vs Black's pieces
        - White's unblocked 2-in-a-rows vs Black's
        """
        if self.check_win():
            return math.inf if self.player == 'W' else -math.inf

        # Temporarily switch player to check opponent's win condition
        self.switch()
        if self.check_win():
            self.switch() # Switch back
            return -math.inf if self.player == 'W' else math.inf
        self.switch() # Switch back

        white_pieces = self.get_piece_count('W')
        black_pieces = self.get_piece_count('B')
        white_2_rows = self.get_unblocked_two_in_a_rows('W')
        black_2_rows = self.get_unblocked_two_in_a_rows('B')

        score = (white_pieces - black_pieces) * 10 + \
                (white_2_rows - black_2_rows) * 5
        
        return score

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_win():
            return self.evaluate(), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            
            # Placement Phase
            if self.placed < 12:
                for y in range(5):
                    for x in range(5):
                        if (x,y) in self.adjacent and self.board[y][x] == '*':
                            temp_game = copy.deepcopy(self)
                            temp_game.place(x, y)
                            if temp_game.check_mill(x, y, temp_game.player):
                                # If a mill is formed, find best piece to remove
                                for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                    mill_game = copy.deepcopy(temp_game)
                                    mill_game.remove_piece(rx, ry, mill_game.player)
                                    mill_game.switch()
                                    evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, False)
                                    if evaluation > max_eval:
                                        max_eval = evaluation
                                        best_move = ('place', (x, y), (rx, ry))
                                    alpha = max(alpha, evaluation)
                                    if beta <= alpha:
                                        break
                                if beta <= alpha:
                                    break
                            else:
                                temp_game.switch()
                                evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, False)
                                if evaluation > max_eval:
                                    max_eval = evaluation
                                    best_move = ('place', (x, y), None)
                                alpha = max(alpha, evaluation)
                                if beta <= alpha:
                                    break
                    if beta <= alpha:
                        break
            # Movement Phase
            else:
                for y in range(5):
                    for x in range(5):
                        if self.board[y][x] == self.player:
                            # Fly rule
                            if self.get_piece_count(self.player) == 3:
                                for ny in range(5):
                                    for nx in range(5):
                                        if (nx, ny) in self.adjacent and self.board[ny][nx] == '*':
                                            temp_game = copy.deepcopy(self)
                                            temp_game.move(x, y, nx, ny)
                                            if temp_game.check_mill(nx, ny, temp_game.player):
                                                 for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                                    mill_game = copy.deepcopy(temp_game)
                                                    mill_game.remove_piece(rx, ry, mill_game.player)
                                                    mill_game.switch()
                                                    evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, False)
                                                    if evaluation > max_eval:
                                                        max_eval = evaluation
                                                        best_move = ('move', (x, y), (nx, ny), (rx, ry))
                                                    alpha = max(alpha, evaluation)
                                                    if beta <= alpha:
                                                        break
                                                 if beta <= alpha:
                                                    break
                                            else:
                                                temp_game.switch()
                                                evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, False)
                                                if evaluation > max_eval:
                                                    max_eval = evaluation
                                                    best_move = ('move', (x, y), (nx, ny), None)
                                                alpha = max(alpha, evaluation)
                                                if beta <= alpha:
                                                    break
                                    if beta <= alpha:
                                        break
                            # Normal move
                            else:
                                for nx, ny in self.adjacent.get((x, y), []):
                                    if self.board[ny][nx] == '*':
                                        temp_game = copy.deepcopy(self)
                                        temp_game.move(x, y, nx, ny)
                                        if temp_game.check_mill(nx, ny, temp_game.player):
                                            for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                                mill_game = copy.deepcopy(temp_game)
                                                mill_game.remove_piece(rx, ry, mill_game.player)
                                                mill_game.switch()
                                                evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, False)
                                                if evaluation > max_eval:
                                                    max_eval = evaluation
                                                    best_move = ('move', (x, y), (nx, ny), (rx, ry))
                                                alpha = max(alpha, evaluation)
                                                if beta <= alpha:
                                                    break
                                            if beta <= alpha:
                                                break
                                        else:
                                            temp_game.switch()
                                            evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, False)
                                            if evaluation > max_eval:
                                                max_eval = evaluation
                                                best_move = ('move', (x, y), (nx, ny), None)
                                            alpha = max(alpha, evaluation)
                                            if beta <= alpha:
                                                break
                        if beta <= alpha:
                            break
                    if beta <= alpha:
                        break
            return max_eval, best_move
        
        else: # Minimizing player
            min_eval = math.inf
            best_move = None
            
            # Placement Phase
            if self.placed < 12:
                for y in range(5):
                    for x in range(5):
                        if (x,y) in self.adjacent and self.board[y][x] == '*':
                            temp_game = copy.deepcopy(self)
                            temp_game.place(x, y)
                            if temp_game.check_mill(x, y, temp_game.player):
                                for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                    mill_game = copy.deepcopy(temp_game)
                                    mill_game.remove_piece(rx, ry, mill_game.player)
                                    mill_game.switch()
                                    evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, True)
                                    if evaluation < min_eval:
                                        min_eval = evaluation
                                        best_move = ('place', (x, y), (rx, ry))
                                    beta = min(beta, evaluation)
                                    if beta <= alpha:
                                        break
                                if beta <= alpha:
                                    break
                            else:
                                temp_game.switch()
                                evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, True)
                                if evaluation < min_eval:
                                    min_eval = evaluation
                                    best_move = ('place', (x, y), None)
                                beta = min(beta, evaluation)
                                if beta <= alpha:
                                    break
                    if beta <= alpha:
                        break
            # Movement Phase
            else:
                for y in range(5):
                    for x in range(5):
                        if self.board[y][x] == self.player:
                            # Fly rule
                            if self.get_piece_count(self.player) == 3:
                                for ny in range(5):
                                    for nx in range(5):
                                        if (nx, ny) in self.adjacent and self.board[ny][nx] == '*':
                                            temp_game = copy.deepcopy(self)
                                            temp_game.move(x, y, nx, ny)
                                            if temp_game.check_mill(nx, ny, temp_game.player):
                                                for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                                    mill_game = copy.deepcopy(temp_game)
                                                    mill_game.remove_piece(rx, ry, mill_game.player)
                                                    mill_game.switch()
                                                    evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, True)
                                                    if evaluation < min_eval:
                                                        min_eval = evaluation
                                                        best_move = ('move', (x, y), (nx, ny), (rx, ry))
                                                    beta = min(beta, evaluation)
                                                    if beta <= alpha:
                                                        break
                                                if beta <= alpha:
                                                    break
                                            else:
                                                temp_game.switch()
                                                evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, True)
                                                if evaluation < min_eval:
                                                    min_eval = evaluation
                                                    best_move = ('move', (x, y), (nx, ny), None)
                                                beta = min(beta, evaluation)
                                                if beta <= alpha:
                                                    break
                                    if beta <= alpha:
                                        break
                            # Normal move
                            else:
                                for nx, ny in self.adjacent.get((x, y), []):
                                    if self.board[ny][nx] == '*':
                                        temp_game = copy.deepcopy(self)
                                        temp_game.move(x, y, nx, ny)
                                        if temp_game.check_mill(nx, ny, temp_game.player):
                                            for rx, ry in temp_game.get_opponent_pieces(temp_game.player):
                                                mill_game = copy.deepcopy(temp_game)
                                                mill_game.remove_piece(rx, ry, mill_game.player)
                                                mill_game.switch()
                                                evaluation, _ = mill_game.minimax(depth - 1, alpha, beta, True)
                                                if evaluation < min_eval:
                                                    min_eval = evaluation
                                                    best_move = ('move', (x, y), (nx, ny), (rx, ry))
                                                beta = min(beta, evaluation)
                                                if beta <= alpha:
                                                    break
                                            if beta <= alpha:
                                                break
                                        else:
                                            temp_game.switch()
                                            evaluation, _ = temp_game.minimax(depth - 1, alpha, beta, True)
                                            if evaluation < min_eval:
                                                min_eval = evaluation
                                                best_move = ('move', (x, y), (nx, ny), None)
                                            beta = min(beta, evaluation)
                                            if beta <= alpha:
                                                break
                        if beta <= alpha:
                            break
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def computer_move(self, depth):
        """Makes a move for the computer based on the priority list."""
        opponent = 'B' if self.player == 'W' else 'W'
        
        # 1. Form a mill
        # Placement Phase
        if self.placed < 12:
            for y in range(5):
                for x in range(5):
                    if (x,y) in self.adjacent and self.board[y][x] == '*':
                        self.board[y][x] = self.player
                        if self.check_mill(x, y, self.player):
                            self.board[y][x] = '*' # Revert change
                            self.place(x, y)
                            print(f"Computer places at ({x}, {y}) to form a mill.")
                            # Remove piece
                            self.remove_best_opponent_piece(depth)
                            return
                        self.board[y][x] = '*' # Revert
        # Movement Phase
        else:
            for y in range(5):
                for x in range(5):
                    if self.board[y][x] == self.player:
                        # Fly rule
                        if self.get_piece_count(self.player) == 3:
                            for ny in range(5):
                                for nx in range(5):
                                    if (nx, ny) in self.adjacent and self.board[ny][nx] == '*':
                                        self.board[ny][nx] = self.player
                                        self.board[y][x] = '*'
                                        if self.check_mill(nx, ny, self.player):
                                            self.board[ny][nx] = '*'
                                            self.board[y][x] = self.player # Revert
                                            self.move(x, y, nx, ny)
                                            print(f"Computer moves from ({x}, {y}) to ({nx}, {ny}) to form a mill.")
                                            self.remove_best_opponent_piece(depth)
                                            return
                                        self.board[ny][nx] = '*'
                                        self.board[y][x] = self.player # Revert
                        # Normal move
                        else:
                            for nx, ny in self.adjacent.get((x, y), []):
                                if self.board[ny][nx] == '*':
                                    self.board[ny][nx] = self.player
                                    self.board[y][x] = '*'
                                    if self.check_mill(nx, ny, self.player):
                                        self.board[ny][nx] = '*'
                                        self.board[y][x] = self.player # Revert
                                        self.move(x, y, nx, ny)
                                        print(f"Computer moves from ({x}, {y}) to ({nx}, {ny}) to form a mill.")
                                        self.remove_best_opponent_piece(depth)
                                        return
                                    self.board[ny][nx] = '*'
                                    self.board[y][x] = self.player # Revert
        
        # 2. Block opponent's mill
        # Placement Phase
        if self.placed < 12:
            for line in self.lines:
                opponent_pieces = 0
                empty_spot = None
                for x, y in line:
                    if self.board[y][x] == opponent:
                        opponent_pieces += 1
                    elif self.board[y][x] == '*':
                        empty_spot = (x, y)
                if opponent_pieces == 2 and empty_spot:
                    self.place(empty_spot[0], empty_spot[1])
                    print(f"Computer places at {empty_spot} to block opponent's mill.")
                    return
        # Movement Phase
        else:
            for line in self.lines:
                opponent_pieces = 0
                empty_spot = None
                for x, y in line:
                    if self.board[y][x] == opponent:
                        opponent_pieces += 1
                    elif self.board[y][x] == '*':
                        empty_spot = (x, y)
                if opponent_pieces == 2 and empty_spot:
                    # Find a piece to move to the blocking spot
                    for y_s in range(5):
                        for x_s in range(5):
                            if self.board[y_s][x_s] == self.player:
                                if self.get_piece_count(self.player) == 3 or empty_spot in self.adjacent.get((x_s, y_s), []):
                                    self.move(x_s, y_s, empty_spot[0], empty_spot[1])
                                    print(f"Computer moves from ({x_s}, {y_s}) to {empty_spot} to block opponent's mill.")
                                    return

        # 3. Use minimax
        print("Computer is thinking...")
        maximizing = self.player == 'W'
        _, best_move = self.minimax(depth, -math.inf, math.inf, maximizing)

        if best_move:
            move_type, pos1, pos2, pos3 = best_move[0], best_move[1], None, None
            if len(best_move) > 2: pos2 = best_move[2]
            if len(best_move) > 3: pos3 = best_move[3]

            if move_type == 'place':
                self.place(pos1[0], pos1[1])
                print(f"Computer places a piece at {pos1}.")
                if pos2:
                    self.remove_piece(pos2[0], pos2[1], self.player)
                    print(f"Computer removes opponent's piece at {pos2}.")
            elif move_type == 'move':
                self.move(pos1[0], pos1[1], pos2[0], pos2[1])
                print(f"Computer moves from {pos1} to {pos2}.")
                if pos3:
                    self.remove_piece(pos3[0], pos3[1], self.player)
                    print(f"Computer removes opponent's piece at {pos3}.")
        else:
            print("Computer has no moves.")
    
    def remove_best_opponent_piece(self, depth):
        """
        Determines the best opponent piece to remove.
        1. From an opponent's 2-in-a-row.
        2. Use minimax if no 2-in-a-row exists.
        """
        opponent = 'B' if self.player == 'W' else 'W'
        
        # Check for opponent's 2-in-a-rows
        for line in self.lines:
            opponent_pieces = []
            player_pieces = 0
            for x, y in line:
                if self.board[y][x] == opponent:
                    opponent_pieces.append((x, y))
                elif self.board[y][x] == self.player:
                    player_pieces += 1
            
            if len(opponent_pieces) == 2 and player_pieces == 0:
                # Found a 2-in-a-row to break
                for x_r, y_r in opponent_pieces:
                    if self.remove_piece(x_r, y_r, self.player):
                        print(f"Computer removes opponent's piece at ({x_r}, {y_r}) from a 2-in-a-row.")
                        return

        # If no 2-in-a-row, use minimax to find best removal
        best_removal = None
        best_score = -math.inf if self.player == 'W' else math.inf
        
        removable_pieces = self.get_opponent_pieces(self.player)
        if not removable_pieces:
            print("No pieces to remove.")
            return

        for x_r, y_r in removable_pieces:
            temp_game = copy.deepcopy(self)
            temp_game.remove_piece(x_r, y_r, self.player)
            temp_game.switch()
            score, _ = temp_game.minimax(depth - 1, -math.inf, math.inf, self.player == 'B')
            
            if self.player == 'W':
                if score > best_score:
                    best_score = score
                    best_removal = (x_r, y_r)
            else:
                if score < best_score:
                    best_score = score
                    best_removal = (x_r, y_r)
        
        if best_removal:
            self.remove_piece(best_removal[0], best_removal[1], self.player)
            print(f"Computer removes opponent's piece at {best_removal} based on minimax.")
        else:
            # Fallback: remove the first available piece
            x_r, y_r = removable_pieces[0]
            self.remove_piece(x_r, y_r, self.player)
            print(f"Computer removes opponent's piece at ({x_r}, {y_r}).")


def main():
    def get_valid_coordinates(prompt):
        """Get valid coordinates from user input"""
        while True:
            try:
                coords = input(prompt).strip().split()
                if len(coords) != 2:
                    print("Please enter two numbers separated by space (e.g., '2 1')")
                    continue
                x, y = int(coords[0]), int(coords[1])
                if 0 <= x <= 4 and 0 <= y <= 4:
                    return x, y
                else:
                    print("Coordinates must be between 0 and 4")
            except ValueError:
                print("Please enter valid numbers")
    
    print("Welcome to the Six Men Morris Solver!")
    game = Game()
    
    while True:
        if not game.game_active:
            print("\n1. Start a new game")
            print("2. Quit")
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                game.start()
                print("New game started!")
            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        else:
            game.display_board()
            print("\n1. Take an action")
            print("2. Let computer play")
            print("3. Undo an action")
            print("4. Restart the game")
            print("5. Quit")
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                # Take an action
                if game.placed < 12:
                    # Placement phase
                    print(f"\n{game.player} player, place your piece.")
                    x, y = get_valid_coordinates("Enter coordinates (x y): ")
                    
                    if game.place(x, y):
                        # Check for mill formation
                        if game.check_mill(x, y, game.player):
                            print(f"{game.player} formed a mill! Remove an opponent's piece.")
                            while True:
                                rx, ry = get_valid_coordinates("Enter coordinates of piece to remove (x y): ")
                                if game.remove_piece(rx, ry, game.player):
                                    break
                                else:
                                    print("Invalid piece to remove. Try again.")
                        
                        if game.check_win():
                            game.display_board()
                            print(f"{game.player} wins!")
                            game.game_active = False
                        else:
                            game.switch()
                    else:
                        print("Invalid placement. Try again.")
                else:
                    # Movement phase
                    print(f"\n{game.player} player, move your piece.")
                    sx, sy = get_valid_coordinates("Enter source coordinates (x y): ")
                    dx, dy = get_valid_coordinates("Enter destination coordinates (x y): ")
                    
                    if game.move(sx, sy, dx, dy):
                        # Check for mill formation
                        if game.check_mill(dx, dy, game.player):
                            print(f"{game.player} formed a mill! Remove an opponent's piece.")
                            while True:
                                rx, ry = get_valid_coordinates("Enter coordinates of piece to remove (x y): ")
                                if game.remove_piece(rx, ry, game.player):
                                    break
                                else:
                                    print("Invalid piece to remove. Try again.")
                        
                        if game.check_win():
                            game.display_board()
                            print(f"{game.player} wins!")
                            game.game_active = False
                        else:
                            game.switch()
                    else:
                        print("Invalid move. Try again.")

            elif choice == '2':
                # Let computer play
                while True:
                    try:
                        depth = int(input("Enter minimax depth: ").strip())
                        if depth > 0:
                            break
                        else:
                            print("Depth must be a positive integer.")
                    except ValueError:
                        print("Please enter a valid integer for depth.")
                
                game.computer_move(depth)
                if game.check_win():
                    game.display_board()
                    print(f"{game.player} wins!")
                    game.game_active = False
                else:
                    game.switch()
                        
            elif choice == '3':
                if game.undo():
                    game.switch()  # Switch back to previous player
                    print("Action undone.")
                else:
                    print("No actions to undo.")
                    
            elif choice == '4':
                game.start()
                print("Game restarted!")
                
            elif choice == '5':
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
