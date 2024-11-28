import pygame
import math

def can_see_player(enemypos, playerpos, plataforms, sight_radius):
	dx = playerpos[0] - enemypos[0]
	dy = playerpos[1] - enemypos[1]
	distance = math.hypot(dx, dy)

	#ver a mesma função em enemy5_0.py

	if distance > sight_radius:
		return False

	for plataform in plataforms:
		if plataform.clipline(player.rect.center, playerpos):
			return False

	return True