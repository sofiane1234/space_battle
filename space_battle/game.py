import sys
import time
import pygame
from pygame.locals import *

from player_class import Player
from second_player_class import SecondPlayer
from affichage import *


class Game:
    def __init__(self, reso):
        self.reso = reso
        
        #Bordures de l'ecran
        self.bord = [ [-50, self.reso[0] + 50], 
                    [-50, self.reso[1] + 50] ]
        #Bordures de vaisseau
        self.ship_bord = [ [40, self.reso[0] - 50], 
                        [40, self.reso[1] - 50] ]
        
        self.titre = "Space Battle"
        self.is_running = True
        self.is_playing = False
        self.j1_score = 0
        self.j2_score = 0
        self.score_font_size = 25
        self.score_pos_j1 = (self.reso[0] - self.reso[0] + 100, 30)
        self.win_pos = (self.reso[0]/2, self.reso[1]/2)
        self.vies_pos_j1 = (self.reso[0] - self.reso[0] + 300, 30)
        self.score_pos_j2 = (self.reso[0] - 100, 30)
        self.vies_pos_j2 = (self.reso[0] - 300, 30) 
        self.clock = pygame.time.Clock()
        self.fin_partie_timer = 3
       
        self.play_button = pygame.image.load('assets/start_button.png')

        self.first_player = pygame.image.load("assets/first_ship.png")
        self.second_player = pygame.image.load("assets/second_ship.png")
        self.img_bullet = pygame.image.load("assets/bullet.png")

        self.p1 = Player((200, 200), 5, self.first_player, self.img_bullet)
        self.p2 = SecondPlayer((400, 200), 5, self.second_player, self.img_bullet)
        self.all_bullets = pygame.sprite.Group()
        self.all_bullets_p2 = pygame.sprite.Group()

        self.fin_partie_start = 0
        self.start()

    #Initialisation de la fenetre et changement de son titre
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.reso)
        pygame.display.set_caption(self.titre)

        while self.is_running:
            text_screen("SPACE BATTLE ", self.score_font_size, pygame.Color(0,0,0), self.screen, (self.reso[0]/2 + 70, self.reso[1]/2 - 70))
            text_screen(" J1 : Z avancer, D pivoter droite, Q pivoter gauche, S reculer ", self.score_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 + 70, self.reso[1]/2 + 70))
            text_screen(" J2 : O avancer, M pivoter droite, J pivoter gauche, L reculer ", self.score_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 + 70, self.reso[1]/2 + 150))
            text_screen("Appuyez sur Espace pour lancer la partie !", self.score_font_size, pygame.Color(255,255,255), self.screen, self.win_pos)
            
            pygame.display.update()
            self.screen.fill('blue')            
            for evt in pygame.event.get():
                self.get_events(evt)
                self.run()
            

    def run(self):
        while self.is_playing:
            for evt in pygame.event.get():
                self.get_events(evt)
                 
              # limites bord angle x joueur 1
            if self.p1.pos[0] < self.ship_bord[0][0]:
                self.p1.pos = (self.ship_bord[0][0], self.p1.pos[1])
            elif self.p1.pos[0] > self.ship_bord[0][1]:
                self.p1.pos = (self.ship_bord[0][1], self.p1.pos[1])
            
           # limites bord angle y joueur 1
            if self.p1.pos[1] < self.ship_bord[1][0]:
                self.p1.pos = (self.p1.pos[0], self.ship_bord[1][0])
            elif self.p1.pos[1] > self.ship_bord[1][1]:
                self.p1.pos = (self.p1.pos[0], self.ship_bord[1][1])

             # limites bord angle x joueur 2
            if self.p2.pos[0] < self.ship_bord[0][0]:
                self.p2.pos = (self.ship_bord[0][0], self.p2.pos[1])
            elif self.p2.pos[0] > self.ship_bord[0][1]:
                self.p2.pos = (self.ship_bord[0][1], self.p2.pos[1])
            
            # limites bord angle y joueur 2
            if self.p2.pos[1] < self.ship_bord[1][0]:
                self.p2.pos = (self.p2.pos[0], self.ship_bord[1][0])
            elif self.p2.pos[1] > self.ship_bord[1][1]:
                self.p2.pos = (self.p2.pos[0], self.ship_bord[1][1])

            self.p1.get_inputs()
            self.p2.get_inputs()
            self.update()
            
    
    #Fonction permettant de gerer les events
    def get_events(self, evt):
        if evt.type == QUIT:
            self.is_running, self.is_playing = False, False
        if evt.type == KEYDOWN:
            if evt.key == K_LALT:
                bullet = self.p1.tirer()
                if bullet:
                    self.all_bullets.add(bullet)
            elif evt.key == K_RALT:
                bullet = self.p2.tirer()
                if bullet:
                    self.all_bullets_p2.add(bullet)
            elif evt.key == K_SPACE:
                self.is_playing = True

    #Dessin des surfaces etc (affichage)
    def draw(self):
        self.screen.blit(self.p1.image, self.p1.rect)
        self.screen.blit(self.p2.image, self.p2.rect)
        self.all_bullets.draw(self.screen)
        self.all_bullets_p2.draw(self.screen)

    #Affichage du score
    def draw_score(self):
        text_screen("J1 Score : " + str(self.j1_score), self.score_font_size, pygame.Color(255,255,0), self.screen, self.score_pos_j1)
        text_screen("J2 Score : " + str(self.j2_score), self.score_font_size, pygame.Color(255,255,0), self.screen, self.score_pos_j2)
    
    def draw_vies(self):
        text_screen("J1 Vies : " + str(self.p1.vies), self.score_font_size, pygame.Color(255,255,0), self.screen, self.vies_pos_j1)
        text_screen("J2 Vies : " + str(self.p2.vies), self.score_font_size, pygame.Color(255,255,0), self.screen, self.vies_pos_j2)
    
    def draw_victoire_j2(self):
        self.fin_partie_start = time.time()
        while time.time() - self.fin_partie_start < self.fin_partie_timer:
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    sys.exit()

            self.screen.fill(pygame.Color(155,0,0))
            text_screen("Joueur 2 Gagne !", self.score_font_size, pygame.Color(255,255,0), self.screen, self.win_pos)
            text_screen("Avec un score de : " + str(self.j2_score), self.score_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 + 15, self.reso[1] /2 + 40))
            text_screen("Veuillez patienter", self.score_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0] /2, self.reso[1]/2 + 70))
            pygame.display.update()
            self.p1.vies = 5
            self.p2.vies = 5
            self.j1_score = self.j1_score
            self.j2_score = 0
           

    def draw_victoire_j1(self):
        self.fin_partie_start = time.time()
        while time.time() - self.fin_partie_start < self.fin_partie_timer:

            for evt in pygame.event.get():
                if evt.type == QUIT:
                    sys.exit()

            self.screen.fill(pygame.Color(155,0,0))
            text_screen("Joueur 1 Gagne !", self.score_font_size, pygame.Color(255,255,0), self.screen, self.win_pos)
            text_screen("Veuillez patienter", self.score_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0] /2, self.reso[1]/2 + 50))
            pygame.display.update()
            self.p2.vies = 5
            self.p1.vies = 5
            self.j1_score = 0
            self.j2_score = 0
           

    #Gestion des collisions
    def gerer_collision(self):

        #Joueur 1
        for bullet in pygame.sprite.spritecollide(self.p1, self.all_bullets_p2, False):
            print("Joueur 1 touche")
            bullet.kill()
            del bullet
            self.p1.vies -= 1
            self.j2_score += 5
            while self.p1.vies < 0:
                self.p1.vies = 0
                self.draw_victoire_j2()            
            print("J1 perd une vie") 


        
        #Joueur 2
        for bullet in pygame.sprite.spritecollide(self.p2, self.all_bullets, False):
            print("Joueur 2 touche")
            bullet.kill()
            del bullet
            self.p2.vies -= 1
            self.j1_score += 5
            while self.p2.vies < 0:
                self.p2.vies = 0
                self.draw_victoire_j1()
            print('J2 perd une vie')
            


    #Suppression des projectiles
    def clear_bullets(self, group):

        for bullet in group.sprites():

            if bullet.rect.centerx < self.bord[0][0] or bullet.rect.centerx > self.bord[0][1]:
                self.all_bullets.remove(bullet)
            if bullet.rect.centery < self.bord[1][0] or bullet.rect.centery > self.bord[1][1]:
                self.all_bullets.remove(bullet) 
            if bullet not in self.all_bullets.sprites():
                del bullet

    #Update des methodes en les appelant
    def update(self):
        self.screen.fill(178)
        self.clear_bullets(self.all_bullets)
        self.clear_bullets(self.all_bullets_p2)
        self.p1.update()
        self.all_bullets.update()
        self.all_bullets_p2.update()
        self.p2.update()
        self.draw()
        self.draw_score() 
        self.draw_vies()
        self.gerer_collision()
        self.clock.tick(60)
        pygame.display.update()
    
    #Mise en arret du programme
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self