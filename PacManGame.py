import pygame
import random as rd


pygame.init()

display_width = 800
display_height = 600

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pac-Man')

icon = pygame.image.load('Images/PacManIcon.png')
pygame.display.set_icon(icon)

usr_width = 40
usr_height = 40
usr_x = (display_width // 2) - (usr_width / 2)
usr_y = (display_height // 2) - (usr_height / 2)

PM_right = pygame.image.load('Images/Player/PacMan_Right.png').convert_alpha()
PM_left = pygame.image.load('Images/Player/PacMan_Left.png').convert_alpha()
PM_down = pygame.image.load('Images/Player/PacMan_Down.png').convert_alpha()
PM_up = pygame.image.load('Images/Player/PacMan_Up.png').convert_alpha()

class Player:
    """Инициализация игрока"""
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.type = 'Player'
        self.image = PM_right
        self.rect = self.image.get_rect()
        self.perm_rect = self.rect
        self.speed = 3
        self.LastMove = 'Right'
        self.mbottom = None
        self.mright = None
        self.mleft = None
        self.mtop = None


    def draw(self):
        """Отрисовать игрока на экране"""
        self.screen.blit(self.image, self.rect)

    def spawn(self):
        """Точка появления игрока на карте"""
        spawn = (usr_x, usr_y)
        self.rect = self.perm_rect.move(spawn)

    def update(self):
        if self.mright and self.rect.right < self.screen_rect.right:
            self.image = PM_right
            self.rect.x += self.speed

        elif self.mleft and self.rect.left > 0:
            self.image = PM_left
            self.rect.x -= self.speed

        elif self.mtop and self.rect.top > 0:
            self.image = PM_up
            self.rect.y -= self.speed

        elif self.mbottom and self.rect.bottom < self.screen_rect.bottom:
            self.image = PM_down
            self.rect.y += self.speed

Hunt_img = pygame.image.load('Images/Hunters/HunterAqua.png').convert_alpha()

class Hunter:
    """Инициализация охотников"""
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.type = 'Hunter'
        self.image = Hunt_img
        self.rect = self.image.get_rect()
        self.perm_rect = self.rect
        self.next_turn = 0
        self.turn = None
        self.ticks = 0
        self.speed = 3

    def draw(self):
        """Отрисовать игрока на экране"""
        self.screen.blit(self.image, self.rect)

    def spawn(self):
        """Точка появления игрока на карте"""
        spawn = (usr_x, usr_y - 150)
        self.rect = self.perm_rect.move(spawn)

    def update(self):
        self.ticks = pygame.time.get_ticks()
        ticks_of_next_turn = self.ticks - self.next_turn

        if self.ticks > self.next_turn:
            if ticks_of_next_turn > 2000:
                self.next_turn = self.ticks - 2000
            self.turn = rd.choice(("Up", "Down", "Left", "Right"))
            self.next_turn += 2000

        if self.turn == "Right":
            if self.rect.right < self.screen_rect.right:
                self.rect.x += self.speed
            else:
                self.next_turn = self.ticks
        if self.turn == "Down":
            if self.rect.bottom < self.screen_rect.bottom:
                self.rect.y += self.speed
            else:
                self.next_turn = self.ticks
        elif self.turn == "Left":
            if self.rect.left > self.screen_rect.left:
                self.rect.x -= self.speed
            else:
                self.next_turn = self.ticks
        elif self.turn == "Up":
            if self.rect.top > self.screen_rect.top:
                self.rect.y -= self.speed
            else:
                self.next_turn = self.ticks

clock = pygame.time.Clock()

player = Player(screen)
player.spawn()

hunter = Hunter(screen)
hunter.spawn()

def run_game():
    global make_move, move_direction
    game = True

    while game:
        for evn in pygame.event.get():
            if evn.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((25,25,112))

        player.draw()
        events(player)
        player.update()

        hunter.draw()
        hunter.update()

        pygame.display.update()
        clock.tick(60)

def events(player):
    """Обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    # Вправо
    if keys[pygame.K_d]:
        player.mright = True
        player.LastMove = "Right"
        player.mtop = False
        player.mbottom = False
        player.mleft = False
    # Влево
    elif keys[pygame.K_a]:
        player.mleft = True
        player.LastMove = "Left"
        player.mtop = False
        player.mbottom = False
        player.mright = False
    # Вверх
    elif keys[pygame.K_w]:
        player.mtop = True
        player.LastMove = "Up"
        player.mleft = False
        player.mbottom = False
        player.mright = False
    # Вниз
    elif keys[pygame.K_s]:
        player.mbottom = True
        player.LastMove = "Down"
        player.mtop = False
        player.mleft = False
        player.mright = False

run_game()