#!/usr/bin/env python3
"""
若若的钓鱼王国 - 原创主角精灵图生成器 V2
两种形态：
  - 创角形态(64x96 原生像素) -> 放大为 128x192 预览
  - Q版形态(32x48 原生像素) -> 用于船舱移动
"""
from PIL import Image, ImageDraw
import os, numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def save(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    img.save(path)
    print(f"Saved: {path}")

def create_image(w, h, bg=(0,0,0,0)):
    return Image.new('RGBA', (w, h), bg)

def dr(draw, x, y, w, h, color):
    if w <= 0 or h <= 0: return
    draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

def dot(draw, x, y, color):
    draw.point((x, y), fill=color)

# ========== 若若调色板 ==========
P = {
    'outline':    (50, 45, 65, 255),
    'skin':       (255, 228, 210, 255),
    'skin_mid':   (248, 200, 180, 255),
    'skin_dark':  (235, 180, 155, 255),
    'skin_light': (255, 235, 220, 255),
    'blush':      (255, 160, 170, 180),

    'eye_red':    (220, 50, 70, 255),
    'eye_dark':   (160, 30, 50, 255),
    'eye_core':   (255, 100, 120, 255),
    'eye_white':  (255, 255, 255, 255),
    'eye_line':   (80, 20, 30, 255),

    'hair':       (245, 245, 255, 255),
    'hair_mid':   (220, 220, 240, 255),
    'hair_dark':  (180, 180, 210, 255),
    'hair_shine': (255, 255, 255, 255),

    'cloth':      (255, 250, 250, 255),
    'cloth_mid':  (245, 240, 245, 255),
    'cloth_dark': (230, 225, 235, 255),
    'lace':       (255, 220, 230, 255),
    'lace_dark':  (230, 190, 210, 255),
    'ribbon':     (220, 60, 90, 255),
    'ribbon_dark':(180, 40, 60, 255),

    'mouth':      (220, 100, 120, 255),
    'black':      (30, 28, 40, 255),
    'shadow':     (0, 0, 0, 40),
}


# ============================================================
# 若若 - 标准形态 (64x96 原生像素)
# ============================================================
def draw_ruoru_64x96(dress_type='full'):
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    o = P['outline']
    sk = P['skin']
    skm = P['skin_mid']
    skd = P['skin_dark']
    skl = P['skin_light']
    hr = P['hair']
    hrm = P['hair_mid']
    hrd = P['hair_dark']
    hrl = P['hair_shine']
    ey = P['eye_red']
    eyd = P['eye_dark']
    eyc = P['eye_core']
    ew = P['eye_white']
    cl = P['cloth']
    clm = P['cloth_mid']
    cld = P['cloth_dark']
    la = P['lace']
    lad = P['lace_dark']
    ri = P['ribbon']
    rid = P['ribbon_dark']
    bl = P['blush']
    mo = P['mouth']

    # ===== 后发（底层长发） =====
    dr(d, 10, 10, 6, 32, hrd)
    dr(d, 12, 8, 4, 36, hr)
    dr(d, 14, 6, 3, 40, hrm)
    dr(d, 48, 10, 6, 32, hrd)
    dr(d, 48, 8, 4, 36, hr)
    dr(d, 47, 6, 3, 40, hrm)
    dr(d, 8, 24, 4, 28, hrd)
    dr(d, 10, 22, 3, 32, hr)
    dr(d, 52, 24, 4, 28, hrd)
    dr(d, 51, 22, 3, 32, hr)
    dr(d, 6, 40, 4, 20, hrd)
    dr(d, 54, 40, 4, 20, hrd)

    # ===== 阴影 =====
    dr(d, 16, 90, 32, 4, P['shadow'])

    # ===== 腿部 =====
    dr(d, 23, 64, 9, 24, skd)
    dr(d, 24, 64, 7, 24, sk)
    dr(d, 24, 64, 2, 24, skd)
    dr(d, 24, 72, 2, 8, skl)
    dr(d, 32, 64, 9, 24, skd)
    dr(d, 33, 64, 7, 24, sk)
    dr(d, 33, 64, 2, 24, skd)
    dr(d, 37, 72, 2, 8, skl)

    # 小皮鞋
    dr(d, 22, 86, 10, 5, o)
    dr(d, 23, 87, 8, 3, P['black'])
    dr(d, 25, 86, 2, 2, ri)
    dr(d, 32, 86, 10, 5, o)
    dr(d, 33, 87, 8, 3, P['black'])
    dr(d, 35, 86, 2, 2, ri)

    # ===== 身体 =====
    if dress_type == 'full':
        # 白色蕾丝内衣
        # 下身
        dr(d, 21, 50, 22, 16, o)
        dr(d, 22, 51, 20, 14, cl)
        dr(d, 22, 51, 20, 3, hrl)
        dr(d, 24, 55, 16, 2, la)
        dr(d, 26, 60, 12, 2, la)
        # 上身
        dr(d, 21, 36, 22, 16, o)
        dr(d, 22, 37, 20, 14, cl)
        dr(d, 22, 37, 20, 3, hrl)
        dr(d, 24, 47, 16, 2, la)
        # 胸前装饰
        dr(d, 28, 40, 8, 6, o)
        dr(d, 29, 41, 6, 4, ri)
        dr(d, 31, 42, 2, 2, rid)
        # 肩带
        dr(d, 22, 36, 3, 10, la)
        dr(d, 39, 36, 3, 10, la)
        # 蕾丝细节
        for sx in range(24, 40, 3):
            for sy in range(42, 58, 4):
                dot(d, sx, sy, (255,255,255,120))
    elif dress_type == 'damaged':
        dr(d, 21, 36, 22, 14, o)
        dr(d, 22, 37, 20, 10, cl)
        dr(d, 22, 37, 20, 3, hrl)
        dr(d, 22, 50, 18, 10, o)
        dr(d, 23, 51, 16, 8, cl)
        dr(d, 23, 51, 16, 2, la)
        dr(d, 25, 42, 6, 6, sk)
        dr(d, 33, 52, 4, 4, sk)
        dr(d, 26, 43, 2, 2, ri)
    else:
        dr(d, 21, 36, 22, 30, o)
        dr(d, 22, 37, 20, 28, cl)
        dr(d, 22, 37, 20, 3, hrl)
        dr(d, 22, 47, 20, 3, la)
        dr(d, 24, 52, 16, 14, cl)
        dr(d, 24, 52, 16, 2, la)

    # ===== 手臂 =====
    dr(d, 13, 38, 8, 22, o)
    dr(d, 14, 39, 6, 20, sk)
    dr(d, 14, 39, 2, 20, skd)
    dr(d, 15, 44, 2, 8, skl)
    if dress_type == 'full':
        dr(d, 14, 38, 6, 8, cl)
        dr(d, 14, 38, 6, 2, hrl)
    dr(d, 43, 38, 8, 22, o)
    dr(d, 44, 39, 6, 20, sk)
    dr(d, 44, 39, 2, 20, skd)
    dr(d, 47, 44, 2, 8, skl)
    if dress_type == 'full':
        dr(d, 44, 38, 6, 8, cl)
        dr(d, 44, 38, 6, 2, hrl)

    # ===== 脖子 =====
    dr(d, 29, 32, 6, 6, o)
    dr(d, 30, 33, 4, 4, skd)

    # ===== 头部 =====
    # 脸轮廓
    dr(d, 19, 10, 26, 24, o)
    dr(d, 20, 11, 24, 22, sk)
    dr(d, 20, 11, 4, 22, skd)
    dr(d, 38, 11, 6, 22, skl)
    dr(d, 22, 28, 20, 6, sk)
    dr(d, 24, 30, 16, 4, sk)
    dr(d, 26, 32, 12, 2, sk)
    dr(d, 22, 26, 4, 4, skd)
    dr(d, 38, 26, 4, 4, skl)

    # ===== 精灵耳 =====
    dr(d, 17, 18, 4, 8, o)
    dr(d, 18, 19, 3, 6, sk)
    dr(d, 18, 19, 1, 6, skd)
    dr(d, 43, 18, 4, 8, o)
    dr(d, 44, 19, 3, 6, sk)
    dr(d, 44, 19, 1, 6, skl)

    # ===== 眼睛（大萌眼） =====
    ey_y = 16
    # 左眼
    dr(d, 23, ey_y, 11, 9, o)
    dr(d, 24, ey_y+1, 9, 2, eyd)
    dr(d, 24, ey_y+1, 9, 1, o)
    dr(d, 24, ey_y+3, 9, 4, (255,245,250))
    dr(d, 25, ey_y+3, 7, 4, ey)
    dr(d, 26, ey_y+3, 5, 2, eyc)
    dr(d, 27, ey_y+4, 3, 3, eyd)
    dr(d, 26, ey_y+3, 3, 3, ew)
    dr(d, 29, ey_y+5, 2, 2, ew)
    dr(d, 24, ey_y+7, 9, 2, ey)
    dr(d, 24, ey_y+8, 9, 1, o)
    dr(d, 22, ey_y, 3, 1, o)
    dr(d, 23, ey_y-1, 2, 1, o)
    dr(d, 32, ey_y, 3, 1, o)
    dr(d, 32, ey_y-1, 2, 1, o)

    # 右眼
    dr(d, 34, ey_y, 11, 9, o)
    dr(d, 35, ey_y+1, 9, 2, eyd)
    dr(d, 35, ey_y+1, 9, 1, o)
    dr(d, 35, ey_y+3, 9, 4, (255,245,250))
    dr(d, 36, ey_y+3, 7, 4, ey)
    dr(d, 37, ey_y+3, 5, 2, eyc)
    dr(d, 38, ey_y+4, 3, 3, eyd)
    dr(d, 37, ey_y+3, 3, 3, ew)
    dr(d, 40, ey_y+5, 2, 2, ew)
    dr(d, 35, ey_y+7, 9, 2, ey)
    dr(d, 35, ey_y+8, 9, 1, o)
    dr(d, 33, ey_y, 3, 1, o)
    dr(d, 33, ey_y-1, 2, 1, o)
    dr(d, 43, ey_y, 3, 1, o)
    dr(d, 43, ey_y-1, 2, 1, o)

    # 眉毛
    dr(d, 24, 13, 3, 1, hrd)
    dr(d, 26, 12, 4, 1, hrd)
    dr(d, 30, 13, 3, 1, hrd)
    dr(d, 35, 13, 3, 1, hrd)
    dr(d, 37, 12, 4, 1, hrd)
    dr(d, 41, 13, 3, 1, hrd)

    # 嘴
    dr(d, 30, 27, 4, 2, o)
    dr(d, 31, 28, 2, 1, mo)
    dr(d, 30, 27, 1, 1, o)
    dr(d, 33, 27, 1, 1, o)

    # 腮红
    for x in range(19, 24):
        for y in range(22, 26):
            dot(d, x, y, bl)
    for x in range(40, 45):
        for y in range(22, 26):
            dot(d, x, y, bl)

    # ===== 前发（蓬松层次） =====
    # 头顶
    dr(d, 18, 4, 28, 10, o)
    dr(d, 19, 5, 26, 8, hr)
    dr(d, 20, 6, 24, 6, hrl)
    dr(d, 22, 7, 20, 4, hr)
    dr(d, 24, 8, 16, 2, hrl)
    # 刘海
    dr(d, 18, 10, 28, 8, o)
    dr(d, 19, 11, 26, 6, hr)
    dr(d, 20, 12, 5, 4, hrl)
    dr(d, 28, 12, 8, 4, hrl)
    dr(d, 38, 12, 6, 4, hrl)
    dr(d, 21, 13, 3, 3, hrm)
    dr(d, 35, 13, 3, 3, hrm)
    # 两侧前发
    dr(d, 16, 12, 5, 18, o)
    dr(d, 17, 13, 4, 16, hr)
    dr(d, 17, 14, 2, 12, hrd)
    dr(d, 18, 16, 2, 8, hrl)
    dr(d, 43, 12, 5, 18, o)
    dr(d, 44, 13, 4, 16, hr)
    dr(d, 45, 14, 2, 12, hrd)
    dr(d, 44, 16, 2, 8, hrl)
    # 更长的发丝
    dr(d, 14, 22, 4, 16, o)
    dr(d, 15, 23, 3, 14, hr)
    dr(d, 15, 25, 2, 10, hrd)
    dr(d, 47, 22, 4, 16, o)
    dr(d, 47, 23, 3, 14, hr)
    dr(d, 48, 25, 2, 10, hrd)

    return img


# ============================================================
# 糯天帝 - 标准形态 (64x96)
# ============================================================
def draw_nuotiandi_64x96(dress_type='full'):
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    o = P['outline']
    sk = P['skin']
    skd = P['skin_dark']
    skm = P['skin_mid']
    hr = (60, 58, 75, 255)
    hrd = (40, 38, 55, 255)
    hrl = (80, 78, 95, 255)
    ey = P['eye_red']
    eyd = P['eye_dark']
    ew = P['eye_white']
    cl = P['cloth']
    la = P['lace']
    ri = P['ribbon']
    mo = P['mouth']

    dr(d, 16, 90, 32, 4, P['shadow'])

    # 腿
    dr(d, 24, 60, 7, 24, P['skin'])
    dr(d, 24, 60, 2, 24, P['skin_dark'])
    dr(d, 33, 60, 7, 24, P['skin'])
    dr(d, 33, 60, 2, 24, P['skin_dark'])

    # 白色短裤
    if dress_type != 'underwear':
        dr(d, 24, 58, 16, 12, cl)
        dr(d, 24, 58, 16, 2, la)
        dr(d, 26, 66, 12, 3, la)
    else:
        dr(d, 24, 58, 16, 8, cl)
        dr(d, 24, 58, 16, 2, la)
        for sx in range(26, 38, 2):
            for sy in range(58, 66, 2):
                dot(d, sx, sy, (255,255,255,60))

    # 鞋子
    dr(d, 23, 86, 9, 4, P['black'])
    dr(d, 33, 86, 9, 4, P['black'])

    # 上身
    if dress_type == 'full':
        dr(d, 22, 36, 20, 14, cl)
        dr(d, 22, 36, 20, 3, la)
        dr(d, 22, 46, 20, 3, la)
        dr(d, 28, 40, 8, 4, ri)
        dr(d, 22, 36, 2, 10, la)
        dr(d, 40, 36, 2, 10, la)
    elif dress_type == 'damaged':
        dr(d, 22, 36, 20, 10, cl)
        dr(d, 22, 36, 20, 3, la)
        dr(d, 26, 42, 5, 4, sk)
        dr(d, 36, 44, 3, 3, sk)
        dr(d, 25, 41, 2, 2, ri)
    else:
        dr(d, 22, 36, 20, 14, cl)
        dr(d, 22, 36, 20, 3, la)
        for sx in range(24, 40, 2):
            for sy in range(38, 50, 2):
                dot(d, sx, sy, (255,255,255,60))

    # 手臂
    dr(d, 14, 36, 6, 22, sk)
    dr(d, 14, 36, 2, 22, skd)
    dr(d, 44, 36, 6, 22, sk)
    dr(d, 44, 36, 2, 22, skd)
    if dress_type != 'underwear':
        dr(d, 14, 36, 6, 6, cl)
        dr(d, 44, 36, 6, 6, cl)

    # 头
    dr(d, 30, 30, 4, 6, skd)
    dr(d, 22, 8, 20, 22, sk)
    dr(d, 22, 8, 4, 22, skd)
    dr(d, 38, 8, 4, 22, skm)
    dr(d, 24, 28, 16, 4, sk)

    # 眼睛（细长）
    sclera_m = (255, 245, 250)
    dr(d, 25, 17, 8, 2, eyd)
    dr(d, 25, 19, 8, 3, sclera_m)
    dr(d, 27, 19, 4, 3, ey)
    dr(d, 28, 20, 2, 2, eyd)
    dr(d, 29, 19, 1, 1, ew)
    dr(d, 25, 22, 8, 1, ey)

    dr(d, 35, 17, 8, 2, eyd)
    dr(d, 35, 19, 8, 3, sclera_m)
    dr(d, 37, 19, 4, 3, ey)
    dr(d, 38, 20, 2, 2, eyd)
    dr(d, 39, 19, 1, 1, ew)
    dr(d, 35, 22, 8, 1, ey)

    # 睫毛
    dr(d, 24, 16, 3, 1, P['eye_line'])
    dr(d, 23, 17, 2, 1, P['eye_line'])
    dr(d, 32, 16, 2, 1, P['eye_line'])
    dr(d, 38, 16, 3, 1, P['eye_line'])
    dr(d, 41, 17, 2, 1, P['eye_line'])
    dr(d, 36, 16, 2, 1, P['eye_line'])

    # 眉毛
    dr(d, 24, 13, 8, 1, hrd)
    dr(d, 25, 12, 3, 1, hrd)
    dr(d, 36, 13, 8, 1, hrd)
    dr(d, 38, 12, 3, 1, hrd)

    # 嘴
    dr(d, 31, 27, 2, 1, mo)

    # 腮红
    dr(d, 20, 22, 5, 4, P['blush'])
    dr(d, 39, 22, 5, 4, P['blush'])

    # 头发
    dr(d, 20, 2, 24, 10, hr)
    dr(d, 18, 6, 5, 18, hr)
    dr(d, 41, 6, 5, 18, hr)
    dr(d, 16, 10, 4, 14, hr)
    dr(d, 44, 10, 4, 14, hr)
    dr(d, 22, 4, 20, 6, hrl)
    dr(d, 24, 6, 4, 4, hrd)
    dr(d, 36, 6, 4, 4, hrd)
    dr(d, 38, 0, 3, 3, hrl)

    return img


# ============================================================
# 若若 - Q版 (32x48)
# ============================================================
def draw_ruoru_chibi(dress_type='full'):
    W, H = 32, 48
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    o = P['outline']
    sk = P['skin']
    skd = P['skin_dark']
    skl = P['skin_light']
    hr = P['hair']
    hrd = P['hair_dark']
    hrl = P['hair_shine']
    ey = P['eye_red']
    eyd = P['eye_dark']
    ew = P['eye_white']
    cl = P['cloth']
    la = P['lace']
    ri = P['ribbon']
    bl = P['blush']
    mo = P['mouth']

    # 地面阴影
    dr(d, 8, 44, 16, 2, P['shadow'])

    # 腿部
    dr(d, 11, 34, 4, 10, skd)
    dr(d, 12, 34, 2, 10, sk)
    dr(d, 17, 34, 4, 10, skd)
    dr(d, 18, 34, 2, 10, sk)
    # 脚
    dr(d, 11, 44, 4, 2, o)
    dr(d, 17, 44, 4, 2, o)

    # 身体
    if dress_type == 'full':
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 10, cl)
        dr(d, 11, 25, 10, 2, hrl)
        dr(d, 12, 30, 8, 2, la)
        dr(d, 14, 27, 4, 3, ri)
    elif dress_type == 'damaged':
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 8, cl)
        dr(d, 13, 28, 3, 3, sk)
    else:
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 10, cl)

    # 手臂
    dr(d, 6, 26, 4, 6, sk)
    dr(d, 22, 26, 4, 6, sk)

    # 头部（大头）
    dr(d, 6, 4, 20, 22, o)
    dr(d, 8, 6, 16, 18, sk)
    dr(d, 8, 6, 4, 18, skd)
    dr(d, 20, 6, 4, 18, skl)

    # 耳朵
    dr(d, 4, 12, 4, 6, o)
    dr(d, 6, 14, 2, 4, sk)
    dr(d, 24, 12, 4, 6, o)
    dr(d, 24, 14, 2, 4, sk)

    # 眼睛（大萌眼）
    # 左眼
    dr(d, 10, 12, 6, 6, o)
    dr(d, 11, 13, 4, 4, ey)
    dr(d, 12, 14, 2, 2, eyd)
    dr(d, 11, 13, 2, 2, ew)
    # 右眼
    dr(d, 18, 12, 6, 6, o)
    dr(d, 19, 13, 4, 4, ey)
    dr(d, 20, 14, 2, 2, eyd)
    dr(d, 19, 13, 2, 2, ew)

    # 眉毛
    dr(d, 10, 9, 4, 1, hrd)
    dr(d, 18, 9, 4, 1, hrd)

    # 嘴
    dr(d, 15, 20, 2, 1, mo)

    # 腮红
    dr(d, 8, 16, 3, 2, bl)
    dr(d, 21, 16, 3, 2, bl)

    # 头发（蓬松，覆盖头部）
    # 头顶
    dr(d, 4, 0, 24, 8, o)
    dr(d, 6, 2, 20, 4, hr)
    dr(d, 8, 2, 16, 2, hrl)
    # 刘海
    dr(d, 4, 6, 24, 6, o)
    dr(d, 6, 8, 20, 4, hr)
    dr(d, 8, 8, 6, 3, hrl)
    dr(d, 16, 8, 6, 3, hrl)
    # 两侧
    dr(d, 2, 8, 6, 12, o)
    dr(d, 4, 10, 4, 8, hr)
    dr(d, 24, 8, 6, 12, o)
    dr(d, 24, 10, 4, 8, hr)
    # 后发
    dr(d, 0, 14, 4, 10, o)
    dr(d, 2, 16, 2, 6, hrd)
    dr(d, 28, 14, 4, 10, o)
    dr(d, 28, 16, 2, 6, hrd)

    return img


