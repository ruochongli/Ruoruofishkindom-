#!/usr/bin/env python3
"""
生成若若的钓鱼王国 - 像素风格角色精灵图 V4
基础款 / 无兔耳 / 无过膝袜 / 白色内衣
"""
from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def save(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    img.save(path)
    print(f"Saved: {path}")

def create_image(w, h, bg=(0,0,0,0)):
    return Image.new('RGBA', (w, h), bg)

def dr(draw, x, y, w, h, color):
    """draw rect"""
    if w <= 0 or h <= 0: return
    draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

def dot(draw, x, y, color):
    draw.point((x, y), fill=color)

# ========== 可爱风调色板 ==========
P = {
    # 肤色
    'skin':       (255, 228, 210, 255),
    'skin_mid':   (248, 200, 180, 255),
    'skin_shade': (235, 180, 155, 255),
    'blush':      (255, 160, 170, 180),

    # 眼睛（水银灯+克鲁鲁风大红眼）
    'eye_red':    (220, 50, 70, 255),
    'eye_dark':   (160, 30, 50, 255),
    'eye_core':   (255, 100, 120, 255),
    'eye_white':  (255, 255, 255, 255),
    'eye_line':   (80, 20, 30, 255),

    # 头发（银白发）
    'hair':       (245, 245, 255, 255),
    'hair_mid':   (220, 220, 240, 255),
    'hair_dark':  (180, 180, 210, 255),
    'hair_shine': (255, 255, 255, 255),

    # 内衣（白色轻薄蕾丝）
    'cloth':      (255, 250, 250, 255),
    'cloth_mid':  (245, 240, 245, 255),
    'cloth_dark': (230, 225, 235, 255),
    'lace':       (255, 220, 230, 255),
    'lace_dark':  (230, 190, 210, 255),
    'ribbon':     (220, 60, 90, 255),
    'ribbon_dark':(180, 40, 60, 255),
    'gold':       (255, 215, 100, 255),

    # 嘴
    'mouth':      (220, 100, 120, 255),
    'mouth_dark': (180, 70, 90, 255),

    # 其他
    'black':      (30, 28, 40, 255),
    'white':      (255, 255, 255, 255),
    'outline':    (50, 45, 65, 255),
    'shadow':     (0, 0, 0, 40),
    'leg':        (255, 220, 205, 255),
    'leg_dark':   (240, 200, 185, 255),
    'sock':       (255, 240, 245, 255),
    'sock_dark':  (235, 220, 230, 255),
    'sock_lace':  (255, 200, 215, 255),
}

# ========== 女性角色（爱丽丝摇篮风）==========
def draw_female_cute(dress_type='full', damaged=False):
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    sclera = (255, 245, 250)  # 眼白

    # 阴影
    dr(d, 16, 90, 32, 4, P['shadow'])

    # ====== 腿部 ======
    dr(d, 24, 64, 7, 22, P['leg'])
    dr(d, 24, 64, 2, 22, P['leg_dark'])
    dr(d, 33, 64, 7, 22, P['leg'])
    dr(d, 33, 64, 2, 22, P['leg_dark'])

    # 小皮鞋（基础款无袜子）
    dr(d, 23, 86, 9, 4, P['black'])
    dr(d, 33, 86, 9, 4, P['black'])
    dr(d, 26, 85, 2, 2, P['ribbon'])
    dr(d, 36, 85, 2, 2, P['ribbon'])

    # ====== 身体 ======
    if dress_type == 'full':
        dr(d, 22, 38, 20, 14, P['cloth'])
        dr(d, 22, 38, 20, 3, P['lace'])
        dr(d, 22, 48, 20, 3, P['lace'])
        dr(d, 29, 42, 6, 4, P['ribbon'])
        dr(d, 30, 41, 4, 2, P['ribbon'])
        dr(d, 31, 40, 2, 2, P['ribbon_dark'])
        dr(d, 23, 36, 2, 6, P['lace_dark'])
        dr(d, 39, 36, 2, 6, P['lace_dark'])
        dr(d, 24, 52, 16, 10, P['cloth'])
        dr(d, 24, 52, 16, 2, P['lace'])
        dr(d, 26, 60, 12, 2, P['lace'])
        for sx in range(26, 38, 2):
            for sy in range(42, 60, 3):
                dot(d, sx, sy, (255,255,255,100))
    elif dress_type == 'damaged':
        dr(d, 22, 38, 20, 10, P['cloth'])
        dr(d, 22, 38, 20, 3, P['lace'])
        dr(d, 24, 52, 14, 8, P['cloth'])
        dr(d, 24, 52, 14, 2, P['lace'])
        dr(d, 26, 44, 6, 4, P['skin'])
        dr(d, 34, 54, 4, 3, P['skin'])
        dr(d, 25, 43, 2, 2, P['ribbon'])
        dr(d, 33, 53, 2, 2, P['ribbon'])
    elif dress_type == 'underwear':
        dr(d, 22, 38, 20, 14, P['cloth'])
        dr(d, 22, 38, 20, 3, P['lace'])
        dr(d, 22, 48, 20, 3, P['lace'])
        dr(d, 29, 42, 6, 4, P['ribbon'])
        dr(d, 24, 52, 16, 10, P['cloth'])
        dr(d, 24, 52, 16, 2, P['lace'])
        for sx in range(24, 40, 2):
            for sy in range(38, 62, 2):
                if (sx+sy) % 4 == 0:
                    dot(d, sx, sy, (255,255,255,60))

    # ====== 手臂 ======
    dr(d, 14, 38, 6, 20, P['skin'])
    dr(d, 14, 38, 2, 20, P['skin_shade'])
    dr(d, 44, 38, 6, 20, P['skin'])
    dr(d, 44, 38, 2, 20, P['skin_shade'])
    dr(d, 14, 54, 6, 2, P['lace'])
    dr(d, 44, 54, 6, 2, P['lace'])

    # ====== 头部 ======
    dr(d, 30, 32, 4, 6, P['skin_shade'])

    # 脸（椭圆带稍尖下巴）
    dr(d, 20, 10, 24, 20, P['skin'])
    dr(d, 20, 10, 4, 20, P['skin_shade'])
    dr(d, 40, 10, 4, 20, P['skin_mid'])
    dr(d, 22, 28, 20, 6, P['skin'])
    dr(d, 24, 30, 16, 4, P['skin'])
    dr(d, 26, 32, 12, 2, P['skin'])

    # ====== 眼睛（精细层次）======
    eye_y = 17
    # 左眼 9x6
    dr(d, 24, eye_y, 9, 2, P['eye_dark'])       # 上眼睑
    dr(d, 24, eye_y+2, 9, 3, sclera)             # 眼白
    dr(d, 26, eye_y+2, 5, 3, P['eye_red'])       # 虹膜
    dr(d, 27, eye_y+3, 3, 2, P['eye_dark'])      # 瞳孔
    dr(d, 28, eye_y+2, 2, 2, P['eye_white'])     # 主高光
    dr(d, 26, eye_y+2, 1, 1, P['eye_white'])     # 侧高光
    dr(d, 24, eye_y+5, 9, 1, P['eye_red'])       # 下眼睑
    # 睫毛
    dr(d, 23, eye_y-1, 3, 1, P['eye_line'])
    dr(d, 22, eye_y, 2, 1, P['eye_line'])
    dr(d, 30, eye_y-1, 2, 1, P['eye_line'])

    # 右眼 9x6
    dr(d, 35, eye_y, 9, 2, P['eye_dark'])
    dr(d, 35, eye_y+2, 9, 3, sclera)
    dr(d, 37, eye_y+2, 5, 3, P['eye_red'])
    dr(d, 38, eye_y+3, 3, 2, P['eye_dark'])
    dr(d, 39, eye_y+2, 2, 2, P['eye_white'])
    dr(d, 37, eye_y+2, 1, 1, P['eye_white'])
    dr(d, 35, eye_y+5, 9, 1, P['eye_red'])
    # 睫毛
    dr(d, 42, eye_y-1, 3, 1, P['eye_line'])
    dr(d, 44, eye_y, 2, 1, P['eye_line'])
    dr(d, 36, eye_y-1, 2, 1, P['eye_line'])

    # 眉毛
    dr(d, 25, 14, 7, 1, P['hair_dark'])
    dr(d, 26, 13, 2, 1, P['hair_dark'])
    dr(d, 36, 14, 7, 1, P['hair_dark'])
    dr(d, 38, 13, 2, 1, P['hair_dark'])

    # 嘴（超小微笑）
    dr(d, 31, 28, 2, 1, P['mouth'])

    # 腮红（眼睛下方）
    dr(d, 20, 23, 5, 4, P['blush'])
    dr(d, 39, 23, 5, 4, P['blush'])

    # ====== 头发 ======
    dr(d, 16, 8, 32, 10, P['hair'])
    dr(d, 14, 10, 4, 30, P['hair'])
    dr(d, 14, 14, 2, 26, P['hair_dark'])
    dr(d, 48, 10, 4, 30, P['hair'])
    dr(d, 50, 14, 2, 26, P['hair_dark'])
    dr(d, 12, 20, 4, 35, P['hair'])
    dr(d, 12, 24, 2, 28, P['hair_dark'])
    dr(d, 48, 20, 4, 35, P['hair'])
    dr(d, 50, 24, 2, 28, P['hair_dark'])

    dr(d, 18, 4, 28, 10, P['hair'])
    dr(d, 20, 2, 24, 6, P['hair_shine'])
    dr(d, 22, 3, 20, 4, P['hair'])

    dr(d, 20, 6, 24, 8, P['hair'])
    dr(d, 22, 8, 6, 5, P['hair_shine'])
    dr(d, 30, 8, 6, 5, P['hair_shine'])
    dr(d, 38, 8, 4, 5, P['hair_shine'])
    dr(d, 20, 10, 24, 2, P['hair_dark'])
    dr(d, 18, 12, 3, 6, P['hair'])
    dr(d, 43, 12, 3, 6, P['hair'])

    dr(d, 38, 0, 3, 4, P['hair'])
    dr(d, 39, 0, 2, 2, P['hair_shine'])

    dr(d, 18, 14, 4, 14, P['hair'])
    dr(d, 42, 14, 4, 14, P['hair'])
    dr(d, 18, 18, 2, 10, P['hair_dark'])
    dr(d, 44, 18, 2, 10, P['hair_dark'])

    # 无头饰 / 无项链（基础款）

    return img


def draw_male_cute(dress_type='full', damaged=False):
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)

    dr(d, 16, 90, 32, 4, P['shadow'])

    # 腿
    dr(d, 24, 60, 7, 24, P['leg'])
    dr(d, 24, 60, 2, 24, P['leg_dark'])
    dr(d, 33, 60, 7, 24, P['leg'])
    dr(d, 33, 60, 2, 24, P['leg_dark'])

    # 白色短裤
    if dress_type != 'underwear':
        dr(d, 24, 58, 16, 12, P['cloth'])
        dr(d, 24, 58, 16, 2, P['lace'])
        dr(d, 26, 66, 12, 3, P['lace'])
    else:
        dr(d, 24, 58, 16, 8, P['cloth'])
        dr(d, 24, 58, 16, 2, P['lace'])
        for sx in range(26, 38, 2):
            for sy in range(58, 66, 2):
                dot(d, sx, sy, (255,255,255,60))

    # 鞋子
    dr(d, 23, 86, 9, 4, P['black'])
    dr(d, 33, 86, 9, 4, P['black'])

    # 上身（白色轻薄内衣/睡衣）
    if dress_type == 'full':
        dr(d, 22, 36, 20, 14, P['cloth'])
        dr(d, 22, 36, 20, 3, P['lace'])
        dr(d, 22, 46, 20, 3, P['lace'])
        dr(d, 28, 40, 8, 4, P['ribbon'])
        dr(d, 22, 36, 2, 10, P['lace_dark'])
        dr(d, 40, 36, 2, 10, P['lace_dark'])
    elif dress_type == 'damaged':
        dr(d, 22, 36, 20, 10, P['cloth'])
        dr(d, 22, 36, 20, 3, P['lace'])
        dr(d, 26, 42, 5, 4, P['skin'])
        dr(d, 36, 44, 3, 3, P['skin'])
        dr(d, 25, 41, 2, 2, P['ribbon'])
    else:
        dr(d, 22, 36, 20, 14, P['cloth'])
        dr(d, 22, 36, 20, 3, P['lace'])
        for sx in range(24, 40, 2):
            for sy in range(38, 50, 2):
                dot(d, sx, sy, (255,255,255,60))

    # 手臂
    dr(d, 14, 36, 6, 22, P['skin'])
    dr(d, 14, 36, 2, 22, P['skin_shade'])
    dr(d, 44, 36, 6, 22, P['skin'])
    dr(d, 44, 36, 2, 22, P['skin_shade'])
    if dress_type != 'underwear':
        dr(d, 14, 36, 6, 6, P['cloth'])
        dr(d, 44, 36, 6, 6, P['cloth'])

    # 头
    dr(d, 30, 30, 4, 6, P['skin_shade'])
    dr(d, 22, 8, 20, 22, P['skin'])
    dr(d, 22, 8, 4, 22, P['skin_shade'])
    dr(d, 38, 8, 4, 22, P['skin_mid'])
    dr(d, 24, 28, 16, 4, P['skin'])

    # 眼睛（横长，参考爱丽丝风）
    sclera_m = (255, 245, 250)
    dr(d, 25, 17, 8, 2, P['eye_dark'])
    dr(d, 25, 19, 8, 3, sclera_m)
    dr(d, 27, 19, 4, 3, P['eye_red'])
    dr(d, 28, 20, 2, 2, P['eye_dark'])
    dr(d, 29, 19, 1, 1, P['eye_white'])
    dr(d, 25, 22, 8, 1, P['eye_red'])

    dr(d, 35, 17, 8, 2, P['eye_dark'])
    dr(d, 35, 19, 8, 3, sclera_m)
    dr(d, 37, 19, 4, 3, P['eye_red'])
    dr(d, 38, 20, 2, 2, P['eye_dark'])
    dr(d, 39, 19, 1, 1, P['eye_white'])
    dr(d, 35, 22, 8, 1, P['eye_red'])

    # 睫毛
    dr(d, 24, 16, 3, 1, P['eye_line'])
    dr(d, 23, 17, 2, 1, P['eye_line'])
    dr(d, 32, 16, 2, 1, P['eye_line'])
    dr(d, 38, 16, 3, 1, P['eye_line'])
    dr(d, 41, 17, 2, 1, P['eye_line'])
    dr(d, 36, 16, 2, 1, P['eye_line'])

    # 眉毛
    dr(d, 24, 13, 8, 1, P['hair_dark'])
    dr(d, 25, 12, 3, 1, P['hair_dark'])
    dr(d, 36, 13, 8, 1, P['hair_dark'])
    dr(d, 38, 12, 3, 1, P['hair_dark'])

    # 嘴
    dr(d, 31, 27, 2, 1, P['mouth'])

    # 腮红
    dr(d, 20, 22, 5, 4, P['blush'])
    dr(d, 39, 22, 5, 4, P['blush'])

    # 头发
    dr(d, 20, 2, 24, 10, P['hair'])
    dr(d, 18, 6, 5, 18, P['hair'])
    dr(d, 41, 6, 5, 18, P['hair'])
    dr(d, 16, 10, 4, 14, P['hair'])
    dr(d, 44, 10, 4, 14, P['hair'])
    dr(d, 22, 4, 20, 6, P['hair_shine'])
    dr(d, 24, 6, 4, 4, P['hair_dark'])
    dr(d, 36, 6, 4, 4, P['hair_dark'])
    dr(d, 38, 0, 3, 3, P['hair_shine'])

    return img


