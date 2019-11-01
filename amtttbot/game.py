import logging
import random

class ATBGame():
    CELL_EMPTY = 0
    CELL_PC = 1
    CELL_PLAYER = 2

    GAME_DRAW = 1
    GAME_WIN = 2
    GAME_LOSE = 3

    SIZE = 3

    PLAYER_FIRST = 0
    PLAYER_SECOND = 1

    def __init__(self, ctx, chat_id):
        self.ctx = ctx
        self.chat_id = chat_id
        self.first_turn = random.choice([self.PLAYER_FIRST, self.PLAYER_SECOND])
        self.size = self.SIZE
        self.board = [[0]*self.size for x in range(self.size)]
        self.moves = 0

        if self.first_turn == self.PLAYER_FIRST:
            ctx.bot.send_message(chat_id=self.chat_id, text="Player has first turn")
        else:
            ctx.bot.send_message(chat_id=self.chat_id, text="PC has first turn")

        if self.first_turn == self.PLAYER_SECOND:
            self.make_pc_move()

        ctx.bot.send_message(chat_id=self.chat_id, text=self.as_string())

    def possible_moves(self):
        moves = []

        for i in range (0, self.size):
            for j in range (0, self.size):
                if self.board[i][j] == 0:
                    moves.append((i,j))

        return moves

    def move(self, i, j):
        res = self.make_move(i-1,j-1)

        if res < 0:
            self.ctx.bot.send_message(chat_id=self.chat_id, text="Illegal turn")
            return -1

        self.ctx.bot.send_message(chat_id=self.chat_id, text=self.as_string())

        if res == self.GAME_DRAW:
            self.ctx.bot.send_message(chat_id=self.chat_id, text="DRAW")
        elif res == self.GAME_WIN:
            self.ctx.bot.send_message(chat_id=self.chat_id, text="PLAYER WON")
        elif res == self.GAME_LOSE:
            self.ctx.bot.send_message(chat_id=self.chat_id, text="PC WON")

        return 0

    def make_move(self, i, j):
        if self.board[i][j] != self.CELL_EMPTY or i > self.size-1 or j > self.size-1:
            return -1

        self.board[i][j] = self.CELL_PLAYER
        self.moves = self.moves + 1

        if self.fast_check(i,j) > 0:
            return self.GAME_WIN

        if self.moves >= self.size * self.size:
            return self.GAME_DRAW

        if self.make_pc_move() > 0:
            return self.GAME_LOSE

        if self.moves >= self.size * self.size:
            return self.GAME_DRAW

        return 0

    def make_pc_move(self):
        # Just random pick
        move = random.choice(self.possible_moves())
        self.board[move[0]][move[1]] = self.CELL_PC
        self.moves = self.moves + 1

        return self.fast_check(move[0],move[1])

    def fast_check(self, x, y):
        done = 1
        side = self.board[x][0]
        for i in range (0, self.size):
            if self.board[x][i] == self.CELL_EMPTY or self.board[x][i] != side:
                done = 0
                break
        if done == 1: return 1

        done = 1
        side = self.board[0][y]
        for j in range(0, self.size):
            if self.board[j][y] == self.CELL_EMPTY or self.board[j][y] != side:
                done = 0
                break
        if done == 1: return 1

        if x == y:
            done = 1
            side = self.board[0][0]
            for i in range(0, self.size):
                if self.board[i][i] == self.CELL_EMPTY or self.board[i][i] != side:
                    done = 0
                    break
        if done == 1: return 1

        if x == (self.size-y-1):
            done = 1
            side = self.board[0][self.size-1]

            for i in range(0, self.size):
                if self.board[i][self.size-i-1] == self.CELL_EMPTY or self.board[i][self.size-i-1] != side:
                    done = 0
                    break

        return done

    def as_string(self):
        HEAVY_X = u'\u2716'
        HEAVY_O = u'\u2b55'
        HEAVY_Q = u'\u2753'

        str = ""

        if self.first_turn == self.PLAYER_FIRST:
            npc = HEAVY_O
            player = HEAVY_X
        else:
            npc = HEAVY_X
            player = HEAVY_O

        for i in range (0, self.size):
            for j in range (0, self.size):
                if self.board[i][j] == self.CELL_EMPTY:
                    str += HEAVY_Q
                elif self.board[i][j] == self.CELL_PC:
                    str += npc
                else:
                    str += player
            str += "\n"

        return str
