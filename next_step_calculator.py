from stockfish import Stockfish

def calculate_next_step(current_fen="rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"):
    # checks correctness of board
    stockfish = Stockfish("/usr/games/stockfish")
    updated_fen = None
    if stockfish.is_fen_valid(current_fen):
        stockfish.set_fen_position(current_fen)
        print("Current board:")
        print(stockfish.get_board_visual())
        best_move = stockfish.get_best_move()
        print(f"best move is {best_move}")
        stockfish.make_moves_from_current_position([best_move])
        updated_fen = stockfish.get_fen_position()
        print("Updated board:")
        print(stockfish.get_board_visual())
        return True, updated_fen
    else:
        return False, updated_fen
    
# calculate_next_step()
