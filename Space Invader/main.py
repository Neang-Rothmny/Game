import pygame
import os
import time
import random
pygame.font.init()
pygame.mixer.init()

W, H = 750, 750
WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders")



# load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# EXPLOSION_SHEET = pygame.image.load(os.path.join("assets", "explosion_blue.png"))





# Load sound effects
LASER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "alienshoot1.ogg"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("sounds", "explosion.ogg"))
# GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "game.ogg"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (W, H))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(H):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
        LASER_SOUND.play()

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # mask tell us where pixels are and where they are not in the image
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(H):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        EXPLOSION_SOUND.play()


    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self, x,y, color, health = 100):
        super().__init__(x,y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



# def collide(obj1, obj2):
#     offset_x = obj2.x - obj1.x
#     offset_y = obj2.y - obj1.y
#     return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None 
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None:
        # flash_screen()  # Call a function to flash the screen
        return True
    return False

# def flash_screen():
#     flash_surface = pygame.Surface((W, H))
#     flash_surface.fill((255, 255, 255))
#     WIN.blit(flash_surface, (0, 0))
#     pygame.display.update()
#     pygame.time.delay(50)

# EXPLOSION_FRAMES = [pygame.image.load(os.path.join("assets", f"explosion_{i}.png")) for i in range(5)]

# def show_explosion(x, y):
#     for frame in EXPLOSION_FRAMES:
#         WIN.blit(frame, (x, y))
#         pygame.display.update()
#         pygame.time.delay(50)

# def fade_to_black():
#     fade_surface = pygame.Surface((W, H))
#     fade_surface.fill((0, 0, 0))
#     for alpha in range(0, 300, 5):
#         fade_surface.set_alpha(alpha)
#         WIN.blit(fade_surface, (0, 0))
#         pygame.display.update()
#         pygame.time.delay(30)


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5

    player_vel = 5

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (W - level_label.get_width() - 10, 10))

        
        for ememy in enemies:
            ememy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (W/2 - lost_label.get_width()/2, 350)) 

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            # fade_to_black()
            # GAME_OVER_SOUND.play()
            lost = True
            lost_count += 1 


        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # enemy = Enemy(random.randrange(50, W-100), random.randrange(-1500*level/5, -100), random.choice(["red", "blue", "green"])) 
                enemy = Enemy(random.randrange(50, W-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])) 
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_vel > 0:
            player.x -= player_vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_vel +player.get_width() < W:
            player.x += player_vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - player_vel > 0:
            player.y -= player_vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player_vel + player.get_height() + 15< H:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                if player.health <= 0:
                    player.explode()
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() > H:
                lives -= 1
                enemies.remove(enemy)
            


        player.move_lasers(-laser_vel, enemies)
        # for enemy in enemies[:]:
        #         if enemy.health <= 0:
        #             enemy.explode()
        #             enemies.remove(enemy)

def main_menu():
    
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (W/2 - title_label.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()