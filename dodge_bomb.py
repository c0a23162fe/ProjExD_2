import os
import sys
import pygame as pg
import random
import math
import time


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def kirikae(vx, vy):
    r = math.atan(sum_mv[0]/sum_mv[1])
    kk_img = pg.transform.rotozoom(kk_img, r,0)

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect, または、爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect、または、爆弾Rect
    戻り値：横方向判定結果、縦方向判定結果（True：画面内/False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def time_acc(tmr, vx, vy) -> tuple[bool, bool, tuple]:
    bb_imgs=[]
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        avx = vx*accs[min(tmr//500, 9)]
        avy = vy*accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        return avx,avy, bb_img



def gameover():
        img = pg.image.load("fig/8.png")
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.draw.rect(screen, (0, 0, 0), (1600, 900, 0, 0))
        pg.Surface.set_alpha(screen, 50)
        fonto = pg.font.Font(None, 80)
        txt = fonto.render("Game Over", True, (255, 255, 255))
        screen.blit(img, [600, 450])#こうかとん１
        screen.blit(img, [1000, 450])#こうかとん２
        screen.blit(txt, [675, 450])#”GAMEOVER”
        pg.display.update()
        time.sleep(5)


def main():

    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))  #背景
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0) #こうかとん
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    bakudan = pg.Surface((20, 20)) #爆弾
    pg.draw.circle(bakudan, (255, 0, 0), (10, 10), 10)
    bakudan.set_colorkey((0, 0, 0))
    bd_rct = bakudan.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5
    key_dic = {pg.K_UP:(0, -5),pg.K_DOWN:(0, +5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(+5,0)}
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            clock.tick(1)
            gameover()
            return
        avx, avy, bb_img = time_acc(tmr, vx, vy)
        print("あ")
        print(bb_img)
        print("あ")
        screen.blit(bg_img, [0, 0]) 
        bd_rct.move_ip(avx, avy)
        screen.blit(bakudan, bd_rct)
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in key_dic.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        time_acc(tmr, vx, vy)
        print(bb_img)
        bakudan1 = pg.transform.scale(bakudan, (20,20))
        screen.blit(bakudan1, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
