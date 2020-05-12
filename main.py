import pygame
from settings import *
from sprites import *
vector = pygame.math.Vector2

def draw_player_hp(surf, x, y, stat):
    # a basic tool for showing player hp
    if stat < 0:
        stat = 0
    # prevent hp from showing weird values
    Hp_bar_length = 100
    Hp_bar_height = 20
    fill = stat * Hp_bar_length
    outline_rect = pygame.Rect(x,y, Hp_bar_length, Hp_bar_height)
    fill_rect = pygame.Rect(x, y, fill, Hp_bar_height)
    if stat > 0.7:
        color = GREEN
    elif stat > 0.3:
        color = YELLOW
    else:
        color = RED
    # Colors the bar based on hp
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)
    # Draws the hp-bar with a white outline for contrast

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Screen_width,Screen_height), 0, 32)
        pygame.display.set_caption(Game_Title)
        self.clock = pygame.time.Clock()
        self.get_data()

    def get_data(self):
        self.Player_sprite = pygame.image.load("Player.png").convert_alpha()
        self.Player_sprite = pygame.transform.scale(self.Player_sprite, (Player_icon_size, Player_icon_size))
        self.Player2_sprite = pygame.image.load("Player2.png").convert_alpha()
        self.Player2_sprite = pygame.transform.scale(self.Player2_sprite, (Player_icon_size, Player_icon_size))
        self.Bullet_sprite = pygame.image.load("Bullet.png").convert_alpha()
        self.Bullet_sprite = pygame.transform.scale(self.Bullet_sprite, (Bullet_size, Bullet_size))
        # Prepares the Images for use
        # "libpng warning: iCCP: known incorrect sRGB profile" error, still unsure what this means | However does not stop the program from running.

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player_1 = pygame.sprite.Group()
        self.player_2 = pygame.sprite.Group()
        self.player = Player(self)
        self.player2 = Player2(self)

    def run(self):
        self.playing = True
        self.new()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def exit(self):
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.K_ESCAPE:
                self.exit()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.groupcollide(self.player_1, self.bullets, False, True, collide_hit_box)
        # Checks if a bullet hits the player, removes the bullet, but not the player on impact.
        # Should use the collide_hit_box instead of the normal sprite.rect when determining hit
        for hit in hits:
            self.player.hp -= Bullet_damage
            # §§ Could add a random element to gun damage
            #hit.vel = vector(0,0)
            # Adds a bit of "stun" on impact
            if self.player.hp <= 0:
                print("Player 2 wins")
                player.kill()
        hits = pygame.sprite.groupcollide(self.player_2, self.bullets, False, True, collide_hit_box)
        for hit in hits:
            self.player2.hp -= Bullet_damage
            #hit.vel = vector(0, 0)
            if self.player2.hp <= 0:
                print("Player 1 wins")
                player2.kill()

    def draw(self):
        self.screen.fill(Background)
        for sprite in self.all_sprites:
            self.screen.blitt(sprite.image, self)
        self.all_sprites.draw(self.screen)
        draw_player_hp(self.screen, 10, 10, self.player.hp / Player_hp)
        draw_player_hp(self.screen, Screen_width-10, 10, self.player2.hp / Player2_hp)
        # Draws the 2 hp bars
        # §§ Should fix the player 2 hp bar to shrink the right way
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        Game().new()
        Game().run()
