import numpy as np
import uvicorn
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import RedirectResponse
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from draughts import __version__
from draughts.standard import Board
from typing import Literal
from collections import defaultdict


class Server:
    def __init__(
        self,
        board=Board(),
        draw_board=True,
        populate_board=True,
        show_pseudo_legal_moves=True,
    ):
        self.app = FastAPI(title="py-draughts", version=__version__)
        self.app.mount(
            "/static", StaticFiles(directory="draughts/static"), name="static"
        )
        self.templates = Jinja2Templates(directory="draughts/templates/")
        self.board = board
        self.router = APIRouter()
        self.router.add_api_route("/", self.index)
        self.router.add_api_route("/set_board/{board_type}", self.set_board)
        self.router.add_api_route("/set_random_position", self.set_random_position)
        self.router.add_api_route("/random_move", self.random_move)
        self.router.add_api_route("/get_board_info", self.get_board_info)
        self.router.add_api_route("/get_legal_moves", self.get_legal_moves)
        self.app.include_router(self.router)
        self.draw_board = draw_board
        self.populate_board = populate_board
        self.show_pseudo_legal_moves = show_pseudo_legal_moves

    def set_board(self, request: Request, board_type: Literal["standard", "american"]):
        if board_type == "standard":
            from draughts.standard import Board

            self.board = Board()
        elif board_type == "american":
            from draughts.american import Board

            self.board = Board()

        return RedirectResponse(url="/")

    def get_legal_moves(self):
        legal_moves = list(self.board.legal_moves)
        from pprint import pprint

        pprint(legal_moves)
        moves_dict = defaultdict(list)
        for move in legal_moves:
            moves_dict[int(move.square_list[0])].extend(move.square_list[1:])
        print(moves_dict)
        return {
            "legal_moves": json.dumps(moves_dict),
        }

    def get_board_info(self, request: Request):
        return (
            {
                "request": request,
                "position": json.dumps(self.board.friendly_form.tolist()),
                "pseudo_legal_king_moves": json.dumps(
                    self.board.PSEUDO_LEGAL_KING_MOVES
                ),
                "pseudo_legal_man_moves": json.dumps(self.board.PSEUDO_LEGAL_MAN_MOVES),
                "draw_board": json.dumps(self.draw_board),
                "populate_board": json.dumps(self.populate_board),
                "show_pseudo_legal_moves": json.dumps(self.show_pseudo_legal_moves),
                "size": self.board.shape[0] ** 2,
            },
        )

    def set_random_position(self, request: Request):
        STARTING_POSITION = np.random.choice(
            [10, 0, -10, 1, -1],
            size=len(self.board.STARTING_POSITION),
            replace=True,
            p=[0.1, 0.6, 0.1, 0.1, 0.1],
        )
        self.board._pos = STARTING_POSITION
        return RedirectResponse(url="/")

    def random_move(self, request: Request):
        legal_moves = list(self.board.legal_moves)
        # print longest capture chain
        print(max(legal_moves, key=lambda x: len(x.captured_list)))
        move = np.random.choice(legal_moves)
        print(move)
        self.board.push(move)
        return {"position": self.board.friendly_form.tolist()}

    def index(self, request: Request):
        return self.templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "board": json.dumps(self.board.friendly_form.tolist()),
                "pseudo_legal_king_moves": json.dumps(
                    self.board.PSEUDO_LEGAL_KING_MOVES
                ),
                "pseudo_legal_man_moves": json.dumps(self.board.PSEUDO_LEGAL_MAN_MOVES),
                "draw_board": json.dumps(self.draw_board),
                "populate_board": json.dumps(self.populate_board),
                "show_pseudo_legal_moves": json.dumps(self.show_pseudo_legal_moves),
                "size": self.board.shape[0] ** 2,
            },
        )

    def run(self, **kwargs):
        uvicorn.run(self.app, **kwargs)


# STARTING_POSITION = np.array([10] * 15 + [0] * 20 + [-10] * 15, dtype=np.int8)
# # random starting position from 10, 0, -10,1,-1
STARTING_POSITION = np.random.choice(
    [10, 0, -10, 1, -1],
    size=len(Board.STARTING_POSITION),
    replace=True,
    p=[0.1, 0.4, 0.1, 0.2, 0.2],
)
# board = Board(STARTING_POSITION)
# board = Board()


# @app.get("/")
# def index(request: Request):
#     pprint(board.PSEUDO_LEGAL_KING_MOVES)
#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "board": board.friendly_form.reshape(10, 10).tolist(),
#             "debug": json.dumps(board.PSEUDO_LEGAL_KING_MOVES),
#         },
#     )


# @app.get("/random_move")
# def random_move(request: Request):
#     moves = list(board.legal_moves)
#     # get move wiht longest capture chain
#     if not moves:
#         print("No legal moves")
#         return {"position": board.friendly_form.reshape(10, 10).tolist()}
#     if np.random.random() < 0.7:
#         move = max(moves, key=lambda x: len(x.captured_list))
#     else:
#         move = np.random.choice(moves)

#     pprint(list(board.legal_moves))
#     print(move)
#     board.push(move)
#     return {"position": board.friendly_form.reshape(10, 10).tolist()}


# @app.get("/board")
# def get_board(request: Request):
#     return {"position": board.friendly_form.reshape(10, 10).tolist()}


if __name__ == "__main__":
    Server().run()
