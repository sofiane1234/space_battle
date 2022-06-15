import pygame

def text_score(txt, size, color, font):
    txt_font = pygame.font.SysFont(font, size)
    return txt_font.render(txt, True, color)

def text_screen(txt, size, color, frame, pos, font="Calibri"):
    surf = text_score(txt, size, color, font)
    rect = surf.get_rect()
    frame.blit(surf, (pos[0] - rect.w / 2, pos[1] - rect.h / 2))