# ============================================================
# 糯天帝 - Q版 (32x48)
# ============================================================
def draw_nuotiandi_chibi(dress_type='full'):
    W, H = 32, 48
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    o = P['outline']
    sk = P['skin']
    skd = P['skin_dark']
    hr = (60, 58, 75, 255)
    hrd = (40, 38, 55, 255)
    ey = P['eye_red']
    eyd = P['eye_dark']
    ew = P['eye_white']
    cl = P['cloth']
    mo = P['mouth']

    # 阴影
    dr(d, 8, 44, 16, 2, P['shadow'])

    # 腿
    dr(d, 11, 34, 4, 10, skd)
    dr(d, 12, 34, 2, 10, sk)
    dr(d, 17, 34, 4, 10, skd)
    dr(d, 18, 34, 2, 10, sk)
    dr(d, 11, 44, 4, 2, o)
    dr(d, 17, 44, 4, 2, o)

    # 身体
    if dress_type == 'full':
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 10, cl)
    elif dress_type == 'damaged':
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 8, cl)
        dr(d, 13, 28, 3, 3, sk)
    else:
        dr(d, 10, 24, 12, 12, o)
        dr(d, 11, 25, 10, 10, cl)

    # 手臂
    dr(d, 6, 26, 4, 6, sk)
    dr(d, 22, 26, 4, 6, sk)

    # 头部
    dr(d, 6, 4, 20, 22, o)
    dr(d, 8, 6, 16, 18, sk)
    dr(d, 8, 6, 4, 18, skd)

    # 眼睛（细长）
    dr(d, 10, 14, 6, 2, o)
    dr(d, 11, 14, 4, 2, ey)
    dr(d, 12, 14, 2, 2, eyd)
    dr(d, 11, 14, 1, 1, ew)
    dr(d, 18, 14, 6, 2, o)
    dr(d, 19, 14, 4, 2, ey)
    dr(d, 20, 14, 2, 2, eyd)
    dr(d, 19, 14, 1, 1, ew)

    # 眉毛
    dr(d, 10, 10, 5, 1, hrd)
    dr(d, 19, 10, 5, 1, hrd)

    # 嘴
    dr(d, 15, 20, 2, 1, mo)

    # 头发
    dr(d, 4, 0, 24, 8, o)
    dr(d, 6, 2, 20, 4, hr)
    dr(d, 4, 6, 6, 10, o)
    dr(d, 6, 8, 4, 6, hr)
    dr(d, 22, 6, 6, 10, o)
    dr(d, 22, 8, 4, 6, hr)
    dr(d, 2, 10, 4, 8, o)
    dr(d, 4, 12, 2, 4, hrd)
    dr(d, 26, 10, 4, 8, o)
    dr(d, 26, 12, 2, 4, hrd)
    # 刘海
    dr(d, 6, 6, 20, 3, hr)

    return img


