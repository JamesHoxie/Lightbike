import pygame
import time
import random
import copy

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 600
BLOCK_SIZE = 10
FPS = 30
FONT = pygame.font.SysFont(None, 25)
CLOCK = pygame.time.Clock()

global p1_wins
global p2_wins
p1_wins = False 
p2_wins = False

def pause():
	paused = True
	message_to_screen("Paused, Press C to continue or Q to quit.", white)
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		CLOCK.tick(5)

def text_objects(text, color):
	text_surface = FONT.render(text, True, color)
	return text_surface, text_surface.get_rect()

def message_to_screen(msg, color):
	text_surface, text_rect = text_objects(msg, color)
	text_rect.center = (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/3)
	game_display.blit(text_surface, text_rect)

def move(light_bike, color):
	for XnY in light_bike:
		game_display.fill(color, rect=[XnY[0], XnY[1], BLOCK_SIZE, BLOCK_SIZE])

def check_for_collisions(light_bikes, light_trails, lead_x_1, lead_y_1, lead_x_2, lead_y_2):
	first_iteration = True
	global p1_wins
	global p2_wins

	for light_bike in light_bikes:
		light_bike_front = light_bike[-1]
		if light_bike_front in light_trails:
			if first_iteration:
				p2_wins = True
			else:
				p1_wins = True

			return True

		else:
			if lead_x_1 > DISPLAY_WIDTH or lead_x_1 < 0 or lead_y_1 > DISPLAY_HEIGHT - 210 or lead_y_1 < 0:
				p2_wins = True
				return True

			if lead_x_2 > DISPLAY_WIDTH or lead_x_2 < 0 or lead_y_2 > DISPLAY_HEIGHT - 210 or lead_y_2 < 0:
				p1_wins = True
				return True

		first_iteration = False

	return False

def game_loop():
	global p1_wins
	global p2_wins
	p1_wins = False 
	p2_wins = False
	game_exit = False
	game_over = False
	lead_x_1 = 300
	lead_y_1 = 300
	lead_x_change_1 = 0
	lead_y_change_1 = -10
	lead_x_2 = 500
	lead_y_2 = 500
	lead_x_change_2 = 0
	lead_y_change_2 = -10
	light_bike_1_front = [lead_x_1, lead_y_1]
	light_bike_1 = [light_bike_1_front]
	light_bike_2_front = [lead_x_2, lead_y_2]
	light_bike_2 = [light_bike_2_front]
	light_bikes = [light_bike_1, light_bike_2]
	light_trails = []

	while not game_exit:
		if p1_wins:
			message_to_screen("P1 wins!, press C to play again or Q to quit", red)

		elif p2_wins:
			message_to_screen("P2 wins!, press C to play again or Q to quit", red)

		pygame.display.update()	

		while game_over == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_exit = True
					game_over = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						game_exit = True
						game_over = False
					if event.key == pygame.K_c:
						game_loop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
			if event.type == pygame.KEYDOWN:
				#p1 inputs
				if event.key == pygame.K_a:
					lead_x_change_1 = -BLOCK_SIZE
					lead_y_change_1 = 0
				elif event.key == pygame.K_d:
					lead_x_change_1 = BLOCK_SIZE
					lead_y_change_1 = 0
				elif event.key == pygame.K_w:
					lead_y_change_1 = -BLOCK_SIZE
					lead_x_change_1 = 0
				elif event.key == pygame.K_s:
					lead_y_change_1 = BLOCK_SIZE
					lead_x_change_1 = 0

				#p2 inputs	
				if event.key == pygame.K_LEFT:
					lead_x_change_2 = -BLOCK_SIZE
					lead_y_change_2 = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change_2 = BLOCK_SIZE
					lead_y_change_2 = 0
				elif event.key == pygame.K_UP:
					lead_y_change_2 = -BLOCK_SIZE
					lead_x_change_2 = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change_2 = BLOCK_SIZE
					lead_x_change_2 = 0

				if event.key == pygame.K_p:
					pause()


		lead_x_1 += lead_x_change_1
		lead_y_1 += lead_y_change_1
		lead_x_2 += lead_x_change_2
		lead_y_2 += lead_y_change_2
		game_display.fill(black)	

		if lead_x_change_1 != 0 or lead_y_change_1 != 0:
			light_bike_1_front = [lead_x_1, lead_y_1]
			light_bike_1.append(light_bike_1_front)
			

		if lead_x_change_2 != 0 or lead_y_change_2 != 0:
			light_bike_2_front = [lead_x_2, lead_y_2]
			light_bike_2.append(light_bike_2_front)
				


		move(light_bike_1, green)
		move(light_bike_2, blue)
		pygame.display.update()


		game_over = check_for_collisions(light_bikes, light_trails, lead_x_1, lead_y_1, lead_x_2, lead_y_2)

		light_trails.append(light_bike_1_front)
		light_trails.append(light_bike_2_front)

		CLOCK.tick(FPS)

	#unitialize pygame
	pygame.quit()
	#exit out of python
	quit()

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_WIDTH))
pygame.display.set_caption('Python Lightbike')

game_loop()
