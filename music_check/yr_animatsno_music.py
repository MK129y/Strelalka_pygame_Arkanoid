# Игра Shmup - 3 часть
# Cтолкновения и стрельба
import pygame
import random
from os import path

# WIDTH = 480
# HEIGHT = 600
WIDTH = 680
HEIGHT = 800
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
Purple = (221,160,221)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME_Arkanoid")
clock = pygame.time.Clock()

#музыка
snd_dir = path.join(path.dirname(__file__), 'music')
# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'blum.mp3'))#пуля
expl_sounds = []
# for snd in ['expl3.wav', 'expl6.wav']:
#     expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#fon = pygame.mixer.music.Sound(path.join(snd_dir, 'Fon.mp3'))
#pygame.mixer.music.set_volume(0.4)


#картинки
img_dir = path.join(path.dirname(__file__), 'img')
# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, 'nebo.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "korabl.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "meteor.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "pul.png")).convert()
#ыводить текст не один раз
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#pygame.mixer.music.play(loops=1)
#fon.play(loops=1)

#Это начало спрайта игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 40))
        #self.image.fill(GREEN)
        self.image = player_img
        self.rect = self.image.get_rect()
        #бесцветный фон
        self.image = pygame.transform.scale(player_img, (150, 130))
        self.image.set_colorkey(WHITE)
        #
        # self.image.fill(Purple)
        # self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
# создает пулю, используя в качестве места появления верхнюю центральную часть игрока
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)#чтобы она отрисовалась и обновилась пуля
        bullets.add(bullet) #будет использоваться для столкновений
        shoot_sound.play(maxtime = 0) #звук пули

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = meteor_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        # self.image.fill(RED)
        # self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        #Вращение
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) % 360
                self.image = pygame.transform.rotate(self.image_orig, self.rot)
            # вращение спрайтов

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    # проверка, попала ли пуля в моб
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Проверка, не ударил ли моб игрока(игра заканчивается если прикоснулся к игроку кубик)
    # hits = pygame.sprite.spritecollide(player, mobs, False)
    # if hits:
    #     running = False
    # for hit in hits:
    #     player.shield -= hit.radius * 2
    #     if player.shield <= 0:
    #         running = False
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

pygame.quit()