# ========== 创角立绘预览（128x192 精细版）==========
def draw_female_portrait():
    W, H = 128, 192
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    s = P['skin']; sd = P['skin_shade']; sm = P['skin_mid']
    h = P['hair']; hd = P['hair_dark']; hl = P['hair_shine']
    e = P['eye_red']; ed = P['eye_dark']; el = P['eye_line']
    c = P['cloth']; cl = P['lace']; cd = P['lace_dark']
    r = P['ribbon']; rd = P['ribbon_dark']
    b = P['black']; m = P['mouth']; sh = P['shadow']

    # 阴影
    dr(d, 28, 180, 72, 8, sh)

    # 腿
    dr(d, 48, 128, 14, 44, s); dr(d, 48, 128, 4, 44, sd)
    dr(d, 66, 128, 14, 44, s); dr(d, 66, 128, 4, 44, sd)

    # 鞋子
    dr(d, 46, 172, 18, 8, b); dr(d, 66, 172, 18, 8, b)
    dr(d, 52, 170, 4, 4, r); dr(d, 72, 170, 4, 4, r)
    dr(d, 46, 176, 18, 4, (50,45,65)); dr(d, 66, 176, 18, 4, (50,45,65))

    # 白色内衣
    dr(d, 44, 76, 40, 28, c); dr(d, 44, 76, 40, 6, cl); dr(d, 44, 100, 40, 6, cl)
    dr(d, 58, 84, 12, 8, r); dr(d, 60, 82, 8, 4, r); dr(d, 62, 80, 4, 4, rd)
    dr(d, 46, 72, 4, 12, cd); dr(d, 78, 72, 4, 12, cd)
    dr(d, 48, 104, 32, 20, c); dr(d, 48, 104, 32, 4, cl); dr(d, 52, 120, 24, 4, cl)

    # 手臂
    dr(d, 28, 76, 12, 40, s); dr(d, 28, 76, 4, 40, sd)
    dr(d, 88, 76, 12, 40, s); dr(d, 88, 76, 4, 40, sd)
    dr(d, 28, 108, 12, 4, cl); dr(d, 88, 108, 12, 4, cl)

    # 脖子
    dr(d, 60, 64, 8, 12, sd)

    # 耳朵
    dr(d, 36, 44, 6, 10, s); dr(d, 86, 44, 6, 10, s)

    # 脸
    dr(d, 40, 20, 48, 36, s); dr(d, 40, 20, 8, 36, sd); dr(d, 80, 20, 8, 36, sm)
    dr(d, 44, 52, 40, 8, s); dr(d, 48, 56, 32, 8, s); dr(d, 52, 60, 24, 4, s); dr(d, 56, 64, 16, 4, s)

    # 眼睛
    ey = 34
    # 左眼
    dr(d, 48, ey-2, 18, 6, ed); dr(d, 48, ey+4, 18, 10, (255,245,250))
    dr(d, 52, ey+4, 10, 10, e); dr(d, 54, ey+6, 6, 6, ed)
    dr(d, 56, ey+4, 4, 4, (255,255,255)); dr(d, 52, ey+8, 2, 2, (255,255,255))
    dr(d, 48, ey+14, 18, 4, e)
    dr(d, 46, ey-2, 6, 2, el); dr(d, 44, ey, 4, 2, el); dr(d, 64, ey-2, 4, 2, el)
    # 右眼
    dr(d, 70, ey-2, 18, 6, ed); dr(d, 70, ey+4, 18, 10, (255,245,250))
    dr(d, 74, ey+4, 10, 10, e); dr(d, 76, ey+6, 6, 6, ed)
    dr(d, 78, ey+4, 4, 4, (255,255,255)); dr(d, 74, ey+8, 2, 2, (255,255,255))
    dr(d, 70, ey+14, 18, 4, e)
    dr(d, 84, ey-2, 6, 2, el); dr(d, 88, ey, 4, 2, el); dr(d, 72, ey-2, 4, 2, el)

    # 眉毛
    dr(d, 50, 28, 14, 2, hd); dr(d, 52, 26, 4, 2, hd)
    dr(d, 72, 28, 14, 2, hd); dr(d, 76, 26, 4, 2, hd)

    # 嘴
    dr(d, 62, 56, 4, 2, m)

    # 腮红
    for x in range(40, 50):
        for y in range(46, 54):
            dot(d, x, y, (255, 160, 170, 100))
    for x in range(78, 88):
        for y in range(46, 54):
            dot(d, x, y, (255, 160, 170, 100))

    # 头发
    dr(d, 32, 16, 64, 20, h); dr(d, 28, 20, 8, 60, h); dr(d, 28, 28, 4, 52, hd)
    dr(d, 96, 20, 8, 60, h); dr(d, 100, 28, 4, 52, hd)
    dr(d, 24, 40, 8, 70, h); dr(d, 24, 48, 4, 56, hd)
    dr(d, 96, 40, 8, 70, h); dr(d, 100, 48, 4, 56, hd)

    dr(d, 36, 8, 56, 20, h); dr(d, 40, 4, 48, 12, hl); dr(d, 44, 6, 40, 8, h)
    dr(d, 40, 12, 48, 16, h); dr(d, 44, 16, 12, 10, hl); dr(d, 60, 16, 12, 10, hl)
    dr(d, 76, 16, 8, 10, hl); dr(d, 40, 20, 48, 4, hd); dr(d, 36, 24, 6, 12, h)
    dr(d, 86, 24, 6, 12, h)

    dr(d, 76, 0, 6, 8, h); dr(d, 78, 0, 4, 4, hl)

    dr(d, 36, 28, 8, 28, h); dr(d, 84, 28, 8, 28, h)
    dr(d, 36, 36, 4, 20, hd); dr(d, 88, 36, 4, 20, hd)

    return img


