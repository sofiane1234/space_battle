import time
import pygame

from bullets import Bullet

class SecondPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, speed, image, img_bullet):
        super().__init__()

        self.pos = pos
        self.speed = speed
        self.angle_speed = 2.5
        self.scale = 1.5    
        self.rotation = 0
        self.direction = pygame.math.Vector2(0,1)
        self.vies = 5
        
        self.can_shoot = True
        self.bullet_timer = 0.3
        self.start_time = 0
        self.img_bullet = img_bullet
        self.image = image
        self.orig_img = image
        self.rect = self.image.get_rect()
    
    def get_inputs(self):
        keys = pygame.key.get_pressed()

        vector = [0, 0]
        if keys[pygame.K_k]:
            vector[0] -= 1
        if keys[pygame.K_m]:
            vector[0] += 1
        if keys[pygame.K_o]:
            vector[1] -= 1
        if keys[pygame.K_l]:
            vector[1] += 1
        self.bouger(vector[0], vector[1])

    def tirer(self):
        if self.can_shoot:
            self.can_shoot = False    
            self.start_time = time.time()
            return Bullet(self.pos, (self.direction.x, self.direction.y), 13, self.img_bullet)
    
    def update(self):
        self.image = pygame.transform.rotozoom(self.orig_img, self.rotation, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
       
        if time.time() - self.start_time >= self.bullet_timer:
            self.can_shoot = True

    def bouger(self, angle_x, angle_y):
        bullet_rotate = angle_x * self.angle_speed
        self.rotation -= bullet_rotate

        vec = pygame.math.Vector2(0, 1)
        vec.y = angle_y*self.speed
        vec.rotate_ip(-self.rotation)

        self.direction.rotate_ip(bullet_rotate)
        self.direction.normalize_ip()

        self.pos = (self.pos[0] + vec.x, self.pos[1] + vec.y)