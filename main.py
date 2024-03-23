import typing

import pygame as pg

from raycaster import *

WIDTH = 700
HEIGHT = 700
TARGET_FPS = 60

fps = 0
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
dt = 0
running = True

pg.display.set_caption("3D Raycaster")

px = 1.5
py = 1.5
dir = 45

_ = False
W = True

level = [
    [W, W, W, W, W, W, W],
    [W, _, _, W, _, _, W],
    [W, _, W, _, _, W, W],
    [W, _, _, _, _, _, W],
    [W, _, _, _, W, _, W],
    [W, W, _, W, _, _, W],
    [W, _, _, _, _, _, W],
    [W, W, W, W, W, W, W]
]

rays = []
columns: typing.Iterable[Column] = []

TILE_SIZE = min(WIDTH, HEIGHT) / min(len(level), len(level[0]))

def move(direction, amount):
    global px, py

    cx = math.sin(math.radians(direction)) * amount * dt
    cy = math.cos(math.radians(direction)) * amount * dt

    px += cx
    if box_touching_level(px, py, 0.15, level):
        px -= cx
    py += cy
    if box_touching_level(px, py, 0.15, level):
        py -= cy
def handle_keys():
    global dir
    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        move(dir, 1)
    if keys[pg.K_DOWN]:
        move(dir, -1)
    if keys[pg.K_LEFT]:
        dir += 180 * dt
    if keys[pg.K_RIGHT]:
        dir += -180 * dt
def draw_ray(x, y, hit: Hit):
    pg.draw.line(screen, (255, 255, 255), (x * TILE_SIZE, y * TILE_SIZE), (hit.x * TILE_SIZE, hit.y * TILE_SIZE))

def draw_2d_debug():
    # Draw Level
    for x in range(0, len(level) - 1):
        for y in range(0, len(level[0]) - 1):
            if level[y][x]:
                pg.draw.rect(screen, (0, 255, 0),
                             pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw Player
    pg.draw.circle(screen, (255, 255, 0), (px * TILE_SIZE, py * TILE_SIZE), 10)
    pg.draw.line(screen, (255, 255, 0),
                 (px * TILE_SIZE, py * TILE_SIZE),
                 ((px + math.sin(math.radians(dir)) * 0.2) * TILE_SIZE,
                  (py + math.cos(math.radians(dir)) * 0.2) * TILE_SIZE))

    # Draw Rays
    for ray in rays:
        draw_ray(px, py, ray)

def update():
    global rays, columns
    handle_keys()
    rays = cast_multiple_rays(px, py, dir, 60, WIDTH * 0.1, level)

    columns = rays_to_columns(rays, 500)
def draw():
    screen.fill((0, 0, 0))

    for i in range(math.floor(HEIGHT / 2), HEIGHT):
        bright = (i / HEIGHT) * 255
        color = (bright, 0, 0)
        color = (max((min((255, color[0])), 0)),
                 max((min((255, color[1])), 0)),
                 max((min((255, color[2])), 0)))
        pg.draw.rect(screen, color, pg.Rect(0, HEIGHT, WIDTH, i))

    # draw_2d_debug()

    col_width = WIDTH / len(columns)
    i = len(columns)
    for col in columns:
        bright = max((min((
            -(col.dist * 50) + 230,
            240)
        ), 0))

        pg.draw.rect(screen, (bright, 0, 0), pg.Rect(
            i * col_width, HEIGHT / 2 - col.height / 2,
            col_width + 1, col.height))
        i -= 1


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(TARGET_FPS) / 1000
    fps = clock.get_fps()

    update()
    draw()
    pg.display.flip()
