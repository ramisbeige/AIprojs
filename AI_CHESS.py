import copy

# Define the chess board dimensions
BOARD_SIZE = 8

# Define the piece values for the evaluation function
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}

# Chess piece symbols for printing the board
PIECE_SYMBOLS = {'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
                 'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚', '.': '□'}

def evaluate_board(board, is_maximizing_player):
    """Evaluate the current state of the board using a simple piece count evaluation function."""
    total_value = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece.isupper():
                total_value += PIECE_VALUES.get(piece.lower(), 0)
            elif piece.islower():
                total_value -= PIECE_VALUES.get(piece, 0)
    return total_value if is_maximizing_player else -total_value

def get_valid_moves(board, player):
    """Generate all valid moves for the given player on the current board."""
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col].lower() == player:
                valid_moves.extend(get_piece_moves(board, (row, col)))
    return valid_moves

def get_piece_moves(board, position):
    """Generate valid moves for a piece at a given position."""
    moves = []
    piece = board[position[0]][position[1]].lower()

    # Pawn moves
    if piece == 'p':
        # Moves forward
        if position[0] + 1 < BOARD_SIZE and board[position[0] + 1][position[1]] == '.':
            moves.append((position, (position[0] + 1, position[1])))
        # Capturing moves
        if position[0] + 1 < BOARD_SIZE and position[1] - 1 >= 0 and board[position[0] + 1][position[1] - 1].isupper():
            moves.append((position, (position[0] + 1, position[1] - 1)))
        if position[0] + 1 < BOARD_SIZE and position[1] + 1 < BOARD_SIZE and board[position[0] + 1][position[1] + 1].isupper():
            moves.append((position, (position[0] + 1, position[1] + 1)))

    # Knight moves
    if piece == 'n':
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for offset in offsets:
            new_row = position[0] + offset[0]
            new_col = position[1] + offset[1]
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if board[new_row][new_col] == '.' or board[new_row][new_col].islower():
                    moves.append((position, (new_row, new_col)))

    # Bishop moves
    if piece == 'b':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves.extend(generate_moves_in_directions(board, position, directions))

    # Rook moves
    if piece == 'r':
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        moves.extend(generate_moves_in_directions(board, position, directions))

    # Queen moves
    if piece == 'q':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
        moves.extend(generate_moves_in_directions(board, position, directions))

    # King moves
    if piece == 'k':
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for offset in offsets:
            new_row = position[0] + offset[0]
            new_col = position[1] + offset[1]
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if board[new_row][new_col] == '.' or board[new_row][new_col].islower():
                    moves.append((position, (new_row, new_col)))

    return moves

def generate_moves_in_directions(board, position, directions):
    """Generate moves in specified directions."""
    moves = []
    for dr, dc in directions:
        new_row, new_col = position[0] + dr, position[1] + dc
        while 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
            if board[new_row][new_col] == '.':
                moves.append((position, (new_row, new_col)))
                new_row, new_col = new_row + dr, new_col + dc
            elif board[new_row][new_col].islower():
                moves.append((position, (new_row, new_col)))
                break
            else:
                break
    return moves

def is_check(board, player):
    """Check if the specified player's king is in check."""
    king_position = find_king(board, player)
    return is_in_check(board, player, king_position)

def is_in_check(board, player, king_position):
    """Check if the specified player's king is in check."""
    opponent = 'b' if player == 'w' else 'w'
    opponent_moves = get_valid_moves(board, opponent)
    for move in opponent_moves:
        if move[1] == king_position:
            return True
    return False

def is_checkmate(board, player):
    """Check if the current player is in checkmate."""
    king_position = find_king(board, player)
    if is_in_check(board, player, king_position):
        for move in get_valid_moves(board, player):
            new_board = make_move(copy.deepcopy(board), move)
            if not is_in_check(new_board, player, king_position):
                return False
        return True
    return False


def is_stalemate(board, player):
    """Check if the current player is in stalemate."""
    # If the player has no legal moves but is not in check, it's a stalemate
    if not get_valid_moves(board, player) and not is_check(board, player):
        return True
    return False

def check_game_over(board, player):
    """Check if the game is over."""
    if is_checkmate(board, player):
        print(f"Checkmate! Player {player.upper()} wins!")
        return True
    elif is_stalemate(board, player):
        print("Stalemate! The game is a draw.")
        return True
    return False


def find_king(board, player):
    """Find the position of the king for the specified player."""
    king_piece = 'K' if player == 'w' else 'k'
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == king_piece:
                return (row, col)
    return None

def minimax(board, depth, alpha, beta, is_maximizing_player, player):
    """Implement the minimax algorithm with alpha-beta pruning."""
    if depth == 0:
        return evaluate_board(board, is_maximizing_player)

    if is_maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_moves(board, player.upper())
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move)
            max_eval = max(max_eval, minimax(new_board, depth - 1, alpha, beta, False, player))
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        valid_moves = get_valid_moves(board, player.lower())
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move)
            min_eval = min(min_eval, minimax(new_board, depth - 1, alpha, beta, True, player))
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval

def make_move(board, move):
    """Apply a move to the board."""
    if move is None:
        return board  # No valid move, return the current board
    start_pos, end_pos = move
    board[end_pos[0]][end_pos[1]] = board[start_pos[0]][start_pos[1]]
    board[start_pos[0]][start_pos[1]] = '.'
    return board

def print_board(board):
    """Print the current state of the chess board."""
    for row in board:
        print(' '.join([PIECE_SYMBOLS[piece] for piece in row]))
    print()

def play_game():
    """Main game loop."""
    board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
             ['p'] * BOARD_SIZE,
             ['.'] * BOARD_SIZE,
             ['.'] * BOARD_SIZE,
             ['.'] * BOARD_SIZE,
             ['.'] * BOARD_SIZE,
             ['P'] * BOARD_SIZE,
             ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

    player = 'w'
    depth = 3  # Default search depth

    while True:
        print_board(board)
        print(f"Player ({player.upper()})'s turn.")

        if player == 'w':
            # Human player's turn
            move = input("Enter your move (e.g., e2e4): ")
            
        else:
            # AI player's turn
            best_move = None
            best_score = float('-inf')
            valid_moves = get_valid_moves(board, player)
            for move in valid_moves:
                new_board = make_move(copy.deepcopy(board), move)
                score = minimax(new_board, depth, float('-inf'), float('inf'), False, player)
                if score > best_score:
                    best_score = score
                    best_move = move
            board = make_move(board, best_move)

        # Check game over conditions
        if check_game_over(board, player):
            break

        # Update player turn
        if player == 'w':
            player = 'b'
        else:
            player = 'w'

if __name__ == "__main__":
    play_game()
