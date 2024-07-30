import dis
import random
import pygame
from pygame.locals import *
import maze_generator
from player import Player
from flash import Flash
import monster

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Into the Byline')
icon = pygame.image.load('assets/icon/icon.png')
pygame.display.set_icon(icon)

RESOLUTION = (1280, 720)
screen = pygame.display.set_mode(RESOLUTION)

home_screen = pygame.image.load('assets/backgrounds/home_screen.png')
home_screen = pygame.transform.scale(home_screen, RESOLUTION)

entering_maze = pygame.mixer.Sound("assets/sounds/entering_the_maze.mp3")
attack = pygame.mixer.Sound("assets/sounds/attack.mp3")

# In game variables
flashs_list = [[]]
num_flashs = 7
'''
monster_steps = 5
monster_pos = (random.randint(1, 20), random.randint(1, 20))
'''

# Home Screen
HS = True
while HS:
    clock.tick(60)

    screen.fill((0, 0, 0))
    screen.blit(home_screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_3:
                pygame.quit()
                exit()
            elif event.key == pygame.K_1:
                HS = False
    
    pygame.display.update()

background = pygame.image.load('assets/backgrounds/background.png')
background = pygame.transform.scale(background, RESOLUTION)

maze_map = maze_generator.get_mazemap()
width_maze, num_pixels = 600, 20

print(maze_map)

x, y, width, height, color = 1, 1, 10, 10, (33, 179, 76)
left, right, up, down = K_a, K_d, K_w, K_s
player = Player(x, y, screen, width, height, color, left, right, up, down, width_maze, num_pixels)
player.spawn(num_pixels)

flash = Flash(screen, Color(0, 0, 255), K_LEFT, K_RIGHT, K_UP, K_DOWN, num_flashs)

is_scared = False

screen.fill((0, 0, 0))
pygame.display.update()
entering_maze.play()
pygame.time.delay(5000)
screen.blit(background, (0, 0))
pygame.display.update()

GAME = True
while GAME:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            pygame.display.update()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        x, y = player.control(event, maze_map)
        flashs_list, trigger = flash.active(event, maze_map, x, y, flashs_list)
        '''
        if trigger:
            try:
                path = monster.solve_path(monster_pos, (x + 1, y + 1), maze_map)
                for i in range(monster_steps):
                    monster_pos = path[monster_pos]
                print(path[monster_pos])
            except:
                print("Dead Screen") 
        '''

    if not is_scared:
        # 605 x 605
        rect = maze_generator.Maze(57.5, 57.5, 600, 600)
        maze_generator.maze_generator(screen, rect.rect, maze_map)

    for flash_list in flashs_list:
        for x_maze, y_maze in flash_list:
            pygame.display.update((x_maze * 30 + 57.5, y_maze * 30 + 57.5, 30, 30))

    player.draw(57.5, 57.5)
    #print(pygame.mouse.get_pos())
    #print(x, y)
