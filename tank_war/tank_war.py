'''
Bilibili > 尚学堂小助理
YJ 20230116
'''
import pygame, time, random


SCREEN_WIDTH = 720
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0,0,0)
TEXT_COLOR = pygame.Color(255,0,0)

# 为了实现‘子弹打坦克’的效果，定义一个基类，继承精灵类Sprite
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

class MainGame():

    window = None
    my_tank = None

    # 敌方坦克
    enemyTankList = []
    enemyTankCount = 5

    # 我方子弹
    myBulletList = []

    # 敌方子弹
    enemyBulletList = []

    # 爆炸效果列表
    explodeList = []

    # 墙壁列表
    wallList = []

    def __init__(self):
        pass
    
    # 开始游戏
    def startGame(self):
        # 加载主窗口
        pygame.display.init()    # 初始化
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # 设置窗口的大小与显示

        # 初始化我方坦克
        self.createMyTank()
        # 初始化敌方坦克，并添加到列表
        self.createEnemyTank()
        # 初始化墙壁
        self.createWall()

        pygame.display.set_caption('!TANK-WAR!')

        while True:
            # 控制移动速度
            time.sleep(0.02)

            MainGame.window.fill(BG_COLOR)
            # 获取事件
            self.getEvent()
            # 绘制文字
            MainGame.window.blit(self.getTextSurface('敌方坦克剩余数量%d'%len(MainGame.enemyTankList)), (10, 10))

            # 显示我方坦克活
            if MainGame.my_tank and MainGame.my_tank.live:
                # 若存活
                MainGame.my_tank.displayTank()
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.my_tank = None
            # 循环显示敌方坦克
            self.blitEnemyTank()
            # 循环显示我方子弹
            self.blitMyBullet()
            # 循环显示敌方子弹
            self.blitEnemyBullet()
            # 循环显示爆炸效果
            self.blitExplode()
            # 循环遍历墙壁列表，展示墙壁
            self.blitWall()
            # 当移动开关是开启时，一直移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
            
            pygame.display.update()

    # 创建墙壁
    def createWall(self):
        for i in range(6):
            # 初始化墙壁
            wall = Wall(i*130, 220)
            # 添加到墙壁列表
            MainGame.wallList.append(wall)
        
    # 创建我方坦克
    def createMyTank(self):
        MainGame.my_tank = Tank(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+100)

    # 初始化敌方坦克，并添加到列表
    def createEnemyTank(self):
        top = 100
        # 循环生成敌方坦克
        for i in range(MainGame.enemyTankCount):
            left = random.randint(100, SCREEN_WIDTH-100)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    # 遍历显示爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                # 展示
                explode.displayExplode()
            else:
                # 移除爆炸列表
                MainGame.explodeList.remove(explode)

    # 遍历敌方坦克列表，显示敌方坦克
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()

                # 发射子弹
                enemyBullet = enemyTank.shot()
                # 只有在敌方子弹不为None的情况下（enemyTank复写了sht()方法，只有小概率情况下会返回Bullet()），再添加进List
                if enemyBullet:
                    # 将敌方子弹存储到敌方子弹列表
                    MainGame.enemyBulletList.append(enemyBullet)
            # 如果不活着（被子弹打死），从敌方坦克列表中移除
            else:
                MainGame.enemyTankList.remove(enemyTank)


    # 遍历我方子弹列表，显示我方子弹
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            # 只显示(live == True)的子弹，否则删除
            if myBullet.live:
                myBullet.displayBullet()
                myBullet.move()
                # 检测是否打中
                myBullet.myBullet_hit_enemyTank()
            else:
                MainGame.myBulletList.remove(myBullet)

    # 循环显示敌方子弹
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            # 只显示(live == True)的子弹，否则删除
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()
                # 打中我方坦克
                enemyBullet.enemyBullet_hit_myTank()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)

    # 遍历墙壁列表，循环显示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            # 调用墙壁的显示方法
            wall.displayWall()

    # 结束游戏
    def endGame(self):
        print("谢谢使用！")
        exit()

    # 左上角文字的绘制
    def getTextSurface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('songti', 18)
        textSurface = font.render(text, True, TEXT_COLOR) # 绘制小的surface
        return textSurface # 返回，绘制到大的surface

    # 获取事件
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.KEYDOWN:
                # 按下方向键，只切换方向，不移动，否则按住的话只能移动一格，不能持续移动
                # 同时打开移动开关
                if MainGame.my_tank and MainGame.my_tank.live:
                    if event.key == pygame.K_UP:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.stop = False
                    elif event.key == pygame.K_DOWN:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                    elif event.key == pygame.K_LEFT:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                    elif event.key == pygame.K_RIGHT:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                    elif event.key == pygame.K_SPACE:
                        # 创建"我方坦克"的子弹，且同时屏幕上的子弹数量最多3个
                        if len(MainGame.myBulletList) < 3:
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                # 我方坦克死亡后，按ESC重生
                elif not MainGame.my_tank:
                    if event.key == pygame.K_ESCAPE:
                        self.createMyTank()

            elif event.type == pygame.KEYUP:
                # 松开方向键，关闭移动开关
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True

