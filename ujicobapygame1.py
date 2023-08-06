import pygame as py
import function as f

py.init()
WIDTH = 900
HEIGHT = 500
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 144

WIN = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("SPACESHIP GAME")

def movement(key_pressed,red,yellow):
    f.movement.up(key_pressed,red,yellow)
    f.movement.down(key_pressed,red,yellow)
    f.movement.left(key_pressed,red,yellow)
    f.movement.right(key_pressed,red,yellow)
    f.bullet.mechanism(red,yellow)
    f.item_drop.ammunition()
    f.item_drop.heart_drop()

def draw(red,yellow,RED_HEALTH,YELLOW_HEALTH):
    f.draw_assets.background()
    f.draw_assets.border(BLACK)
    f.draw_assets.spaceship(red,yellow)
    f.draw_assets.draw_bullet(RED,YELLOW)
    f.draw_assets.ammo_drop_list(red,yellow)
    f.draw_assets.health_drop_list(red,yellow)
    f.font_and_particle.particle(RED_HEALTH,YELLOW_HEALTH)
    py.display.update()

def main():
    run = True
    clock = py.time.Clock()
    red = py.Rect(20,(HEIGHT-f.draw_assets.WIDTH_SPACESHIP)/2,f.draw_assets.HEIGHT_SPACESHIP,f.draw_assets.HEIGHT_SPACESHIP)
    yellow = py.Rect(WIDTH-20-f.draw_assets.HEIGHT_SPACESHIP,(HEIGHT-f.draw_assets.WIDTH_SPACESHIP)/2,f.draw_assets.HEIGHT_SPACESHIP,f.draw_assets.HEIGHT_SPACESHIP)
    BULLET_LIMIT = 3
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    while run:
        clock.tick(FPS)
        for e in py.event.get():
            if e.type == py.QUIT:
                run = False
            if e.type == py.KEYDOWN:
                if (e.key == py.K_LCTRL and len(f.bullet.red_bullet_list) < BULLET_LIMIT) and f.bullet.RED_AMMUNITION_USE > 0:
                    f.bullet.red_append_list(red)
                if (e.key == py.K_RCTRL and len(f.bullet.yellow_bullet_list) < BULLET_LIMIT) and f.bullet.YELLOW_AMMUNITION_USE > 0:
                    f.bullet.yellow_append_list(yellow)
                if e.key == py.K_SPACE and (RED_HEALTH == 0 or YELLOW_HEALTH == 0):
                    RED_HEALTH = YELLOW_HEALTH = 10
                    f.bullet.RED_AMMUNITION_USE = f.bullet.YELLOW_AMMUNITION_USE = 50

            if e.type == f.bullet.RED_HIT and RED_HEALTH > 0 and YELLOW_HEALTH > 0:
                RED_HEALTH -= 1
                print(RED_HEALTH)

            if e.type == f.bullet.YELLOW_HIT and YELLOW_HEALTH > 0 and RED_HEALTH > 0:
                YELLOW_HEALTH -= 1
                print(YELLOW_HEALTH)

            if e.type == f.draw_assets.RED_HEART_GET_UP and RED_HEALTH < 12 and RED_HEALTH > 0 and YELLOW_HEALTH > 0:
                RED_HEALTH += 1
                print(RED_HEALTH)

            if e.type == f.draw_assets.YELLOW_HEART_GET_UP and YELLOW_HEALTH < 12 and RED_HEALTH > 0 and YELLOW_HEALTH > 0:
                YELLOW_HEALTH += 1
                print(YELLOW_HEALTH)

        key_pressed = py.key.get_pressed()
        movement(key_pressed,red,yellow)
        draw(red,yellow,RED_HEALTH,YELLOW_HEALTH)

    py.quit()

if __name__ == '__main__':
    main()