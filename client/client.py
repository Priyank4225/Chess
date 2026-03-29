import pygame_ce as pygame
import asyncio, websockets, json, threading, queue, os

pygame.init()
size = 480
tile = size // 8
screen = pygame.display.set_mode((size, size))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load(path):
    return pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()

def scale(img):
    return pygame.transform.scale(img, (tile, tile))

board_img = pygame.transform.scale(load("board.png"), (size, size))

white_pawn = scale(load("Resources/white-pawn.png"))
white_rook = scale(load("Resources/white-rook.png"))
white_knight = scale(load("Resources/white-knight.png"))
white_bishop = scale(load("Resources/white-bishop.png"))
white_queen = scale(load("Resources/white-queen.png"))
white_king = scale(load("Resources/white-king.png"))

black_pawn = scale(load("Resources/black-pawn.png"))
black_rook = scale(load("Resources/black-rook.png"))
black_knight = scale(load("Resources/black-knight.png"))
black_bishop = scale(load("Resources/black-bishop.png"))
black_queen = scale(load("Resources/black-queen.png"))
black_king = scale(load("Resources/black-king.png"))

dot = scale(load("Resources/dot.png"))

PIECES = {
    (1,1): white_pawn,
    (1,2): white_bishop,
    (1,3): white_knight,
    (1,4): white_rook,
    (1,5): white_queen,
    (1,6): white_king,
    (2,1): black_pawn,
    (2,2): black_bishop,
    (2,3): black_knight,
    (2,4): black_rook,
    (2,5): black_queen,
    (2,6): black_king,
}

board = [[0]*8 for _ in range(8)]
pos = []
gid = ""

to_server = queue.Queue()
from_server = queue.Queue()

async def net():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        async def send():
            while True:
                d = await asyncio.to_thread(to_server.get)
                if d is None:
                    break
                await ws.send(json.dumps(d))
        async def recv():
            while True:
                msg = await ws.recv()
                from_server.put(json.loads(msg))
        await asyncio.gather(send(), recv())

threading.Thread(target=lambda: asyncio.run(net()), daemon=True).start()

running = True
clock = pygame.time.Clock()

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            to_server.put(None)
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos[0] // tile, e.pos[1] // tile
            move = str(y) + str(x)
            if pos and move in pos[0]:
                to_server.put({"Type":"Move","Part":"End","game_id":gid,"Move":move})
                pos = []
            else:
                to_server.put({"Type":"Move","Part":"Start","game_id":gid,"Move":move})

    try:
        while True:
            m = from_server.get_nowait()
            if m["Type"] == "Auth":
                gid = m["game_id"]
                board = m["Board"]
            elif m["Part"] == "Start":
                pos = m["pos"]
            elif m["Part"] == "End":
                board = m["Board"]
    except:
        pass

    screen.blit(board_img, (0, 0))

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece != 0:
                color = piece // 10
                kind = piece % 10
                screen.blit(PIECES[(color, kind)], (j*tile, i*tile))

            if pos and str(i)+str(j) in pos[0]:
                screen.blit(dot, (j*tile, i*tile))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
