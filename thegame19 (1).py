# Imports
import pygame
import random
import json

# Window settings
GRID_SIZE = 64
WIDTH = 22 * GRID_SIZE
HEIGHT = 17 * GRID_SIZE
TITLE = "Swagotrons cool guy adventure"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)
GRAY = (175, 175, 175)

#stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3

# Load fonts
font_xs = pygame.font.Font(None, 12)
font_md = pygame.font.Font("assets/fonts/Dinomouse-Regular.otf", 32)
font_sm = pygame.font.Font("assets/fonts/Dinomouse-Regular.otf", 24)
font_lg = pygame.font.Font("assets/fonts/Dinomouse-Regular.otf", 64)
font_xl = pygame.font.Font("assets/fonts/Dinomouse-Regular.otf", 96)

# Load images
hero_img = pygame.image.load('assets/images/characters/player_idle.png').convert_alpha()
grass_dirt_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()
gem_img = pygame.image.load('assets/images/items/gem.png').convert_alpha()
background1_img = pygame.image.load('assets//levels/background1.png').convert_alpha()
zombie_img = pygame.image.load('assets/images/characters/enemy1a.png').convert_alpha()
Jibjad_img = pygame.image.load('assets/images/characters/jibjadsa.png').convert_alpha()
ghost_img = pygame.image.load('assets/images/characters/ghost.png').convert_alpha()
bee_img = pygame.image.load('assets/images/characters/bee.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()
door_img = pygame.image.load('assets/images/tiles/locked_door.png').convert_alpha()
door_top_img = pygame.image.load('assets/images/tiles/locked_door_top.png').convert_alpha()

# Load sounds


# Game classes
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
        
        self.vx = 0
        self.vy = 0
        
    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity
            
class Hero(Entity):
    def __init__(self, x, y, image):
        super().__init__( x, y, image)
        
        self.speed = 5
        self.jump_power = 15
        self.vx = 0
        self.vy = 0

        self.hearts = 1
        self.gems = 0
        self.score = 0
        
        self.hurt_timer = 0
    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE //2
        self.rect.centery = x * GRID_SIZE + GRID_SIZE //2

    def move_right(self):
        
    	self.vx = self.speed
    	
    def move_left(self):
    	self.vx = -1 * self.speed
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
            self.vy = -1 * self.jump_power
    
        
    def stop(self):
        self.vx = 0
        

    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                
        self.rect.y += self.vy
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
                
            self.vy = 0
                
    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)
            
    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hits:
            if self.rect.x < enemy.rect.x:
                self.vx =-15
            elif self.rect.x > enemy.rect.y:
                self.vx = 15

            if self.rect.y < enemy.rect.y:
                if self.vy > 0:
                    enemy.kill()
                self.vy =-5

                
            elif self.hurt_timer == 0:
                self.hearts -= 1
                self.hurt_timer = 1.0 * FPS
                print(self.hearts)
                print("OUCH!")
            else:
                self.hurt_timer -= 1

                if self.hurt_timer < 0:
                    self.hurt_timer = 0
                    


            
            
    
    def reached_goal(self):
       return pygame.sprite.spritecollideany(self, goal)


    
    def update(self):
        self.apply_gravity()
        self.check_world_edges()
        self.check_items()
        self.check_enemies()
        self.move_and_check_platforms()
    
class Gem(Entity):
    
    def __init__(self, x, y, image):
        super().__init__( x, y, image)
        
        
    def apply(self, character):
        character.gems += 1
        character.score += 10
        print(character.gems)

    	
    	 
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Flag(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

class Enemy(Entity):

    def __init__(self, x, y, image):
        super().__init__( x, y, image)

        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0
        
    def reverse(self):
       self.vx *= -1
       
    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.vx = -1 * self.speed

            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.vx = self.speed
                
        self.rect.y += self.vy
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
                self.vy = 0
                
    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
            
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.reverse()
            
    def check_platform_edges(self):
        self.rect.y +=2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        must_reverse = True

        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()
    

        
class Zombie(Enemy):

    def __init__(self, x, y, image):
        super().__init__( x, y, image)

    def update(self):
            self.move_and_check_platforms()
            self.check_world_edges()
            self.check_platform_edges()
            self.apply_gravity()

class Ghost(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__( x, y, image)

    def move(self):
         self.rect.x += self.vx
         
    def update(self):
            self.check_world_edges()
            self.move()




        

#Helper Functions
def show_start_screen():
    text = font_xl.render(TITLE, True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render('Press any key to start', True, BLACK)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)
    
def show_lose_screen():
    text = font_lg.render('Game Over!, You really suck man!', True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Want to lose again? Press 'r' to start over", True, BLACK)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)

def show_level_complete_screen():
    text = font_lg.render('Nice Level is Compelted', True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

 
def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])

def show_hud():
    text = font_md.render(str(hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)

    screen.blit(gem_img, [WIDTH -128, 16])
    text = font_md.render('x ' +str(hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = [WIDTH - 90, 16]
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36 + 16
        y = 16
        screen.blit(heart_img, [x, y])      


# Setup
def start_game():
    global hero, stage
    start = (3, 7)
    hero =  Hero(0,0, hero_img)
    stage = START
    
def start_level():
    global setup, items, platforms, hero, enemies, stage, player, goal, gravity, terminal_velocity
    
    platforms = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    enemies= pygame.sprite.Group()
    items  = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    
    with open('assets/levels/world-1.json') as f:
        data = json.load(f)

    
    #Blocks
       
    for loc in data['grass_locs']:
       platforms.add( Platform(loc[0], loc[1], grass_dirt_img))

    for loc in data['block_locs']:
        platforms.add( Platform(loc[0], loc[1], platform_img))
      
    #GOAL

    door_loc = (18, 14)
    
    doortop_loc = (18, 13)

    goal.add( Flag(door_loc[0], door_loc[1], door_img))

    goal.add(Flag(doortop_loc[0], doortop_loc[1], door_top_img))
    
    #HERO
        
    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)



    # Items
    for loc in data['gem_locs']:
        items.add( Gem(loc[0], loc[1], gem_img))

    #Enemies  

    for loc in data['zombie_locs']:
        enemies.add( Zombie(loc[0], loc[1], zombie_img))
        
    for loc in data['ghost_locs']:
        enemies.add(Ghost(loc[0], loc[1], ghost_img))
        

#Game Physics
    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']


# Game loop
running = True
grid_on = False

start_game()
start_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                stage = PLAYING
                
            elif stage == PLAYING:
                if event.key == pygame.K_UP:
                    hero.jump()

            elif stage == LOSE:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()

            if event.key == pygame.K_g:
                grid_on = not grid_on

            elif stage == START:
                stage = PLAYING
            
    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            hero.move_left()
            
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        
        else:
            hero.stop()
            
        

    
    # Game logic
    if stage == PLAYING:
        player.update()
        enemies.update()

        if hero.hearts == 0:
            stage =  LOSE
            
        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            countdown = 2 * FPS
    elif stage == LEVEL_COMPLETE:
        countdown -= 1
        if countdown <=0:
            start_level()
            stage = PLAYING
    




    
    # Drawing code
    screen.fill(SKY_BLUE)
    screen.blit(background1_img, [0,0])
    platforms.draw(screen)
    items.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    goal.draw(screen)
    show_hud()

    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()

    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()

        
    if grid_on:
        draw_grid()
    
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