def draw_male_portrait():
    W, H = 128, 192
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    s = P['skin']; sd = P['skin_shade']; sm = P['skin_mid']
    h = P['hair']; hd = P['hair_dark']; hl = P['hair_shine']
    e = P['eye_red']; ed = P['eye_dark']; el = P['eye_line']
    c = P['cloth']; cl = P['lace']; cd = P['lace_dark']
    r = P['ribbon']; rd = P['ribbon_dark']
    b = P['black']; m = P['mouth']; sh = P['shadow']

    dr(d, 28, 180, 72, 8, sh)

    dr(d, 48, 120, 14, 48, s); dr(d, 48, 120, 4, 48, sd)
    dr(d, 66, 120, 14, 48, s); dr(d, 66, 120, 4, 48, sd)

    dr(d, 46, 172, 18, 8, b); dr(d, 66, 172, 18, 8, b)

    dr(d, 48, 116, 32, 24, c); dr(d, 48, 116, 32, 4, cl); dr(d, 52, 132, 24, 6, cl)
    dr(d, 48, 140, 32, 16, c); dr(d, 48, 140, 32, 4, cl); dr(d, 52, 152, 24, 4, cl)

    dr(d, 56, 80, 16, 8, r); dr(d, 46, 76, 4, 12, cd); dr(d, 78, 76, 4, 12, cd)
    dr(d, 44, 72, 40, 28, c); dr(d, 44, 72, 40, 6, cl); dr(d, 44, 96, 40, 6, cl)

    dr(d, 28, 72, 12, 44, s); dr(d, 28, 72, 4, 44, sd)
    dr(d, 88, 72, 12, 44, s); dr(d, 88, 72, 4, 44, sd)
    dr(d, 28, 72, 12, 12, c); dr(d, 88, 72, 12, 12, c)

    dr(d, 60, 60, 8, 12, sd)

    dr(d, 40, 16, 48, 40, s); dr(d, 40, 16, 8, 40, sd); dr(d, 80, 16, 8, 40, sm)
    dr(d, 44, 52, 40, 8, s); dr(d, 48, 56, 32, 8, s)

    ey = 30
    dr(d, 50, ey-2, 16, 6, ed); dr(d, 50, ey+4, 16, 8, (255,245,250))
    dr(d, 54, ey+4, 8, 8, e); dr(d, 56, ey+6, 4, 4, ed)
    dr(d, 58, ey+4, 2, 2, (255,255,255)); dr(d, 54, ey+8, 2, 2, (255,255,255))
    dr(d, 50, ey+12, 16, 4, e)
    dr(d, 48, ey-2, 6, 2, el); dr(d, 46, ey, 4, 2, el); dr(d, 64, ey-2, 4, 2, el)

    dr(d, 70, ey-2, 16, 6, ed); dr(d, 70, ey+4, 16, 8, (255,245,250))
    dr(d, 74, ey+4, 8, 8, e); dr(d, 76, ey+6, 4, 4, ed)
    dr(d, 78, ey+4, 2, 2, (255,255,255)); dr(d, 74, ey+8, 2, 2, (255,255,255))
    dr(d, 70, ey+12, 16, 4, e)
    dr(d, 84, ey-2, 6, 2, el); dr(d, 88, ey, 4, 2, el); dr(d, 72, ey-2, 4, 2, el)

    dr(d, 50, 26, 14, 2, hd); dr(d, 52, 24, 4, 2, hd)
    dr(d, 72, 26, 14, 2, hd); dr(d, 76, 24, 4, 2, hd)

    dr(d, 62, 54, 4, 2, m)

    for x in range(40, 50):
        for y in range(44, 52):
            dot(d, x, y, (255, 160, 170, 90))
    for x in range(78, 88):
        for y in range(44, 52):
            dot(d, x, y, (255, 160, 170, 90))

    dr(d, 40, 4, 48, 20, h); dr(d, 36, 12, 10, 36, h); dr(d, 82, 12, 10, 36, h)
    dr(d, 32, 20, 8, 28, h); dr(d, 88, 20, 8, 28, h)
    dr(d, 44, 8, 40, 12, hl); dr(d, 48, 12, 8, 8, hd); dr(d, 72, 12, 8, 8, hd)
    dr(d, 40, 20, 48, 4, hd); dr(d, 76, 0, 6, 8, hl)

    return img


