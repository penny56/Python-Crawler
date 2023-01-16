# Bilibili > 编程侯老师
# YJ 20230113

import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# initialization game
pygame.init()
pygame.mixer.init() # init sound mixer
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('!PLANE-WAR!')
clock = pygame.time.Clock()

background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 20))
player_mini_img.set_colorkey(BLACK)
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_images = []
for i in range(7):
    # 7张rock图片随机使用
    rock_images.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
    # 一组爆炸声音
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.2) # 设置背景音乐音量

# 定义得分
font_name = pygame.font.match_font('arial')
# 显示得分
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# 显示血量条
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # 两个rect来画这个血量条
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# 
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect) 

# 生成陨石
def new_rock():
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)         # 加入陨石列表，记录下陨石的位置

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,40)) # 把图片大小改成50*40
        self.image.set_colorkey(BLACK) # 把飞机周边的黑色设置为透明色

        # pygame是以屏幕的左上角为坐标原点(0,0)
        self.rect = self.image.get_rect()

        # 给飞机加一些“圆”的属性，这样可以用圆的方式检测碰撞，这里的radius值可以把飞机图片“盖住”就可以
        self.radius = 23
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 测试的时候可以画出来看看有没有“盖住“

        self.rect.centerx = WIDTH/2   # 初始位置
        self.rect.bottom = HEIGHT-20

        self.speedx = 3

        # 飞机初始化生命值
        self.health = 100

        # 飞机有3条命
        self.lives = 3

        self.hidden = False
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            # 如果飞机当前是隐藏状态，并且隐藏超过1s时间
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 20
    
    def shoot(self):
        # 生成子弹时，要同时把飞机的坐标传入
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)     # 加入子弹列表，记录下子弹的位置
        shoot_sound.play()
    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500) # 把飞机的位置移动到超出屏幕，相当于隐藏

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 引入origin变量的目的是为了消除“旋转”累积的误差
        self.image_origin = random.choice(rock_images) # rock_images中随机挑选一张rock的图片
        self.image_origin.set_colorkey(BLACK)
        self.image = self.image_origin.copy()

        # pygame是以屏幕的左上角为坐标原点(0,0)
        self.rect = self.image.get_rect()

        # 陨石为了优化碰撞检测，加个半径属性，radius值“盖住”陨石大小即可
        self.radius = self.rect.width/2.2

        self.rect.x = random.randrange(0, WIDTH-self.rect.width)   # 陨石初始位置，上方掉下
        self.rect.y = -100 # 这里大一点，从屏幕上方就出现，不会从一半出现

        self.speedy = random.randrange(2,4)     # 陨石掉落速度随机
        self.speedx = random.randrange(-2,2)     # 陨石左右漂移随机

        self.rot_degree = random.randrange(-3,3)
        self.total_degree = 0 # 基于origin的旋转角度，引入的目的是消除累积误差

    def rotate(self):
        # self.image = pygame.transform.rotate(self.image,2) # 这种方式累积的误差过大，改为下面的方式
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360 # 旋转不要超过360度
        self.image = pygame.transform.rotate(self.image_origin, self.total_degree)

        # 每次旋转之后，重新绘制”中心点“，以消除旋转时”抽动“的效果
        center = self.rect.center
        self.center = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 陨石出界，就马上再生成另一个陨石
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            # 这里最好与__init__()里的操作保持一致
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y = -100

            self.speedy = random.randrange(2,4)     # 陨石掉落速度随机
            self.speedx = random.randrange(-2,2)     # 陨石左右漂移随机

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img # 图片大小合适，不调整
        self.image.set_colorkey(BLACK)

        # pygame是以屏幕的左上角为坐标原点(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedy = -10     # 子弹向上，是负值，没有x速度
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:        # 子弹打出屏幕
            self.kill()

all_sprites = pygame.sprite.Group()     # 所有的屏幕元素

player = Player()
all_sprites.add(player)

# 存放陨石和子弹，来实现子弹打爆陨石
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

score = 0

# 背景音乐，无限时间播放
pygame.mixer.music.play(-1)

for i in range(5):          # 同时出现几个陨石
    new_rock()

running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 发射子弹
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # moving
    all_sprites.update()

    # 陨石与子弹的碰撞检测
    hits_bullet_rock = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits_bullet_rock:
        # 随机挑一个爆炸音效运行
        random.choice(expl_sounds).play() 

        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

        # 得分
        score = score + int(hit.radius)
        

    # 陨石与飞机的碰撞检测，第4个参数表示以“circle”方式检测碰撞，比方形更加准确一点
    hits_rock_plane = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits_rock_plane:
        player.health = player.health - hit.radius

        # 碰撞之后，重新生成陨石
        new_rock()

        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            player.hide()
            if player.lives <= 0:
                running = False

    # display
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 0)
    draw_health(screen, player.health, 10, 30)
    draw_lives(screen, player.lives, player_mini_img, WIDTH-100, 15)
    pygame.display.update()

pygame.quit()