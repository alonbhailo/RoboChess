    
import sys
sys.path.append("LiveChess2Fen")

from LiveChess2Fen.lc2fen.fen import board_to_fen, list_to_board
from LiveChess2Fen.lc2fen.infer_pieces import infer_chess_pieces


def prop2fen(probs, a1_pos="BL", previous_fen=None):
    prob_list = [probs[i] for i in range(probs.shape[0])]
    predictions = infer_chess_pieces(prob_list, a1_pos, previous_fen)
    board = list_to_board(predictions)
    fen = board_to_fen(board)
    return fen
