import pygame

from pygame.locals import *
from monster import Monster
from boxes import Boxes
from pygame.font import Font
import os
import requests
from datetime import datetime
from time import time


def load_display(map_id, resolution):
    if map_id == "config":
        display = pygame.Surface((1280, 720))
        display.fill("Red")
    else:
        display = pygame.image.load(f"assets/backgrounds/{map_id}.png")
        display = pygame.transform.scale(display, resolution)
    return display


def draw(m, win, color, size, pos):
    sqr = pygame.Surface(size)
    sqr.fill(color)

    pixel_xy = cell_to_pixels(m, pos)
    cell_rect = pygame.Rect(pixel_xy, (m.cell_grid_width, m.cell_grid_width))
    win.blit(sqr, (cell_rect.centerx - 7, cell_rect.centery - 7))


def get_monster_draw(m, win, monster_list):
    for i in range(len(monster_list)):
        if i == 0 and monster_list[0][0]:
            draw(m, win, "#F40000", (14, 14), monster_list[i][1])
        elif i == 1 and monster_list[1][0]:
            draw(m, win, "#F44E3F", (14, 14), monster_list[i][1])


def active_radar(win, maze, billy_bob_position: tuple):

    if billy_bob_position != ((-1, -1), (-1, -1)):
        billy, bob = billy_bob_position
        x_billy, y_billy = cell_to_pixels(maze, billy)
        x_bob, y_bob = cell_to_pixels(maze, bob)
        pygame.draw.rect(win, (255, 153, 51),
                         (x_billy + 8, y_billy + 8, 14, 14))
        pygame.draw.rect(win, (255, 153, 51), (x_bob + 8, y_bob + 8, 14, 14))

    '''
    for i in range(len(monster_list)):
        if monster_list[i][1] == 0:
            draw(m, win, "#F40000", (14, 14), monster_list[i][0])
        if monster_list[i][1] == 1:
            draw(m, win, "#F44E3F", (14, 14), monster_list[i][0])
    '''


def show_battery(win, battery_trigger):
    surface_battery = pygame.Surface((115, 110), pygame.SRCALPHA)
    if battery_trigger:
        surface_battery.fill((255, 255, 255, 50))
    else:
        surface_battery.fill((0, 0, 0, 0))
    win.blit(surface_battery, (720, 450))


def remove_least_monster(monster_list):
    index = []
    for i in range(len(monster_list)):
        if monster_list[i][0]:
            if monster_list[i][2] > 0:
                monster_list[i][2] -= 1
            else:
                monster_list[i][0] = False


def set_music(map_id):
    musics = {"background": "entering_the_maze"}

    music_text = musics[map_id]
    music = pygame.mixer.Sound(f'assets/sounds/{music_text}.mp3')
    music.set_volume(0.3)

    return music


def cell_to_pixels(maze, cell_position):
    pos_x = cell_position[0]
    pos_y = cell_position[1]

    pixel_x = maze.initial_point_x + ((pos_y - 1) * maze.cell_grid_width)
    pixel_y = maze.initial_point_y + ((pos_x - 1) * maze.cell_grid_width)

    new_pos = (pixel_x, pixel_y)

    return new_pos


def update_qty_items(font, inventory):
    text_k = font.render(f"{inventory['k']}", False, (255, 255, 255))
    text_g = font.render(f"{inventory['g']}", False, (255, 255, 255))
    text_r = font.render(f"{inventory['r']}", False, (255, 255, 255))
    text_s = font.render(f"{inventory['s']}", False, (255, 255, 255))
    return [text_k, text_g, text_r, text_s]


def draw_qty_items(screen, texts):
    pos_y = 116

    for text in texts:
        screen.blit(text, (800, pos_y))
        pos_y += 135


def draw_item_found(screen, font: Font, item, rect_item):
    text_item_found = font.render(f"{item}", False, (255, 255, 255))
    text_item_support = font.render(f"Found!", False, (255, 255, 255))
    text_item_found_rect = text_item_found.get_rect(midbottom=rect_item.center)
    text_item_support_rect = text_item_support.get_rect(
        midtop=rect_item.center)
    screen.blit(text_item_found, text_item_found_rect)
    screen.blit(text_item_support, text_item_support_rect)


def draw_no_item(screen, font: Font, rect_item):
    text_no_item = font.render(f". . .", False, (255, 255, 255))
    text_no_item_rect = text_no_item.get_rect(center=rect_item.center)
    screen.blit(text_no_item, text_no_item_rect)


API_URL = "https://into-the-byline-web.vercel.app/api"


def get_nickname() -> str:
    data_path = os.path.dirname(
        os.path.abspath(__file__)) + "/data/nickname.txt"
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            nickname = f.read()

        return nickname

    nickname = input("Insert your nickname: ")
    res = requests.post(f"{API_URL}/users",
                        json={"nickname": nickname})

    if res.status_code == 400:
        print("Nickname already exists!")
        return get_nickname()

    print("Nickname saved!")
    return nickname


def send_score(
        score: int,
        used_flashs: int,
        used_items: int,
        monsters_appeared: int,
        start_time: float):

    nickname = get_nickname()
    date = datetime.now().strftime("%Y-%m-%d")

    total_time = time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    milliseconds = int((total_time - int(total_time)) * 1000)

    formatted_time = f"{minutes}:{seconds:02}:{milliseconds:03}"

    data = {
        "nickname": nickname,
        "points": score,
        "total_time": formatted_time,
        "used_flashs": used_flashs,
        "used_items": used_items,
        "monsters_appearances": monsters_appeared,
        "date": date
    }

    requests.post(f"{API_URL}/leadboard",
                  json=data)
