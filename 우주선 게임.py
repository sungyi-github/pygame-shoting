import pygame
import random
import time
from datetime import datetime

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [600, 700]
screen = pygame.display.set_mode(size)

title = "우주선 게임"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else :
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x,self.y))
        
def crash(a, b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
        if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
    else : 
        return False
ss = obj()
ss.put_img("images-n.png")
ss.change_size(50,80)
ss.x = round(size[0]/2- ss.sx/2)
ss.y = size[1] -ss.sy - 15
ss.move = 5

left_go = False
right_go = False
space_go = False

m_list = []
a_list = []

black = (0,0,0)
white = (100,100,100)
k = 0

GO = 0
kill = 0
loss = 0
level = 3

# 4-0. 게임 시작 대기 화면
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(black)
    font = pygame.font.Font("COOPBL.TTF", 15)
    text = font.render("PRESS SPACE KEY TO START THE GAME", True, (255,255,255))
    screen.blit(text, (140, round(size[1]/2-50)))    
    pygame.display.flip()


# 4. 메인 이벤트
start_time = datetime.now()
SB = 0
while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False 
                
    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())
    if kill == 30:
        level = 4
    if kill == 50:
        level = 5 
    if kill == 70:
        level = 6  
    if kill == 100:
        level = 7   
    if kill == 130:
        level = 8
    if kill == 150:
        level = 9
    if kill == 170:
        level = 10
    if kill == 200:
        level = 11
                       
    
    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0
    elif right_go == True:
        ss.x += ss.move
        if ss.x >= size[0] - ss.sx:
            ss.x = size[0] - ss.sx
    
    if space_go == True and k % 6 == 0:
        mm = obj()
        mm.put_img("images.png")
        mm.change_size(5,15)
        mm.x = round(ss.x + ss.sx/2 - mm.sx/2)
        mm.y = ss.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)
    k += 1
    d_list = []    
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y <= -m.sy:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del m_list[d]
        
    if random.random() > 0.98: 
        aa = obj()
        aa.put_img("images-s.png")
        aa.change_size(40,40)
        aa.x = random.randrange(0, size[0]-aa.sx-round(ss.sx/2))
        aa.y = 10
        aa.move = level
        a_list.append(aa)
    d_list = []
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del a_list[d]
        loss += 1
    
    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m,a) == True:
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))
    dm_list.reverse()
    da_list.reverse()
    try:
        for dm in dm_list:
            del m_list[dm]
        for da in da_list:
            del a_list[da]
            kill += 1
    except:
        pass
        
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1
            GO = 1
    
    # 4-4. 그리기
    screen.fill(white)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()
        
    font = pygame.font.Font("COOPBL.TTF", 20)
    text_kill = font.render("killed : {} loss : {}".format(kill, loss), True, (255,255,0))
    screen.blit(text_kill, (10, 5))
    
    text_time = font.render("time : {}".format(delta_time), True, (255,255,255))
    screen.blit(text_time, (size[0]-100, 5))
    
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    font = pygame.font.Font("COOPBL.TTF", 40)
    text = font.render("GAME OVER", True, (255,0,0))
    screen.blit(text, (140, round(size[1]/2-50)))
    pygame.display.flip()
pygame.quit()
