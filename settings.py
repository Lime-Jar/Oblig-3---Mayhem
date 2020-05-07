import pygame

# Game Settings:
Screen_width = 1200
Screen_height = 800
FPS = 120
Game_Title = "Mayhem"

# Player settings:
hit_box = pygame.Rect(0,0,40,40)
Player_starting_position = (Screen_width/4, Screen_height/2)
# Hardcoded player starting position based on screen width | Consider changing
Player_hp = 100
Player_icon_size = 40
Player_speed = 1
Player_rotation_speed = 0.5
Player_inertia = 0.75
Player_gravity = 0.2

# Player 2 settings:
Player2_starting_position = ((Screen_width/4)*3, Screen_height/2)
Player2_hp = 100

# Bullet Settings:
Bullet_vel = 120
Bullet_fire = 500
Bullet_damage = 10
Bullet_size = 6
# General settings:
Obstacle_dimmensions = (Screen_width/5, Screen_height/5)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
RED = (255,0,0)
Obstacle_colour = (WHITE)
Background = (BLACK)