import pygame, sys
from pygame.locals import *
from random import randint
from time import sleep
import os
import ctypes

pygame.init()
fpsClock = pygame.time.Clock()

screenwidth = 1000
screenheight = 750
user32 = ctypes.windll.user32
userscreenwidth = user32.GetSystemMetrics(0)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (userscreenwidth / 2 - screenwidth / 2, 2)

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
	def __init__(self, x, y, xvel, yvel, damage):
		self.x = x
		self.y = y
		self.xvel = xvel
		self.yvel = yvel
		self.damage = damage

	def move(self):
		self.x += self.xvel
		self.y += self.yvel

class Gun(object):
	def __init__(self):
		self.type = None
		self.damage = 7
		self.reloadtime = None
		self.reloadtimer = None
		self.canfire = True
		self.knockback = 0
		self.vel = 13

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
			self.vel = -abs(self.vel)
		else:
			self.vel = abs(self.vel)
		return [Bullet(x, y, self.vel, randint(-1, 0), self.damage)]

class DualPistol(Pistol):
	def __init__(self):
		super(DualPistol, self).__init__()
		self.type = 'DualPistol'

	def bulletfire(self, x, y, direction):
		if direction == 'right':
			return [Bullet(x, y, self.vel, randint(-1, 0), self.damage), Bullet(x - 30, y, -abs(self.vel), randint(-1, 0), self.damage)]
		return [Bullet(x + 30, y, self.vel, randint(-1, 0), self.damage), Bullet(x, y, -abs(self.vel), randint(-1, 0), self.damage)]

class Revolver(Pistol):
	def __init__(self):
		super(Revolver, self).__init__()
		self.type = 'Revolver'
		self.reloadtime = 1700
		self.reloadtimer = 1700
		self.damage = 13

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			self.vel = -abs(self.vel)
		else:
			self.vel = abs(self.vel)
		return [Bullet(x, y, self.vel, 0, self.damage)]

class Shotgun(Pistol):
	def __init__(self):
		super(Shotgun, self).__init__()
		self.type = 'Shotgun'
		self.reloadtime = 2500
		self.reloadtimer = 2500
		self.damage = 3
		self.knockback = 5
		self.vel = 17

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			self.vel = -abs(self.vel)
		else:
			self.vel = abs(self.vel)
		tmplist = []
		for i in range(randint(8, 13)):
			tmplist.append(Bullet(x, y, self.vel, randint(-10, 3), self.damage))
		return tmplist

class Machinegun(Pistol):
	def __init__(self):
		super(Machinegun, self).__init__()
		self.type = 'Machinegun'
		self.reloadtime = 300
		self.reloadtimer = 300
		self.damage = 5
		self.knockback = 2
		self.vel = 17

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			self.vel = -abs(self.vel)
		else:
			self.vel = abs(self.vel)
		return [Bullet(x, randint(y - 5, y + 5), randint(self.vel - 2, self.vel + 2), randint(-1, 1), self.damage)]

class Gatlinggun(Machinegun):
	def __init__(self):
		super(Gatlinggun, self).__init__()
		self.type = 'Gatlinggun'
		self.reloadtimer = 100
		self.reloadtime = 100
		self.knockback = 4
		self.vel = 25
		self.damage = 6

class Laser(Gun):
	def __init__(self):
		super(Laser, self).__init__()
		self.reloadtime = 7000
		self.reloadtimer = 7000
		self.type = 'Laser'
		self.damage = 1000
		self.knockback = 5
		self.firedurationtimer = 0
		self.fireduration = 1500
		self.firing = False

	def fire(self):
		if self.reloadtimer >= self.reloadtime:
			self.canfire = False
			self.reloadtimer = 0
			self.firedurationtimer = 0
			self.firing = True
			return True
		return False

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			return Rect(0, y - 3, x, 6)
		else:
			return Rect(x, y - 3, screenwidth - x, 6)

class TrollGun(Gatlinggun):
	def __init__(self):
		super(TrollGun, self).__init__()
		self.reloadtime = 0
		self.reloadtimer = 0
		self.type = 'TrollGun'
		self.damage = 1000
		self.knockback = 0
		self.vel = 30

	def bulletfire(self, x, y, direction):
		if direction == 'left':
			self.vel = -abs(self.vel)
		else:
			self.vel = abs(self.vel)
		tmplist = []
		for i in range(30):
			if direction == 'left':
				tmplist.append(Bullet(x, randint(y - 5, y + 5), randint(self.vel - 2, self.vel + 2), randint(-30, 30), self.damage))
				tmplist.append(Bullet(x + 30, randint(y - 5, y + 5), -randint(self.vel - 2, self.vel + 2), randint(-30, 30), self.damage))
			else:
				tmplist.append(Bullet(x, randint(y - 5, y + 5), randint(self.vel - 2, self.vel + 2), randint(-30, 30), self.damage))
				tmplist.append(Bullet(x - 30, randint(y - 5, y + 5), -randint(self.vel - 2, self.vel + 2), randint(-30, 30), self.damage))
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

