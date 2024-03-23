import math
import typing

from typing import Tuple


class Hit:
    def __init__(self, x, y, dir, dist):
        self.x = x
        self.y = y
        self.dir = dir
        self.dist = dist


def point_touching_level(x, y, level) -> bool:
    return level[math.floor(y)][math.floor(x)]


def box_touching_level(x, y, size, level) -> bool:
    return (point_touching_level(x + size, y + size, level) or
            point_touching_level(x - size, y + size, level) or
            point_touching_level(x - size, y - size, level) or
            point_touching_level(x + size, y - size, level)
            )


def move_point(x, y, dir, amount) -> Tuple[int, int]:
    return (math.sin(math.radians(dir)) * amount + x,
            math.cos(math.radians(dir)) * amount + y)


def cast_ray(x, y, dir, level) -> Hit:
    cx = x
    cy = y
    dist = 0
    while dist < 20 and not box_touching_level(cx, cy, 0.1, level):
        p = move_point(cx, cy, dir, 0.07)
        cx = p[0]
        cy = p[1]
        dist += 0.07
    while box_touching_level(cx, cy, 0.1, level):
        p = move_point(cx, cy, dir, -0.01)
        cx = p[0]
        cy = p[1]
        dist += -0.01

    return Hit(cx, cy, dir, dist)


def cast_multiple_rays(x, y, dir, fov, amount, level):
    rays = []

    d = dir - fov / 2
    while d <= dir + fov / 2:
        rays.append(cast_ray(x, y, d, level))
        d += fov / amount

    return rays


class Column:
    def __init__(self, dist, height, color=None):
        self.dist = dist
        self.height = height
        self.color = color


def rays_to_columns(rays: typing.Iterable[Hit], wall_height) -> typing.Iterable[Column]:
    columns = []
    for ray in rays:
        dist = ray.dist
        height = wall_height / dist
        columns.append(Column(ray.dist, height))
    return columns
