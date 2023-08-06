import pygame as py
import ujicobapygame1 as uj
import random

py.init()

class draw_assets:
    BACKGROUND = py.transform.scale(py.image.load("assets/space.png"),(uj.WIDTH,uj.HEIGHT))
    BORDER = py.Rect(uj.WIDTH/2 - 5,0,10,uj.HEIGHT)
    WIDTH_SPACESHIP = 55
    HEIGHT_SPACESHIP = 40
    RED_SPACESHIP = py.transform.rotate(py.transform.scale(py.image.load("assets/spaceship_red.png"),(WIDTH_SPACESHIP,HEIGHT_SPACESHIP)),90)
    YELLOW_SPACESHIP = py.transform.rotate(py.transform.scale(py.image.load("assets/spaceship_yellow.png"),(WIDTH_SPACESHIP,HEIGHT_SPACESHIP)),-90)
    DROP_SIZE = 40
    AMMO = py.transform.scale(py.image.load("assets/ammo.png"),(DROP_SIZE,DROP_SIZE))
    HEART = py.transform.scale(py.image.load("assets/heart.png"),(DROP_SIZE,DROP_SIZE))
    RED_HEART_GET_UP = py.USEREVENT + 3
    YELLOW_HEART_GET_UP = py.USEREVENT + 4

    @classmethod
    def background(cls):
        uj.WIN.blit(cls.BACKGROUND,(0,0))

    @classmethod
    def border(cls,COLOR):
        py.draw.rect(uj.WIN,COLOR,cls.BORDER)

    @classmethod
    def spaceship(cls,red,yellow):
        uj.WIN.blit(cls.RED_SPACESHIP, red)
        uj.WIN.blit(cls.YELLOW_SPACESHIP, yellow)

    @staticmethod
    def draw_bullet(RED,YELLOW):
        for bulletelement in getattr(bullet,'red_bullet_list'):
            py.draw.rect(uj.WIN,RED,bulletelement)
            draw_assets.red_remove_list(bulletelement)

        for bulletelement in getattr(bullet,'yellow_bullet_list'):
            py.draw.rect(uj.WIN,YELLOW,bulletelement)
            draw_assets.yellow_remove_list(bulletelement)

    @staticmethod
    def red_remove_list(bulletelement):
        if bulletelement.x > uj.WIDTH:
            bullet.red_bullet_list.remove(bulletelement)

    @staticmethod
    def yellow_remove_list(bulletelement):
        if bulletelement.x < 0:
            bullet.yellow_bullet_list.remove(bulletelement)

    @classmethod
    def ammo_drop_list(cls,red,yellow):
        DROP_VEL = getattr(item_drop,'DROP_VEL')
        for ammo in getattr(item_drop,'ammo_list'):
            ammo.y += DROP_VEL
            uj.WIN.blit(cls.AMMO,ammo)
            if ammo.colliderect(red):
                item_drop.ammo_list.remove(ammo)
                if bullet.RED_AMMUNITION_USE <= bullet.AMMO_LIMIT - 5:
                    bullet.RED_AMMUNITION_USE += 5
                elif bullet.AMMO_LIMIT - 5 < bullet.RED_AMMUNITION_USE < bullet.AMMO_LIMIT:
                    bullet.RED_AMMUNITION_USE += bullet.AMMO_LIMIT - bullet.RED_AMMUNITION_USE

            if ammo.colliderect(yellow):
                item_drop.ammo_list.remove(ammo)
                if bullet.YELLOW_AMMUNITION_USE <= bullet.AMMO_LIMIT - 5:
                    bullet.YELLOW_AMMUNITION_USE += 5
                elif bullet.AMMO_LIMIT - 5 < bullet.YELLOW_AMMUNITION_USE < bullet.AMMO_LIMIT:
                    bullet.YELLOW_AMMUNITION_USE += bullet.AMMO_LIMIT - bullet.YELLOW_AMMUNITION_USE

            if ammo.y + DROP_VEL > uj.HEIGHT:
                item_drop.ammo_list.remove(ammo)

    @classmethod
    def health_drop_list(cls,red,yellow):
        DROP_VEL = getattr(item_drop,'DROP_VEL')
        for heart in getattr(item_drop,'heart_list'):
            heart.y += DROP_VEL
            uj.WIN.blit(cls.HEART,heart)
            if heart.colliderect(red):
                py.event.post(py.event.Event(cls.RED_HEART_GET_UP))
                item_drop.heart_list.remove(heart)

            if heart.colliderect(yellow):
                py.event.post(py.event.Event(cls.YELLOW_HEART_GET_UP))
                item_drop.heart_list.remove(heart)

            if heart.y + DROP_VEL > uj.HEIGHT:
                item_drop.heart_list.remove(heart)

class movement:
    VEL = 3

    @classmethod
    def up(cls,key_pressed,red,yellow):
        if key_pressed[py.K_w] and red.y - cls.VEL > 0:
            red.y -= cls.VEL
        if key_pressed[py.K_UP] and yellow.y - cls.VEL > 0:
            yellow.y -= cls.VEL

    @classmethod
    def down(cls,key_pressed,red,yellow):
        if key_pressed[py.K_s] and red.y + cls.VEL < uj.HEIGHT - draw_assets.WIDTH_SPACESHIP:
            red.y += cls.VEL
        if key_pressed[py.K_DOWN] and yellow.y + cls.VEL < uj.HEIGHT - draw_assets.WIDTH_SPACESHIP:
            yellow.y += cls.VEL

    @classmethod
    def left(cls,key_pressed,red,yellow):
        if key_pressed[py.K_a] and red.x - cls.VEL > 0:
            red.x -= cls.VEL
        if key_pressed[py.K_LEFT] and yellow.x - cls.VEL > draw_assets.BORDER.right:
            yellow.x -= cls.VEL

    @classmethod
    def right(cls,key_pressed,red,yellow):
        if key_pressed[py.K_d] and red.x + cls.VEL < draw_assets.BORDER.left - draw_assets.HEIGHT_SPACESHIP:
            red.x += cls.VEL
        if key_pressed[py.K_RIGHT] and yellow.x + cls.VEL < uj.WIDTH - draw_assets.HEIGHT_SPACESHIP:
            yellow.x += cls.VEL

