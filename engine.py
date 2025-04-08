from stockfish import Stockfish
import os
from data.classes.Board import Board

STOCKFISH_PATH = "C:/Users/ethan/stockfish/stockfish.exe"

if "stockfish" not in globals():
    stockfish = Stockfish(STOCKFISH_PATH)

if not os.path.exists(STOCKFISH_PATH):
    raise RuntimeError(f"Stockfish binary not found at: {STOCKFISH_PATH}. Please verify the path.")

try:
    stockfish = Stockfish(STOCKFISH_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Stockfish failed to start. Check the binary at: {STOCKFISH_PATH}")

# Configure Stockfish settings
stockfish.update_engine_parameters({
    "Threads": 2,
    "Hash": 256,
    "UCI_LimitStrength": True,
    "UCI_Elo": 1500,
})
stockfish.set_depth(10)

def set_stockfish_level(skill_level=8):
    stockfish.set_skill_level(skill_level)

def get_best_move(board):
    fen = board.get_fen() or "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    print("Current FEN:", f"'{fen}'")
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    print("Best move:", best_move)
    return best_move