class Tank(BaseItem):
    # 位置 => left：距离左边；top：距离上边
    def __init__(self, left, top):
        # 图片集
        self.images = {'U': pygame.image.load('img/p1tankU.gif'),
                       'D': pygame.image.load('img/p1tankD.gif'),
                       'L': pygame.image.load('img/p1tankL.gif'),
                       'R': pygame.image.load('img/p1tankR.gif')}
        # 方向
        self.direction = 'U'
        # 根据图片和方向，获取tank的surface
        self.image = self.images[self.direction]
        # 根据图片，获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left和top
        self.rect.left = left
        self.rect.top = top
        # 移动速度
        self.speed = 5
        # 坦克移动的开关
        self.stop = True
        # 死活
        self.live = True

    # 移动
    def move(self):
        # 判断移动方向
        if self.direction == 'U':
            if self.rect.top > 0: self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT: self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0: self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH: self.rect.left += self.speed

    # 射击，如果self是敌方坦克，就返回敌方子弹
    def shot(self):
        return Bullet(self)

    # 展示
    def displayTank(self):
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect) # 这里把rect换成坐标组，也是可以的

# 我方坦克，继承自Tank class
class MyTank(Tank):
    def __init__(self):
        pass

# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # EnemyTank如果可用父类的live属性，就需要调用父类的init()
        super(EnemyTank, self).__init__(left, top)
        # 加载图片集
        self.images = {'U': pygame.image.load('img/enemy1U.gif'),
                       'D': pygame.image.load('img/enemy1D.gif'),
                       'L': pygame.image.load('img/enemy1L.gif'),
                       'R': pygame.image.load('img/enemy1R.gif')}
        # 随机生成方向
        self.direction = self.randDirection()
        # 获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left, top, speed 进行赋值
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.flag = True # ??? 就是stop

        # 随机移动的步数变量
        self.step = 20


    # 随机生成方向
    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1: return 'U'
        if num == 2: return 'D'
        if num == 3: return 'L'
        if num == 4: return 'R'

    # 敌方坦克随机移动
    def randMove(self):
        if self.step <= 0:
            # 随机修改方向
            self.direction = self.randDirection()
            # step复位
            self.step = 60
        else:
            self.move()
            self.step -= 1
    
    # 重写 shot() 方法
    def shot(self):
        num = random.randint(1, 100)
        if num < 5:
            return Bullet(self)

# 子弹
class Bullet(BaseItem):
    def __init__(self, tank):
        # 加载图片
        self.image = pygame.image.load('img/enemymissile.gif')
        # 坦克方向决定子弹方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 坦克位置决定子弹位置
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width/2 - self.rect.width/2
        
        # 子弹速度
        self.speed = 6
        # 子弹状态，是否撞墙
        self.live = True


    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False

    # 展示子弹
    def displayBullet(self):
        # 将图片surface加载到窗口
        MainGame.window.blit(self.image, self.rect)

    # 我方子弹打敌方坦克
    def myBullet_hit_enemyTank(self):
        # 遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                # 修改二者的状态
                enemyTank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
    
    # 敌方子弹打中我方坦克
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 产生爆炸对象
                explode = Explode(MainGame.my_tank)
                # 添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 修改子弹与我方坦克的状态
                self.live = False
                MainGame.my_tank.live = False

# 墙壁
class Wall():
    def __init__(self, left, top):
        # 加载图片
        self.image = pygame.image.load('img/steels.gif')
        # 获取墙壁区域
        self.rect = self.image.get_rect()
        # 设置位置 left, top
        self.rect.left = left
        self.rect.top = top
        # 是否存活
        self.live = True
        # 设置生命值，如果被击中，生命值--
        self.hp = 3

    # 展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)

class Explode():
    def __init__(self, tank):
        # 爆炸的位置与衩打中的坦克位置相同
        self.rect = tank.rect
        self.images = [pygame.image.load('img/blast0.gif'),
                       pygame.image.load('img/blast1.gif'),
                       pygame.image.load('img/blast2.gif'),
                       pygame.image.load('img/blast3.gif'),
                       pygame.image.load('img/blast4.gif')]
        self.step = 0
        self.image = self.images[self.step]
        # 是否活着(爆炸这组图片是否已展示完成???)
        self.live = True

    # 展示爆炸效果的方法
    def displayExplode(self):
        if self.step < len(self.images):
            # 根据index获取爆炸对象
            self.image = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0
        

class Music():
    def __init__(self):
        pass

    # 播放
    def play(self):
        pass



if __name__ == '__main__':
    MainGame().startGame()
