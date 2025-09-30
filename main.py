import pygame
import os
import random
import csv
import button
import asyncio


BASE_DIR = os.path.dirname(__file__)
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

def load_level_csv(filename):
    path = os.path.join(LEVELS_DIR, filename)
    with open(path,newline="", encoding='utf-8') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data
pygame.init()




SCREEN_WIDTH = 800 
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

TILE_TYPES = 27
MAX_LEVELS = 5
screen_scroll = 0
bg_scroll   = 0
level = 1

start_game = False
start_intro = False
game_finished = False

total_coins = 0



start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha() 
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

reset_btn_size = 50
reset_btn_x = SCREEN_WIDTH - reset_btn_size  - 10
reset_btn_y = 10
restart_button = button.Button(reset_btn_size , reset_btn_y, restart_img, reset_btn_size / restart_img.get_width())
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()


plan1_img = pygame.image.load('img/Background/plan1.png').convert_alpha()
plan2_img = pygame.image.load('img/Background/plan2.png').convert_alpha()
plan3_img = pygame.image.load('img/Background/plan3.png').convert_alpha()
plan4_img = pygame.image.load('img/Background/plan4.png').convert_alpha()
plan5_img = pygame.image.load('img/Background/plan5.png').convert_alpha()

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    img_list.append(img)


   
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
fireball = False



BG = (144,203,120)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
PINK = (235,65,54)
ORANGE = (255,165,0)


bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
fire_ball_img = pygame.image.load('img/icons/fire_ball.png').convert_alpha()
purple_fireball_img = pygame.image.load('img/icons/purple_fire.png').convert_alpha()


item_boxes = {
    'Health'  : health_box_img,
    'Ammo'    : ammo_box_img,
    'Grenade' : grenade_box_img,

}

font = pygame.font.SysFont('Futura', 30)
small_font = pygame.font.SysFont('Futura' , 15)
tiny_font = pygame.font.SysFont ('Futura', 10)

skill_1_img = pygame.image.load('img/skill_1.jpg').convert_alpha()
skill_2_img = pygame.image.load('img/skill_2.jpg').convert_alpha( )



def load_level_csv(filename):
    path = os.path.join(LEVELS_DIR, filename)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True, text_col)
    screen.blit(img, (x,y))


def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()

    if level == 5:
        screen.fill(BLACK)
        for x in range(5):
            screen.blit(plan1_img, ((x * SCREEN_WIDTH) - bg_scroll * 0.5 , SCREEN_HEIGHT - plan1_img.get_height()))
            screen.blit(plan2_img, ((x * SCREEN_WIDTH) - bg_scroll * 0.5, SCREEN_HEIGHT - plan2_img.get_height()))
            screen.blit(plan3_img, ((x * SCREEN_WIDTH) - bg_scroll * 0.5, SCREEN_HEIGHT - plan3_img.get_height()))
            screen.blit(plan4_img, ((x * SCREEN_WIDTH) - bg_scroll * 0.5, SCREEN_HEIGHT - plan4_img.get_height()))
    else:
        for x in range(5):
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5 ,0))
            screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7 , SCREEN_HEIGHT - pine1_img.get_height() - 150))
            screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))



def super_jump_tile(player, world_data):
    player_feet_x = player.rect.centerx // TILE_SIZE
    player_feet_y = (player.rect.bottom + 1) // TILE_SIZE
    if 0 <= player_feet_y < ROWS and 0 <= player_feet_x < COLS:
        return world_data[player_feet_y][player_feet_x] == 12
    return False


def reset_level(): 
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explostion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    fireball_group.empty()
    boss_group.empty()
    sword_enemy_group.empty()
    coin_group.empty()
    
    
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data


def draw_text1(text, font, text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x - bg_scroll, y))

def draw_text1(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x - bg_scroll, y))