def scale4x(img):
    return img.resize((img.width * 4, img.height * 4), Image.NEAREST)


if __name__ == '__main__':
    print("Generating original hero sprites V2...")

    # ========== 若若（女）==========
    # 标准形态 64x96
    ruoru_std = draw_ruoru_64x96('full')
    save(ruoru_std, 'sprite_f.png')
    save(scale4x(ruoru_std), 'sprite_f_preview.png')

    ruoru_damaged = draw_ruoru_64x96('damaged')
    save(ruoru_damaged, 'sprite_f_damaged.png')
    save(scale4x(ruoru_damaged), 'sprite_f_damaged_preview.png')

    ruoru_broken = draw_ruoru_64x96('broken')
    save(ruoru_broken, 'sprite_f_broken.png')
    save(scale4x(ruoru_broken), 'sprite_f_broken_preview.png')

    # Q版 32x48
    ruoru_q = draw_ruoru_chibi('full')
    save(ruoru_q, 'sprite_f_q.png')
    save(scale4x(ruoru_q), 'sprite_f_q_preview.png')

    ruoru_q_damaged = draw_ruoru_chibi('damaged')
    save(ruoru_q_damaged, 'sprite_f_q_damaged.png')
    save(scale4x(ruoru_q_damaged), 'sprite_f_q_damaged_preview.png')

    # 预览大图 128x192 (从64x96放大)
    char_preview_f = ruoru_std.resize((128, 192), Image.NEAREST)
    save(char_preview_f, 'char_preview_f.png')
    save(scale4x(char_preview_f), 'char_preview_f_preview.png')

    # ========== 糯天帝（男）==========
    nuotd_std = draw_nuotiandi_64x96('full')
    save(nuotd_std, 'sprite_m.png')
    save(scale4x(nuotd_std), 'sprite_m_preview.png')

    nuotd_damaged = draw_nuotiandi_64x96('damaged')
    save(nuotd_damaged, 'sprite_m_damaged.png')
    save(scale4x(nuotd_damaged), 'sprite_m_damaged_preview.png')

    nuotd_broken = draw_nuotiandi_64x96('broken')
    save(nuotd_broken, 'sprite_m_broken.png')
    save(scale4x(nuotd_broken), 'sprite_m_broken_preview.png')

    nuotd_q = draw_nuotiandi_chibi('full')
    save(nuotd_q, 'sprite_m_q.png')
    save(scale4x(nuotd_q), 'sprite_m_q_preview.png')

    nuotd_q_damaged = draw_nuotiandi_chibi('damaged')
    save(nuotd_q_damaged, 'sprite_m_q_damaged.png')
    save(scale4x(nuotd_q_damaged), 'sprite_m_q_damaged_preview.png')

    char_preview_m = nuotd_std.resize((128, 192), Image.NEAREST)
    save(char_preview_m, 'char_preview_m.png')
    save(scale4x(char_preview_m), 'char_preview_m_preview.png')

    print("\nAll hero sprites generated!")
