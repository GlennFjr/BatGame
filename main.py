import pygame
from sys import exit
import random
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.speed = 5
        self.direction = 'left'
        self.x_offset = 10
        self.score = 0
        self.current_level = 1
        self.next_level = 0
        player_model1 = pygame.image.load('Assets/bat1.png').convert_alpha()
        player_model2 = pygame.image.load('Assets/bat2.png').convert_alpha()
        self.player_model = [player_model1, player_model2]
        self.player_index = 0
        self.image = self.player_model[self.player_index]
        self.rect = self.image.get_rect(center=(400, 200))

        self.attack = Attack()

    def update(self):
        self.animation_state()
        self.boundary_check()
        self.level()

    def animation_state(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_model):
            self.player_index = 0
        self.image = self.player_model[int(self.player_index)]
        keys = pygame.key.get_pressed()
        dx, dy = self.handle_input(keys, attack)

        self.rect.x += dx
        self.rect.y += dy

        if self.direction == 'right':
            self.image = pygame.transform.flip(self.player_model[int(self.player_index)], True, False)
        else:
            self.image = self.player_model[int(self.player_index)]

    def handle_input(self, keys, attack):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = 'left'
        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = 'right'
        if keys[pygame.K_SPACE]:
            attack.sprite.in_motion = False
            attack.sprite.is_attacking = True
            if self.direction == 'left':
                attack.sprite.shot_right = False
            else:
                attack.sprite.shot_right = True
        else:
            attack.sprite.is_attacking = False

        return dx, dy

    def boundary_check(self):
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 335:
            self.rect.y = 335
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 735:
            self.rect.x = 735

    def level(self):
        if self.score == 0:

            enemy_exists = False
            for active_enemy in active_enemy_list:
                if active_enemy == 'blackbat':
                    enemy_exists = True
                    break

            if not enemy_exists:
                active_enemy_list.append('blackbat')
        if self.score == 0:

            enemy_exists = False
            for active_enemy in active_enemy_list:
                if active_enemy == 'greenbat':
                    enemy_exists = True
                    break

            if not enemy_exists:
                active_enemy_list.append('greenbat')


class Attack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_attacking = False
        self.in_motion = False
        self.speed = 10
        self.loaded = False

        attack_model1 = pygame.image.load('Assets/wave1.png').convert_alpha()
        attack_model2 = pygame.image.load('Assets/wave2.png').convert_alpha()
        self.attack_model = [attack_model1, attack_model2]
        self.attack_index = 0

        attack_start1 = pygame.image.load('Assets/attack_start1.png').convert_alpha()
        attack_start2 = pygame.image.load('Assets/attack_start2.png').convert_alpha()
        self.attack_start_model = [attack_start1, attack_start2]

        self.image = self.attack_model[self.attack_index]
        self.rect = self.image.get_rect(center=(0, -200))
        self.shot_right = True

        # image_rect = pygame.Rect(
        #     sprite_rect.x + offset_x,
        #     sprite_rect.y + offset_y,
        #     sprite_width,
        #     sprite_height
        # )

    def update(self):
        self.animation_state()
        self.movement()
        self.attack_hit()

    def animation_state(self):
        # Alternates frames
        self.attack_index += 0.1
        if self.attack_index >= len(self.attack_model):
            self.attack_index = 0

        if self.shot_right and self.in_motion:
            self.image = self.attack_model[int(self.attack_index)]
        elif not self.shot_right and self.in_motion:
            self.image = self.attack_model[int(self.attack_index)]
            self.image = pygame.transform.flip(self.image, True, False)

        if self.shot_right and not self.in_motion:
            self.image = self.attack_start_model[int(self.attack_index)]
        elif not self.shot_right and not self.in_motion:
            self.image = self.attack_start_model[int(self.attack_index)]
            self.image = pygame.transform.flip(self.image, True, False)

    def movement(self):
        if self.is_attacking:
            self.rect = self.image.get_rect()
            self.rect.y = player.sprite.rect.y + 6
            if player.sprite.direction == 'right':
                self.rect.x = player.sprite.rect.x + 50
            else:
                self.rect.x = player.sprite.rect.x - 50
        if not self.is_attacking and self.in_motion:
            if self.shot_right:
                self.rect.x += self.speed
            elif not self.shot_right:
                self.rect.x -= self.speed
        if self.rect.x <= -50 or self.rect.x >= 850:
            self.in_motion = False
            self.rect.y = 500

    # def destroy(self):
    #     if self.rect.x <= -50 or self.rect.x >= 850:
    #

    def attack_hit(self):
        for bat in enemy:
            if pygame.sprite.spritecollide(attack.sprite, enemy, not attack.sprite.is_attacking) and self.rect.x <= 700 and not attack.sprite.is_attacking:
                player.sprite.score += 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.go = False

        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.current_time = 0

        if self.type == 'redbat':
            self.health = 1
            enemy_frame1 = pygame.image.load('Assets/redbat1.png').convert_alpha()
            enemy_frame2 = pygame.image.load('Assets/redbat2.png').convert_alpha()
            self.enemy_model = [enemy_frame1, enemy_frame2]
            enemy_y_pos = random.randint(100, 400)
            enemy_x_pos = random.randint(900, 1100)

        elif self.type == 'blackbat':
            self.health = 1
            enemy_frame1 = pygame.image.load('Assets/blackbat1.png').convert_alpha()
            enemy_frame2 = pygame.image.load('Assets/blackbat2.png').convert_alpha()
            self.enemy_model = [enemy_frame1, enemy_frame2]
            enemy_y_pos = 60
            enemy_x_pos = random.randint(0, 750)

        elif self.type == 'greenbat':
            self.health = 1
            enemy_frame1 = pygame.image.load('Assets/greenbat1.png').convert_alpha()
            enemy_frame2 = pygame.image.load('Assets/greenbat2.png').convert_alpha()
            enemy_frame3 = pygame.image.load('Assets/greenbat3.png').convert_alpha()
            enemy_frame1 = pygame.transform.rotozoom(enemy_frame1, 0, 2)
            enemy_frame2 = pygame.transform.rotozoom(enemy_frame2, 0, 2)
            enemy_frame3 = pygame.transform.rotozoom(enemy_frame3, 0, 2)
            self.enemy_model = [enemy_frame1, enemy_frame2, enemy_frame3]
            enemy_y_pos = random.randint(100, 400)
            enemy_x_pos = random.randint(900, 1100)

        else:
            enemy_x_pos = 400
            enemy_y_pos = 200

        self.enemy_index = 0
        self.image = self.enemy_model[self.enemy_index]
        self.rect = self.image.get_rect(midbottom=(enemy_x_pos, enemy_y_pos))

    def animation_state(self):
        self.enemy_index += 0.1
        if self.enemy_index >= len(self.enemy_model):
            self.enemy_index = 0
        self.image = self.enemy_model[int(self.enemy_index)]

        # if self.direction == 'right':
        #     self.image = pygame.transform.flip(self.enemy_model[int(self.enemy_index)], True, False)
        # else:
        #     self.image = self.enemy_model[int(self.enemy_index)]

    def update(self):
        self.animation_state()
        self.movement()
        self.destroy()

    def movement(self):
        if self.type == 'redbat':
            self.rect.x -= 6
        if self.type == 'blackbat':
            for bat in enemy:
                if bat.elapsed_time >= delay_times[bat.type] and bat.type == 'blackbat':
                    bat.rect.y += 4
        if self.type == 'greenbat':
            self.rect.x -= 3

    def destroy(self):
        if self.rect.x <= -50 or self.rect.y >= 450:
            self.kill()


