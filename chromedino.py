#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import pygame
import os
import threading
import random

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Chrome Dino Runner')

Ico = pygame.image.load('assets/DinoWallpaper.png')
pygame.display.set_icon(Ico)

RUNNING = [pygame.image.load(os.path.join('assets/Dino', 'DinoRun1.png'
                                          )), pygame.image.load(os.path.join('assets/Dino',
                                                                             'DinoRun2.png'))]
JUMPING = pygame.image.load(os.path.join('assets/Dino', 'DinoJump.png'))
DUCKING = [pygame.image.load(os.path.join('assets/Dino', 'DinoDuck1.png'
                                          )), pygame.image.load(os.path.join('assets/Dino',
                                                                             'DinoDuck2.png'))]

SMALL_CACTUS = [pygame.image.load(os.path.join('assets/Cactus',
                                               'SmallCactus1.png')),
                pygame.image.load(os.path.join('assets/Cactus',
                                               'SmallCactus2.png')),
                pygame.image.load(os.path.join('assets/Cactus',
                                               'SmallCactus3.png'))]
LARGE_CACTUS = [pygame.image.load(os.path.join('assets/Cactus',
                                               'LargeCactus1.png')),
                pygame.image.load(os.path.join('assets/Cactus',
                                               'LargeCactus2.png')),
                pygame.image.load(os.path.join('assets/Cactus',
                                               'LargeCactus3.png'))]

BIRD = [pygame.image.load(os.path.join('assets/Bird', 'Bird1.png')),
        pygame.image.load(os.path.join('assets/Bird', 'Bird2.png'))]

CLOUD = pygame.image.load(os.path.join('assets/Other', 'Cloud.png'))

BG = pygame.image.load(os.path.join('assets/Other', 'Track.png'))

DEBUG = False


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput == 1 and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        # elif self.dino_jump and userInput == -1:
        #    self.jump_vel -= .8
        elif userInput == -1:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput == -1):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        if DEBUG: pygame.draw.rect(SCREEN, (0, 255, 0, 50), self.dino_rect)
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def info(self):
        return self.dino_rect.y


class Cloud:

    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            return False
        return True

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        if DEBUG: pygame.draw.rect(SCREEN, (255, 0, 0, 100), self.rect)


class SmallCactus(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        if DEBUG: pygame.draw.rect(SCREEN, (255, 0, 0, 100), self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    obstacles_timeout = 30
    obstacles_timeout_counter = obstacles_timeout

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            pass
            # game_speed += 1

        text = font.render('Points: ' + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((247, 247, 247))
        userInput = pygame.key.get_pressed()

        action = 0
        if userInput[pygame.K_UP]:
            action = 1

        player.draw(SCREEN)
        player.update(action)

        obstacles_timeout_counter -= 1

        if obstacles_timeout_counter <= 0:
            obstacles_timeout_counter = obstacles_timeout
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(LargeCactus(LARGE_CACTUS))  # obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


class Game:
    def __init__(self):
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles, SCREEN
        self.run = True
        self.clock = pygame.time.Clock()
        self.player = Dinosaur()
        self.cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        obstacles = []
        self.death_count = 0
        self.game_over = False
        self.obstacles_timeout_min = 25
        self.obstacles_timeout_max = 35
        self.obstacles_timeout_counter = 0
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def step(self, action, render=False, fps=36):
        global game_speed

        start = time.time()
        pygame.event.get()

        SCREEN.fill((247, 247, 247))
        userInput = round(action)
        self.player.draw(SCREEN)
        self.player.update(userInput)
        self.obstacles_timeout_counter -= 1

        if self.obstacles_timeout_counter <= 0:
            self.obstacles_timeout_counter = random.randint(self.obstacles_timeout_min,
                                                            self.obstacles_timeout_max) - round(game_speed / 10)
            if random.randint(0, 1) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 1) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 1) == 2:
                obstacles.append(LargeCactus(LARGE_CACTUS))
                # obstacles.append(Bird(BIRD))
            # print("made obstacle")

        rem_obs = None
        for obstacle in obstacles:
            # print(obstacle.rect.x)
            if not obstacle.update(): rem_obs = obstacle
            obstacle.draw(SCREEN)
            if self.player.dino_rect.colliderect(obstacle.rect):
                # pygame.time.delay(2000)
                self.death_count += 1
                self.game_over = True
                # menu(death_count)

        if rem_obs:
            obstacles.remove(rem_obs)

        self.background()
        self.cloud.draw(SCREEN)
        self.cloud.update()
        self.score()

        global points
        if points > 1000:
            pass
            # self.game_over = True

        if render:
            # time.sleep(max(1./40 - (time.time() - start), 0))
            self.clock.tick(fps)
            rect = pygame.Rect(100, 25, 100*action, 50)
            rectoutline = pygame.Rect(98, 25, 102, 50)
            pygame.draw.rect(SCREEN, (255, 0, 0), rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rectoutline, 2)


    # print("y", player.info())
        # print("deaths", death_count)
        pygame.display.update()

        #      [player y, distance to obstacle, height of obstacle]

        obstacle = None
        for obs in obstacles:
            if obs.rect.x > self.player.X_POS:
                obstacle = obs
                break

        if not obstacle:
            obstacle = LargeCactus(LARGE_CACTUS)
            obstacles.append(obstacle)
            self.obstacles_timeout_counter = random.randint(self.obstacles_timeout_min,
                                                            self.obstacles_timeout_max) - round(game_speed / 20)

        return [self.player.info(), obstacle.rect.x, obstacle.rect.y]

    def score(self):
        global points, game_speed
        points += 1
        if points % 100 == 0:
            pass
            # game_speed += 1

        text = self.font.render('Points: ' + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background(self):
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render('Press any Key to Start', True, (0, 0,
                                                                0))
        elif death_count > 0:
            text = font.render('Press any Key to Restart', True, (0, 0,
                                                                  0))
            score = font.render('Your Score: ' + str(points), True, (0,
                                                                     0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                                + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT
                                 // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


# t1 = threading.Thread(target=menu(death_count=0), daemon=True)
# t1.start()
if __name__ == '__main__':
    game = Game()
    while True:
        print(game.step(random.randint(0, 1)))
