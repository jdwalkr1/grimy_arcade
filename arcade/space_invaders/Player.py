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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < self.screen_width - self.size:
            self.rect.x += self.speed