def draw_shop(player):
    shop_y = 100
    shop_width = 250
    shop_height = 280
    shop_x = SCREEN_WIDTH - shop_width - 60
    shop_rect = pygame.Rect(shop_x, shop_y, shop_width, shop_height)
    pygame.draw.rect(screen , (30,30,30) , shop_rect)
    pygame.draw.rect(screen, (100,100,100), shop_rect, 2)

    draw_text('SHOP', tiny_font , WHITE , shop_x + 3, shop_y + 3)
    draw_text(f'Coins: {player.coins}', tiny_font, (255,255,0), shop_x + 19, shop_y +35)

    water_shield_rect = pygame.Rect(shop_x + 10, shop_y + 65, 220, 30)
    if player.owns_water_shield:
        pygame.draw.rect(screen, (0,100,0), water_shield_rect)
        draw_text('Water Shield (Owned)', small_font, WHITE,shop_x + 15, shop_y + 70)

    else:
        color = (50,50,150) if player.coins >= player.water_shield_cost else (100,50,50)
        pygame.draw.rect(screen, color, water_shield_rect)
        draw_text(f'Water Shield - {player.water_shield_cost} coins', small_font, WHITE, shop_x + 15, shop_y + 70)
    
    fireball_rect = pygame.Rect(shop_x + 10, shop_y + 105, 220,30)
    if player.owns_fireball:
        pygame.draw.rect(screen, (0,100,0), fireball_rect)
        draw_text('Fireball (owned)', small_font, WHITE, shop_x + 15, shop_y + 110)
    else:
        color = (150,50,50) if player.coins >= player.fireball_cost else (100,50,50)
        pygame.draw.rect(screen, color, fireball_rect)
        draw_text(f'Fireball - {player.fireball_cost} coins', small_font, WHITE, shop_x + 15, shop_y + 110) 

    draw_text('Click to buy!', small_font, (200,200,200), shop_x + 10, shop_y + 145)
    draw_text('Press S to toggle shop',small_font, (150,150,150), shop_x + 10, shop_y + 170)

    return water_shield_rect, fireball_rect

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed,ammo,grenades , custom_animation_types  = None):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.dead = False
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.coins = 0
        self.max_health = self.health 
        self.char_type = char_type
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vison = pygame.Rect(0,0,150,20)
        self.idling = False
        self.idling_counter = 0
        self.is_dying = False
    

        self.shooting_animation_timer = 0

        self.owns_water_shield = False
        self.owns_fireball = False
        self.water_shield_cost = 10
        self.fireball_cost = 20
    
        self.water_shield_active = False
        self.water_shield_duration = 1500
        self.water_shield_cooldown = 18000
        self.water_shield_duration_timer = 0
        self.water_shield_cooldown_timer = 0


        self.fireball_active = False
        self.fireball_duration = 1000
        self.fireball_cooldown = 25000
        self.fireball_duration_timer = 0
        self.fireball_cooldown_timer = 0

        if custom_animation_types:
            animation_types = custom_animation_types
        else:
            animation_types = ['Idle','Run','jumping','death','shooting', 'water_shield','attack']
        for animation in animation_types:
            temp_list = []
            num_of_frames =len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img , (int(img.get_width() * scale) ,int(img.get_height() * scale)))
                temp_list.append(img) 
            self.animation_list.append(temp_list)
            

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def  update(self):
        self.update_animation()
        self.check_alive()


        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.shooting_animation_timer > 0:
            self.shooting_animation_timer -= 1
            if self.shooting_animation_timer == 0:
                if self.in_air:
                    self.update_action(2)
                elif self.action == 4:
                    self.update_action(0) 
                elif self.action == 6:
                    self.update_action(0)

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0
        
        if self.alive:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1


        self.vel_y += GRAVITY
        if self.vel_y >= 10:
            self.vel_y = 10
        dy += self.vel_y

        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx,  self.rect.y, self.width , self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy , self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        level_complete = False
        if any(exit.active and pygame.sprite.collide_rect(player, exit) for exit in exit_group):
            level_complete = True
        


        if self.char_type == 'player' and self.rect.top > SCREEN_HEIGHT:
            self.health = 0
        
        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right =  SCREEN_WIDTH



        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
            or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll ,  level_complete              
    
   
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            self.shooting_animation_timer = 20
            self.update_action(4)



    def cast_fireball(self):
            if not self.owns_fireball:
                return
            current_time = pygame.time.get_ticks()
            if not self.fireball_active and current_time >= self.fireball_cooldown_timer:
                fireball_projectile = Fireball(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery , self.direction)
                fireball_group.add(fireball_projectile)
                self.fireball_active = True
                self.fireball_duration_timer = current_time + self.fireball_duration
                self.fireball_cooldown_timer = current_time + self.fireball_cooldown
                self.update_action(6)
                self.shooting_animation_timer = 20

    def buy_water_shield(self):
        if self.coins >= self.water_shield_cost and not self.owns_water_shield:
            self.coins -= self.water_shield_cost
            self.owns_water_shield = True
            return True 
        return False 
    def buy_fireball(self):
        if self.coins >= self.fireball_cost and not self.owns_fireball:
            self.coins -= self.fireball_cost
            self.owns_fireball = True
            return True
        return False                                                                                                                                                                                                                                                        
    
    def ai(self):
        if self.alive and player.alive:
            distance_to_player = abs(self.rect.centerx - player.rect.centerx)
            if distance_to_player < 300:
                if player.rect.centerx > self.rect.centerx:
                    self.direction = 1
                    ai_moving_right = True
                    ai_moving_left = False
                else:
                    self.direction = -1
                    ai_moving_right = False
                    ai_moving_left = True
                
                if distance_to_player > 100:
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                else:
                    self.update_action(0)

                if distance_to_player < 200:
                    self.shoot()

                self.vison.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
            else:
                if self.idling == False and random.randint(1,200) == 1:
                    self.update_action(0)
                    self.idling = True
                    self.idling_counter = 50
                if self.vison.colliderect(player.rect):
                    self.shoot()
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1)
                        self.move_counter += 1
                        
                        self.vison.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)                  
                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1

                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

            if self.alive:
                self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 200

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1   
            
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.kill()
                
            elif self.action == 4:
                self.frame_index = 0
                self.update_action(0)
            elif self.action == 6:
                self.frame_index = 0
                self.update_action(0)
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0 and self.alive:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            coin = Coin(self.rect.centerx, self.rect.centery)
            coin_group.add(coin)
            print(f"Coin spanwed at ({self.rect.centerx} , {self.rect.centery}) for {self.char_type}")

    def activate_water_shield(self):
        if not self.owns_water_shield:
            return
        current_time = pygame.time.get_ticks()
        if not self.water_shield_active and current_time >= self.water_shield_cooldown_timer:
            self.water_shield_active = True
            self.water_shield_duration_timer = current_time + self.water_shield_duration
            self.water_shield_cooldown_timer = current_time + self.water_shield_cooldown
            self.update_action(5)
    

    def update_skills(self):
        current_time = pygame.time.get_ticks()
        if self.water_shield_active:
            if current_time >= self.water_shield_duration_timer:
                self.water_shield_active = False

                self.update_action(0)

        if self.fireball_active:
            if current_time >= self.fireball_duration_timer:
                self.fireball_active = False
                self.update_action(0)  

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
      
    