def display_score():
    score_surf = score_font.render('Score: ' + str(player.sprite.score), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemy, False):
        enemy.empty()

        return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Bat Game')
score_font = pygame.font.Font('Assets/font/fancy.otf', 50)
clock = pygame.time.Clock()
game_active = False
active_enemy_list = ['redbat']

player = pygame.sprite.GroupSingle()
player.add(Player())

attack = pygame.sprite.GroupSingle()
attack.add(Attack())

enemy = pygame.sprite.Group()

background_surface = pygame.image.load('Assets/cave_back.png').convert()
batground = pygame.image.load('Assets/batground.png').convert()


# Timers
delay_times = {'blackbat': 2000, 'redbat': 0, 'greenbat': 0}

attack_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(attack_animation_timer, 1500)

enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, 800)

animation_pause_timer = pygame.USEREVENT + 3
pygame.time.set_timer(animation_pause_timer, 100)

while True:

    for bat in enemy:
        bat.current_time = pygame.time.get_ticks()
        bat.elapsed_time = bat.current_time - bat.start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                attack.sprite.is_attacking = False
                attack.sprite.in_motion = True
                if player.sprite.direction == 'right':
                    attack.sprite.shot_right = True
                else:
                    attack.sprite.shot_right = False

        if game_active:
            # Enemy Spawns
            if event.type == enemy_timer:
                enemy.add(Enemy(choice(active_enemy_list)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player.rect = player.sprite.image.get_rect(center=(400, 200))
                game_active = True

                #   Doesn't Evven WORK
                #  Want player to reset after game starts


                player.sprite.score = 0
                attack.sprite.is_attacking = False
                attack.sprite.rect.x = 900
        # if event.type == attack_animation_timer:
        #     attack_group.add('wave')

    if game_active:
        screen.blit(background_surface, (0, 0))
        score = display_score()

        player.draw(screen)
        player.update()
        attack.draw(screen)
        attack.update()
        enemy.draw(screen)
        enemy.update()

        # Collisions
        game_active = collision_sprite()
    else:

        score_message = score_font.render('Your score: ' + str(player.sprite.score), False, 'White')
        score_message_rect = score_message.get_rect(center=(300, 200))

        game_message = score_font.render('Press Enter to Play!', False, 'White')
        game_message_rect = game_message.get_rect(center=(300, 300))

        screen.blit(batground, (0, 0))
        if player.sprite.score == 0:
            player.sprite.score = 0
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(game_message, game_message_rect)


    pygame.display.update()
    clock.tick(60)