def draw_npc_lily():
    W, H = 48, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)

    dr(d, 20, 50, 20, 10, P['shadow'])

    # 腿
    dr(d, 20, 40, 5, 18, P['skin'])
    dr(d, 28, 40, 5, 18, P['skin'])
    dr(d, 20, 48, 5, 10, (255,200,220,255))
    dr(d, 28, 48, 5, 10, (255,200,220,255))

    # 粉色裙子
    dr(d, 18, 30, 18, 16, (255,180,200,255))
    dr(d, 16, 38, 22, 8, (255,180,200,255))
    dr(d, 18, 32, 18, 2, (255,150,180,255))

    # 上身
    dr(d, 20, 18, 14, 14, (255,220,230,255))
    dr(d, 24, 22, 6, 4, (255,150,180,255))

    # 手臂
    dr(d, 14, 20, 5, 14, P['skin'])
    dr(d, 35, 20, 5, 14, P['skin'])

    # 头
    dr(d, 20, 4, 14, 16, P['skin'])
    dr(d, 20, 4, 3, 16, P['skin_shade'])

    # 大眼睛
    dr(d, 22, 10, 5, 6, (100,200,180,255))
    dr(d, 22, 10, 5, 2, (60,160,140,255))
    dr(d, 23, 11, 2, 2, P['eye_white'])
    dr(d, 29, 10, 5, 6, (100,200,180,255))
    dr(d, 29, 10, 5, 2, (60,160,140,255))
    dr(d, 30, 11, 2, 2, P['eye_white'])

    # 嘴
    dr(d, 25, 16, 4, 1, P['mouth'])

    # 腮红
    dr(d, 19, 13, 3, 3, P['blush'])
    dr(d, 33, 13, 3, 3, P['blush'])

    # 粉色双马尾
    dr(d, 18, 2, 18, 8, (255,160,180,255))
    dr(d, 12, 6, 6, 20, (255,160,180,255))
    dr(d, 36, 6, 6, 20, (255,160,180,255))
    dr(d, 10, 12, 4, 16, (255,140,160,255))
    dr(d, 40, 12, 4, 16, (255,140,160,255))
    dr(d, 20, 4, 14, 4, (255,180,200,255))

    # 蝴蝶结
    dr(d, 14, 4, 4, 4, (255,100,140,255))
    dr(d, 36, 4, 4, 4, (255,100,140,255))

    return img


