import pygame
import math

def can_see_player(enemypos, playerpos, plataforms, sight_radius):
    dx = playerpos[0] - enemypos[0]
    dy = playerpos[1] - enemypos[1]
    distance = math.hypot(dx, dy)

    if distance > sight_radius:
        return False

    steps = int(distance)
    for step in range(steps):
        x = enemypos[0] + dx * step / steps
        y = enemypos[1] + dy * step / steps

        for plataform in plataforms:
            if plataform.collidepoint((x, y)):
                return False

    return True