class bullet:
    WIDTH_BULLET = 10
    HEIGHT_BULLET = 5
    RED_HIT = py.USEREVENT + 1
    YELLOW_HIT = py.USEREVENT + 2
    VEL = 7
    red_bullet_list = []
    yellow_bullet_list = []
    AMMO_LIMIT = 50
    RED_AMMUNITION_USE = AMMO_LIMIT
    YELLOW_AMMUNITION_USE = AMMO_LIMIT

    @classmethod
    def red_append_list(cls,red):
        red_bullet = py.Rect(red.x + red.height,red.y + red.width//2 + cls.HEIGHT_BULLET/2 + 3,cls.WIDTH_BULLET,cls.HEIGHT_BULLET)
        cls.red_bullet_list.append(red_bullet)
        cls.RED_AMMUNITION_USE -= 1

    @classmethod
    def yellow_append_list(cls,yellow):
        yellow_bullet = py.Rect(yellow.x - cls.WIDTH_BULLET,yellow.y + yellow.width//2 + cls.HEIGHT_BULLET/2 + 3,cls.WIDTH_BULLET,cls.HEIGHT_BULLET)
        cls.yellow_bullet_list.append(yellow_bullet)
        cls.YELLOW_AMMUNITION_USE -= 1

    @classmethod
    def mechanism(cls,red,yellow):
        for bullet in cls.red_bullet_list:
            bullet.x += cls.VEL
            if yellow.colliderect(bullet):
                py.event.post(py.event.Event(cls.YELLOW_HIT))
                cls.red_bullet_list.remove(bullet)
            for yellow_bullet in cls.yellow_bullet_list:
                if bullet.colliderect(yellow_bullet):
                    cls.red_bullet_list.remove(bullet)
                    cls.yellow_bullet_list.remove(yellow_bullet)

        for bullet in cls.yellow_bullet_list:
            bullet.x -= cls.VEL
            if red.colliderect(bullet):
                py.event.post(py.event.Event(cls.RED_HIT))
                cls.yellow_bullet_list.remove(bullet)

class item_drop:
    ammo_list = []
    heart_list = []
    DROP_SIZE = getattr(draw_assets,"DROP_SIZE")
    DROP_VEL = 1

    @classmethod
    def ammunition(cls):
        if random.randint(0,5000) == 50:
            ammo_x_position = random.randint(0,uj.WIDTH - cls.DROP_SIZE)
            ammo_drop = py.Rect(ammo_x_position,0,cls.DROP_SIZE,cls.DROP_SIZE)
            cls.ammo_list.append(ammo_drop)

    @classmethod
    def heart_drop(cls):
        if random.randint(0,8000) == 50:
            heart_x_position = random.randint(0,uj.WIDTH - cls.DROP_SIZE)
            heart_drop = py.Rect(heart_x_position,0,cls.DROP_SIZE,cls.DROP_SIZE)
            cls.heart_list.append(heart_drop)

class font_and_particle:
    WINNER_FONT = py.font.SysFont('berlin sans fb demi',70)
    CONTINUE_FONT = py.font.SysFont('berlin sans fb demi',30)
    PARTICLE_SIZE = 40
    HEART_PARTICLE = py.transform.scale(py.image.load("assets/heart.png"),(PARTICLE_SIZE,PARTICLE_SIZE))
    AMMO_PARTICLE = py.transform.scale(py.image.load("assets/ammo.png"),(PARTICLE_SIZE,PARTICLE_SIZE))
    ammo_particle = (bullet.RED_AMMUNITION_USE + 4)//5

    @classmethod
    def render_font(cls):
        pass

    @classmethod
    def particle(cls,RED_HEALTH,YELLOW_HEALTH):
        red_ammo_particle = (bullet.RED_AMMUNITION_USE + 4)//5
        yellow_ammo_particle = (bullet.YELLOW_AMMUNITION_USE + 4)//5
        for i in range(RED_HEALTH):
            health_point = py.Rect((cls.PARTICLE_SIZE-13)*i,2,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE)
            uj.WIN.blit(cls.HEART_PARTICLE,health_point)

        for i in range(YELLOW_HEALTH):
            health_point = py.Rect(uj.WIDTH-(cls.PARTICLE_SIZE-13)*(i+2)+11,2,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE)
            uj.WIN.blit(cls.HEART_PARTICLE,health_point)

        for i in range(red_ammo_particle):
            ammo_point = py.Rect((cls.PARTICLE_SIZE-13)*i,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE)
            uj.WIN.blit(cls.AMMO_PARTICLE,ammo_point)

        for i in range(yellow_ammo_particle):
            ammo_point = py.Rect(uj.WIDTH-(cls.PARTICLE_SIZE-13)*(i+2)+11,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE,cls.PARTICLE_SIZE)
            uj.WIN.blit(cls.AMMO_PARTICLE,ammo_point)