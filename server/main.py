from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uuid
from server.chess import Chess

app = FastAPI()

class Manager:
    def __init__(self):
        self.waiting=[]
        self.games={}

    async def connect(self,ws):
        await ws.accept()
        if self.waiting:
            other=self.waiting.pop()
            gid=str(uuid.uuid4())
            game=Chess(ws,other)
            self.games[gid]=game
            await ws.send_json({"Type":"Auth","game_id":gid,"color":"Black","Board":game.board})
            await other.send_json({"Type":"Auth","game_id":gid,"color":"White","Board":game.board})
        else:
            self.waiting.append(ws)

    async def handle(self,ws,msg):
        g=self.games[msg["game_id"]]
        if msg["Part"]=="Start":
            pos=g.move_start(msg["Move"],ws)
            await ws.send_json({"Type":"Move","Part":"Start","pos":pos})
        else:
            board=g.move_end(msg["Move"],ws)
            for c in g.clients:
                await c.send_json({"Type":"Move","Part":"End","Board":board})

manager=Manager()

@app.websocket("/ws")
async def ws(ws:WebSocket):
    await manager.connect(ws)
    try:
        while True:
            msg=await ws.receive_json()
            await manager.handle(ws,msg)
    except WebSocketDisconnect:
        pass