import pygame
import time
import random


class Player:
    def __init__(self, screen, board, pos):
        self.screen = screen
        self.board = board
        self.x, self.y = pos
        self.dir = 'down'
        self.new_dir = 'down'
        self.speed = 0.1
        self.board_pos = self.get_board_pos()
        self.spos = self.board_pos

    def reverse_dir(self):
        if self.dir == 'up':
            return 'down'
        if self.dir == 'down':
            return 'up'
        if self.dir == 'left':
            return 'right'
        if self.dir == 'right':
            return 'left'

    def set_dir(self, dir):
        self.new_dir = dir

    def check_change(self):
        if self.board_pos != self.get_board_pos():
            self.board_pos = self.get_board_pos()
            self.spos = self.get_board_pos(5, 5)
            return True
        return False

    def get_board_pos(self, offsetx=0, offsety=0):
        return board.get_cell((self.x + offsetx, self.y + offsety))

    def get_possibles(self):
        a = []
        if self.board.wall_map[self.spos[1] + 1][self.spos[0]] == 0:
            a.append('down')
        if self.board.wall_map[self.spos[1] - 1][self.spos[0]] == 0:
            a.append('up')
        if self.board.wall_map[self.spos[1]][self.spos[0] - 1] == 0:
            a.append('left')
        if self.board.wall_map[self.spos[1]][self.spos[0] + 1] == 0:
            a.append('right')
        print(a)
        print(self.dir, self.reverse_dir())
        if self.reverse_dir() in a:
            a.remove(self.reverse_dir())
        return a # ['up', 'down', 'right', 'left']



    def move(self, possibles):
        if self.check_change():
            possibles = self.get_possibles()
            print(self.spos)
            print(possibles)
            if self.dir not in possibles:
                self.dir = random.choice(possibles)
            if self.new_dir in possibles:
                self.dir = self.new_dir
        if self.dir == 'up':
            self.y -= self.speed
        if self.dir == 'down':
            self.y += self.speed
        if self.dir == 'left':
            self.x -= self.speed
        if self.dir == 'right':
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(self.screen, (200, 200, 10), (self.x, self.y, self.board.cell_size, self.board.cell_size))


class Cell:
    def __init__(self, x, y, color="black"):
        self.x = x
        self.y = y
        self.color = color

    def print_me(self):
        print(self.x, self.y)

    def change_color(self):
        if self.color == "black":
            self.color = "white"
        elif self.color == "white":
            self.color = "black"


class Board:
    # создание поля
    def __init__(self, width, height, wall_map=[[1, 1, 1, 1, 1],
                         [1, 0, 0, 0, 1],
                         [1, 0, 1, 0, 1],
                         [1, 0, 0, 0, 1],
                         [1, 0, 1, 0, 1],
                         [1, 0, 0, 0, 1],
                         [1, 1, 1, 1, 1]]):
        self.width = width
        self.height = height
        self.wall_map = wall_map
        self.board = []
        self.cells = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.fill_cells()
        self.create_cells()

    def create_cells(self):
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                if self.wall_map[j][i] == 0:
                    self.board[i].append(Cell(i, j))
                if self.wall_map[j][i] == 1:
                    self.board[i].append(Cell(i, j, color='white'))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.fill_cells()

    def render(self):
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if self.board[i][j].color == "white":
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))
                if self.board[i][j].color == "black":
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size), 1)
                if self.board[i][j].color == "red":
                    pygame.draw.rect(screen, (155, 0, 0), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))

    def fill_cells(self):
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j] = [self.top + i * self.cell_size,
                                    self.left + j * self.cell_size,
                                    self.cell_size,
                                    self.cell_size]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def get_cell(self, pos):
        pos = int(pos[0] + 0), int(pos[1] + 0)
        i, j = -1, -1
        for cell_row in self.cells:
            i += 1
            if cell_row[0][0] <= pos[0] < cell_row[0][0] + self.cell_size:
                for cell in cell_row:
                    j += 1
                    if cell[1] <= pos[1] < cell[1] + self.cell_size:
                        return [i, j]
        return [-1, -1]

    def on_click(self, cell):
        return

    def load_map(self, file_adr):
        with open(file_adr, 'r') as f:
            _map = list(f.read().split('\n'))
            wall_map = [x.split() for x in _map]
            print(wall_map)
            x = len(wall_map)
            y = len(wall_map[0])
            print(x, y)
            for i in range(x - 1):
                for j in range(y - 1):
                    wall_map[i][j] = int(wall_map[i][j])
                    print(i, j)
        a = Board(x, y, wall_map)
        a.wall_map = wall_map
        return a


up, down, left, right = ([119, 275], [115, 273], [97, 274], [100, 276])
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
board = Board.load_map(None, 'C:\\Users\\79807\\Desktop\\map1.html')
board.set_view(50, 50, 50)
running = True
player = Player(screen, board, (100, 100))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key in up:
                player.set_dir('up')
            if event.key in down:
                player.set_dir('down')
            if event.key in left:
                player.set_dir('left')
            if event.key in right:
                player.set_dir('right')
    screen.fill((0, 0, 0))
    board.render()
    player.draw()
    player.move([])
    pygame.display.flip()

pygame.quit()