import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screenwidth = 400
screenheight = 400

class Player:
	def __init__(self):
		global screenwidth, screenheight
		self.rectangle = Rect(screenwidth / 2, screenheight - 50, 50, 50)
		self.doublejump = True
		self.accel = 2
		self.gravity = 2
		self.defjumpvel = 20
		self.jumpvel = self.defjumpvel

	def move(self, l, r, u, d, time, timejump):
		global screenwidth, screenheight
		if time < 1000:
			speed = 4
		elif time < 1500:
			speed = 7
		elif time < 2000:
			speed = 8
		else:
			speed = 10
		if l:
			self.rectangle.x -= speed
			if self.rectangle.x < 0:
				self.rectangle.x = 0
		if r:
			self.rectangle.x += speed
			if self.rectangle.right > screenwidth:
				self.rectangle.x = screenwidth - self.rectangle.width
		if u:
			if self.rectangle.bottom < screenheight and self.doublejump:
				self.doublejump = False
				self.jumpvel = self.defjumpvel
			self.rectangle.y -= self.jumpvel
			self.jumpvel -= self.gravity
			if self.rectangle.bottom > screenheight:
				self.rectangle.y = screenheight - self.rectangle.height
				self.jumpvel = self.defjumpvel
				self.doublejump = True
		if not u and self.rectangle.bottom < screenheight:
			self.rectangle.y -= self.jumpvel
			self.jumpvel -= self.gravity


	def getrect(self):
		return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)


windowSurfaceObj = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Physics Test')

player = Player()
left=right=up=down=False
time = 0
doubletime = 0
while True:
	windowSurfaceObj.fill(pygame.Color(255, 255, 255))
	player.move(left, right, up, down, time, doubletime)
	pygame.draw.rect(windowSurfaceObj, pygame.Color(0, 0, 255), player.getrect())

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				left = True
				time = 0
			elif event.key in (K_RIGHT, K_d):
				right = True
				time = 0
			elif event.key in (K_UP, K_w):
				up = True
			elif event.key == K_q:
				pygame.quit()
				sys.exit()
		elif event.type == KEYUP:
			if event.key in (K_LEFT, K_a):
				left = False
			elif event.key in (K_RIGHT, K_d):
				right = False
			elif event.key in (K_UP, K_w):
				up = False
	if left and not right or not left and right:
		time += 30
	if up:
		doubletime += 30


	pygame.display.update()
	fpsClock.tick(30)