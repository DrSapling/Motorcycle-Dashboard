import pygame
import time
import math

pygame.init()

windowSize = [800, 400]

window = pygame.display.set_mode((windowSize[0], windowSize[1]))
pygame.display.set_caption("dashboard")
pygame.mouse.set_visible(False)



def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def loadDark():
	global tlo
	global biegi
	global kierunkowskazy
	global swiatla
	global color_text
	global color_default
	global color_bg

	tlo = pygame.image.load('dark/bg.png')
	biegi = [
				pygame.image.load('dark/n.png'),
				pygame.image.load('dark/1.png'),
				pygame.image.load('dark/2.png'),
				pygame.image.load('dark/3.png'),
				pygame.image.load('dark/4.png'),
				pygame.image.load('dark/5.png')
			]
	kierunkowskazy = [
						 pygame.image.load('dark/turn_L.png'),
						 pygame.image.load('dark/turn_R.png')

					 ]
	swiatla = [
				  pygame.image.load('dark/postojowe.png'),
				  pygame.image.load('dark/drogowe.png'),
				  pygame.image.load('dark/dlugie.png')
			  ]
	color_text = (255, 255, 255)
	color_default = (51, 160, 52)
	color_bg = (50,50,50)


def loadBright():
	global tlo
	global biegi
	global kierunkowskazy
	global swiatla
	global color_text
	global color_default
	global color_bg

	tlo = pygame.image.load('bright/bg.png')
	biegi = [
				pygame.image.load('bright/n.png'),
				pygame.image.load('bright/1.png'),
				pygame.image.load('bright/2.png'),
				pygame.image.load('bright/3.png'),
				pygame.image.load('bright/4.png'),
				pygame.image.load('bright/5.png')
			]
	kierunkowskazy = [
						 pygame.image.load('bright/turn_L.png'),
						 pygame.image.load('bright/turn_R.png')

					 ]
	swiatla = [
				  pygame.image.load('bright/postojowe.png'),
				  pygame.image.load('bright/drogowe.png'),
				  pygame.image.load('bright/dlugie.png')
			  ]
	color_text = (0, 0, 0)
	color_default = (0, 0, 0)
	color_bg = (204,204,204)



FPS = 30
DELAY = 1000/FPS
key_pressed = False

font_Bold_35 = pygame.font.Font('UNVR67W.TTF', 35)
font_Normal_100 = pygame.font.Font('UNVR57W.TTF', 100)
font_Normal_30 = pygame.font.Font('UNVR57W.TTF', 30)


mode = "dark"

current_gear = 0
blinker_l = 0
blinker_r = 0
lights = [False, False, False]
gas_level = 100
speed = 0
ODO = 13000.0  # przejechane kilometry
ODO_wait_measure = 0
TRIP = 100.0  # mierzona
TRIP_wait_reset = 0
TRIP_wait_measure = 0

point_A = -0.44
point_B = -0.44




loadDark()

