import pygame
import os
import random
import sys
from random import randint

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
        if (self.coords[0] > pos[0] and pos[0] > self.coords[0] + self.size[0]) and (
                self.coords[1] > pos[1] and pos[1] > self.coords[1] + self.size[1]):
            self.image = Button.image_pressed
            if clicked:
                #print('ACTION PERFORMED!!!')
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
            self.x, self.y = self.get_board_pos(5, 5)[0] * self.board.cell_size + self.board.left, \
                             self.get_board_pos(5, 5)[1] * self.board.cell_size + self.board.top
            self.spos = self.get_board_pos(5, 5)
            if self.board.board[self.spos[0]][self.spos[1]].collectable:
                self.board.board[self.spos[0]][ self.spos[1]].collected = True
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
        return a  # ['up', 'down', 'right', 'left']

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
        self.collectable = True if color == "black" else False
        self.collected = False

    def change_color(self):
        if self.color == "white":
            self.color = "black"
        if self.color == "black":
            self.color = "white"

    def draw(self, *args):
        # args = (self.top + i * self.cell_size,
        # self.left + j * self.cell_size, self.cell_size,
        # self.cell_size)

        if self.color == "black" and self.collectable and self.collected:
            pygame.draw.rect(screen, (0, 0, 0), args)
        elif self.color == "black" and self.collectable and not self.collected:
            #draw collectable sprite
            pygame.draw.rect(screen, (0, 0, 0), args)
            pygame.draw.circle(screen, (255, 255, 255), (args[0] + args[2] // 2, args[1] + args[2] // 2), args[2] // 6)
        elif self.color == "white" and not self.collectable:
            pygame.draw.rect(screen, (200, 200, 255), args)




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
                self.board[i][j].draw(self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size)
                if self.board[i][j].color == "white" and False:
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))
                if self.board[i][j].color == "black" and False:
                    pygame.draw.rect(screen, (0, 0, 0), (
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

    def on_click(self, cell):
        return

    def load_map(self, file_adr):
        with open(file_adr, 'r') as f:
            _map = list(f.read().split('\n'))
            wall_map = [x.split() for x in _map]
            x = len(wall_map)
            y = len(wall_map[0])
            for i in range(x - 1):
                for j in range(y - 1):
                    wall_map[i][j] = int(wall_map[i][j])
        a = Board(x, y, wall_map)
        a.wall_map = wall_map
        return a

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

    def get_coords(self, ij):
        return (30 * ij[0] + 30, 30 * ij[1] + 30)

    def change_color(self, i):
        if self.board[i[0]][i[1]].color == "black":
            self.board[i[0]][i[1]].color = "white"
        elif self.board[i[0]][i[1]].color == "white":
            self.board[i[0]][i[1]].color = "black"

    def open_map(self, i):
        self.board[i[0]][i[1]].change_color()

    def get_color(self, i):
        return self.board[i[0]][i[1]].color


lob_img = load_image('lob.png', None)


class Tverdolobiy(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y, board, player):
        super().__init__(group)
        self.image = lob_img
        self.board = board
        self.player = player
        self.speed = 0.1
        self.chek_lst = []
        self.wall = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def payment(self, player, lob):
        n = 200
        if abs(player[0] - lob[0]) > n or abs(player[1] - lob[1]) > 150:
            return True
        return False

    def move(self):
        board, player = self.board, self.player
        lob_cell = (self.rect.x, self.rect.y)
        player_cell = (int(player.x), int(player.y))
        if not len(self.chek_lst) and self.payment(player_cell, lob_cell):
            self.chek_lst.append(player_cell)
        elif len(self.chek_lst) and self.payment(player_cell, self.chek_lst[-1]):
            self.chek_lst.append(player_cell)
        if len(self.chek_lst):
            if self.chek_lst[0][0] > lob_cell[0]:
                self.rect = self.rect.move(1, 0)
            elif self.chek_lst[0][0] < lob_cell[0]:
                self.rect = self.rect.move(-1, 0)
            elif self.chek_lst[0][1] > lob_cell[1]:
                self.rect = self.rect.move(0, 1)
            elif self.chek_lst[0][1] < lob_cell[1]:
                self.rect = self.rect.move(0, -1)
            self.rect = self.rect.move(0, 0)
            if self.chek_lst[0] == lob_cell:
                del self.chek_lst[0]
        ls = board.get_cell((self.rect.x, self.rect.y))
        if board.get_color(ls) == 'white':
            board.open_map(ls)
            self.wall.append(ls)
        if len(self.wall) and ls != self.wall[0]:
            board.open_map(self.wall[0])
            del self.wall[0]

    def die(self):
        self.kill()


leg_img = load_image('leg.png')


class Legushka(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y, board, player):
        super().__init__(group)
        self.image = leg_img
        self.board = board
        self.player = player
        self.speed = 0.5
        self.x = self.y = 0
        self.chek_lst = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def payment(self, leg_cell):
        lst = [self.chek_lst[0], leg_cell]
        count = 1
        x = (lst[0][0] - lst[1][0])
        y = (lst[0][1] - lst[1][1])
        while True:
            if 0 != abs(x / (count + 1)) < 1 or 0 != abs(y / (count + 1)) < 1:
                x, y = x / count, y / count
                break
            count += 1
        if not int(x) and not int(y):
            y = x = 1
        return (x, y)

    def move(self):
        x, y = self.x, self.y
        board, player = self.board, self.player
        leg_cell = (self.rect.x, self.rect.y)
        player_cell = (int(player.x), int(player.y))
        if not len(self.chek_lst) and board.get_color(board.get_cell(player_cell)) \
                and player_cell[0] % 30 == 0 and player_cell[1] % 30 == 0:
            self.chek_lst.append(player_cell)
            self.x, self.y = x, y = self.payment(leg_cell)
        elif len(self.chek_lst) and (leg_cell[0], leg_cell[1]) == self.chek_lst[0]:
            if abs(leg_cell[0] - player_cell[0]) >= 150 or \
                    abs(leg_cell[1] - player_cell[1]) >= 150:
                del self.chek_lst[0]
            else:
                x = y = 0
        if len(self.chek_lst):
            if leg_cell[0] == self.chek_lst[0][0]:
                self.rect = self.rect.move(0, y)
            elif leg_cell[1] == self.chek_lst[0][1]:
                self.rect = self.rect.move(x, 0)
            else:
                self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()


mersz = load_image('mersz.jpg')


class Merzopakostniy(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y, board, player):
        super().__init__(group)
        self.group = group
        self.image = mersz
        self.board = board
        self.player = player
        self.x = self.y = 0
        self.chek_lst = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.time = self.step = 0
        self.list_bomb = []

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def move(self):
        b = self.board
        self.step += 1
        i, ln = 0, len(self.chek_lst)
        while i < ln and ln:
            self.chek_lst[i] -= 1
            if not self.chek_lst[i]:
                self.list_bomb[i].die()
                del self.list_bomb[i], self.chek_lst[i]
                ln = len(self.chek_lst)
            i += 1
        if self.step == 240:
            bx, by = b.get_coords((b.get_cell((self.rect.x, self.rect.y))))
            bomb = Bomb(self.group, bx, by)
            bomb.resize(30)
            self.list_bomb.append(bomb)
            self.chek_lst.append(randint(300, 390))
            self.step = 0
        if not self.y and not self.x:
            while True:
                self.y = randint(1, (len(self.board.wall_map) - 3))
                self.x = randint(1, (len(self.board.wall_map[0]) - 3))
                if not self.board.wall_map[self.y][self.x]:
                    self.x, self.y = self.board.get_coords((self.x, self.y))
                    break
        ls = (self.rect.x, self.rect.y)
        if self.y == self.rect.y and self.rect.x == self.x:
            self.x = self.y = 0
        elif self.y == self.rect.y:
            if self.x > self.rect.x:
                if 'black' == b.get_color(b.get_cell((ls[0] + 30, ls[1]))):
                    self.rect = self.rect.move(1, 0)
                    #print(b.get_color(b.get_cell((ls[0] + 30, ls[1]))))
                else:
                    self.x = self.rect.x
            elif self.x < self.rect.x:
                if 'black' == b.get_color(b.get_cell((ls[0] - 1, ls[1]))):
                    self.rect = self.rect.move(-1, 0)
                    #print(b.get_color(b.get_cell((ls[0] - 1, ls[1]))))
                else:
                    self.x = self.rect.x
        else:
            if self.y > self.rect.y:
                if 'black' == b.get_color(b.get_cell((ls[0], ls[1] + 30))):
                    self.rect = self.rect.move(0, 1)
                    print(b.get_color(b.get_cell((ls[0], ls[1] + 30))))
                else:
                    self.y = self.rect.y
            elif self.y < self.rect.y:
                if 'black' == b.get_color(b.get_cell((ls[0], ls[1] - 1))):
                    self.rect = self.rect.move(0, -1)
                    print(b.get_color(b.get_cell((ls[0], ls[1] - 1))))
                else:
                    self.y = self.rect.y

    def num_bomb(self):
        return self.list_bomb


# 3 to 7
bb = load_image('bomb.jpg')


class Bomb(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y):
        super().__init__(group)
        self.image = bb
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def die(self):
        self.kill()


class Check:
    def __init__(self, player, lst):
        self.lst = lst
        self.player = player

    def checkaed(self):
        x, y = int(self.player.x), int(self.player.y)
        x, y = set(range(x, x + 30)), set(range(y, y + 30))
        for name in self.lst:
            name_x = set(range(name.rect.x + 7, name.rect.x + 23))
            name_y = set(range(name.rect.y + 7, name.rect.y + 23))
            if name_x & x and name_y & y:
                print('YOU LOSE')
                terminate()


def game():
    group = pygame.sprite.Group()
    player_anim = Anime(group, (228, 288))
    board = Board.load_map(None, 'data\\map1.html')
    board.set_view(30, 30, 30)
    player = Player(screen, player_anim, board, (60, 300))
    legushka = Legushka(group, 60, 60, board, player)
    tverdolobiy = Tverdolobiy(group, 240, 60, board, player)
    merzopakostniy = Merzopakostniy(group, 300, 60, board, player)
    running = True
    c = 0
    check = Check(player, merzopakostniy.num_bomb() + [legushka, tverdolobiy])
    player_anim.resize(30)
    legushka.resize(30)
    tverdolobiy.resize(30)
    merzopakostniy.resize(30)
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
                if event.key == pygame.K_LEFT:
                    player.set_dir('left')
                if event.key == pygame.K_RIGHT:
                    player.set_dir('right')
                if event.key == pygame.K_UP:
                    player.set_dir('up')
                if event.key == pygame.K_DOWN:
                    player.set_dir('down')
        screen.fill((0, 0, 0))
        board.render()
        player.move([])
        player_anim.rect.x, player_anim.rect.y = player.x, player.y
        merzopakostniy.move()
        if not c % 2:
            legushka.move()
            tverdolobiy.move()
        group.draw(screen)
        if c % 20 == 0:
            player_anim.update()
        check.checkaed()
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
            group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


load_screen()
game()
