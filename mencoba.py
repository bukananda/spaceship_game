import pygame

pygame.init()
WIDTH = 450
HEIGHT = 250
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BG = pygame.transform.scale(pygame.image.load("assets/space.png"),(WIDTH,HEIGHT))

def bg_movement(coordinat_1_y,coordinat_2_y):
    WIN.blit(BG,(0,coordinat_1_y))
    WIN.blit(pygame.transform.flip(BG,False,True),(0,coordinat_2_y))
    pygame.display.update()

def bg_movement_rule(coordinat_1_y,coordinat_2_y):
    coordinat_1_y += 2
    coordinat_2_y += 2
    if coordinat_1_y > HEIGHT:
        coordinat_1_y = -HEIGHT
    elif coordinat_2_y > HEIGHT:
        coordinat_2_y = -HEIGHT

def main():
    run =True
    clock = pygame.time.Clock()
    coordinat_1_y = 0
    coordinat_2_y = -HEIGHT
    while run:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        bg_movement(coordinat_1_y,coordinat_2_y)
        bg_movement_rule(coordinat_1_y,coordinat_2_y)
    pygame.quit()

main()