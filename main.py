import pygame
import utils
import maze_generator

from pygame.locals import *
from sys import exit
from player import Player
from flash import Flash
from boxes import Boxes
from inventory import Inventory


RESOLUTION = (1280, 720)
FPS = 60

maze_position = (57.5, 57.5)
side_maze = 600
num_pixels = 20
side_pixel = side_maze / num_pixels

flashs_list = [[]]
glowsticks_list = [[]]
num_flashs = 7


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Into the Byline")

        self.clock = pygame.time.Clock()

        self.icon = pygame.image.load('assets/icon/icon.png')
        pygame.display.set_icon(self.icon)

        self.map_id = "home_screen"
        self.display = utils.load_display(self.map_id, RESOLUTION)

        self.music = "None :)"
        self.font = pygame.font.Font("assets/fonts/Pixelation.ttf", 25)

        left_player, right_player, up_player, down_player = K_a, K_d, K_w, K_s
        self.player = Player(self.screen, left_player, right_player, up_player, down_player, num_pixels, side_pixel)

        left_flash, right_flash, up_flash, down_flash = K_LEFT, K_RIGHT, K_UP, K_DOWN
        self.flash = Flash(self.screen, Color(0, 0, 255), left_flash, right_flash, up_flash, down_flash, False, False, num_flashs)

        self.maze_map = maze_generator.get_mazemap()
        self.maze = maze_generator.Maze(57.5, 57.5, 600, 600, self.maze_map)

        self.boxes = Boxes()
        self.boxes.generate_boxes(self.maze_map)

        self.inventory = Inventory(self.boxes, self.player, self.flash, self.maze_map)

    #1 glowstick 2# radar 3# bateria
    def run(self):
        global flashs_list
        global glowsticks_list

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                    if self.map_id == "background":
                        self.boxes.get_box(event, flashs_list, self.player)
                        self.player.control(event, self.maze_map)

                        self.inventory.use_item(event)

                        flashs_list = self.flash.active(event, self.maze_map, self.player.position, flashs_list)
                        glowsticks_list = self.flash.get_glowsticks_list()

                    if self.map_id == "home_screen":
                        if event.key == pygame.K_1:
                            self.map_id = "background"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                            self.music = utils.set_music(self.map_id)
                            self.screen.fill((0, 0, 0))
                            pygame.display.update()
                            self.music.play()
                            pygame.time.delay(5000)
                            self.player.spawn()
                        if event.key == pygame.K_2:
                            self.map_id = "config"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                            self.music = utils.set_music(self.map_id)
                        if event.key == pygame.K_3:
                            pygame.quit()
                            exit()

                    cells = []

                    for flash_list in flashs_list:
                        for column, line in flash_list:
                            cells.append((line + 1, column + 1))

                    if len(glowsticks_list) > 0:
                        for glowstick_position in glowsticks_list:
                            for column, line in glowstick_position:
                                cells.append((line + 1, column + 1))

                    cells.append(self.player.position_maze)

            if self.map_id in ["home_screen", "config"]:
                self.screen.blit(self.display, (0, 0))
                pygame.display.update()
            else:
                self.screen.blit(self.display, (0, 0))
                text_k = self.font.render(f"{self.player.inventory['k']}", False, (255, 255, 255))
                text_g = self.font.render(f"{self.player.inventory['g']}", False, (255, 255, 255))
                text_r = self.font.render(f"{self.player.inventory['r']}", False, (255, 255, 255))
                text_s = self.font.render(f"{self.player.inventory['s']}", False, (255, 255, 255))
                self.screen.blit(text_k, (800, 116))
                self.screen.blit(text_g, (800, 251))
                self.screen.blit(text_r, (800, 386))
                self.screen.blit(text_s, (800, 521))
                #print(pygame.mouse.get_pos())
                self.boxes.draw(self.screen, self.maze, flashs_list)
                self.player.draw(maze_position)

                self.maze.display_maze_cells(self.screen, cells)

                pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