class Monster:
	def __init__(self):
		size = randint(30, 50)
		if randint(0, 1) == 0:
			self.direction = 'right'
			self.rectangle = Rect(300, -50, size, size)
		else:
			self.direction = 'left'
			self.rectangle = Rect(screenwidth - 300, -50, size, size)
		self.gravity = .8
		self.xvel = randint(3, 5)
		self.yvel = 0
		self.onground = False
		self.despawn = False
		self.health = size / 3
		self.randomjumptime = randint(3000, 10000)
		self.randomjumptimer = 0
		self.jumpconst = 15

	def move(self):
		if self.randomjumptimer >= self.randomjumptime:
			self.randomjumptime = randint(3000, 10000)
			self.randomjumptimer = 0
			if self.onground:
				self.yvel = self.jumpconst
				self.onground = False
		self.randomjumptimer += 60
		if self.direction == 'right':
			self.rectangle.x += self.xvel
		if self.direction == 'left':
			self.rectangle.x -= self.xvel
		self.yvel -= self.gravity
		self.rectangle.y -= self.yvel
		if self.rectangle.left < 0:
			self.rectangle.x = 0
			self.direction = 'right'
		if self.rectangle.right > screenwidth:
			self.rectangle.x = screenwidth - self.rectangle.width
			self.direction = 'left'
		if self.rectangle.top > screenheight:
			self.despawn = True
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
				if b < t and b < l and b < r: #bottom
					self.rectangle.top = box.bottom
					self.yvel = 0
				if l < r and l < t and l < b: #left
					self.rectangle.right = box.left
					self.time = 0
				if r < l and r < t and r < b: #right
					self.rectangle.left = box.right
		if abs(self.yvel) != self.gravity and self.yvel != 0:
			self.onground = False



class Player:
	def __init__(self):
		size = 30
		self.rectangle = Rect(screenwidth / 2 - size / 2, screenheight / 2, size, size)
		self.jumpcount = 0
		self.maxjump = 0
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
		self.isalive = True

	def fire(self):
		global bulletlist, laserrect
		if self.weapon.type in ['Laser', 'Sword']:
			if self.weapon.fire() or self.weapon.firing:
				if self.direction == 'right':
					laserrect = self.weapon.bulletfire(self.rectangle.right, self.rectangle.centery, self.direction)
				else:
					laserrect = self.weapon.bulletfire(self.rectangle.left, self.rectangle.centery, self.direction)
				self.weapon.firedurationtimer += 60
				if self.weapon.firedurationtimer > self.weapon.fireduration:
					laserrect = None
					self.weapon.firing = False
				self.justfired = True
				self.knockback = self.weapon.knockback
		elif self.weapon.fire():
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
		if self.weapon.type in ['Laser', 'Sword'] and self.weapon.firing:
			if self.direction == 'right' and r:
				self.rectangle.x += self.xvel
			if self.direction == 'left' and l:
				self.rectangle.x -= self.xvel
		else:
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
			if self.knockback != 0:
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
		if self.rectangle.top > screenheight:
			self.isalive = False
			"""
			self.rectangle.y = screenheight - self.rectangle.height
			self.yvel = 0
			self.jumpcount = 0
			self.onground = True
			"""
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
		elif self.jumpcount < self.maxjump: #player can jump n + 1 times
			self.yvel = self.jumpconst
			self.jumpcount += 1

	def endjump(self):
		if self.yvel > 10:
			self.yvel = 10

	def getrect(self):
		return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)


windowSurfaceObj = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Box Shooter Game by Mitsuru Otsuka')

