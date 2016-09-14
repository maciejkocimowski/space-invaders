from sys import exit
import random
import pygame
from pygame.locals import *
from abc import ABCMeta, abstractmethod


class Options(object):
    SCREEN_SIZE = (800, 600)
    RED = (250, 0, 0)
    BRIGHT_RED = (255, 0, 0)
    GREEN = (0, 250, 0)
    BRIGHT_GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    CLOCK = pygame.time.Clock()
    SCORE = 0
    LIFE = 3


class EnemyAndGift(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, surface): pass


class Bullets(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, y_amount): pass


class Opponent(EnemyAndGift):
    def __init__(self, x_coord, y_coord, points, image):
        self.x = x_coord
        self.y = y_coord
        self.points = points
        self.image = pygame.image.load(image)
        self.speed = 3
        return

    def update(self, surface):
        self.y += self.speed
        surface.blit(self.image, (self.x, self.y))
        return


class Gift(EnemyAndGift):
    def __init__(self, x_coord, y_coord, function, image):
        self.x = x_coord
        self.y = y_coord
        self.function = function
        self.image = pygame.image.load(image)
        self.speed = 3
        return

    def update(self, surface):
        self.y += self.speed
        surface.blit(self.image, (self.x, self.y))
        return


class OppBullet(Bullets):

    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 13
        self.y = y_coord + 35
        self.image = pygame.image.load('laser.jpg')
        return

    def update(self, y_amount=5):
        self.y += y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


class Bullet(Bullets):

    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 20
        self.y = y_coord + 20
        self.image = pygame.image.load('laser.jpg')
        return

    def update(self, y_amount=30):
        self.y -= y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


class Generators(object):
    @staticmethod
    def generate_opponents():
        matrix = []
        for y in range(7):
            if y == 0:
                points = 30
                image = 'red.jpg'
            elif y == 1 or y == 2:
                points = 20
                image = 'yellow.jpg'
            else:
                points = 10
                image = 'green.jpg'
            opponents = [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                  random.randrange(-600, 0, 50), points, image)]
            matrix.append(opponents)
        return matrix

    @staticmethod
    def generate_gifts():
        matrix = []
        for y in range(8):
            if y == 0:
                function = 'addPoints'
                image = 'bonus2.png'
            # elif y == 1:
            #    function = 'laser'
            #    image = 'clean.png'
            elif y == 2:
                function = 'addLife'
                image = 'life.jpg'
            else:
                function = 'oddPoints'
                image = 'bonus1.png'
            gifts = [Gift(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                          random.randrange(-600, 0, 50),
                          function, image)]
            matrix.append(gifts)
        return matrix