def draw_npc_hein():
    W, H = 48, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)

    dr(d, 20, 50, 20, 10, P['shadow'])

    dr(d, 20, 40, 5, 18, P['black'])
    dr(d, 28, 40, 5, 18, P['black'])

    dr(d, 18, 24, 18, 20, (60,60,80,255))
    dr(d, 24, 26, 6, 8, P['white'])
    dr(d, 26, 28, 2, 2, P['gold'])

    dr(d, 14, 24, 5, 16, (60,60,80,255))
    dr(d, 35, 24, 5, 16, (60,60,80,255))

    dr(d, 20, 4, 14, 16, P['skin'])
    dr(d, 20, 4, 3, 16, P['skin_shade'])

    dr(d, 22, 10, 5, 6, (80,120,200,255))
    dr(d, 22, 10, 5, 2, (50,90,160,255))
    dr(d, 23, 11, 2, 2, P['eye_white'])
    dr(d, 29, 10, 5, 6, (80,120,200,255))
    dr(d, 29, 10, 5, 2, (50,90,160,255))
    dr(d, 30, 11, 2, 2, P['eye_white'])

    dr(d, 25, 16, 4, 1, P['mouth'])

    dr(d, 18, 2, 18, 8, (40,50,80,255))
    dr(d, 16, 6, 5, 14, (40,50,80,255))
    dr(d, 33, 6, 5, 14, (40,50,80,255))
    dr(d, 20, 4, 14, 4, (60,70,100,255))

    return img