'''  START  '''
start = time.perf_counter()
run = True
while run:
	finish = time.perf_counter()
	pygame.time.delay(int(DELAY - round(finish-start, 3) * 1000))
	start = time.perf_counter()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			exit()

	keys = pygame.key.get_pressed()


	# Zmienia jasne/ciemne

	if keys[pygame.K_j]:
		loadBright()
		mode = "bright"
	elif keys[pygame.K_c]:
		loadDark()
		mode = "dark"



	# Tło 1 warstwa

	window.fill(color_bg)



	# Obroty

	if keys[pygame.K_e] and point_B < -0.44:
		point_B = round(point_B+0.04, 2)

	if keys[pygame.K_3] and point_B > -2.7:
		point_B = round(point_B-0.04, 2)

	pygame.draw.polygon(window, color_default, [((int(math.sin(point_A)*500)+400), (int(math.cos(point_A)*500)+200)),
												((int(math.sin(point_B)*500)+400), (int(math.cos(point_B)*500)+200)),
												(400,200)])



	# Paliwo

	if keys[pygame.K_q] and gas_level > 0:
		gas_level -= 60/FPS

	elif keys[pygame.K_1] and gas_level < 100:
		gas_level += 60/FPS
	
	if mode == "dark":
		pygame.draw.rect(window, (int(2.04*(100-gas_level)+51), int(1.6*gas_level), 52), (729, 195, 41, int(-1.66 * gas_level)))
	if mode == "bright":
		pygame.draw.rect(window, (0, 0, 0), (729, 195, 41, int(-1.66 * gas_level)))


	TextSurf, TextRect = text_objects(f'{int(gas_level)}%', font_Bold_35, color_text)
	TextRect.center = ((670), (60))
	window.blit(TextSurf, TextRect)



	# Tło 2 warstwa

	window.blit(tlo, (0, 0))



	# TRIP

	if keys[pygame.K_r]: # reset
		TRIP_wait_reset += 1
		if TRIP_wait_reset == 2*FPS:
			TRIP = 0.0

	if TRIP_wait_measure == FPS:
		TRIP += (speed/60)/60
		TRIP_wait_measure = 0
	else:
		TRIP_wait_measure += 1

	TextSurf, TextRect = text_objects(str(round(TRIP, 1)), font_Normal_30, color_text)
	window.blit(TextSurf, (65,44))



	# ODO

	if ODO_wait_measure == FPS:
		ODO += (speed/60)/60
		ODO_wait_measure = 0
	else:
		ODO_wait_measure += 1

	TextSurf, TextRect = text_objects(str(round(ODO, 1)), font_Normal_30, color_text)
	window.blit(TextSurf, (65,4))



	# Prędkość

	if keys[pygame.K_2]:
		speed += 1

	elif keys[pygame.K_w] and speed > 0:
		speed -= 1

	TextSurf, TextRect = text_objects(str(int(speed)), font_Normal_100, color_text)
	TextRect.center = ((400), (175))
	window.blit(TextSurf, TextRect)



	# Biegi

	if keys[pygame.K_UP] and current_gear == 0 and key_pressed == False:
		current_gear = 1

	if keys[pygame.K_DOWN] and current_gear == 0 and key_pressed == False:
		current_gear = 1

	elif keys[pygame.K_UP] and current_gear < 5 and key_pressed == False:
		current_gear += 1

	elif keys[pygame.K_DOWN] and current_gear > 1 and key_pressed == False:
		current_gear -= 1

	elif keys[pygame.K_n] and current_gear == 1 and key_pressed == False:
		current_gear = 0

	window.blit(biegi[current_gear], (593, 193))



	# Lewy Kierunkowskaz

	if keys[pygame.K_LEFT] and key_pressed == False:
		if blinker_l == 0:
			blinker_r = 0
			blinker_l = 1
		else:
			blinker_l = 0
	
		
	if blinker_l >= 1 and blinker_l < FPS/2:
		window.blit(kierunkowskazy[0], (3, 291))
		blinker_l += 1

	elif blinker_l >= FPS/2 and blinker_l < FPS:
		blinker_l += 1
		if blinker_l == FPS:
			blinker_l = 1



	# Prawy Kierunkowskaz

	if keys[pygame.K_RIGHT] and key_pressed == False:
		if blinker_r == 0:
			blinker_l = 0
			blinker_r = 1
		else:
			blinker_r = 0


	if blinker_r >= 1 and blinker_r < FPS/2:
		window.blit(kierunkowskazy[1], (696, 291))
		blinker_r += 1

	elif blinker_r >= FPS/2 and blinker_r < FPS:
		blinker_r += 1
		if blinker_r == FPS:
			blinker_r = 1



	# swiatla

	if keys[pygame.K_i] and key_pressed == False:
		if lights[0] == False:
			lights[0] = True
		else:
			lights[0] = False

	if keys[pygame.K_o] and key_pressed == False:
		if lights[1] == False:
			lights[1] = True
		else:
			lights[1] = False

	if keys[pygame.K_p] and key_pressed == False:
		if lights[2] == False:
			lights[2] = True
		else:
			lights[2] = False


	if lights[0] == True:
		window.blit(swiatla[0], (17, 110))

	if lights[1] == True:
		window.blit(swiatla[1], (28, 156))

	if lights[2] == True:
		window.blit(swiatla[2], (26, 211))



	# sprawdza, czy jakokolwiek z przycisków został wciśnięty

	if event.type == pygame.KEYUP:
		key_pressed = False

	else:
		key_pressed = True
	
	pygame.display.update()


pygame.quit()
exit()