class SpaceInvadersGame(object):
    options = Options()

    def __init__(self, score=options.SCORE, life=options.LIFE):
        pygame.init()
        flag = pygame.DOUBLEBUF
        self.surface = pygame.display.set_mode(options.SCREEN_SIZE, flag)
        pygame.display.set_caption('Space Invaders')
        game_icon = pygame.image.load('ship.jpg')
        pygame.display.set_icon(game_icon)
        self.surface.fill(options.BLACK)
        self.score = score
        self.bullets_array = []
        self.opponents_bullets = []
        generate = Generators()
        self.opponents_matrix = generate.generate_opponents()
        self.gifts_matrix = generate.generate_gifts()
        self.life = life
        self.image_r = pygame.image.load('red.jpg')
        self.image_g = pygame.image.load('green.jpg')
        self.image_y = pygame.image.load('yellow.jpg')
        self.image_bonus1 = pygame.image.load('bonus1.png')
        self.image_bonus2 = pygame.image.load('bonus2.png')
        self.image_life = pygame.image.load('life.jpg')

        self.game_intro_screen()
        self.player = pygame.image.load("ship.png")
        self.speed = 13
        self.player_x = options.SCREEN_SIZE[0] / 2 - 25
        self.player_y = options.SCREEN_SIZE[1] - 75
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and \
                                event.key == pygame.K_RETURN:
                    self.gamestate = 1
                    self.loop()
                if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_ESCAPE)):
                    exit()

    def move(self, dirx, diry):
        self.player_x += (dirx * self.speed)
        self.player_y += (diry * self.speed)

    def loop(self):
        """ glowna petla gry """
        can_shoot = True
        fire_wait = 60
        can_create = True
        create_wait = 2000
        opponent_can_shoot = True
        opponent_fire_wait = 60
        myfont = pygame.font.SysFont("Arial", 10)

        while self.gamestate == 1:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN and
                            event.key == pygame.K_ESCAPE)):
                    exit()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] \
                    and self.player_x < options.SCREEN_SIZE[0] - 50:
                self.move(1, 0)

            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.move(-1, 0)

            if keys[pygame.K_UP] and self.player_y > 0:
                self.move(0, -1)

            if keys[pygame.K_DOWN] \
                    and self.player_y < options.SCREEN_SIZE[1] - 75:
                self.move(0, 1)

            if keys[pygame.K_SPACE] and can_shoot:
                bullet = Bullet(self.surface, self.player_x, self.player_y)
                can_shoot = False
                self.bullets_array.append(bullet)

            if not self.life:
                self.gamestate = 0

            if not can_shoot and fire_wait <= 0:
                can_shoot = True
                fire_wait = 100

            if can_create and create_wait <= 0:
                can_create = True
                self.opponents_matrix.append(
                    random.choice([[Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                    random.randrange(-600, 0, 50), 10, 'green.jpg')],
                                   [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                    random.randrange(-600, 0, 50), 10, 'green.jpg')],
                                   [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                    random.randrange(-600, 0, 50), 10, 'green.jpg')],
                                   [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                    random.randrange(-600, 0, 50), 20, 'yellow.jpg')],
                                   [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                    random.randrange(-600, 0, 50), 20, 'yellow.jpg')],
                                  [Opponent(random.randrange(0, Options.SCREEN_SIZE[0], 50),
                                            random.randrange(-600, 0, 50), 30, 'red.jpg')]]))
                create_wait = 2000

            fire_wait -= options.CLOCK.tick(100)
            opponent_fire_wait -= options.CLOCK.tick(100)
            create_wait -= options.CLOCK.tick(100)

            self.surface.fill(options.BLACK)
            self.surface.blit(self.player, (self.player_x, self.player_y))

            for opponents in self.opponents_matrix:
                for opponent in opponents:
                    if opponent.y > 530:
                        opponent.y = random.randrange(-100, -35, 50)
                        opponent.x = random.randrange(0, Options.SCREEN_SIZE[0], 50)
                    elif (check_collision(self.player_x, self.player_y,
                                          opponent.x, opponent.y) or
                            check_collision(opponent.x, opponent.y,
                                            self.player_x, self.player_y)):
                        self.score += opponent.points
                        opponent.y = random.randrange(-100, -35, 50)
                        opponent.x = random.randrange(0, Options.SCREEN_SIZE[0], 50)
                        self.life -= 1

                    opponent.update(self.surface)

            for gifts in self.gifts_matrix:
                for gift in gifts:
                    if gift.y > 530:
                        gift.y = random.randrange(-3000, -35, 50)
                        gift.x = random.randrange(0, Options.SCREEN_SIZE[0], 50)
                    elif (check_collision(self.player_x, self.player_y,
                                          gift.x, gift.y) or
                            check_collision(gift.x, gift.y,
                                            self.player_x, self.player_y)):
                        if gift.function == 'addPoints':
                            self.score += 100
                        elif gift.function == 'addLife':
                            self.life += 1
                        # elif gift.function == 'cleanScreen':
                        #    bonus = True
                        elif gift.function == 'oddPoints':
                            self.score -= 100
                        gift.y = random.randrange(-3000, -35, 50)
                        gift.x = random.randrange(0, Options.SCREEN_SIZE[0], 50)

                    gift.update(self.surface)

            if opponent_can_shoot:
                flat_list = [opponent for opponents in self.opponents_matrix
                             for opponent in opponents
                             ]
                random_opponent = random.choice(flat_list)
                opponent_bullet = OppBullet(self.surface, random_opponent.x, random_opponent.y)
                self.opponents_bullets.append(opponent_bullet)
                opponent_can_shoot = False

            if not opponent_can_shoot and opponent_fire_wait <= 0:
                opponent_fire_wait = 500
                opponent_can_shoot = True

            for opponent_bullet in self.opponents_bullets:
                opponent_bullet.update()
                if opponent_bullet.y > 550:
                    self.opponents_bullets.remove(opponent_bullet)

                if (check_collision(opponent_bullet.x, opponent_bullet.y,
                                    self.player_x, self.player_y) and
                        opponent_bullet in self.opponents_bullets):
                    self.opponents_bullets.remove(opponent_bullet)
                    self.life -= 1

            for bullet in self.bullets_array:
                bullet.update()
                if bullet.y < 0:
                    self.bullets_array.remove(bullet)

                for opponents in self.opponents_matrix:
                    for opponent in opponents:
                        if (check_collision(bullet.x, bullet.y,
                                            opponent.x, opponent.y) and
                                bullet in self.bullets_array):
                            self.score += opponent.points
                            opponent.y = random.randrange(-100, -35, 50)
                            opponent.x = random.randrange(0, Options.SCREEN_SIZE[0], 50)
                            self.bullets_array.remove(bullet)

            score_label = myfont.render("SCORE: {}".format(self.score),
                                        1, options.YELLOW)
            self.surface.blit(score_label, (25, 575))
            life_label = myfont.render("LIFE: {}".format(self.life),
                                       1, options.YELLOW)
            self.surface.blit(life_label, (750, 575))

            pygame.display.flip()

        self.game_over_screen()


