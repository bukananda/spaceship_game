import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
SCALE = (55,40)
SCALE_X,SCALE_Y = SCALE
BORDER = pygame.Rect((WIDTH/2)-5, 0, 10, HEIGHT)
MAX_BULLET = 3
BULLET_VEL = 10
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_TEXT_FONT = pygame.font.SysFont('berlin sans fb demi', 70)
CONTINUE = pygame.font.SysFont('berlin sans fb demi', 30)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PYGAME SPACESHIP")

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","space.png")), (WIDTH,HEIGHT))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets","spaceship_red.png"))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets","spaceship_yellow.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, SCALE), 90)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SCALE), -90)
GUN_SOUND = pygame.mixer.Sound(os.path.join("assets","Assets_Gun+Silencer.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("assets","Assets_Grenade+1.mp3"))

pygame.display.set_icon(RED_SPACESHIP_IMAGE)

FPS = 60
RED_COORDINAT = (30,230)
RED_X,RED_Y = RED_COORDINAT
YELLOW_COORDINAT = (825,230)
YELLOW_X,YELLOW_Y = YELLOW_COORDINAT

def red_handle_movement(keys_pressed, red, VEL):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < (WIDTH/2) - SCALE_Y:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - SCALE_X:
        red.y += VEL

def yellow_handle_movement(keys_pressed, yellow, VEL):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > (WIDTH/2):
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < WIDTH - SCALE_Y:
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL < HEIGHT - SCALE_X:
        yellow.y += VEL

def handle_bullet(red_bullet, red, yellow_bullet, yellow):
    for bullet1 in red_bullet:
        bullet1.x += BULLET_VEL
        if yellow.colliderect(bullet1):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            EXPLOSION_SOUND.play()
            red_bullet.remove(bullet1)

        if bullet1.x + BULLET_VEL > WIDTH:
            red_bullet.remove(bullet1)

    for bullet2 in yellow_bullet:
        bullet2.x -= BULLET_VEL
        if red.colliderect(bullet2):
            pygame.event.post(pygame.event.Event(RED_HIT))
            EXPLOSION_SOUND.play()
            yellow_bullet.remove(bullet2)

        if bullet2.x + BULLET_VEL < 0:
            yellow_bullet.remove(bullet2)
            
def draw(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health, red_win, yellow_win, winner_text):
    WIN.blit(BG, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    summon_red_winner_text = WINNER_TEXT_FONT.render(winner_text, 1, RED)
    summon_yellow_winner_text = WINNER_TEXT_FONT.render(winner_text, 1, YELLOW)
    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, WHITE)
    continue_text = CONTINUE.render("Press SPACE to continue", 1, WHITE)
    WIN.blit(red_health_text, (10,10))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width()-10,10))

    if red_win == True:
        WIN.blit(summon_red_winner_text, ((WIDTH/2) - (summon_red_winner_text.get_width()//2),(HEIGHT/2)-(summon_red_winner_text.get_height()//2)))
        WIN.blit(continue_text, ((WIDTH/2) - continue_text.get_width()//2, (HEIGHT/2) + red_health_text.get_height()//2 + 10))

    if yellow_win == True:
        WIN.blit(summon_yellow_winner_text, ((WIDTH/2) - (summon_yellow_winner_text.get_width()//2),(HEIGHT/2)-(summon_yellow_winner_text.get_height()//2)))
        WIN.blit(continue_text, ((WIDTH/2) - continue_text.get_width()//2, (HEIGHT/2) + yellow_health_text.get_height()//2 + 10))

    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    red = pygame.Rect(RED_X,RED_Y,SCALE_X,SCALE_Y)
    yellow = pygame.Rect(YELLOW_X,YELLOW_Y,SCALE_X,SCALE_Y)
    VEL = 4
    width_bullet = 10
    height_bullet = 5
    red_bullet = []
    yellow_bullet = []
    red_health = 10
    yellow_health = 10
    substraction = True
    red_win = False
    yellow_win = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullet) < MAX_BULLET:
                    spawn_bullet = pygame.Rect(red.x + SCALE_Y + width_bullet,red.y + SCALE_X//2 - 2,width_bullet,height_bullet)
                    red_bullet.append(spawn_bullet)
                    GUN_SOUND.play()

                if event.key == pygame.K_RCTRL and len(yellow_bullet) < MAX_BULLET:
                    spawn_bullet = pygame.Rect(yellow.x - width_bullet,yellow.y + SCALE_X//2 - 2,width_bullet,height_bullet)
                    yellow_bullet.append(spawn_bullet)
                    GUN_SOUND.play()

                if (yellow_win or red_win == True) and event.key == pygame.K_SPACE:
                    yellow_win = red_win = False
                    red_bullet = []
                    yellow_bullet = []
                    substraction = True
                    red_health = yellow_health = 10

            if event.type == RED_HIT and substraction == True:
                red_health -= 1

            if event.type == YELLOW_HIT and substraction == True:
                yellow_health -= 1

            winner_text = ""
            if red_health <= 0:
                substraction = False
                yellow_win = True
                winner_text = "YELLOW WIN"

            elif yellow_health <= 0:
                substraction = False
                red_win = True
                winner_text = "RED WIN"

            elif winner_text != "":
                pass

        handle_bullet(red_bullet, red, yellow_bullet, yellow)
        draw(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health, red_win, yellow_win, winner_text)
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red, VEL)
        yellow_handle_movement(keys_pressed, yellow, VEL)

    pygame.quit()

if __name__ == '__main__':
    main()