collisionboxes = []
height = 30
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
#weaponlist = ['pistol', 'dualpistol', 'revolver', 'shotgun', 'machinegun', 'gatlinggun', 'laser', 'rocketlauncher' 'sword']
weaponlist = [Pistol(), DualPistol(), Revolver(), Shotgun(), Machinegun(), Gatlinggun(), Laser()]
fontObj = pygame.font.Font('freesansbold.ttf', 14)
trollObj = pygame.font.Font('freesansbold.ttf', 30)
trollrect = None
while True:
	player = Player()
	left=right=up=down=False
	timeconst = 1
	gunbox = GunBox()
	space = False
	bulletlist = []
	laserrect = None
	monsterlist = []
	monstertimer = 0
	monstertime = 3500
	trollmode = False
	if randint(0, 30) == 1:
		trollmode = True
		monstertime = 0
		player.maxjump = 5
	while player.isalive:
		windowSurfaceObj.fill(pygame.Color(255, 255, 255))
		if trollmode:
			player.jumpcount = 0
			player.weapon = TrollGun()
		if space:
			if player.weapon.type in ['Laser', 'Sword']:
				if not player.weapon.firing:
					player.fire()
			else:
				player.fire()
		if player.weapon.type in ['Laser', 'Sword']:
			if player.weapon.firing:
				player.fire()
				if laserrect != None:
					pygame.draw.rect(windowSurfaceObj, pygame.Color(255, 0, 0), laserrect)
		for index, bullet in enumerate(bulletlist):
			bullet.move()
			bulletlist[index] = bullet
			for box in collisionboxes:
				if box.collidepoint(int(bullet.x), int(bullet.y)):
					bulletlist.remove(bullet)
					break;
			if bullet.x > screenwidth or bullet.x < 0:
				if bullet in bulletlist:
					bulletlist.remove(bullet)
			if bullet.y > screenheight or bullet.y < 0:
				if bullet in bulletlist:
					bulletlist.remove(bullet)
			for monster in monsterlist:
				if monster.rectangle.collidepoint(bullet.x, bullet.y) or monster.rectangle.collidepoint(bullet.x - bullet.xvel, bullet.y - bullet.yvel):
					monster.health -= bullet.damage
					if bullet in bulletlist:
						bulletlist.remove(bullet)
				if monster.health <= 0:
					monsterlist.remove(monster)
			pygame.draw.line(windowSurfaceObj, pygame.Color(0, 0, 0), (int(bullet.x - bullet.xvel), int(bullet.y - bullet.yvel)), (bullet.x, bullet.y))
		for box in collisionboxes:
			pygame.draw.rect(windowSurfaceObj, pygame.Color(119, 136, 153), box)
		player.move(left, right, up, down)
		if player.rectangle.colliderect(gunbox.rectangle):
			player.score += 1
			gunbox = GunBox()
			if player.score > 5:
				monstertime = 3000
			elif player.score > 15:
				monstertime = 2500
			elif player.score > 20:
				monstertime = 2000
			elif player.score > 30:
				monstertime = 500
			while True:
				tmp = weaponlist[randint(0, len(weaponlist) - 1)]
				if player.weapon.type != tmp.type:
					player.weapon = tmp
					break
			#print(player.weapon.type)
		if player.weapon.reloadtimer <= player.weapon.reloadtime:
			player.weapon.reloadtimer += 60
		pygame.draw.rect(windowSurfaceObj, pygame.Color(0, 0, 255), player.getrect())
		monstertimer += 60
		if monstertimer > monstertime:
			monstertimer = 0
			monsterlist.append(Monster())
		for index, monster in enumerate(monsterlist):
			monster.move()
			monsterlist[index] = monster
			if laserrect != None:
					if laserrect.colliderect(monster.rectangle):
						monster.health -= player.weapon.damage
			if monster.rectangle.colliderect(player.rectangle):
				player.isalive = False
			if monster.health <= 0:
				monsterlist.remove(monster)
			else:
				pygame.draw.rect(windowSurfaceObj, pygame.Color(255, 0, 0), monster.rectangle)
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
		msgSurfaceObj = fontObj.render('Score: ' + str(player.score), False, pygame.Color(0, 0, 0))
		msgRectobj = msgSurfaceObj.get_rect()
		msgRectobj.center = (screenwidth / 2, 8)
		windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
		msgSurfaceObj = fontObj.render('Weapon: ' + str(player.weapon.type), False, pygame.Color(0, 0, 0))
		msgRectobj = msgSurfaceObj.get_rect()
		msgRectobj.center = (screenwidth / 2, screenheight - 8)
		windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
		if trollmode:
			msgSurfaceObj = trollObj.render('TROLL MODE ACTIVE!!!', False, pygame.Color(34, 139, 34))
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.center = (screenwidth / 2, screenheight / 2 + 70)
			windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
		pygame.display.update()
		fpsClock.tick(60)
	msgSurfaceObj = fontObj.render('GAMEOVER', False, pygame.Color(0,0,0))
	msgRectobj = msgSurfaceObj.get_rect()
	msgRectobj.center = (screenwidth / 2, screenheight / 2)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	pygame.display.update()
	sleep(3)