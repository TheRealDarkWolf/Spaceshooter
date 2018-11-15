import pygame
import random
import os

WIDTH=480
HEIGHT=600
FPS=30
RED=(255, 0, 0)
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
GREEN=(0, 255, 0)
BLUE= (0, 0, 255)
YELLOW=(255, 255, 0)

#set up assets
game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, "img")
snd_folder= os.path.join(game_folder, "snd")

#text function for score
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    #sprite object
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius=20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2, HEIGHT-20)
        self.speedx=0
        self.speedy=0

    def update(self):
        self.speedx=0
        self.speedy=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx=9
        if keystate[pygame.K_LEFT]:
            self.speedx=-9
        self.rect.x +=self.speedx
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser.play()
        pygame.mixer.music.set_volume(0.4)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig=random.choice(meteor_image)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect=self.image.get_rect()
        self.radius=int((self.rect.width*0.85)/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x= random.randrange(0, WIDTH-self.rect.width)
        self.rect.y= random.randrange(-150,-100)
        self.speedy=random.randrange(5,10)
        self.speedx=random.randrange(-3,3)
        self.rot=0
        self.rot_speed = random.randrange( -8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top> HEIGHT + 10 or self.rect.left < -50 or self.rect.right> WIDTH+ 50:
            self.rect.x= random.randrange(0, WIDTH-self.rect.width)
            self.rect.y= random.randrange(-150,-100)
            self.speedy=random.randrange(5,10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_image, (9, 54))
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= -20

    def update(self):
        self.rect.y+=self.speedy
        #kill if moves out of screen
        if self.rect.bottom < 0:
            self.kill()
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()


#load graphics
background= pygame.image.load(os.path.join(img_folder, "starfield.png")).convert()
background_rect = background.get_rect()
player_image= pygame.image.load(os.path.join(img_folder, "playerShip1_green.png")).convert()
bullet_image= pygame.image.load(os.path.join(img_folder, "laserBlue01.png")).convert()
meteor_image= []
meteor_list=['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_med1.png'
            ,'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_image.append(pygame.image.load(os.path.join(img_folder, img)).convert())

#load all the sounds
laser= pygame.mixer.Sound(os.path.join(snd_folder, "Laser_Shoot.wav"))
expl_sounds =[]
for snd in ["Explosion4.wav", "Explosion10.wav"]:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, snd)))

pygame.mixer.music.load(os.path.join(snd_folder, "Eminem - Space Bound.ogg"))
all_sprites = pygame.sprite.Group()
mobs= pygame.sprite.Group()
pygame.mixer.music.set_volume(0.8)

player = Player()
all_sprites.add(player)
for i in range(8):
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)
bullets= pygame.sprite.Group()
score=0
pygame.mixer.music.play(loops=-1)
#game loop

running = True
while running:
    clock.tick(FPS)
    #process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #update
    all_sprites.update()

    #collision detection
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        pygame.mixer.music.set_volume(0.4)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False
    #draw/render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    #flip at the end only
    pygame.display.flip()
pygame.quit()
