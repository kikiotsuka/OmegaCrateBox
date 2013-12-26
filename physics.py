import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screenwidth = 800
screenheight = 600

class Player:
	def __init__(self):
		global screenwidth, screenheight
		self.rectangle = Rect(screenwidth / 2, screenheight - 50, 50, 50)
		self.doublejump = True
		self.gravity = 2
		self.xvel = 4
		self.yvel = 0
		self.jumpconst = 30
		self.direction = 'none'

	def move(self, l, r, u, d, time):
		global screenwidth, screenheight
		if time < 500:
			self.xvel = 4
		elif time < 725:
			self.xvel = 6
		elif time < 1000:
			self.xvel = 8
		else:
			self.xvel = 10
		tmpcoord = self.rectangle.x
		self.rectangle.x += self.xvel * r
		self.rectangle.x -= self.xvel * l
		if self.rectangle.x < tmpcoord:
			self.direction = 'left'
		elif self.rectangle.x > tmpcoord:
			self.direction = 'right'
		else:
			self.direction = 'none'
		self.yvel -= self.gravity
		self.rectangle.y -= self.yvel
		if self.rectangle.left < 0:
			self.rectangle.x = 0
		if self.rectangle.right > screenwidth:
			self.rectangle.x = screenwidth - self.rectangle.width
		if self.rectangle.bottom > screenheight:
			self.rectangle.y = screenheight - self.rectangle.height
			self.yvel = 0
			self.doublejump = True

	def startjump(self):
		global screenheight
		if self.rectangle.bottom == screenheight:
			self.yvel = self.jumpconst
		elif self.doublejump:
			self.yvel = self.jumpconst
			self.doublejump = False

	def endjump(self):
		if self.yvel > 10:
			self.yvel = 10

	def getrect(self):
		return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)


windowSurfaceObj = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Physics Test')

player = Player()
left=right=up=down=0
time = 0
doubletime = 0
timeconst = 1
while True:
	windowSurfaceObj.fill(pygame.Color(255, 255, 255))
	player.move(left, right, up, down, time)
	pygame.draw.rect(windowSurfaceObj, pygame.Color(0, 0, 255), player.getrect())

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				left += timeconst
			elif event.key in (K_RIGHT, K_d):
				right += timeconst
			elif event.key in (K_UP, K_w):
				up += timeconst
				player.startjump()
			elif event.key == K_q:
				pygame.quit()
				sys.exit()
		elif event.type == KEYUP:
			if event.key in (K_LEFT, K_a):
				left = 0
			elif event.key in (K_RIGHT, K_d):
				right = 0
			elif event.key in (K_UP, K_w):
				up = 0
				player.endjump()
	time += 30
	if left != 0 and right != 0:
		time = 0


	pygame.display.update()
	fpsClock.tick(30)