class SwordEnemy(Soldier):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.char_type = 'sword_enemy'
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        self.attack_range = TILE_SIZE * 1.5
        self.move_counter = 0


        temp_list_run = []          
        for i in range(6):
            img = pygame.image.load(f'img/{self.char_type}/run/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_run.append(img)
        self.animation_list.append(temp_list_run)
    
        temp_list_attack = []
        for i in range(12):
            img = pygame.image.load(f'img/{self.char_type}/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_attack.append(img)
        self.animation_list.append(temp_list_attack)    
        temp_list_death = []
        for i in range(21):
            img = pygame.image.load(f'img/{self.char_type}/death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img , (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_death.append(img)
        self.animation_list.append(temp_list_death)

        temp_list_hurt = []
        for i in range(2):
            img = pygame.image.load(f'img/{self.char_type}/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale )))
            temp_list_hurt.append(img)
        self.animation_list.append(temp_list_hurt)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.update_animation()
        self.check_alive()

    def update_animation(self):
        ANIMATION_COOLDOWN = 200
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time  > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
    

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)
        

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self,amount):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0 
        if self.action != 2:
            self.update_action(2)
        self.alive = False
     

    def ai(self):
        if self.alive and player.alive:
            if abs(self.rect.centerx - player.rect.centerx) > self.attack_range:
                if player.rect.centerx > self.rect.centerx:
                    ai_moving_right = True 
                    ai_moving_left = False
                else:
                    ai_moving_right = False
                    ai_moving_left = True
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(0)
            else:
                self.update_action(1)
                self.melee_attack()
        self.rect.x += screen_scroll
    

    def melee_attack(self):
        if self.attack_cooldown == 0:
            if self.rect.colliderect(player.rect):
                if not player.water_shield_active:
                    player.health -= 10
                    self.attack_cooldown = 70
                    self.shooting_animation_timer = 20



class   PurpleFireball(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = purple_fireball_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.flip = True if direction == -1 else False
        self.rect = self.rect.inflate(1,1)


    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        if pygame.sprite.spritecollide(player, purple_fireball_group, False):
            if player.alive and not player.water_shield_active:
                player.health -= 5
 
    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)       

class  Boss(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 999
        self.max_health = self.health
        self.char_type = char_type
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vison = pygame.Rect(0,0, 300, 50)
        self.idling = False
        self.idling_counter = 0
        self.is_dying = False
        self.attack_interval = 10700
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        
        self.sword_enemy_spawnTime = pygame.time.get_ticks()
        self.sword_enemy_spawnInterval = 3000
        self.spawned_attack = False
        self.has_fired_purple = False
        self.purple_fire_cooldown = 20000
        self.last_purple_time = pygame.time.get_ticks()
        self.boss_warning_time = 2000
        self.show_red_aura = False
        self.purple_fire_delay  = random.randint(0,5000)

        self.movement_direction = random.choice([-1,1])
        self.movement_change_time = pygame.time.get_ticks()
        self.movement_change_interval = random.randint(3000,6000)
        
        temp_list_idle = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.char_type}/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_idle.append(img)
        self.animation_list.append(temp_list_idle)



        temp_list_attack = []
        for i in range(13):
            img = pygame.image.load(f'img/{self.char_type}/attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_attack.append(img)
        self.animation_list.append(temp_list_attack)
        


        temp_list_death = []
        for i  in range(8):
              img = pygame.image.load(f'img/{self.char_type}/death/{i}.png').convert_alpha()
              img = pygame.transform.scale( img, (int(img.get_width() * scale), int(img.get_height() * scale)))
              temp_list_death.append(img)
        self.animation_list.append(temp_list_death)

        
        temp_list_hurt = []
        for i in range(2):
            img = pygame.image.load(f'img/{self.char_type}/hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list_hurt.append(img)
        self.animation_list.append(temp_list_hurt)


        self.image = self.animation_list[self.action][self.frame_index]                        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.update_action(2)
            self.alive = False
        elif self.action != 1 and self.action != 2:
            self.update_action(3)


    def update_animation(self):
        ANIMATION_COOLDOWN = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                elif self.action == 1:
                    self.frame_index = 0
                    self.update_action(0)
                elif self.action == 3  :
                    self.frame_index = 0
                    self.update_action(0)           
                else:
                    self.frame_index = 0    

        if self.action == 1 and self.frame_index >= len(self.animation_list[self.action]) // 2:
            current_time = pygame.time.get_ticks()
            if current_time - self.sword_enemy_spawnTime > self.sword_enemy_spawnInterval:

                self.spawn_sword_enemy()
                self.sword_enemy_spawnTime = current_time
                
        
              
        

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self,dx,dy):

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy 

    def ai(self):
        self.rect.x += screen_scroll
        current_time = pygame.time.get_ticks()

        if self.alive and player.alive:
            if current_time - self.movement_change_time > self.movement_change_interval:
                self.movement_direction = random.choice([-1,1])
                self.movement_change_time = current_time
                self.movement_change_interval = random.randint(3000,6000)
            
            player_direction = 1 if player.rect.centerx > self.rect.centerx else -1

            if self.movement_direction == 1:
                self.move(self.speed * player_direction, 0)
                self.flip = player_direction == -1
            else:
                self.move(-self.speed  * player_direction, 0)
                self.flip = player_direction == 1
             
            time_since_last_fireball = current_time - self.last_purple_time - self.purple_fire_delay
            if time_since_last_fireball >= self.purple_fire_cooldown - self.boss_warning_time - self.purple_fire_delay:
                self.show_red_aura = True
            

            if time_since_last_fireball >= self.purple_fire_cooldown:
                self.has_fired_purple = False
                self.fire_purple_fireball()
                self.last_purple_time = current_time
                self.purple_fire_delay = random.randint(0,5000)
                self.show_red_aura = False
            

            if current_time - self.last_attack_time > self.attack_interval:
                self.last_attack_time = current_time
                self.update_action(1)
                self.attack_cooldown = 60
                self.spawned_attack = False
            elif self.action == 0:
                pass

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


    def spawn_sword_enemy(self):
        spawn_x = self.rect.centerx + (self.direction * TILE_SIZE)
        spawn_y = self.rect.bottom - TILE_SIZE
        temp_enemy = SwordEnemy(spawn_x, spawn_y, 2.2, 3)
        temp_enemy.rect.bottom = spawn_y
    
        is_clear = True
        for tile in world.obstacle_list:
            if tile[1].colliderect(temp_enemy.rect):
                is_clear = False
                break
                
        if is_clear:
            sword_enemy = SwordEnemy(spawn_x, spawn_y, 2.2, 3)
            sword_enemy_group.add(sword_enemy)

            return
        else:
                spawn_x += self.direction * TILE_SIZE // 2

    def fire_purple_fireball(self):
        if not self.has_fired_purple:
            direction = 1 if player.rect.centerx > self.rect.centerx else -1
            purple_fireball = PurpleFireball(self.rect.centerx, self.rect.centery, direction)
            purple_fireball_group.add(purple_fireball)
            self.update_action(1)
            self.has_fired_purple = True  
                
    def draw(self):
        if self.show_red_aura:
            aura_surface = pygame.Sureface((self.rect.width + 20, self.rect.height + 20))
            aura_surface.set_alpha(100)
            aura_surface.fill((255, 0, 0))
            screen.blit(aura_surface, (self.rect.x - 10,  self.rect.y - 10))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive =False
            self.update_action(2)
            self.is_dying = True 
       
    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.update_action(2)
            self.alive = False
        elif self.action != 1 and self.action != 2:
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self,data):
        self.obstacle_list.clear()
        player  = None
        health_bar = None
        boss_health_bar = None
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = pygame.Rect( x  * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_data = (img, img_rect)
                    if ( 0 <= tile <= 8) or (22 <= tile <= 27) or tile == 12:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.2, 5,20,5)
                        health_bar = HealthBar(10,10, player.health, player.health)
                        boss_health_bar = HealthBar(SCREEN_WIDTH// 2 - 50, 55, 1000,1000)
  
                    elif tile == 16:
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.2, 2 , 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:
                        boss = Boss('boss', x * TILE_SIZE, y * TILE_SIZE, 2 , 1)
                        boss_group.add(boss)

   
        if player is None:
            player = Soldier('player', 100,100,1.2,5,20,5)
            health_bar = HealthBar(10,10, player.health, player.health)
            boss_health_bar = HealthBar(SCREEN_WIDTH // 2 - 50, 50 , 1000, 1000)
        return player, health_bar , boss_health_bar

    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite. __init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))



    def update(self):
        self.rect.x += screen_scroll
          
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x , y):
        pygame.sprite.Sprite. __init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
class Exit(pygame.sprite.Sprite):
    def __init__ (self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.active = False

    def update(self):
        self.rect.x += screen_scroll
    def draw(self,surface):
        if self.active:
            surface.blit(self.image, self.rect)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            self.kill()


class HealthBar():
    def __init__ (self,x,y,health,max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self,health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x,self.y - 2, 150, 20))
        pygame.draw.rect(screen,RED, (self.x, self.y,150,20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH - 100:
            self.kill()
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive and not player.water_shield_active:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group,False):
                    if enemy.alive:
                            enemy.health -= 25
                        
            
        for boss_enemy in boss_group:
            if pygame.sprite.spritecollide(boss_enemy, bullet_group, False):
                if boss_enemy.alive:
                    boss_enemy.take_damage(10)
                    self.kill()
                    
        for sword_enemy in sword_enemy_group:
            if pygame.sprite.spritecollide(sword_enemy, bullet_group, False):
                if sword_enemy.alive:
                    sword_enemy.take_damage(50)
                    
class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        for tile in world.obstacle_list:

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width , self.height):
                self.speed = 0

                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom


        level_complete = False
        if pygame.sprite.spritecollide( self, exit_group, False):
            level_complete = True
       
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
 
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explostion = Explosion(self.rect.x, self.rect.y, 0.5)
            explostion_group.add(explostion)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    if not player.water_shield_active:
                        player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50

            for boss_enemy in boss_group :
                if abs(self.rect.centerx - boss_enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - boss_enemy.rect.centery) < TILE_SIZE * 2:
                        boss_enemy.take_damage(25)
            

            for sword_enemy in sword_enemy_group:
                if abs(self.rect.centerx - sword_enemy.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - sword_enemy.rect.centerx) < TILE_SIZE * 2:
                    sword_enemy.take_damage(50)
                    self.kill()                   


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image = fire_ball_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.flip = True if direction == -1 else False
        self.rect = self.rect.inflate(20,20)
        self.has_hit = False


    def update(self):
        if self.has_hit:
            return
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()  

        hit_enemies = pygame.sprite.spritecollide(self, enemy_group, False)
        for enemy in hit_enemies:
            if enemy.alive:
                enemy.health -= 100
                break
             
        hit_bosses = pygame.sprite.spritecollide(self, boss_group, False)
        for boss_enemy in hit_bosses:
            if boss_enemy.alive and not self.has_hit:
                boss_enemy.take_damage(250)
                self.has_hit = True
                self.kill()
                break
        
        hit_sword_enemies = pygame.sprite.spritecollide(self, sword_enemy_group, False)
        for sword_enemy in hit_sword_enemies:
            if sword_enemy.alive:
                sword_enemy.health -= 75
                

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image , self.flip, False), self.rect) 

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_width() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    
    def update(self):
        self.rect.x  += screen_scroll
        EXPLOSION_SPEED = 4
        self.counter += 1
        
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE) , pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255, 0), (TILE_SIZE // 2, TILE_SIZE // 2,), TILE_SIZE // 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        print(f"Coin creared at ({x}, {y})")
    
    def update(self):
        self.rect.x += screen_scroll
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.color = colour
        self.speed = speed
        self.fade_counter = 0

    def update(self):
        self.rect.x += screen_scroll

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen , self.color, (0 - self.fade_counter ,0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0 , SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0,0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2 ))
            pygame.draw.rect( screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT ))
        if self.direction == 2:
            pygame.draw.rect(screen, self.color, (0,0, SCREEN_WIDTH, 0 +  self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True  
        
        return fade_complete

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)



start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 +  110,exit_img, 1 )
restart_button = button.Button(SCREEN_WIDTH - reset_btn_size - 70, reset_btn_y, restart_img, 1)
play_again_button = button.Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 + 50, restart_img, 1)


enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explostion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
sword_enemy_group = pygame.sprite.Group()
purple_fireball_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()


world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

level_data = load_level_csv(f'level{level}_data.csv')

for x, row in enumerate(level_data):
    for y, tile in enumerate(row):
        world_data[x][y] = int(tile)    

world = World()
player , health_bar, boss_health_bar  = world.process_data(world_data)

water_shield_icon = pygame.Surface((TILE_SIZE , TILE_SIZE), pygame.SRCALPHA)
pygame.draw.rect(water_shield_icon, (0,100,255,180), water_shield_icon.get_rect(), border_radius=5)
pygame.draw.circle(water_shield_icon , (200,230,255,200), (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 3)


def draw_inventory(player):  
    inventory_height = 70
    inventory_bottom = 20
    inventory_rect = pygame.Rect(0, SCREEN_HEIGHT - inventory_height - inventory_bottom, SCREEN_WIDTH, inventory_height)
    
    inventory_surface = pygame.Surface(inventory_rect.size, pygame.SRCALPHA)

    inventory_surface.fill((50,50,50,180))
    screen.blit(inventory_surface, inventory_rect.topleft)

    skill_slot_x = 20
    skill_slot_y = SCREEN_HEIGHT - inventory_height  - inventory_bottom + 10
    skill_slot_size = 50


    water_shield_slot_rect = pygame.Rect(skill_slot_x, skill_slot_y, skill_slot_size, skill_slot_size)
    fireball_slot_x = skill_slot_x + skill_slot_size + 20
    fireball_slot_rect = pygame.Rect(fireball_slot_x, skill_slot_y , skill_slot_size, skill_slot_size)

    # Water shield drawing logic
    screen.blit(pygame.transform.scale(skill_1_img, (skill_slot_size , skill_slot_size)), water_shield_slot_rect.topleft)
    if player.owns_water_shield:
        pygame.draw.rect(screen, (100,100,100), water_shield_slot_rect,2)
        screen.blit(pygame.transform.scale(skill_1_img,(skill_slot_size , skill_slot_size)), water_shield_slot_rect.topleft)
        current_time = pygame.time.get_ticks()
        cooldown_remaining = max(0, player.water_shield_cooldown_timer - current_time)
        if cooldown_remaining > 0:
            cooldown_ratio = cooldown_remaining / player.water_shield_cooldown
            cooldown_height = skill_slot_size * cooldown_ratio
            cooldown_rect = pygame.Rect(skill_slot_x, skill_slot_y + (skill_slot_size - cooldown_height) , skill_slot_size, cooldown_height)
            pygame.draw.rect(screen, (0,0,0,180), cooldown_rect)
            draw_text(f'{int(cooldown_remaining / 1000) + 1}', small_font, WHITE, skill_slot_x + skill_slot_size // 2 - 10, skill_slot_y + skill_slot_size // 2 - 10)        
        if player.water_shield_active:
            duration_remaining = max(0, player.water_shield_duration_timer - current_time)
            shield_surface = pygame.Surface((player.rect.width * 1.5, player.rect.height * 1.5) , pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0,150,255,100), (shield_surface.get_width() // 2, shield_surface.get_height() // 2), min(shield_surface.get_width(), shield_surface.get_height()) // 2)
            alpha = int(100 + 50 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            shield_surface.set_alpha(alpha)
            screen.blit(shield_surface , (player.rect.centerx - shield_surface.get_width() // 2, player.rect.centery  - shield_surface.get_height() // 2))       
            draw_text(f'{int(duration_remaining / 1000 ) + 1}', small_font , (255,255,0) , skill_slot_x + skill_slot_size // 2 - 10, skill_slot_x + skill_slot_size // 2-10)
    else:
        pygame.draw.rect(screen, BLACK, water_shield_slot_rect)
        pygame.draw.rect(screen, (100,100,100), water_shield_slot_rect,2)
        cost_color = WHITE if player.coins >= player.water_shield_cost else RED
        draw_text(f'{player.water_shield_cost}', small_font, cost_color, skill_slot_x + skill_slot_size // 2 - 10, skill_slot_y + skill_slot_size // 2 - 10)
        draw_text('coins', small_font, cost_color, skill_slot_x + 5, skill_slot_y + skill_slot_size - 15)

    # Fireball drawing logic
    screen.blit(pygame.transform.scale(skill_2_img, (skill_slot_size , skill_slot_size)) , fireball_slot_rect.topleft)

    if player.owns_fireball:
        pygame.draw.rect(screen, (100,100,100), fireball_slot_rect,2)
        screen.blit(pygame.transform.scale(skill_2_img, (skill_slot_size , skill_slot_size)) , fireball_slot_rect.topleft)
        current_time = pygame.time.get_ticks()
        fireball_cooldown_remaining = max(0, player.fireball_cooldown_timer - current_time)
        if fireball_cooldown_remaining > 0:
            fireball_cooldown_ratio = fireball_cooldown_remaining / player.fireball_cooldown
            fireball_cooldown_height = skill_slot_size * fireball_cooldown_ratio 
            cooldown_rect = pygame.Rect(fireball_slot_x, skill_slot_y + (skill_slot_size -   fireball_cooldown_height), skill_slot_size , fireball_cooldown_height)
            pygame.draw.rect(screen, (0,0,0,180), cooldown_rect)
            draw_text(f' {int (fireball_cooldown_remaining / 1000) + 1}' , small_font, WHITE, fireball_slot_x + skill_slot_size // 2 - 10, skill_slot_y + skill_slot_size // 2 - 10)
        if player.fireball_active:
            fireball_duration_remaining = max(0,player.fireball_duration_timer - current_time )
            draw_text(f'{int(fireball_duration_remaining / 1000) + 1}', small_font, WHITE, fireball_slot_x + skill_slot_size // 2 - 10, skill_slot_y + skill_slot_size // 2 - 10)
    else:
        pygame.draw.rect(screen, BLACK, fireball_slot_rect)
        pygame.draw.rect(screen, (100,100,100) , fireball_slot_rect, 2)
        cost_color = WHITE if player.coins >= player.fireball_cost else RED
        draw_text(f'{player.fireball_cost}' , small_font, cost_color, fireball_slot_x + skill_slot_size // 2 - 10, skill_slot_y + skill_slot_size // 2 - 10)
        draw_text('coins', small_font, cost_color, fireball_slot_x + 5, skill_slot_y + skill_slot_size - 15)

    separator_x = skill_slot_x + skill_slot_size + 10
    pygame.draw.line(screen, WHITE, (separator_x, skill_slot_y) , (separator_x, skill_slot_y + skill_slot_size), 2)

    return water_shield_slot_rect, fireball_slot_rect




show_shop = False
run = True
show_icons = False



while run:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_1:
                player.activate_water_shield()
            if event.key == pygame.K_2:
                fireball = True
            if event.key == pygame.K_s:
                show_shop = not show_shop
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.draw(screen):
                level = 1
                bg_scroll = 0
                world_data = reset_level()
                level_data = load_level_csv(f'level{level}_data.csv')
                for x, row in enumerate(level_data):
                    for y,tile in enumerate(row):
                        world_data[x][y] = int(tile)
                world = World()
                player, health_bar , boss_health_bar = world.process_data(world_data)
                player.coins = 0
                player.owns_water_shield = False
                player.owns_fireball = False
                game_finished = False
                start_game = True
                start_intro = True
                print("Game reset to level 1")
                continue 

            if show_shop:
                water_shield_shop_rect , fireball_shop_rect = draw_shop(player)

                if water_shield_shop_rect.collidepoint(mouse_pos):
                    if player.buy_water_shield():
                        print("What shield has been purchased from the shop!")
                    else:
                        print("Not enogh coins or already owned")
                if fireball_shop_rect.collidepoint(mouse_pos):
                    if player.buy_fireball():
                        print("Fireball has been purchased from shop!")
                    else:
                        print("Not enough coins or already owned")

            if water_shield_inventory_rect.collidepoint(mouse_pos) and not player.owns_water_shield:
                if player.buy_water_shield():
                    print("Water shield has been purchased")
                else:
                    print("Not enough coins or alraedy owned")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_SPACE:
                shoot = False
                
    clock.tick(FPS)

  

    
    water_shield_inventory_rect, fireball_inventory_rect = draw_inventory(player)

    if start_game == False:
        screen.fill(BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        draw_text('AMMO: ' , font, WHITE, 10 , 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (145 +( x * 10), 51))

        draw_text('GRENADES:', font , WHITE, 10,60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (205 + (x * 15), 75)) 
        draw_text('COINS:', font, WHITE, 10, 85)

        draw_text(str(player.coins), font, WHITE, 130, 90)
        
        alive_bosses = [boss for boss in boss_group if boss.alive]
        if alive_bosses:
            draw_text('BOSS HEALTH:', font, WHITE,SCREEN_WIDTH // 2 - 48,30)
            boss_health_bar.draw(alive_bosses[0].health)

        if level == 1:      
            draw_text1('W,A,S,D TO MOVE AND SPACEBAR TO SHOOT', font, WHITE, 200, 300)
            draw_text1(' Press Q TO THROW A GRENADE', font,WHITE,1000,200)
            draw_text1('Press S to view the Shop', font, WHITE, 1600,200)
            draw_text1('These are your powers. Remember Them as they can defeat bosses faster' , font , WHITE, 2300,200)
            draw_text1('Make sure you Killed  all the enemys to get the Maxiumum amount of coins', font , WHITE, 3700,300)
            player.update()
            player.draw()
        elif level == 2:
            draw_text1('Well Done You Have Completed The First Level', font, WHITE, 200,300)
            draw_text1('Buy the Water Shield', font, WHITE,2000,200)
            player.update()
            player.draw()

        elif level == 5:
            draw_text1('Press 2 To use Fireball to kill mulitple Enemies', font, WHITE,200,200)
            draw_text1(' The Boss is Ranged and ONE SHOTS, use Shield and move towards the fireball while the shield is active',font,WHITE,900,200)
            player.update()
            player.draw() 
        
        elif level == 6:
            screen.fill(BLACK)
            draw_text("Congratulations!", font, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 100)
            draw_text(" You  have Beatean The game!", font, WHITE, SCREEN_WIDTH // 2 - 180 , SCREEN_HEIGHT // 2 - 50)
            player.update()
            player.draw()
        else:
            player.update()
            player.draw()

        for boss_enemy in boss_group:
            boss_enemy.ai()
            boss_enemy.update()
            boss_enemy.draw()
        
        if level == 5:
            for boss_enemy in boss_group:
                if not boss_enemy.alive:
                    for exit in exit_group:
                        exit.active = True
        else:
            for exit in exit_group:
                 exit.active = True

        for enemy in enemy_group:    
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        for sword_enemy in sword_enemy_group:
            sword_enemy.ai()
            sword_enemy.update()
            sword_enemy.draw()
            
    
        coin_group.update()
        coin_group.draw(screen)

        for coin in pygame.sprite.spritecollide(player, coin_group, True):
            if player.alive:
                player.coins += 1
                total_coins += 1
 
        bullet_group.update()
        grenade_group.update()
        explostion_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explostion_group.draw(screen)
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        fireball_group.update()
        purple_fireball_group.update()
        
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explostion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        fireball_group.draw(screen)
        purple_fireball_group.draw(screen)


        for exit in exit_group:
            exit.draw(screen)


        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        

        for fireball_obj in fireball_group:
            fireball_obj.draw(screen)
 
        for purple_fireball_obj in purple_fireball_group:
            purple_fireball_obj.draw(screen)

        player.update_skills()
        


        
        if show_shop:
            water_shield_shop_rect , fireball_shop_rect = draw_shop(player)
       

        if player.alive:
            if player.water_shield_active:
                player.update_action(5)
            elif player.fireball_active:
                player.update_action(6)
            elif player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            if shoot:
                player.shoot()
                player.update_action(4)
            if grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
                print(player.grenades)

            if fireball:
                player.cast_fireball()
                fireball = False
        
            screen_scroll, level_complete = player.move(moving_left,moving_right)
            bg_scroll -= screen_scroll
            if level_complete:
                old_water = player.owns_water_shield
                old_fire = player.owns_fireball
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    level_data = load_level_csv(f'level{level}_data.csv')
                    for x, row in enumerate(level_data):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                        
                    world = World()
                    player, health_bar, boss_health_bar = world.process_data(world_data)
                    player.owns_water_shield = old_water
                    player.owns_fireball = old_fire
                    player.coins = total_coins
                else:
                    game_finished = True
        else:
           
            screen_scroll = 0
            if death_fade.fade():

                if restart_button.draw(screen) and not player.alive:
                    old_water = player.owns_water_shield
                    old_fire = player.owns_fireball
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0   
                    world_data =  reset_level()
            
                    level_data = load_level_csv(f'level{level}_data.csv')
                    for x, row in enumerate(level_data):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar, boss_health_bar = world.process_data(world_data)
                    player.owns_water_shield = old_water
                    player.owns_fireball = old_fire
                    player.coins = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not player.in_air:
            if super_jump_tile(player, world_data):
                player.vel_y = -22
            else:
                player.vel_y = -10
            player.in_air = True

    draw_inventory(player)
    restart_button.draw(screen)
    pygame.display.update()
    



pygame.quit()
