import pygame

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Into the Byline')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

res0 = (896, 504)
res1 = (1280, 720)
res2 = (1920, 1080)
resolution = res1
screen = pygame.display.set_mode(resolution)

home_screen = pygame.image.load('assets/home_screen.png')
home_screen = pygame.transform.scale(home_screen, resolution)

home_screen_sound = pygame.mixer.Sound('assets/Main Sound.mp3')
# Volume: 0 ~ 0.3
home_screen_sound.set_volume(0.3)

# Home Screen
HS = True
while HS:
    home_screen_sound.play(loops=-1)
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

not_scared_background = pygame.image.load('assets/not_scared.png')
not_scared_background = pygame.transform.scale(not_scared_background, resolution)

is_scared = False
GAME = True
while GAME:
    clock.tick(60)

    screen.fill((0, 0, 0))
    screen.blit(home_screen, (0, 0))

    if not is_scared:
        screen.blit(not_scared_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    pygame.display.update()