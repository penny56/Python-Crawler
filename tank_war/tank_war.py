'''
Bilibili > 尚学堂小助理
YJ 20230116
'''
import pygame, time, random


SCREEN_WIDTH = 700
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

   def __init__(self):
      pass
   
   # 开始游戏
   def startGame(self):
      # 加载主窗口
      pygame.display.init()   # 初始化
      MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # 设置窗口的大小与显示

      # 初始化我方坦克
      MainGame.my_tank = Tank(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
      # 初始化敌方坦克，并添加到列表
      self.createEnemyTank()

      pygame.display.set_caption('!TANK-WAR!')

      while True:
         # 控制移动速度
         time.sleep(0.02)

         MainGame.window.fill(BG_COLOR)
         # 获取事件
         self.getEvent()
         # 绘制文字
         MainGame.window.blit(self.getTextSurface('敌方坦克剩余数量%d'%len(MainGame.enemyTankList)), (10, 10))

         # 显示我方坦克
         MainGame.my_tank.displayTank()
         # 循环显示敌方坦克
         self.blitEnemyTank()
         # 循环显示我方子弹
         self.blitMyBullet()
         # 循环显示敌方子弹
         self.blitEnemyBullet()
         # 当移动开关是开启时，一直移动
         if not MainGame.my_tank.stop:
            MainGame.my_tank.move()
         
         pygame.display.update()

   # 初始化敌方坦克，并添加到列表
   def createEnemyTank(self):
      top = 100
      # 循环生成敌方坦克
      for i in range(MainGame.enemyTankCount):
         left = random.randint(100, SCREEN_WIDTH-100)
         speed = random.randint(1, 4)
         enemy = EnemyTank(left, top, speed)
         MainGame.enemyTankList.append(enemy)

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
         else:
            MainGame.enemyBulletList.remove(enemyBullet)

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
         elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               # 松开方向键，关闭移动开关
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

# 墙壁
class Wall():
   def __init__(self):
      pass

   # 展示墙壁的方法
   def displayWall(self):
      pass

class Explode():
   def __init__(self):
      pass

   # 展示爆炸效果的方法
   def displayExplode(self):
      pass

class Music():
   def __init__(self):
      pass

   # 播放
   def play(self):
      pass



if __name__ == '__main__':
   MainGame().startGame()
