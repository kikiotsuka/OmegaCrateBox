import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()
fpsClock = pygame.time.Clock()

screenwidth = 1000
screenheight = 750

"""
Types of guns
	pistol
	dual pistol
	revolver
	shotgun
	machine gun
	gatling gun
	laser
	missilelauncher
	sword
"""

class Bullet:
	def __init__(self, x, y, xvel, yvel):
		self.x = x
		self.y = y
		self.xvel = xvel
		self.yvel = yvel

	def move(self):
		self.x += self.xvel
		self.y += self.yvel

class Gun(object):
	def __init__(self):
		self.type = None
		self.damage = 5
		self.reloadtime = None
		self.reloadtimer = None
		self.canfire = True
		self.knockback = 0

class Pistol(Gun):
	def __init__(self):
		super(Pistol, self).__init__()
		self.reloadtime = 1000
		self.reloadtimer = 1000
		self.type = 'Pistol'

	def fire(self):
		if self.reloadtimer >= self.reloadtime:
			self.canfire = False
			self.reloadtimer = 0
			return True
		return False

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			return [Bullet(x, y, -13, 0)]
		return [Bullet(x, y, 13, 0)]

class DualPistol(Pistol):
	def __init__(self):
		super(DualPistol, self).__init__()
		self.type = 'DualPistol'

	def bulletfire(self, x, y, direction):
		if direction == 'right':
			return [Bullet(x, y, 13, 0), Bullet(x - 30, y, -13, 0)]
		return [Bullet(x + 30, y, 13, 0), Bullet(x, y, -13, 0)]

class Revolver(Pistol):
	def __init__(self):
		super(Revolver, self).__init__()
		self.type = 'Revolver'
		self.reloadtime = 1700
		self.reloadtimer = 1700
		self.damage = 8

class Shotgun(Pistol):
	def __init__(self):
		super(Shotgun, self).__init__()
		self.type = 'Shotgun'
		self.reloadtime = 2500
		self.reloadtimer = 2500
		self.damage = 7
		self.knockback = 5

	def bulletfire(self, x, y, direction):
		if direction == 'right':
			vel = 17
		else:
			vel = -17
		tmplist = []
		for i in range(randint(8, 13)):
			tmplist.append(Bullet(x, y, vel, randint(-10, 3)))
		return tmplist

class GunBox:
	def __init__(self):
		self.size = 15
		while True:
			rect = collisionboxes[randint(0, len(collisionboxes) - 3)]
			self.x = randint(rect.left, rect.right - self.size)
			self.y = rect.top - self.size
			self.rectangle = Rect(self.x, self.y, self.size, self.size)
			if not self.rectangle.colliderect(player.rectangle):
				break

class Player:
	def __init__(self):
		size = 30
		self.rectangle = Rect(screenwidth / 2 - size / 2, screenheight / 2, size, size)
		self.jumpcount = 0
		self.gravity = .8
		self.xvel = 3
		self.yvel = 0
		self.jumpconst = 20
		self.direction = 'right'
		self.time = 0
		self.onground = False
		self.weapon = Pistol()
		self.score = 0
		self.knockback = 0
		self.friction = .5
		self.justfired = False

	def fire(self):
		global bulletlist
		if self.weapon.fire():
			if self.direction == 'right':
				b = self.weapon.bulletfire(self.rectangle.right, self.rectangle.centery, self.direction)
			else:
				b = self.weapon.bulletfire(self.rectangle.left, self.rectangle.centery, self.direction)
			for bullets in b:
				bulletlist.append(bullets)
			self.justfired = True
			self.knockback = self.weapon.knockback

	def move(self, l, r, u, d):
		if self.time < 500: self.xvel = 3
		elif self.time < 750: self.xvel = 4
		elif self.time < 1000: self.xvel = 6
		else: self.xvel = 9
		self.time += 25
		tmpcoord = self.rectangle.x
		tmpcenter = self.rectangle.center
		if r: 
			self.rectangle.x += self.xvel
		if l: 
			self.rectangle.x -= self.xvel
		if self.rectangle.x < tmpcoord:
			if self.direction == 'right':
				self.time = 0
			self.direction = 'left'
		elif self.rectangle.x > tmpcoord:
			if self.direction == 'left':
				self.time = 0
			self.direction = 'right'
		else:
			self.time = 0
		if self.justfired:
			self.time = 0
			#friction thing
			if self.direction == 'right':
				self.rectangle.x -= self.knockback
			else:
				self.rectangle.x += self.knockback
			self.knockback -= self.friction
		if self.knockback < 0:
			self.knockback = 0
			self.justfired = False
		self.yvel -= self.gravity
		self.rectangle.y -= self.yvel
		if self.rectangle.left < 0:
			self.rectangle.x = 0
		if self.rectangle.right > screenwidth:
			self.rectangle.x = screenwidth - self.rectangle.width
		if self.rectangle.bottom > screenheight:
			self.rectangle.y = screenheight - self.rectangle.height
			self.yvel = 0
			self.jumpcount = 0
			self.onground = True
		if self.rectangle.top < 0:
			self.rectangle.y = 0
			self.yvel = 0
		for box in collisionboxes:
			if self.rectangle.colliderect(box):
				b = box.bottom - self.rectangle.y
				t = self.rectangle.bottom - box.y
				l = self.rectangle.right - box.x
				r = box.right - self.rectangle.x
				if t < b and t < l and t < r: #top
					self.rectangle.bottom = box.top
					self.yvel = 0
					self.onground = True
					self.jumpcount = 0
				if b < t and b < l and b < r: #bottom
					self.rectangle.top = box.bottom
					self.yvel = 0
				if l < r and l < t and l < b: #left
					self.rectangle.right = box.left
					self.time = 0
				if r < l and r < t and r < b: #right
					self.rectangle.left = box.right
					self.time = 0
		if abs(self.yvel) != self.gravity and self.yvel != 0:
			self.onground = False

	def startjump(self):
		if self.onground:
			self.yvel = self.jumpconst
			self.onground = False
		elif self.jumpcount < 0: #player can jump n + 1 times
			self.yvel = self.jumpconst
			self.jumpcount += 1

	def endjump(self):
		if self.yvel > 10:
			self.yvel = 10

	def getrect(self):
		return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)


