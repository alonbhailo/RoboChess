from stockfish import Stockfish

def calculate_next_step(current_fen="rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"):
    # checks correctness of board
    stockfish = Stockfish("/usr/games/stockfish")
    if stockfish.is_fen_valid(current_fen):
        print(stockfish.get_board_visual())
        return f"best move is {stockfish.get_best_move()}"
    else:
        return -1
    
# calculate_next_step()