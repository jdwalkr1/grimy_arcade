import pygame
import random
import sys
from Player import Player

class SpaceInvaders:
    def __init__(self):
        pygame.init()

        self.top_scores = []

        self.initialize_default_top_scores()

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

        self.splat_img = pygame.image.load('pngs/splat.png')
        self.splat_img = pygame.transform.scale(self.splat_img, (self.enemy_size, self.enemy_size))
        self.splat_list = []
        self.splat_duration = 500

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
            self.enemy_speed = 1

    def drop_enemies(self):
        delay = random.random()
        if len(self.enemy_list) < 10 and delay < 0.1:
            x_pos = random.randint(0, self.WIDTH - self.enemy_size)
            y_pos = 0
            self.enemy_list.append([x_pos, y_pos])

    def draw_enemies(self):
        for enemy_pos in self.enemy_list:
            self.screen.blit(self.enemy_img, enemy_pos)

    def draw_bullets(self):
        for bullet_pos in self.bullet_list:
            self.screen.blit(self.bullet_img, bullet_pos)

    def draw_splats(self):
        current_time = pygame.time.get_ticks()
        for splat in self.splat_list:
            splat_time, splat_pos = splat
            if current_time - splat_time < self.splat_duration:
                self.screen.blit(self.splat_img, splat_pos)
            else:
                self.splat_list.remove(splat)  # Remove splat after duration

    def update_bullets(self):
        for bullet_pos in self.bullet_list:
            bullet_pos[1] -= self.bullet_speed
            if bullet_pos[1] < 0:
                self.bullet_list.remove(bullet_pos)

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
                print("Collision detected!")  # Debugging
                if self.player.state == "normal":
                    self.player.lose_life()
                    self.enemy_list.remove(enemy_pos)
                    if self.player.lives <= 0:
                        print("Player out of lives!")  # Debugging
                        return True  # Return True if player runs out of lives
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

                    # Record splat position and time
                    splat_pos = (enemy_pos[0], enemy_pos[1])
                    self.splat_list.append((pygame.time.get_ticks(), splat_pos))

                    self.check_for_extra_life()

                    break  # Exit the loop after a hit to avoid modifying the list during iteration

    def display_score_and_lives(self):
        score_text = "Score: " + str(self.score)
        score_label = self.font.render(score_text, 1, self.WHITE)
        self.screen.blit(score_label, (self.WIDTH - 200, self.HEIGHT - 40))

        lives_text = "Lives: " + str(self.player.lives)
        lives_label = self.font.render(lives_text, 1, self.WHITE)
        self.screen.blit(lives_label, (10, self.HEIGHT - 40))

    def check_for_extra_life(self):
        for threshold in self.extra_life_thresholds:
            if self.score >= threshold and not self.extra_life_granted[threshold]:
                self.player.gain_life()
                self.extra_life_granted[threshold] = True

    def display_top_scores(self):
        self.screen.fill(self.BLACK)  # Clear the screen
        title_text = "Top 5 High Scores"
        title_label = self.font.render(title_text, 1, self.WHITE)
        self.screen.blit(title_label, (self.WIDTH / 2 - title_label.get_width() / 2, 50))

        # Display top scores
        y_offset = 100
        for idx, (name, score) in enumerate(self.top_scores):
            score_text = f"{idx + 1}. {name}: {score}"
            score_label = self.font.render(score_text, 1, self.WHITE)
            self.screen.blit(score_label, (self.WIDTH / 2 - score_label.get_width() / 2, y_offset))
            y_offset += 30

        pygame.display.update()

    def update_top_scores(self, player_score):
        if any(player_score > score for _, score in self.top_scores):
            player_name = self.prompt_player_name()
            self.top_scores.append((player_name, player_score))
            self.top_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order
            self.top_scores = self.top_scores[:5]  # Keep only top 5 scores
            return True
        return False

    def prompt_player_name(self):
        input_box = pygame.Rect(self.WIDTH / 2 - 100, self.HEIGHT / 2 + 80, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        player_name = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode

            self.screen.fill(self.BLACK)
            prompt_text = "Congratulations! New High Score! Your name?"
            prompt_label = self.font.render(prompt_text, 1, self.WHITE)
            self.screen.blit(prompt_label, (self.WIDTH / 2 - prompt_label.get_width() / 2, self.HEIGHT / 2 - 50))

            txt_surface = self.font.render(player_name, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()

        return player_name

    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cleanup()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_pos = [self.player.rect.x + self.player.size / 2, self.player.rect.y]
                    self.bullet_list.append(bullet_pos)

    def initialize_default_top_scores(self):
        self.top_scores = [("McNasty", 1060), ("HoochieMama", 860), ("AshyBoi", 610), ("Joker", 500), ("YuhDawg", 200)]

    def display_game_over(self, new_high_score):
        # Clear the screen
        self.screen.fill(self.BLACK)

        # Display "Game Over" text
        game_over_text = "Game Over"
        game_over_label = self.font.render(game_over_text, 1, self.WHITE)
        self.screen.blit(game_over_label, (self.WIDTH / 2 - game_over_label.get_width() / 2, self.HEIGHT / 2 - 50))

        # Display new high scores if applicable
        if new_high_score:
            new_high_text = "New High Scores!"
            new_high_label = self.font.render(new_high_text, 1, self.WHITE)
            self.screen.blit(new_high_label, (self.WIDTH / 2 - new_high_label.get_width() / 2, self.HEIGHT / 2))

        # Prompt to play again
        prompt_text = "Play Again? (Y/N)"
        prompt_label = self.font.render(prompt_text, 1, self.WHITE)
        self.screen.blit(prompt_label, (self.WIDTH / 2 - prompt_label.get_width() / 2, self.HEIGHT / 2 + 50))

        # Display top scores
        self.display_top_scores()

        pygame.display.update()

        # Wait for input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True  # Play again
                    elif event.key == pygame.K_n:
                        return False  # Quit game

    def reset_game(self):
        self.player.rect.x = self.WIDTH // 2
        self.player.rect.y = self.HEIGHT - self.player.size - 10
        self.player.lives = 1
        self.enemy_list.clear()
        self.bullet_list.clear()
        self.splat_list.clear()  # Clear splats
        self.score = 0
        self.extra_life_granted = {threshold: False for threshold in self.extra_life_thresholds}

    def play_game(self):
        game_over = False
        clock = pygame.time.Clock()

        while not game_over:
            self.handle_player_input()
            self.screen.fill(self.BLACK)

            # Draw and update game elements
            self.player.toggle_blink()  # Toggle blinking
            self.player.draw(self.screen)
            self.draw_bullets()
            self.draw_enemies()
            self.draw_splats()  # Draw splats
            self.player_group.update()

            self.update_bullets()
            self.drop_enemies()
            self.update_enemy_positions()
            self.set_level()
            self.bullet_hit()

            # Draw score and lives
            self.display_score_and_lives()

            if self.collision_check():
                game_over = True

            pygame.display.update()
            clock.tick(60)

        # Handle game over and update top scores
        self.update_top_scores(self.score)

    def run(self):
        while True:  # Main game loop
            self.reset_game()  # Reset the game state
            self.play_game()  # Start the game

            new_high_score = self.update_top_scores(self.score)  # Update top scores and get new high score flag
            if new_high_score:
                # If the player achieved a new high score, prompt to play again immediately
                restart = True  # Assume player wants to play again
            else:
                # Game over screen
                restart = self.display_game_over(new_high_score)  # Display game over screen and get player's choice

            if not restart:  # If player chooses not to restart
                pygame.quit()
                sys.exit()

            # Reset the game state if the player chooses to play again
            self.reset_game()





