import pygame
from settings import *
vector = pygame.math.Vector2

pygame.display.set_caption("Mayhem")
screen = pygame.display.set_mode((Screen_width,Screen_height), 0, 32)
clock = pygame.time.Clock()

Player_sprite = pygame.image.load("Player.png").convert_alpha()
Player_sprite = pygame.transform.scale(Player_sprite, (Player_icon_size, Player_icon_size))
Player2_sprite = pygame.image.load("Player2.png").convert_alpha()
Player2_sprite = pygame.transform.scale(Player2_sprite, (Player_icon_size, Player_icon_size))
Bullet_sprite = pygame.image.load("Bullet.png").convert_alpha()
Bullet_sprite = pygame.transform.scale(Bullet_sprite, (Bullet_size, Bullet_size))

def collide_hit_box(a,b):
    return a.hit_box.colliderect(a,b)
# Function that overrides spritecollide using only the normal rect.

def collide_obstacle(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
        # Checks to see if any sprite hits anything in a group, and removes neither on impact.
        if hits:
            if hits[0].rect.centerx > sprite.hit_box.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_box.width / 2
            if hits[0].rect.centerx < sprite.hit_box.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_box.width / 2
            sprite.vel.x = 0
            sprite.hit_box.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if hits[0].rect.centery > sprite.hit_box.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_box.height / 2
            if hits[0].rect.centery < sprite.hit_box.centery:
                 sprite.pos.y = hits[0].rect.bottom + sprite.hit_box.height / 2
            sprite.vel.y = 0
            sprite.hit_box.centery = sprite.pos.y

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.player_1
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.Player_sprite
        self.rect = self.image.get_rect()
        self.hit_box = hit_box
        self.hit_box.center = self.rect.center
        # Added a hit-box to help with wall collision and hit detection.
        # Without it the sprite gets weird when colliding with walls after rotating
        self.vel = vector(0,0)
        self.pos = vector(Player_starting_position)
        self.rot = 0
        self.hp = Player_hp
        self.cooldown = 0



    def update(self):
        self.mechanics()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 # Holds the players rotation in degrees, while not extending beyond 360
        self.image = pygame.transform.rotate(self.game.Player_sprite, self.rot-90) # Rotated 90 degrees, to match up controls with image... still unclear why this is
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # Lets the sprite rotate around the center, instead of the corner.
        self.pos += self.vel * self.game.dt
        self.hit_box.centerx = self.pos.x
        collide_obstacle(self, self.game.obstacles, 'x')
        self.hit_box.centery = self.pos.y
        collide_obstacle(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_box.center

    def mechanics(self):
        self.rot_speed = 0
        self.vel = vector(0, Player_gravity) # Gives constant gravity downwards
        Press = pygame.key.get_pressed()
        if Press[pygame.K_LEFT]:
            self.rot_speed = Player_rotation_speed
            # Rotates the player around itself, at a given speed.
        if Press[pygame.K_RIGHT]:
            self.rot_speed = -Player_rotation_speed
        if Press[pygame.K_UP]:
            self.vel += vector(Player_speed, 0).rotate(-self.rot)
            # Changed from "= vector" to "+= vector" to maintain gravity while moving.
        if Press[pygame.K_DOWN]:
            self.vel += vector(-Player_speed, 0).rotate(-self.rot)
            # Added a reverse option
        if Press[pygame.K_INSERT]:
            # does the PEW PEW
            # Added a mechanic for bullet rate, to prevent it from shooting at every tick...
            check = pygame.time.get_ticks()
            if check - self.cooldown > Bullet_fire:
                self.cooldown = check
                direction = vector(1, 0).rotate(-self.rot)
                Bullet(self.game, self.pos, direction)

class Player2(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.player_2
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.Player2_sprite
        self.rect = self.image.get_rect()
        self.hit_box = hit_box
        self.hit_box.center = self.rect.center
        # Added a hit-box to help with wall collision and hit detection.
        # Without it the sprite gets weird when colliding with walls after rotating
        self.vel = vector(0, 0)
        self.pos = vector(Player2_starting_position)
        self.rot = 0
        self.hp = Player2_hp
        self.cooldown = 0

    def update(self):
        self.mechanics()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360  # Holds the players rotation in degrees, while not extending beyond 360
        self.image = pygame.transform.rotate(self.game.Player2_sprite, self.rot - 90)  # Rotated 90 degrees, to match up controls with image... still unclear why this is
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # Lets the sprite rotate around the center, instead of the corner.
        self.pos += self.vel * self.game.dt
        self.hit_box.centerx = self.pos.x
        collide_obstacle(self, self.game.obstacles, 'x')
        self.hit_box.centery = self.pos.y
        collide_obstacle(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_box.center

    def mechanics(self):
        self.rot_speed = 0
        self.vel = vector(0,Player_gravity)
        Press = pygame.key.get_pressed()
        if Press[pygame.K_a]:
            self.rot_speed = Player_rotation_speed
        if Press[pygame.K_d]:
            self.rot_speed = -Player_rotation_speed
        if Press[pygame.K_w]:
            self.vel += vector(Player_speed, 0).rotate(-self.rot)
        if Press[pygame.K_s]:
            self.vel += vector(-Player_speed, 0).rotate(-self.rot)
        if Press[pygame.K_SPACE]:
            check = pygame.time.get_ticks()
            if check == Bullet_fire:
                dir = vector(1,0).rotate(-self.rot)
                Bullet(self.game, self.pos, dir)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.obstacles, game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface(Obstacle_dimmensions)
        self.image.fill(Obstacle_colour)
        self.rect = self.image.get_rect()
        self.rect.center = (Screen_width/2, Screen_height/2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.Bullet_sprite
        # Gets the image from the "Game" class
        self.rect = self.image.get_rect()
        self.hit_box = self.rect
        self.pos = vector(pos)
        # vector2 gives us a clean vector for the bullet to travel, so that it does not affect the player position.
        self.rect.center = pos
        self.vel = dir * Bullet_vel

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.obstacles):
            # Checks to see if the bullet collides with any obstacle(s)?
            self.kill()
            # Removes the sprite from all groups
            # §§ might cause an issue since the bullets technically exist still, just are not drawn anymore.

#all_sprites = pygame.sprite.Group()
#obstacles_g = pygame.sprite.Group()
#bullet_g = pygame.sprite.Group()
#player = Player()
#player2 = Player2()
#obstacles = Obstacles()
#all_sprites.add(player)
#all_sprites.add(player2)
#all_sprites.add(obstacles)

#running = True
#while running:
#    clock.tick(FPS)
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#
#    all_sprites.update()
#
#    screen.fill(Background)
#    all_sprites.draw(screen)
#    pygame.display.flip()
#
#pygame.quit()
