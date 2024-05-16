import pygame
import random
import sys
from Player import Player

class SpaceInvaders:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Invaders")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Player
        self.player = Player(self.WIDTH, self.HEIGHT)

        # Enemy
        self.enemy_size = 50
        self.enemy_img = pygame.image.load('pngs/enemy.png')
        self.enemy_img = pygame.transform.scale(self.enemy_img, (self.enemy_size, self.enemy_size))
        self.enemy_list = []
        self.enemy_speed = 2

        # Bullet
        self.bullet_size = 10
        self.bullet_img = pygame.image.load('pngs/bullet.png')
        self.bullet_img = pygame.transform.scale(self.bullet_img, (self.bullet_size, self.bullet_size))
        self.bullet_list = []
        self.bullet_speed = 5

        # Score
        self.score = 0
        self.font = pygame.font.SysFont(None, 35)

        # Explosion
        self.explosion_sound = pygame.mixer.Sound('sounds/small-explosion-129477.mp3')

    # Functions
    def set_level(self):
        if self.score < 20:
            self.enemy_speed = 2
        elif self.score < 40:
            self.enemy_speed = 3
        elif self.score < 60:
            self.enemy_speed = 4
        else:
            self.enemy_speed = 5

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
        player_rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.player.size, self.player.size)
        for enemy_pos in self.enemy_list:
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], self.enemy_size, self.enemy_size)
            if self.detect_collision(player_rect, enemy_rect):
                return True
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

            self.player.update()  # Update player position

            self.screen.fill(self.BLACK)

            # Update position of bullets
            for bullet_pos in self.bullet_list:
                bullet_pos[1] -= self.bullet_speed
                if bullet_pos[1] < 0:
                    self.bullet_list.remove(bullet_pos)

            # Update enemy positions
            self.drop_enemies()
            self.update_enemy_positions()
            self.set_level()
            self.bullet_hit()

            text = "Score: " + str(self.score)
            label = self.font.render(text, 1, self.WHITE)
            self.screen.blit(label, (self.WIDTH - 200, self.HEIGHT - 40))

            if self.collision_check():
                game_over = True
                break

            self.draw_enemies()

            # Draw player
            self.screen.blit(self.player.image, self.player.rect)

            # Draw bullets
            for bullet_pos in self.bullet_list:
                self.screen.blit(self.bullet_img, bullet_pos)

            pygame.display.update()
            clock.tick(30)


