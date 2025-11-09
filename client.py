import pygame
import random
import csv
import os
import sys
import socket
import threading
import json

# 初始化Pygame
FPS = 60
WIDTH = 680
HEIGHT = 600
IP = '192.168.0.102' #須改為玩家的IP
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

class Button():
    def __init__(self,image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.image.get_rect(center=(self.x_pos,self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos,self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position): #偵測滑鼠點擊
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position): #鼠標掠過變色
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

botton_img = pygame.image.load("images/item/button.png")
def main_menu():
    pygame.display.set_caption("遊戲主畫面")

    pygame.mixer.music.load("music/music_menu.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while True:
        clock.tick(FPS)
        bg_img = pygame.image.load("images/item/bg_menu.png").convert()
        screen.blit(bg_img, (0,0))

        MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(botton_img, (340,350), "開始遊玩", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")
        TEACH_BUTTON = Button(botton_img, (340,450), "遊戲教學", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")
        QUIT_BUTTON = Button(botton_img, (340,550), "離開", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")

        for botton in [PLAY_BUTTON, TEACH_BUTTON, QUIT_BUTTON]:
            botton.changeColor(MOUSE_POS)
            botton.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    play()
                if TEACH_BUTTON.checkForInput(MOUSE_POS):
                    how_to_play()
                    pygame.display.set_caption("遊戲主畫面")
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    pygame.quit()
                    client.close()
                    sys.exit()
        pygame.display.update()

def how_to_play():
    pygame.display.set_caption("遊戲教學")

    bg_img = pygame.image.load("images/item/bg_teach.png")
    font = pygame.font.Font("fonts/font.ttf", 18)
    font_en = pygame.font.Font("fonts/font_en.ttf", 20)
    p1_0 = pygame.image.load("images/player/p1_0.png")
    p1_1 = pygame.image.load("images/player/p1_1.png")
    p1_2 = pygame.image.load("images/player/p1_2.png")
    p2_0 = pygame.image.load("images/player/p2_0.png")
    p2_1 = pygame.image.load("images/player/p2_1.png")
    p2_2 = pygame.image.load("images/player/p2_2.png")
    p1 = [p1_0, p1_1, p1_2, p1_1]
    p2 = [p2_0, p2_1, p2_2, p2_1]
    frame = 0
    running = True
    last_update = pygame.time.get_ticks()
    while running:
        clock.tick(FPS)
        screen.blit(bg_img, (0,0))

        MOUSE_POS = pygame.mouse.get_pos()

        img = pygame.transform.scale(botton_img,(200,50))
        BACK_BUTTON = Button(img, (575,40), "返回", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")

        p1_img = p1[frame]
        p2_img = p2[frame]
        p1_rect = p1_img.get_rect(center=(180,200))
        p2_rect = p2_img.get_rect(center=(500,200))

        text_en = font_en.render("1P", True, "white")
        text2_en = font_en.render("2P", True, "white")
        text_rect = text_en.get_rect(center=(180,150))
        text2_rect = text2_en.get_rect(center=(500,150))

        text = font.render("上下左右鍵移動", True, "white")
        text2 = font.render("空白鍵放水球", True, "white")
        text3_rect = text.get_rect(center=(500,310))
        text4_rect = text2.get_rect(center=(500,475))

        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(screen)
        screen.blit(p1_img, p1_rect)
        screen.blit(p2_img, p2_rect)
        screen.blit(text_en, text_rect)
        screen.blit(text2_en, text2_rect)
        screen.blit(text, text3_rect)
        screen.blit(text2, text4_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    running = False
        
        now = pygame.time.get_ticks()
        if now - last_update > 200:
            frame = (frame + 1) % 4
            last_update = now
        
        pygame.display.update()

def p1_win():
    pygame.mixer.music.stop()
    sounds['win'].play()
    win_images = []
    win_images.append(pygame.image.load("images/item/p1_win0.png"))
    win_images.append(pygame.image.load("images/item/p1_win1.png"))
    frame = 0
    last_frame = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        MOUSE_POS = pygame.mouse.get_pos()

        bg_img = pygame.image.load("images/item/bg_p1.png").convert()
        screen.blit(bg_img, (0,0))
        
        win_rect = win_images[0].get_rect(center=(340,300))

        img = pygame.transform.scale(botton_img,(200,50))
        BACK_BUTTON = Button(img, (340,450), "退出", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")

        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(screen)
        screen.blit(win_images[frame], win_rect)
        now = pygame.time.get_ticks()
        if now - last_frame > 200:
            frame = (frame + 1) % 2
            last_frame = now


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    main_menu()
        pygame.display.update()

def p2_win():
    pygame.mixer.music.stop()
    sounds['win'].play()
    win_images = []
    win_images.append(pygame.image.load("images/item/p2_win0.png"))
    win_images.append(pygame.image.load("images/item/p2_win1.png"))
    frame = 0
    last_frame = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        MOUSE_POS = pygame.mouse.get_pos()

        bg_img = pygame.image.load("images/item/bg_p2.jpg").convert()
        screen.blit(bg_img, (0,0))

        win_rect = win_images[0].get_rect(center=(340,300))

        img = pygame.transform.scale(botton_img,(200,50))
        BACK_BUTTON = Button(img, (340,450), "退出", pygame.font.Font("fonts/font.ttf", 20), "white", "Yellow")

        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(screen)
        screen.blit(win_images[frame], win_rect)
        now = pygame.time.get_ticks()
        if now - last_frame > 200:
            frame = (frame + 1) % 2
            last_frame = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    main_menu()
        pygame.display.update()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        down0_img = pygame.image.load('images/player/r_down0.png')
        down1_img = pygame.image.load('images/player/r_down1.png')
        down2_img = pygame.image.load('images/player/r_down2.png')
        left0_img = pygame.image.load('images/player/r_left0.png')
        left1_img = pygame.image.load('images/player/r_left1.png')
        left2_img = pygame.image.load('images/player/r_left2.png')
        right0_img = pygame.image.load('images/player/r_right0.png')
        right1_img = pygame.image.load('images/player/r_right1.png')
        right2_img = pygame.image.load('images/player/r_right2.png')
        up0_img = pygame.image.load('images/player/r_up0.png')
        up1_img = pygame.image.load('images/player/r_up1.png')
        up2_img = pygame.image.load('images/player/r_up2.png')
        self.images = {
            'up': [up0_img, up1_img, up2_img],
            'down': [down0_img, down1_img, down2_img],
            'left': [left0_img, left1_img, left2_img],
            'right': [right0_img, right1_img, right2_img]
        }
        self.current_frame = 1
        self.image = self.images['down'][1]
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(0, -2)
        self.rect.x = 40
        self.rect.y = 40
        self.speed = 3.5  # 速度
        self.power = 1  # 水球威力
        self.remain_bomb = 1
        self.overlap_bomb = []
        self.animation_timer = 0
        self.animation_delay = 1000
        self.keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
        self.key_pressed = {'up': False, 'down': False, 'left': False, 'right': False}

    def update(self):
        keys = pygame.key.get_pressed()
        self.prev_rect = self.rect.copy()  # 保留上一個位置
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.animate('left')
            self.key_pressed['left'] = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.animate('right')
            self.key_pressed['right'] = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.animate('up')
            self.key_pressed['up'] = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.animate('down')
            self.key_pressed['down'] = True
        else:
            if self.key_pressed['left']:
                self.current_frame = 1
                self.image = self.images['left'][1]
            elif self.key_pressed['right']:
                self.current_frame = 1
                self.image = self.images['right'][1]
            elif self.key_pressed['up']:
                self.current_frame = 1
                self.image = self.images['up'][1]
            elif self.key_pressed['down']:
                self.current_frame = 1
                self.image = self.images['down'][1]

        # 更新按鍵狀態
        for key in self.key_pressed:
            if not keys[self.keys[key]]:
                self.key_pressed[key] = False
        
        if(self.rect.right > WIDTH-40):
            self.rect.right = WIDTH-40
        if(self.rect.left < 40):
            self.rect.left = 40
        if(self.rect.bottom > HEIGHT-40):
            self.rect.bottom = HEIGHT-40
        if(self.rect.top < 40):
            self.rect.top = 40

        #石塊碰撞
        for tile in world.tile_list:
            if self.rect.colliderect(tile[1]):
                self.rect = self.prev_rect  # 將角色位置還原到上一個位置
                break

    def animate(self, direction):  # 走動動畫
        self.animation_timer += pygame.time.get_ticks() - self.animation_timer
        if self.animation_timer >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % 3
            self.image = self.images[direction][self.current_frame]
            self.animation_timer = 0

    def placeBomb(self): #放水球
        if(self.remain_bomb > 0):
            sounds['bubble'].play()
            bomb = Bomb(self,self.rect.centerx,self.rect.centery,world)
            collisions = pygame.sprite.spritecollide(bomb, players, False)
            for player in collisions:
                player.overlap_bomb.append(bomb)
            bombs.add(bomb)
            self.remain_bomb -=1

    def placeBomb_from_xy(self, x, y):
        bomb = Bomb(self, x, y, world)
        collisions = pygame.sprite.spritecollide(bomb, players, False)
        for player in collisions:
            player.overlap_bomb.append(bomb)
        bombs.add(bomb)

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        down0_img = pygame.image.load('images/player/b_down0.png')
        down1_img = pygame.image.load('images/player/b_down1.png')
        down2_img = pygame.image.load('images/player/b_down2.png')
        left0_img = pygame.image.load('images/player/b_left0.png')
        left1_img = pygame.image.load('images/player/b_left1.png')
        left2_img = pygame.image.load('images/player/b_left2.png')
        right0_img = pygame.image.load('images/player/b_right0.png')
        right1_img = pygame.image.load('images/player/b_right1.png')
        right2_img = pygame.image.load('images/player/b_right2.png')
        up0_img = pygame.image.load('images/player/b_up0.png')
        up1_img = pygame.image.load('images/player/b_up1.png')
        up2_img = pygame.image.load('images/player/b_up2.png')
        self.images = {
            'up': [up0_img, up1_img, up2_img],
            'down': [down0_img, down1_img, down2_img],
            'left': [left0_img, left1_img, left2_img],
            'right': [right0_img, right1_img, right2_img]
        }
        self.current_frame = 1
        self.image = self.images['down'][1]
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(0, -2)
        self.rect.x = 600
        self.rect.y = 520
        self.speed = 3.5  # 速度
        self.power = 1  # 水球威力
        self.remain_bomb = 1
        self.overlap_bomb = []
        self.animation_timer = 0
        self.animation_delay = 1000
        self.keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
        self.key_pressed = {'up': False, 'down': False, 'left': False, 'right': False}

    def update(self):
        keys = pygame.key.get_pressed()
        self.prev_rect = self.rect.copy()  # 保留上一個位置
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.animate('left')
            self.key_pressed['left'] = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.animate('right')
            self.key_pressed['right'] = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.animate('up')
            self.key_pressed['up'] = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.animate('down')
            self.key_pressed['down'] = True
        else:
            if self.key_pressed['left']:
                self.current_frame = 1
                self.image = self.images['left'][1]
            elif self.key_pressed['right']:
                self.current_frame = 1
                self.image = self.images['right'][1]
            elif self.key_pressed['up']:
                self.current_frame = 1
                self.image = self.images['up'][1]
            elif self.key_pressed['down']:
                self.current_frame = 1
                self.image = self.images['down'][1]

        # 更新按鍵狀態
        for key in self.key_pressed:
            if not keys[self.keys[key]]:
                self.key_pressed[key] = False

        if(self.rect.right > WIDTH-40):
            self.rect.right = WIDTH-40
        if(self.rect.left < 40):
            self.rect.left = 40
        if(self.rect.bottom > HEIGHT-40):
            self.rect.bottom = HEIGHT-40
        if(self.rect.top < 40):
            self.rect.top = 40

        #石塊碰撞
        for tile in world.tile_list:
            if self.rect.colliderect(tile[1]):
                self.rect = self.prev_rect  # 將角色位置還原到上一個位置
                break

    def animate(self, direction):  # 走動動畫
        self.animation_timer += pygame.time.get_ticks() - self.animation_timer
        if self.animation_timer >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % 3
            self.image = self.images[direction][self.current_frame]
            self.animation_timer = 0

    def placeBomb(self): #放水球
        if(self.remain_bomb > 0):
            sounds['bubble'].play()
            bomb = Bomb(self,self.rect.centerx,self.rect.centery,world)
            collisions = pygame.sprite.spritecollide(bomb, players, False)
            for player in collisions:
                player.overlap_bomb.append(bomb)
            bombs.add(bomb)
            self.remain_bomb -=1
    
    def placeBomb_from_xy(self, x, y):
        bomb = Bomb(self, x, y, world)
        collisions = pygame.sprite.spritecollide(bomb, players, False)
        for player in collisions:
            player.overlap_bomb.append(bomb)
        bombs.add(bomb)

def load_data_from_csv(filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

class World(object):
    def __init__(self):
        tile_size = 40
        self.tile_list = []
        self.data = load_data_from_csv("csv/rock_place.csv")

        # load raw_images
        rock_img = pygame.image.load('images/item/stone_block.png')

        row_count = 0
        for row in self.data:
            col_count = 0
            for tile in row:
                if tile == "0":
                    img = pygame.transform.scale(rock_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        block_img = pygame.image.load('images/item/block1.png')
        self.image = block_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def load_blocks(filename):
    blocks = pygame.sprite.Group()  # Group to hold all blocks
    data = load_data_from_csv("csv/block_place.csv")
    tile_size = 40
    row_count = 0
    for row in data:
        col_count = 0
        for tile in row:
            if tile == "0":
                x = col_count * tile_size
                y = row_count * tile_size
                block = Block(x, y)
                blocks.add(block) 
            col_count += 1
        row_count += 1
    return blocks

bomb0_img = pygame.image.load('images/item/bomb0.png')
bomb1_img = pygame.image.load('images/item/bomb1.png')
bomb_center_img = pygame.image.load('images/item/bomb_center.png')
bomb_up_img = pygame.image.load('images/item/bomb_up.png')
bomb_down_img = pygame.image.load('images/item/bomb_down.png')
bomb_left_img = pygame.image.load('images/item/bomb_left.png')
bomb_right_img = pygame.image.load('images/item/bomb_right.png')
expl = [bomb0_img,bomb1_img,bomb0_img,bomb1_img,bomb0_img,bomb1_img]
expl_direction = {'center':bomb_center_img,'up':bomb_up_img,'down':bomb_down_img,'left':bomb_left_img,'right':bomb_right_img}
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = expl_direction[dir] #爆炸方向
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 175:
            self.kill() 

class Bomb(pygame.sprite.Sprite):
    def __init__(self,player,x,y,world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world.data #石塊的位置
        self.owner = player
        self.power = player.power #爆炸從中心擴散格數
        self.image = expl[0]
        self.rect = self.image.get_rect()
        self.rect.x = x - x%40
        self.rect.y = y - y%40
        self.frame = 0
        self.init_time = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 250

    def update(self): #水球動畫
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: 
            self.last_update = now
            self.frame += 1

            if self.frame == len(expl):
                sounds['broke'].play()
                self.kill()
                self.owner.remain_bomb += 1
                self.create_explosion()
            else:
                self.image = expl[self.frame]
    
    def check_rock_collision(self,x,y):
        if x < 40 or x >= WIDTH-40 or y < 40 or y >= HEIGHT-40:
            return True
        x = int(x/40)
        y = int(y/40)
        if(self.world[y][x] == '0'):
            return True
        return False
    
    def create_explosion(self):
        expl_dir = Explosion(self.rect.x,self.rect.y,'center')
        explosion.add(expl_dir)
        for i in range(1,self.power+1): #left
            if not self.check_rock_collision(self.rect.x-40*i,self.rect.y):
                expl_dir = Explosion(self.rect.x-40*i,self.rect.y,'left')
                explosion.add(expl_dir)
            else:
                break
        for i in range(1,self.power+1): #right
            if not self.check_rock_collision(self.rect.x+40*i,self.rect.y):
                expl_dir = Explosion(self.rect.x+40*i,self.rect.y,'right')
                explosion.add(expl_dir)
            else:
                break
        for i in range(1,self.power+1): #up
            if not self.check_rock_collision(self.rect.x,self.rect.y-40*i):
                expl_dir = Explosion(self.rect.x,self.rect.y-40*i,'up')
                explosion.add(expl_dir)
            else:
                break
        for i in range(1,self.power+1): #down
            if not self.check_rock_collision(self.rect.x,self.rect.y+40*i):
                expl_dir = Explosion(self.rect.x,self.rect.y+40*i,'down')
                explosion.add(expl_dir)
            else:
                break

items_img = {'bubble':[], 'liquid':[], 'roller':[]}
items_img['bubble'].append(pygame.image.load('images/item/bubble_0.png'))
items_img['bubble'].append(pygame.image.load('images/item/bubble_1.png'))
items_img['liquid'].append(pygame.image.load('images/item/liquid_0.png'))
items_img['liquid'].append(pygame.image.load('images/item/liquid_1.png'))
items_img['roller'].append(pygame.image.load('images/item/roller_0.png'))
items_img['roller'].append(pygame.image.load('images/item/roller_1.png'))
class Item(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['bubble','liquid','roller'])
        self.image = items_img[self.type][0]
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 225:
            self.frame = (self.frame + 1) %2
            self.image = items_img[self.type][self.frame]
            self.last_update = now

def reset_game():
    players.empty()
    bombs.empty()
    explosion.empty()
    items.empty()

# 設置伺服器地址和端口
server_address = (IP, 8080)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(server_address)
    print("連接到伺服器")
except Exception as e:
    print(f"無法連接到伺服器: {e}")
    exit()

world = World()
players = pygame.sprite.Group()
bombs = pygame.sprite.Group()
explosion = pygame.sprite.Group()
items = pygame.sprite.Group()
players_statement = [{'x': 40, 'y': 40, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False},
                     {'x': 600, 'y': 520, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False}]
bombs_place = []
player_id = None
clock = pygame.time.Clock()

sounds = {}
sounds['start'] = pygame.mixer.Sound("music/sound_start.mp3")
sounds['bubble'] = pygame.mixer.Sound("music/sound_bubble.mp3")
sounds['broke'] = pygame.mixer.Sound("music/sound_broke.mp3")
sounds['item'] = pygame.mixer.Sound("music/sound_item.mp3")
sounds['win'] = pygame.mixer.Sound("music/sound_win.mp3")

data_lock = threading.Lock()
def receive_data():
    global players_statement, player_id, bombs_place
    buffer = ""
    while True:
        try:
            # 接收數據
            data = client.recv(1024).decode('utf-8')
            if not data:
                print("與伺服器的連接丟失")
                break
            buffer += data
            while '\n' in buffer:
                message, buffer = buffer.split('\n', 1)
                with data_lock:
                    try:
                        received_data = json.loads(message)
                        if 'player_id' in received_data:
                            player_id = received_data['player_id']
                            print(f"收到玩家ID: {player_id}")
                        else:
                            players_statement = received_data
                            if received_data[0]['bomb'] ==True:
                                if player_id == 1:
                                    bombs_place.append(received_data[0])
                            if received_data[1]['bomb'] ==True:
                                if player_id == 0:
                                    bombs_place.append(received_data[1])
                    except json.JSONDecodeError as e:
                        print(f"JSON 解碼錯誤: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON 解碼錯誤: {e}")
            break
        except Exception as e:
            print(f"接收數據時出錯: {e}")
            break

threading.Thread(target=receive_data).start()

def redraw_window():
    players.draw(screen)
    bombs.draw(screen)
    explosion.draw(screen)
    items.draw(screen)
    pygame.display.update()

def wait_for_player():
    bg_img = pygame.image.load("images/item/bg_wait.jpg").convert()
    font = pygame.font.Font("fonts/font.ttf", 20)
    texts = ['等候其他玩家連線', '等候其他玩家連線。', '等候其他玩家連線。。', '等候其他玩家連線。。。']
    frame = 0
    last_update = pygame.time.get_ticks()
    while not(players_statement[0]['start'] and players_statement[1]['start']):
        screen.blit(bg_img, (0, 0))

        text = font.render(texts[frame], True, "white")
        now = pygame.time.get_ticks()
        if now - last_update > 300:
            frame = (frame + 1) %4
            last_update = now
        
        text_rect = text.get_rect(center=(340,300))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
        pygame.display.update()

seed = 1000
def play():
    pygame.display.set_caption("爆爆王")
    bg_img = pygame.image.load("images/item/bg_map.png").convert()
    reset_game()

    global seed
    random.seed(seed)
    seed += 1

    global players_statement
    players_statement = [{'x': 40, 'y': 40, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False}, 
                     {'x': 600, 'y': 520, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False}]
    
    global bombs_place
    bombs_place = []
    # 等待接收到玩家ID
    while player_id is None:
        pass

    # 根據玩家ID初始化玩家對象
    if player_id == 0:
        player1 = Player()
        player2 = Player2()
        players_statement[0]['start'] = True
        try:
            message = json.dumps(players_statement[0]) + '\n'
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"發送數據時出錯: {e}")
    else:
        player1 = Player2()
        player2 = Player()
        players_statement[1]['start'] = True
        try:
            message = json.dumps(players_statement[1]) + '\n'
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"發送數據時出錯: {e}")
    players.add(player1)
    players.add(player2)

    wait_for_player()

    #初始化木箱
    blocks = load_blocks('csv/block_place.csv')

    #start動畫
    frame = 0
    last_frame = pygame.time.get_ticks()
    start_images = []
    start_images.append(pygame.image.load("images/item/word_start0.png"))
    start_images.append(pygame.image.load("images/item/word_start1.png"))
    start_images.append(pygame.image.load("images/item/word_start0.png"))
    start_images.append(pygame.image.load("images/item/word_start1.png"))
    start_rect = start_images[0].get_rect(center = (340,300))
    sounds['start'].play()

    pygame.mixer.music.load("music/music_game.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    run = True
    while run:
        clock.tick(FPS)
        screen.blit(bg_img, (0, 0))
        world.draw()

        if frame < 4:
            screen.blit(start_images[frame], start_rect)
            now = pygame.time.get_ticks()
            if now - last_frame > 100:
                frame += 1
                last_frame = now
        
        with data_lock:
            if player_id == 0:
                player2.rect.centerx = players_statement[1]['x']
                player2.rect.centery = players_statement[1]['y']
                player2.image = player2.images[players_statement[1]['dir']][players_statement[1]['frame']]
                if bombs_place:
                    player2.placeBomb_from_xy(bombs_place[0]['x'],bombs_place[0]['y'])
                    bombs_place.pop(0)
            else:
                player2.rect.centerx = players_statement[0]['x']
                player2.rect.centery = players_statement[0]['y']
                player2.image = player2.images[players_statement[0]['dir']][players_statement[0]['frame']]
                if bombs_place:
                    player2.placeBomb_from_xy(bombs_place[0]['x'],bombs_place[0]['y'])
                    bombs_place.pop(0)
        
        player1.update()
        bombs.update()
        explosion.update()
        items.update()

        place_bomb = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player1.remain_bomb > 0:
                        place_bomb = True
                    player1.placeBomb()

        #偵測玩家碰撞木箱
        collisions = pygame.sprite.spritecollide(player1, blocks, False)
        if collisions:
            player1.rect = player1.prev_rect

        #偵測玩家碰撞水球 (水球與玩家不重疊)
        for bomb in player1.overlap_bomb:
            if not bomb.rect.colliderect(player1.rect):
                player1.overlap_bomb.remove(bomb)

        collisions = pygame.sprite.spritecollide(player1, bombs, False)
        for bomb in collisions:
            if bomb not in player1.overlap_bomb:
                player1.rect = player1.prev_rect
        
        #炸掉木箱，掉道具
        collisions = pygame.sprite.groupcollide(blocks, explosion, True, False)
        for block in collisions:
            if random.random() > 0.6: #掉道具的機率
                item = Item(block.rect.center)
                items.add(item)

        #吃道具
        collisions = pygame.sprite.spritecollide(player1, items, True)
        for item in collisions:
            sounds['item'].play()
            if item.type == 'bubble':
                player1.remain_bomb += 1
            elif item.type == 'liquid' and player1.power<4:
                player1.power += 1
            elif item.type == 'roller' and player1.speed<5:
                player1.speed += 0.5
        collisions = pygame.sprite.spritecollide(player2, items, True)
        for item in collisions:
            if item.type == 'bubble':
                player2.remain_bomb += 1
            elif item.type == 'liquid' and player2.power<4:
                player2.power += 1
            elif item.type == 'roller' and player2.speed<5:
                player2.speed += 0.5

        dir = None
        for direction, pressed in player1.key_pressed.items():
            if pressed:
                dir = direction
                break
        
        player_message = {'x': player1.rect.centerx, 'y': player1.rect.centery, 'dir':dir, 'frame':player1.current_frame, 'bomb':place_bomb, 'start':False}
        try:
            message = json.dumps(player_message) + '\n'
            client.send(message.encode('utf-8'))

        except Exception as e:
            print(f"發送數據時出錯: {e}")

        #偵測玩家被炸
        collisions = pygame.sprite.groupcollide(players, explosion, True, False)
        for player in collisions:
            if player == player1:
                if player_id == 0:
                    p2_win()
                else:
                    p1_win()
            if player == player2:
                if player_id == 0:
                    p1_win()
                else:
                    p2_win()

        blocks.draw(screen)
        redraw_window()

    pygame.quit()
    client.close()

main_menu()