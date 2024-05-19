import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, size=50, speed=5):
        super().__init__()
        self.size = size
        self.image = pygame.image.load('pngs/player.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - 2 * self.size
        self.speed = speed
        self.screen_width = screen_width
        self.lives = 1
        self.state = "normal"
        self.invincible_time = 0
        self.blink_timer = 0
        self.blink_interval = 10

    def update(self):
        if self.state == "normal":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.x < self.screen_width - self.size:
                self.rect.x += self.speed
        elif self.state == "invincible":
            self.invincible_time -= 1
            self.blink_timer = (self.blink_timer + 1) % (self.blink_interval * 2)
            if self.invincible_time <= 0:
                self.state = "normal"

    def draw(self, screen):
        if self.state == "invincible":
            # Only draw the player if blink_timer is in the first half of the interval
            if self.blink_timer < self.blink_interval:
                screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def make_invincible(self, invincible_time):
        self.state = "invincible"
        self.invincible_time = invincible_time

    def gain_life(self):
        self.lives += 1

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            # Game over logic here
            pass
        else:
            self.make_invincible(100)  # Player is invincible for 100 frames after losing a life
