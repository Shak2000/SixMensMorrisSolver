from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from main import Game

app = FastAPI()
game = Game()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start():
    game.start()


@app.post("/switch")
async def switch():
    game.switch()


@app.post("/place")
async def place(x: int, y: int):
    game.place(x, y)


@app.post("/move")
async def move(x: int, y: int, nx: int, ny: int):
    game.move(x, y, nx, ny)


@app.get("/get_piece_count")
async def get_piece_count(player: str):
    return game.get_piece_count(player)


@app.get("/check_mill")
async def check_mill(x: int, y: int, player: str):
    return game.check_mill(x, y, player)


@app.get("/get_opponent_pieces")
async def get_opponent_pieces(player: str):
    return game.get_opponent_pieces(player)


@app.post("/remove_piece")
async def remove_piece(x: int, y: int, player: str):
    game.remove_piece(x, y, player)


@app.get("/check_win")
async def check_win():
    return game.check_win()


@app.get("/has_valid_moves")
async def has_valid_moves(player: str):
    return game.has_valid_moves(player)


@app.post("/undo")
async def undo():
    game.undo()


@app.get("/get_unblocked_two_in_a_rows")
async def get_unblocked_two_in_a_rows(player: str):
    return game.get_unblocked_two_in_a_rows(player)


@app.get("/evaluate")
async def evaluate():
    return game.evaluate_for_player()


@app.get("/minimax")
async def minimax(depth: int, alpha: int, beta: int, maximizing_player: bool):
    return game.minimax(depth, alpha, beta, maximizing_player)


@app.post("/computer_move")
async def computer_move(depth: int):
    game.computer_move(depth)


@app.post("/remove_best_opponent_piece")
async def remove_best_opponent_piece(depth: int):
    game.remove_best_opponent_piece(depth)
