import pygame
import random

def roam(enemy):
	if enemy.seeingplayer == True or enemy.roaming == False:
		return

	if enemy.tomove > 0:
		enemy.move()
		return

	enemy.timer -= 1
	if enemy.timer <= 0:
		action = random.choice([1,2])

		if action == 1:
			enemy.direction = change_direction()
		elif action == 2:
			enemy.move()

		enemy.timer = enemy.max_timer
		enemy.tomove = enemy.max_tomove


def change_direction():
	new_direction = random.choice([(1,0), (-1,0)])
	return new_direction