def draw_boss():
    W, H = 80, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    colors = {
        'body': (80, 40, 120, 255),
        'body_light': (120, 60, 160, 255),
        'eye': (255, 80, 80, 255),
        'eye_glow': (255, 200, 200, 255),
        'tentacle': (100, 50, 140, 255),
    }
    dr(d, 20, 10, 40, 30, colors['body'])
    dr(d, 25, 12, 30, 20, colors['body_light'])
    dr(d, 30, 16, 20, 14, colors['eye'])
    dr(d, 34, 19, 6, 6, colors['eye_glow'])
    dr(d, 32, 18, 3, 3, P['eye_white'])
    for i, tx in enumerate([10, 18, 26, 50, 58, 66]):
        dr(d, tx, 38, 6, 20 - i*2, colors['tentacle'])
        dr(d, tx+1, 56, 4, 4, colors['body'])
    dr(d, 22, 14, 4, 4, colors['body_light'])
    dr(d, 52, 20, 4, 4, colors['body_light'])
    dr(d, 28, 32, 3, 3, colors['body_light'])
    return img


def draw_bg_cabin():
    W, H = 340, 400
    img = create_image(W, H, (25, 20, 35, 255))
    d = ImageDraw.Draw(img)
    for y in range(320, H, 8):
        dr(d, 0, y, W, 4, (60, 45, 35, 255))
        dr(d, 0, y+4, W, 4, (50, 38, 30, 255))
    dr(d, 0, 0, W, 320, (35, 30, 50, 255))
    for x in range(0, W, 20):
        dr(d, x, 0, 1, 320, (40, 35, 55, 255))
    dr(d, 120, 40, 100, 120, (20, 18, 30, 255))
    dr(d, 125, 45, 90, 110, (15, 25, 50, 255))
    dr(d, 165, 45, 4, 110, (60, 55, 45, 255))
    dr(d, 125, 95, 90, 4, (60, 55, 45, 255))
    dr(d, 140, 60, 2, 2, (255, 255, 220, 255))
    dr(d, 180, 75, 2, 2, (255, 255, 220, 255))
    dr(d, 155, 110, 2, 2, (255, 255, 220, 255))
    dr(d, 20, 240, 80, 60, (50, 40, 60, 255))
    dr(d, 20, 240, 80, 15, (70, 55, 75, 255))
    dr(d, 25, 255, 70, 40, (80, 60, 90, 255))
    dr(d, 25, 255, 70, 8, (100, 80, 110, 255))
    dr(d, 240, 180, 80, 120, (55, 45, 35, 255))
    dr(d, 242, 182, 36, 116, (65, 55, 45, 255))
    dr(d, 282, 182, 36, 116, (65, 55, 45, 255))
    dr(d, 278, 182, 4, 116, (45, 38, 30, 255))
    dr(d, 100, 300, 140, 20, (80, 40, 60, 255))
    dr(d, 105, 302, 130, 16, (70, 35, 50, 255))
    return img


