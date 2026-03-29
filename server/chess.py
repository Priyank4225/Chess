import copy

class Chess:
    def __init__(self, p1, p2):
        self.board = [
            [24,23,22,25,26,22,23,24],
            [21,21,21,21,21,21,21,21],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [11,11,11,11,11,11,11,11],
            [14,13,12,15,16,12,13,14]
        ]
        self.clients = {p1:1, p2:2}
        self.turn = 1
        self.start = ""
        self.ep = ""

    def find_king(self, color):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color*10+6:
                    return str(i)+str(j)

    def pawn(self, s, u):
        c = self.clients[u]
        d = -1 if c == 1 else 1
        y,x = int(s[0]),int(s[1])
        m=[]
        if 0<=y+d<=7 and self.board[y+d][x]==0:
            m.append(str(y+d)+str(x))
            if (c==1 and y==6) or (c==2 and y==1):
                if self.board[y+2*d][x]==0:
                    m.append(str(y+2*d)+str(x))
        for dx in (-1,1):
            if 0<=x+dx<=7 and 0<=y+d<=7:
                if self.board[y+d][x+dx]//10==3-c:
                    m.append(str(y+d)+str(x+dx))
        return m, False

    def bishop(self,s,u):
        c=self.clients[u]
        y,x=int(s[0]),int(s[1])
        m=[]
        for dy,dx in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            i=1
            while 0<=y+dy*i<=7 and 0<=x+dx*i<=7:
                if self.board[y+dy*i][x+dx*i]//10==c: break
                m.append(str(y+dy*i)+str(x+dx*i))
                if self.board[y+dy*i][x+dx*i]//10==3-c: break
                i+=1
        return m, False

    def rook(self,s,u):
        c=self.clients[u]
        y,x=int(s[0]),int(s[1])
        m=[]
        for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            i=1
            while 0<=y+dy*i<=7 and 0<=x+dx*i<=7:
                if self.board[y+dy*i][x+dx*i]//10==c: break
                m.append(str(y+dy*i)+str(x+dx*i))
                if self.board[y+dy*i][x+dx*i]//10==3-c: break
                i+=1
        return m, False

    def knight(self,s,u):
        c=self.clients[u]
        y,x=int(s[0]),int(s[1])
        m=[]
        for dy,dx in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            if 0<=y+dy<=7 and 0<=x+dx<=7:
                if self.board[y+dy][x+dx]//10!=c:
                    m.append(str(y+dy)+str(x+dx))
        return m, False

    def queen(self,s,u):
        return self.bishop(s,u)[0]+self.rook(s,u)[0], False

    def king(self,s,u):
        c=self.clients[u]
        y,x=int(s[0]),int(s[1])
        m=[]
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dy==dx==0: continue
                ny,nx=y+dy,x+dx
                if 0<=ny<=7 and 0<=nx<=7:
                    if self.board[ny][nx]//10!=c:
                        m.append(str(ny)+str(nx))
        return m, False

    def get_moves(self,s,u):
        p=self.board[int(s[0])][int(s[1])] % 10
        if p==1: return self.pawn(s,u)
        if p==2: return self.bishop(s,u)
        if p==3: return self.knight(s,u)
        if p==4: return self.rook(s,u)
        if p==5: return self.queen(s,u)
        if p==6: return self.king(s,u)
        return [],False

    def move(self,s,e,u):
        if e not in self.get_moves(s,u)[0]: return self.board
        self.board[int(e[0])][int(e[1])] = self.board[int(s[0])][int(s[1])]
        self.board[int(s[0])][int(s[1])] = 0
        self.turn = 3-self.turn
        return self.board

    def move_start(self,m,u):
        if self.clients[u]!=self.turn: return []
        self.start=m
        return self.get_moves(m,u)

    def move_end(self,m,u):
        return self.move(self.start,m,u)