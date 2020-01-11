import pygame
import os
import random
import sys

FPS = 60
size = WIDTH, HEIGHT = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
up, down, left, right = ([119, 275], [115, 273], [97, 274], [100, 276])
clock = pygame.time.Clock()


pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    print(fullname)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey == 2:
        image = pygame.image.load(fullname).convert()
    return image


class Button(pygame.sprite.Sprite):
    image = load_image('btnBG.png')
    image_pressed = load_image("btnPressed.png")
    def __init__(self, group, coords, action, text):
        super().__init__(group)
        self.image = Button.image
        self.coords = coords
        self.size = 200, 30
        self.rect = (0, 0)
        self.text = text
        self.action = action

    def click(self):
        self.action()

    def update(self, pos, clicked):
        if (self.coords[0] > pos[0] and pos[0] > self.coords[0] + self.size[0]) and (self.coords[1] > pos[1] and pos[1] > self.coords[1] + self.size[1]):
            self.image = Button.image_pressed
            print('asd')
            if clicked:
                print('ACTION PERFORMED!!!')
                # self.click()
        else:
            self.sprite = Button.image


class Anime(pygame.sprite.Sprite):
    kadrs = [load_image('packman_1.png'),
             load_image('packman_2.png'),
             load_image('packman_3.png'),
             load_image('packman_4.png')]

    def __init__(self, group, pos):
        super().__init__(group)
        self.index = 0
        self.angle = 0
        self.image = pygame.transform.rotate(Anime.kadrs[0], self.angle)
        self.cimage = self.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'down'

    def update(self):
        a = [0, 1, 2, 3, 2, 1]
        self.index += 1
        self.index %= 6
        self.cimage = Anime.kadrs[a[self.index]]
        self.rotate(self.dir)

    def resize(self, size):
        for i in range(len(Anime.kadrs)):
            Anime.kadrs[i] = pygame.transform.scale(Anime.kadrs[i], (size, size))

    def rotate(self, dir):
        if dir == 'up':
            self.angle = 90
        if dir == 'down':
            self.angle = -90
        if dir == 'left':
            self.angle = -180
        if dir == 'right':
            self.angle = 0
        self.image = pygame.transform.rotate(self.cimage, self.angle)


class Player:
    def __init__(self, screen, anime, board, pos):
        self.anime = anime
        self.screen = screen
        self.board = board
        self.x, self.y = pos
        self.dir = 'down'
        self.new_dir = '_'
        self.speed = 0.7
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
            self.x, self.y = self.get_board_pos(5, 5)[0] * self.board.cell_size + self.board.left,  self.get_board_pos(5, 5)[1] * self.board.cell_size + self.board.top
            self.spos = self.get_board_pos(5, 5)
            return True
        return False

    def get_board_pos(self, offsetx=0, offsety=0):
        return self.board.get_cell((self.x + offsetx, self.y + offsety))

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
        if self.reverse_dir() in a:
            a.remove(self.reverse_dir())
        return a # ['up', 'down', 'right', 'left']

    def move(self, possibles):
        if self.check_change():
            possibles = self.get_possibles()
            if self.dir not in possibles:
                self.dir = random.choice(possibles)
                self.anime.rotate(self.dir)
            if self.new_dir in possibles:
                self.dir = self.new_dir
                self.anime.rotate(self.dir)
        self.anime.dir = self.dir
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
                    pygame.draw.rect(screen, (0, 0, 0), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))
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


class Cursor(pygame.sprite.Sprite):
    image = load_image("transparent pixel.png", colorkey=2)

    def __init__(self, group):
        super().__init__(group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 500)
        self.rect.y = random.randint(0, 500)

class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png", colorkey=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, 420)
        self.rect.y = random.randint(30, 420)
        self.collideble = True


    def update(self, pos):
        if pygame.sprite.collide_rect(self, pos) and self.collideble:
            self.image = load_image("boom.png")
            self.rect.x -= 25
            self.rect.y -= 25
            self.collideble = False

    def in_collide(self, pos):
        return pygame.sprite.collide_rect(self, pos)


def game():
    group = pygame.sprite.Group()
    player_anim = Anime(group, (228, 288))
    board = Board.load_map(None, 'C:\\Users\\79807\\Desktop\\map1.html')
    board.set_view(30, 30, 30)
    running = True
    c = 0
    player_anim.resize(30)
    player = Player(screen, player_anim, board, (100, 100))
    while running:
        c += 1
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
        player.move([])
        player_anim.rect.x, player_anim.rect.y = player.x, player.y
        group.draw(screen)
        if c % 20 == 0:
            player_anim.update()
        pygame.display.flip()

    pygame.quit()


def load_screen():
    if True:
        if True:
            p = (-1, -1)
            f = False
            fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
            group = pygame.sprite.Group()
            screen.blit(fon, (0, 0))
            b = Button(group, (0, 0), lambda x: x, 'TJDNP:VIO')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    p = event.pos
                    group.update(event.pos, False)
            group.update(p, f)
            print(p)
            group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

load_screen()
game()