import pygame
from pygame.locals import *
from pygame import mixer

flash_sound = mixer.Sound("assets/sounds/flash_sound.mp3")

class Flash(pygame.sprite.Sprite):
    def __init__(self, win: pygame.Surface, color: pygame.Color, left: int, right: int, up: int, down: int, num_flashs: int):
        pygame.sprite.Sprite.__init__(self)

        self.window = win
        self.color = color

        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.num_flashs = num_flashs

    def active(self, event: pygame.event, maze_map: dict, x: int, y: int, flashs_list: list):
        trigger = False
        if event.type == KEYDOWN:
            if event.key in [self.left, self.right, self.up, self.down]:
                trigger = True
                directions = {
                    self.left: ["W", [-1, 0]],
                    self.right: ["E", [1, 0]],
                    self.up: ["N", [0, -1]],
                    self.down: ["S", [0, 1]]
                }
                flash_sound.play()
                possible_directions = maze_map[(y + 1, x + 1)]

                flash_list = [(x, y)]
                direction = directions[event.key][0]
                movement = directions[event.key][1]
                print(direction)
                while possible_directions[direction]:  # enquanto a direção estiver aberta
                    x += movement[0]
                    y += movement[1]
                    flash_list.append((x, y))
                    possible_directions = maze_map[(y + 1, x + 1)]

                flashs_list.append(flash_list)

        if len(flashs_list) > 1 and str(flashs_list[-1])[1:-1] in str(flashs_list[:-1])[1:-1]:
            flashs_list.pop(-1)
        elif len(flashs_list) > self.num_flashs:
            flashs_list.pop(0)

        return flashs_list, trigger
