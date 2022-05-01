import pygame
from sys import exit
from random import randint


def display_score(current_time,position = (130,50)):
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = position)
    screen.blit(score_surf,score_rect)

def calculate_score():
    return int(pygame.time.get_ticks()/1000) - start_time

def obstacle_movement(obstacle_list):
    if(obstacle_list):
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 210:
                screen.blit(fly_surf,obstacle_rect)
            else:
                screen.blit( snail_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                 return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index =0
        player_surf = player_walk[int(player_index)]


pygame.init()
pygame.display.set_caption("Runboi 7000")

screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

title_surf = test_font.render("Runboi",False, 'Green').convert()
title_rect = title_surf.get_rect(center=(400,50))

# Obstacles
monster_speed = 4

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [ fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames =[snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf= player_walk[player_index]
player_rect = player_surf.get_rect(midbottom= (80,300))
player_gravity = 0

# Intro Image
player_stand_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf,0,2)
player_stand_rect = player_surf.get_rect(midbottom= (370,180))
# Intro Txt
intro_text = test_font.render("Press SPACE to start",False, 'Black').convert()
intro_text_rect = intro_text.get_rect(center=(400,350))


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()

       if game_active:
           if event.type == snail_animation_timer:
               if snail_frame_index: snail_frame_index = 0
               else: snail_frame_index = 1
               snail_surf = snail_frames[snail_frame_index]
           if event.type == fly_animation_timer:
               if fly_frame_index: fly_frame_index = 0
               else: fly_frame_index = 1
               fly_surf = fly_frames[fly_frame_index]
           if event.type == obstacle_timer:
               if randint(0,2): obstacle_rect_list.append(fly_surf.get_rect(midbottom= (randint(900,1100),210)))
               else: obstacle_rect_list.append(snail_surf.get_rect(midbottom= (randint(900,1100),300)))
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE and player_rect.bottom == 300 : player_gravity = -20
       else:
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   game_active = True

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(title_surf,title_rect)
        display_score(calculate_score())

        # Player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >=300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #colission
        if collision(player_rect,obstacle_rect_list):
            game_active = False
            obstacle_rect_list.clear()
            score = calculate_score()


    else:
        screen.fill((90,129,162))
        screen.blit(player_stand_surf,player_stand_rect)
        if score >0 :display_score(score, (400,300))
        else: screen.blit(intro_text, intro_text_rect)
        start_time = int(pygame.time.get_ticks()/1000)

    pygame.display.update()
    clock.tick(60)