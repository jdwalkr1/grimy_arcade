import pygame
import random
import sys
from Player import Player

class SpaceInvaders:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.player = Player(self.WIDTH, self.HEIGHT)
        self.player_group = pygame.sprite.Group(self.player)

        self.enemy_size = 50
        self.enemy_img = pygame.image.load('pngs/enemy.png')
        self.enemy_img = pygame.transform.scale(self.enemy_img, (self.enemy_size, self.enemy_size))
        self.enemy_list = []
        self.enemy_speed = 2

        self.bullet_size = 10
        self.bullet_img = pygame.image.load('pngs/bullet.png')
        self.bullet_img = pygame.transform.scale(self.bullet_img, (self.bullet_size, self.bullet_size))
        self.bullet_list = []
        self.bullet_speed = 5

        self.score = 0
        self.font = pygame.font.SysFont(None, 35)

        self.explosion_sound = pygame.mixer.Sound('sounds/small-explosion-129477.mp3')

        # Extra life thresholds
        self.extra_life_thresholds = [50, 200, 500, 1000]
        self.extra_life_granted = {threshold: False for threshold in self.extra_life_thresholds}

    def set_level(self):
        if self.score < 50:
            self.enemy_speed = 2
        elif self.score < 100:
            self.enemy_speed = 3
        elif self.score < 300:
            self.enemy_speed = 4
        elif self.score < 750:
            self.enemy_speed = 5
        elif self.score < 1000:
            self.enemy_speed = 6
        else:
            self.enemy_speed = 8

    def drop_enemies(self):
        delay = random.random()
        if len(self.enemy_list) < 10 and delay < 0.1:
            x_pos = random.randint(0, self.WIDTH - self.enemy_size)
            y_pos = 0
            self.enemy_list.append([x_pos, y_pos])

    def draw_enemies(self):
        for enemy_pos in self.enemy_list:
            self.screen.blit(self.enemy_img, enemy_pos)

    def update_enemy_positions(self):
        for idx, enemy_pos in enumerate(self.enemy_list):
            if enemy_pos[1] >= 0 and enemy_pos[1] < self.HEIGHT:
                enemy_pos[1] += self.enemy_speed
            else:
                self.enemy_list.pop(idx)
                self.score += 1

    def collision_check(self):
        player_rect = self.player.rect
        for enemy_pos in self.enemy_list:
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], self.enemy_size, self.enemy_size)
            if self.detect_collision(player_rect, enemy_rect):
                if self.player.state == "normal":
                    self.player.lose_life()
                    self.enemy_list.remove(enemy_pos)
                    if self.player.lives <= 0:
                        return True
                elif self.player.state == "invincible":
                    self.enemy_list.remove(enemy_pos)
        return False

    def detect_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def bullet_hit(self):
        for bullet_pos in self.bullet_list:
            bullet_rect = pygame.Rect(bullet_pos[0], bullet_pos[1], self.bullet_size, self.bullet_size)
            for enemy_pos in self.enemy_list:
                enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], self.enemy_size, self.enemy_size)
                if self.detect_collision(bullet_rect, enemy_rect):
                    self.explosion_sound.play()
                    self.bullet_list.remove(bullet_pos)
                    self.enemy_list.remove(enemy_pos)
                    self.score += 1

                    self.check_for_extra_life()

                    break  # Exit the loop after a hit to avoid modifying the list during iteration

    def check_for_extra_life(self):
        for threshold in self.extra_life_thresholds:
            if self.score >= threshold and not self.extra_life_granted[threshold]:
                self.player.gain_life()
                self.extra_life_granted[threshold] = True

    def run(self):
        game_over = False
        clock = pygame.time.Clock()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet_pos = [self.player.rect.x + self.player.size / 2, self.player.rect.y]
                        self.bullet_list.append(bullet_pos)

            self.screen.fill(self.BLACK)

            self.player_group.update()

            for bullet_pos in self.bullet_list:
                bullet_pos[1] -= self.bullet_speed
                if bullet_pos[1] < 0:
                    self.bullet_list.remove(bullet_pos)

            self.drop_enemies()
            self.update_enemy_positions()
            self.set_level()
            self.bullet_hit()

            # Draw score
            score_text = "Score: " + str(self.score)
            score_label = self.font.render(score_text, 1, self.WHITE)
            self.screen.blit(score_label, (self.WIDTH - 200, self.HEIGHT - 40))

            # Draw lives
            lives_text = "Lives: " + str(self.player.lives)
            lives_label = self.font.render(lives_text, 1, self.WHITE)
            self.screen.blit(lives_label, (10, self.HEIGHT - 40))

            if self.collision_check():
                game_over = True
                break

            self.draw_enemies()

            # Draw player using the new draw method
            self.player.draw(self.screen)

            for bullet_pos in self.bullet_list:
                self.screen.blit(self.bullet_img, bullet_pos)

            clock.tick(30)
            pygame.display.update()


