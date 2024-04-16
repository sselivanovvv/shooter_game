#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
FPS = 60
game = True
finish = False
img_back = 'forest.jpg' 
img_hero = 'bowmaster.jpg'
img_mons = 'goblin.jpg'
img_bull = 'bullet.png'
img_as = 'asteroid.png'
win_w = 700
win_h = 500
lost = 0
font.init()
font1 = font.SysFont('Arial', 45)
font2 = font.SysFont('Arial', 65)
win_point = 0
reloadd = False
numfire = 0
life = 3
class GameSprite(sprite.Sprite):
    def __init__(self, imagepng, size_x, size_y, rect_x, rect_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(imagepng), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.speed = speed

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y <= 395:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 595:
            self.rect.x += self.speed

    def attack(self):
        bullet = Bullet(img_bull, 30, 20, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
        
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 5
            self.rect.x = randint(5, 595)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

            

win = display.set_mode((win_w, win_h))
display.set_caption('pygame window')
clock = time.Clock()

background = transform.scale(image.load(img_back), (win_w, win_h))
hero = Player(img_hero, 90, 90, win_h-100, 350, 6)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_mons, 80, 50, randint(80, win_w-80), 5, randint(1, 3))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 2):
    asteroid = Enemy(img_as, 80, 50, randint(80, win_w-80), 5, 2)
    asteroids.add(asteroid)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if numfire < 5 and reloadd != True:
                    numfire += 1
                    hero.attack()
                    fire.play()
                else:
                    end = timer()
                    reloadd = True
                

    if finish != True:
        win.blit(background, (0, 0))
        lost_enem = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        win.blit(lost_enem, (5, 80))
        lost_num = font1.render('Счет:' + str(win_point), 1, (255, 255, 255))
        win.blit(lost_num, (5, 40))
        life_txt = font1.render(str(life), 1, (255, 1, 1))
        win.blit(life_txt, (660, 40))
        hero.reset()
        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides:
            win_point += 1
            monster = Enemy(img_mons, 80, 50, randint(80, win_w-80), 5, randint(1, 3))
            monsters.add(monster)
        monsters.draw(win)
        bullets.draw(win)
        asteroids.draw(win)
        hero.update()
        monsters.update()
        bullets.update()   
        asteroids.update()
        display.update()
        
        if win_point >= 10:
            finish = True
            win_txt = font2.render('YOU WIN!', 1, (1, 255, 1))
            win.blit(win_txt, (200, 200))

        if sprite.spritecollide(hero, monsters, True) or sprite.spritecollide(hero, asteroids, True):
            life -= 1
        if lost >= 3 or life <= 0:
            finish = True
            lose_txt = font2.render('YOU LOSE!', 1, (255, 1, 1))
            win.blit(lose_txt, (200, 200))
        if reloadd == True:
            start = timer()
            if start - end < 3:
                reload = font1.render('Wait, reload...', 1, (255, 1, 1))
                win.blit(reload, (350, 440))
            else:
                numfire = 0
                reloadd = False

        display.update()
        
    else:
        finish = False
        win_point = 0
        lost = 0
        life = 3
        numfire = 0
        hero.rect.x = 400
        hero.rect.y = 350
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_mons, 80, 50, randint(80, win_w-80), 5, randint(1, 3))
            monsters.add(monster)
        for i in range(1, 2):
            asteroid = Enemy(img_as, 80, 50, randint(80, win_w-80), 5, 2)
            asteroids.add(asteroid)
    time.delay(50)