windowSurfaceObj = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Physics Test')

player = Player()
left=right=up=down=False
timeconst = 1
collisionboxes = []
height = 25
collisionboxes.append(Rect(0, screenheight / 2 - height / 2, screenwidth / 5, height))
collisionboxes.append(Rect(screenwidth - screenwidth / 5, screenheight / 2 - height / 2, screenwidth / 5, height))
collisionboxes.append(Rect(screenwidth / 5, screenheight / 4 - height / 2, screenwidth * 3 / 5, height))
collisionboxes.append(Rect(screenwidth / 5, screenheight * 3 / 4 - height / 2, screenwidth * 3 / 5, height))
tmpconst = 2.0 / 7.0
collisionboxes.append(Rect(0, screenheight - height, screenwidth * tmpconst, height))
collisionboxes.append(Rect(screenwidth - screenwidth * tmpconst, screenheight - height, screenwidth * tmpconst, height))
tmpconst = 3.0 / 7.0
collisionboxes.append(Rect(0, 0, screenwidth * tmpconst, height))
collisionboxes.append(Rect(screenwidth - screenwidth * tmpconst, 0, screenwidth * tmpconst, height))
space = False
bulletlist = []
gunbox = GunBox()
#weaponlist = ['pistol', 'dualpistol', 'revolver', 'shotgun', 'machinegun', 'gatlinggun', 'laser', 'sword']
weaponlist = [Pistol(), DualPistol(), Revolver(), Shotgun()]
while True:
	windowSurfaceObj.fill(pygame.Color(255, 255, 255))
	for index, bullet in enumerate(bulletlist):
		bullet.move()
		bulletlist[index] = bullet
		for box in collisionboxes:
			if box.collidepoint(int(bullet.x), int(bullet.y)):
				bulletlist.remove(bullet)
				break;
		if bullet.x > screenwidth or bullet.x < 0: bulletlist.remove(bullet)
		if bullet.y > screenheight or bullet.y < 0: bulletlist.remove(bullet)
		pygame.draw.line(windowSurfaceObj, pygame.Color(0, 0, 0), (int(bullet.x - bullet.xvel), int(bullet.y - bullet.yvel)), (bullet.x, bullet.y))
	for box in collisionboxes:
		pygame.draw.rect(windowSurfaceObj, pygame.Color(119, 136, 153), box)
	player.move(left, right, up, down)
	if player.rectangle.colliderect(gunbox.rectangle):
		player.score += 1
		gunbox = GunBox()
		while True:
			tmp = weaponlist[randint(0, len(weaponlist) - 1)]
			if player.weapon.type != tmp.type:
				player.weapon = tmp
				break
		print(player.weapon.type)
	if space:
		player.fire()
	if player.weapon.reloadtimer <= player.weapon.reloadtime:
		player.weapon.reloadtimer += 60
	pygame.draw.rect(windowSurfaceObj, pygame.Color(0, 0, 255), player.getrect())
	pygame.draw.rect(windowSurfaceObj, pygame.Color(139, 69, 19), gunbox.rectangle)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				left = True
			elif event.key in (K_RIGHT, K_d):
				right = True
			elif event.key in (K_UP, K_w):
				up = True
				player.startjump()
			elif event.key == K_SPACE:
				space = True
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
				player.endjump()
			elif event.key -- K_SPACE:
				space = False
	if up and player.onground:
		player.startjump()
	pygame.display.update()
	fpsClock.tick(60)