class Screens(SpaceInvadersGame):
    def __init__(self):
        SpaceInvadersGame.__init__(self)

    def game_intro_screen(self):
        bigfont = pygame.font.SysFont("Arial", 75)
        smallfont = pygame.font.SysFont("Arial", 25)
        name = bigfont.render("Space Invaders", 1, options.YELLOW)
        enter_t = smallfont.render("ENTER", 1, options.BLACK)
        esc_t = smallfont.render("ESC", 1, options.BLACK)
        or_t = smallfont.render("or", 1, options.YELLOW)
        f1_t = smallfont.render("Press F1 to get help", 1, options.YELLOW)
        self.surface.fill(options.BLACK)
        self.surface.blit(name, (140, 200))
        pygame.draw.rect(self.surface, options.GREEN, (150, 390, 150, 50))
        pygame.draw.rect(self.surface, options.RED, (500, 390, 150, 50))
        self.surface.blit(enter_t, (183, 402))
        self.surface.blit(esc_t, (550, 402))
        self.surface.blit(or_t, (390, 410))
        self.surface.blit(f1_t, (270, 570))
        self.player = pygame.image.load("ship.png")
        self.speed = 13
        self.player_x = options.SCREEN_SIZE[0] / 2 - 25
        self.player_y = options.SCREEN_SIZE[1] - 75
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.game_loop()

                elif (event.type == QUIT or
                        (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    exit()

                elif event.type == KEYDOWN and event.key == K_F1:
                    self.help_screen()

    def game_loop(self):
        self.gamestate = 1
        self.loop()

    def help_screen(self):
        bigfont = pygame.font.SysFont("Arial", 75)
        smallfont = pygame.font.SysFont("Arial", 20)
        name = bigfont.render("Help", 1, options.YELLOW)
        plus30 = smallfont.render("+ 30 points", 1, options.YELLOW)
        plus20 = smallfont.render("+ 20 points", 1, options.YELLOW)
        plus10 = smallfont.render("+ 10 points", 1, options.YELLOW)
        plus100 = smallfont.render("+ 100 points", 1, options.YELLOW)
        minus100 = smallfont.render("- 100 points", 1, options.YELLOW)
        plus1life = smallfont.render("+ 1 life", 1, options.YELLOW)
        opponents = smallfont.render("Opponents:", 1, options.YELLOW)
        gifts = smallfont.render("Gifts:", 1, options.YELLOW)
        moving = smallfont.render("Press UP, DOWN, LEFT and RIGHT to "
                                  "navigate the ship",
                                  1, options.YELLOW)
        space = smallfont.render("Press SPACE to fire", 1, options.YELLOW)
        lives = smallfont.render("You have 3 lives", 1, options.YELLOW)

        self.surface.fill(options.BLACK)
        self.surface.blit(name, (320, 30))

        self.surface.blit(opponents, (60, 130))
        self.surface.blit(self.image_r, (60, 170))
        self.surface.blit(self.image_y, (60, 220))
        self.surface.blit(self.image_g, (60, 270))

        self.surface.blit(gifts, (520, 130))
        self.surface.blit(self.image_bonus1, (520, 170))
        self.surface.blit(self.image_bonus2, (520, 220))
        self.surface.blit(self.image_life, (520, 270))

        self.surface.blit(plus30, (100, 175))
        self.surface.blit(plus20, (100, 225))
        self.surface.blit(plus10, (100, 275))
        self.surface.blit(minus100, (560, 175))
        self.surface.blit(plus100, (560, 225))
        self.surface.blit(plus1life, (560, 275))

        self.surface.blit(moving, (60, 375))
        self.surface.blit(space, (60, 435))
        self.surface.blit(lives, (60, 495))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if (event.type == QUIT or
                        (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    self.game_intro_screen()

    def game_over_screen(self):
        bigfont = pygame.font.SysFont("Arial", 75)
        smallfont = pygame.font.SysFont("Arial", 20)
        g_o = bigfont.render("GAME OVER", 1, options.RED)
        label = smallfont.render("Press Y to restart game, N to exit",
                                 1, options.YELLOW)
        score = smallfont.render("You finished with "
                                 "score: {}".format(self.score),
                                 1, options.YELLOW)
        self.surface.fill(options.BLACK)
        self.surface.blit(g_o, (100, 50))
        self.surface.blit(label, (100, 150))
        self.surface.blit(score, (100, 200))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_y:
                    Screens()
                    SpaceInvadersGame()
                if (event.type == QUIT or
                        (event.type == KEYDOWN and event.key == K_ESCAPE) or
                        (event.type == KEYDOWN and event.key == K_n)):
                    exit()


def check_collision(object1_x, object1_y, object2_x, object2_y):
    return (
        (object1_x > object2_x) and (object1_x < object2_x + 35) and
        (object1_y > object2_y) and (object1_y < object2_y + 35)
    )

options = Options()
screens = Screens()
if __name__ == '__main__':
    Screens()
    SpaceInvadersGame()