def draw_bg_city():
    W, H = 640, 480
    img = create_image(W, H, (80, 120, 160, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, 200):
        c = int(80 + y * 0.4)
        dr(d, 0, y, W, 1, (c, c+40, c+80, 255))
    dr(d, 0, 300, W, 180, (60, 80, 60, 255))
    for x in range(0, W, 40):
        for y in range(300, H, 20):
            dr(d, x, y, 38, 18, (70, 90, 70, 255))
    for bx in [50, 200, 380, 520]:
        bw, bh, by = 100, 180, 300 - 180
        dr(d, bx, by, bw, bh, (50, 50, 70, 255))
        dr(d, bx+5, by+10, bw-10, bh-20, (60, 60, 80, 255))
        dr(d, bx+40, by-40, 20, 40, (50, 50, 70, 255))
        dr(d, bx+45, by-50, 10, 10, (50, 50, 70, 255))
        for wy in range(by+20, by+bh-20, 30):
            dr(d, bx+20, wy, 20, 20, (30, 30, 50, 255))
            dr(d, bx+60, wy, 20, 20, (30, 30, 50, 255))
    return img


def draw_bg_sea():
    W, H = 640, 480
    img = create_image(W, H, (10, 20, 50, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, H):
        c = int(10 + y * 0.15)
        dr(d, 0, y, W, 1, (c//2, c, c+20, 255))
    import random
    random.seed(42)
    for _ in range(30):
        bx = random.randint(0, W-4)
        by = random.randint(50, H-10)
        dr(d, bx, by, 3, 3, (200, 230, 255, 100))
    for rx in [0, 100, 250, 400, 550]:
        rh = random.randint(30, 60)
        dr(d, rx, H-rh, 80, rh, (20, 25, 40, 255))
        dr(d, rx+10, H-rh+10, 60, rh-20, (30, 35, 50, 255))
    return img


if __name__ == '__main__':
    print("Generating cute pixel art sprites V3...")
    save(draw_female_cute('full', False), 'sprite_f.png')
    save(draw_female_cute('full', True), 'sprite_f_damaged.png')
    save(draw_female_cute('damaged', False), 'sprite_f_broken.png')
    save(draw_female_cute('underwear', False), 'sprite_f_underwear.png')
    save(draw_male_cute('full', False), 'sprite_m.png')
    save(draw_male_cute('full', True), 'sprite_m_damaged.png')
    save(draw_male_cute('underwear', False), 'sprite_m_underwear.png')
    save(draw_female_portrait(), 'char_preview_f.png')
    save(draw_male_portrait(), 'char_preview_m.png')
    save(draw_npc_lily(), 'sprite_lily.png')
    save(draw_npc_hein(), 'sprite_hein.png')
    save(draw_boss(), 'sprite_boss.png')
    save(draw_bg_cabin(), 'bg_cabin.png')
    save(draw_bg_city(), 'bg_city.png')
    save(draw_bg_sea(), 'bg_sea.png')
    print("\nAll cute sprites generated!")
