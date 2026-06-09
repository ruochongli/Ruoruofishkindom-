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


# ========== 创角立绘预览（128x192 参考全身比例版）==========
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

    # 地面阴影
    dr(d, 24, 176, 80, 6, sh)

    # ===== 腿（修长，自然微分站立）=====
    # 左腿
    dr(d, 46, 116, 14, 56, s); dr(d, 46, 116, 4, 56, sd)
    # 右腿
    dr(d, 68, 116, 14, 56, s); dr(d, 68, 116, 4, 56, sd)
    # 膝盖阴影
    dr(d, 48, 144, 10, 2, sd); dr(d, 70, 144, 10, 2, sd)

    # 脚（裸足/简单平底）
    dr(d, 46, 172, 14, 6, b); dr(d, 68, 172, 14, 6, b)
    dr(d, 48, 174, 4, 2, r); dr(d, 70, 174, 4, 2, r)

    # ===== 白色内衣（修身收腰短款）=====
    # 下半身（白色内裤）
    dr(d, 50, 96, 28, 20, c); dr(d, 50, 96, 28, 4, cl); dr(d, 54, 112, 20, 4, cl)
    # 上半身（白色抹胸）
    dr(d, 48, 60, 32, 36, c); dr(d, 48, 60, 32, 6, cl); dr(d, 48, 90, 32, 6, cl)
    # 胸前红色装饰
    dr(d, 60, 74, 8, 6, r); dr(d, 62, 72, 4, 4, rd)
    # 肩带
    dr(d, 48, 58, 4, 16, cd); dr(d, 76, 58, 4, 16, cd)

    # ===== 双臂交叉胸前 =====
    # 左臂（从左侧伸到胸前）
    dr(d, 34, 66, 18, 10, s); dr(d, 34, 66, 4, 10, sd)
    dr(d, 38, 68, 14, 6, c)   # 袖口白色
    # 右臂（从右侧伸到胸前）
    dr(d, 76, 66, 18, 10, s); dr(d, 76, 66, 4, 10, sd)
    dr(d, 76, 68, 14, 6, c)   # 袖口白色
    # 交叉的手
    dr(d, 52, 68, 24, 6, s); dr(d, 52, 68, 4, 6, sd)

    # ===== 脖子 =====
    dr(d, 58, 52, 12, 10, sd)

    # ===== 尖耳（精灵耳，参考图特征）=====
    dr(d, 34, 26, 4, 10, s); dr(d, 34, 26, 2, 8, sd)
    dr(d, 32, 28, 2, 4, s)    # 耳尖
    dr(d, 90, 26, 4, 10, s); dr(d, 92, 26, 2, 8, sd)
    dr(d, 94, 28, 2, 4, s)    # 耳尖

    # ===== 脸（参考图比例，稍修长）=====
    dr(d, 42, 14, 44, 36, s); dr(d, 42, 14, 6, 36, sd); dr(d, 80, 14, 6, 36, sm)
    dr(d, 46, 46, 36, 6, s); dr(d, 50, 50, 28, 4, s)
    # 下巴略尖
    dr(d, 56, 54, 16, 2, s); dr(d, 60, 56, 8, 2, s)

    # ===== 五官（参考模板：细长上挑眼、细弯眉、小嘴、腮红）=====
    ey = 26
    # --- 左眼（细长上挑，外眼角高） ---
    # 上眼线 - 粗，眼尾上挑
    dr(d, 48, ey, 14, 2, el); dr(d, 48, ey+2, 14, 2, el)
    dr(d, 46, ey-2, 4, 2, el)      # 眼头上挑
    dr(d, 60, ey-2, 4, 2, el)      # 眼尾上挑
    dr(d, 48, ey+2, 14, 2, ed)     # 上眼睑阴影
    # 眼白（较小）
    dr(d, 50, ey+4, 10, 6, (255,245,250))
    # 瞳孔（细长）
    dr(d, 52, ey+4, 6, 4, e); dr(d, 54, ey+4, 4, 4, ed)
    # 高光（小而锐利）
    dr(d, 52, ey+4, 2, 2, (255,255,255))
    dr(d, 56, ey+6, 2, 2, (255,255,255))
    # 下眼睑
    dr(d, 50, ey+10, 10, 2, (240,210,220))
    # 睫毛（几根向上翘）
    dr(d, 60, ey-2, 2, 2, el); dr(d, 62, ey-4, 2, 2, el)

    # --- 右眼（细长上挑，外眼角高） ---
    dr(d, 72, ey, 14, 2, el); dr(d, 72, ey+2, 14, 2, el)
    dr(d, 70, ey-2, 4, 2, el)
    dr(d, 84, ey-2, 4, 2, el)
    dr(d, 72, ey+2, 14, 2, ed)
    dr(d, 74, ey+4, 10, 6, (255,245,250))
    dr(d, 76, ey+4, 6, 4, e); dr(d, 78, ey+4, 4, 4, ed)
    dr(d, 76, ey+4, 2, 2, (255,255,255))
    dr(d, 80, ey+6, 2, 2, (255,255,255))
    dr(d, 74, ey+10, 10, 2, (240,210,220))
    dr(d, 84, ey-2, 2, 2, el); dr(d, 86, ey-4, 2, 2, el)

    # --- 细弯眉（参考图：细、弯、位置在眼睛上方） ---
    dr(d, 50, 18, 4, 2, hd); dr(d, 54, 16, 6, 2, hd); dr(d, 60, 18, 4, 2, hd)
    dr(d, 74, 18, 4, 2, hd); dr(d, 78, 16, 6, 2, hd); dr(d, 84, 18, 4, 2, hd)

    # --- 小嘴（参考图：小巧，平静/微笑） ---
    dr(d, 62, 42, 4, 2, m)
    dr(d, 63, 43, 2, 2, (255,160,170))

    # --- 腮红（参考图：淡粉，在眼下） ---
    for x in range(46, 52):
        for y in range(34, 40):
            dot(d, x, y, (255, 160, 170, 120))
    for x in range(76, 82):
        for y in range(34, 40):
            dot(d, x, y, (255, 160, 170, 120))

    # ===== 头发（参考图：蓬松长发，波浪，覆盖头部两侧）=====
    # 头顶蓬松
    dr(d, 36, 2, 56, 14, h); dr(d, 40, 0, 48, 6, hl); dr(d, 44, 4, 40, 6, h)
    dr(d, 38, 12, 52, 6, hd)
    # 前额刘海（蓬松，有层次感）
    dr(d, 42, 8, 44, 10, h); dr(d, 46, 6, 36, 6, hl); dr(d, 50, 10, 28, 4, h)
    dr(d, 44, 14, 12, 6, hd); dr(d, 60, 14, 12, 6, hd); dr(d, 74, 14, 8, 6, hd)
    # 左侧长发（波浪状下垂）
    dr(d, 32, 16, 10, 50, h); dr(d, 30, 24, 6, 40, hd); dr(d, 28, 36, 6, 30, h)
    dr(d, 26, 48, 8, 40, h); dr(d, 24, 56, 6, 30, hd); dr(d, 26, 86, 4, 20, h)
    # 右侧长发（波浪状下垂）
    dr(d, 86, 16, 10, 50, h); dr(d, 92, 24, 6, 40, hd); dr(d, 94, 36, 6, 30, h)
    dr(d, 94, 48, 8, 40, h); dr(d, 98, 56, 6, 30, hd); dr(d, 98, 86, 4, 20, h)
    # 发梢卷曲（波浪）
    dr(d, 22, 80, 6, 12, hl); dr(d, 100, 80, 6, 12, hl)
    dr(d, 24, 96, 4, 8, h); dr(d, 100, 96, 4, 8, h)

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


def draw_fishing_scene(palette):
    """
    像素风钓鱼场景背景（参考图风格）
    palette: 色调配置字典
    """
    W, H = 640, 360
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    import random
    random.seed(42)

    sky_top = palette['sky_top']
    sky_mid = palette['sky_mid']
    sky_bot = palette['sky_bot']
    mountain_far = palette['mountain_far']
    mountain_mid = palette['mountain_mid']
    mountain_near = palette['mountain_near']
    forest = palette['forest']
    water_top = palette['water_top']
    water_bot = palette['water_bot']
    wave = palette['wave']
    sun = palette.get('sun', None)
    aurora = palette.get('aurora', None)

    # ===== 天空渐变 =====
    sky_h = 160
    for y in range(sky_h):
        ratio = y / sky_h
        r = int(sky_top[0] + (sky_mid[0] - sky_top[0]) * ratio)
        g = int(sky_top[1] + (sky_mid[1] - sky_top[1]) * ratio)
        b = int(sky_top[2] + (sky_mid[2] - sky_top[2]) * ratio)
        dr(d, 0, y, W, 1, (r, g, b, 255))

    # ===== 太阳/月亮 =====
    if sun:
        sx, sy, sr = sun
        for dy in range(-sr, sr+1):
            for dx in range(-sr, sr+1):
                if dx*dx + dy*dy <= sr*sr:
                    brightness = 1 - (dx*dx + dy*dy) / (sr*sr)
                    c = int(200 + 55 * brightness)
                    dot(d, sx+dx, sy+dy, (c, c, int(c*0.9), 255))

    # ===== 极光 =====
    if aurora:
        for i in range(3):
            ax = 80 + i * 200
            ay = 20 + i * 15
            for dy in range(0, 40):
                for dx in range(0, 160):
                    fade = max(0, 1 - abs(dx - 80) / 80) * max(0, 1 - dy / 40)
                    if fade > 0.3 and random.random() < fade * 0.5:
                        a = int(120 * fade)
                        dot(d, ax+dx, ay+dy, (aurora[0], aurora[1], aurora[2], a))

    # ===== 星星 =====
    if palette.get('stars', False):
        for _ in range(60):
            sx = random.randint(0, W-1)
            sy = random.randint(0, sky_h-40)
            br = random.randint(180, 255)
            dot(d, sx, sy, (br, br, int(br*0.95), 255))
            if random.random() < 0.3:
                dot(d, sx+1, sy, (br, br, int(br*0.95), 180))

    # ===== 远山（多层，空气透视）=====
    # 最远山
    for i in range(8):
        mx = i * 90 - 30
        mh = random.randint(40, 70)
        dr(d, mx, sky_h - mh, 100, mh, mountain_far)
    # 中山
    for i in range(6):
        mx = i * 120 - 40
        mh = random.randint(50, 85)
        dr(d, mx, sky_h - mh, 130, mh, mountain_mid)
    # 近山
    for i in range(5):
        mx = i * 150 - 50
        mh = random.randint(60, 100)
        dr(d, mx, sky_h - mh, 160, mh, mountain_near)

    # ===== 树林剪影 =====
    # 松树群
    for i in range(20):
        tx = random.randint(0, W-20)
        ty = sky_h - random.randint(10, 30)
        th = random.randint(30, 55)
        # 树干
        dr(d, tx+8, ty, 4, th, forest)
        # 树冠三层
        dr(d, tx, ty-10, 20, 15, forest)
        dr(d, tx+2, ty-20, 16, 12, forest)
        dr(d, tx+5, ty-28, 10, 10, forest)

    # ===== 水面 =====
    water_y = sky_h
    water_h = H - water_y
    for y in range(water_h):
        ratio = y / water_h
        r = int(water_top[0] + (water_bot[0] - water_top[0]) * ratio)
        g = int(water_top[1] + (water_bot[1] - water_top[1]) * ratio)
        b = int(water_top[2] + (water_bot[2] - water_top[2]) * ratio)
        dr(d, 0, water_y+y, W, 1, (r, g, b, 255))

    # ===== 水面波纹（参考图风格：白色水平短线）=====
    for _ in range(80):
        wx = random.randint(0, W-40)
        wy = random.randint(water_y+5, H-5)
        wl = random.randint(8, 30)
        alpha = random.randint(40, 100)
        dot(d, wx, wy, (wave[0], wave[1], wave[2], alpha))
        for i in range(1, wl):
            if random.random() < 0.7:
                dot(d, wx+i, wy, (wave[0], wave[1], wave[2], alpha))

    # ===== 岸边岩石（左下角+右下角）=====
    # 左侧岩石群
    for i in range(5):
        rx = random.randint(-20, 80)
        ry = random.randint(water_y-10, water_y+15)
        rw = random.randint(30, 60)
        rh = random.randint(20, 40)
        dr(d, rx, ry, rw, rh, mountain_near)
        dr(d, rx+5, ry+5, rw-10, rh-10, palette.get('rock_light', mountain_mid))
    # 右侧岩石群
    for i in range(5):
        rx = random.randint(W-80, W+20)
        ry = random.randint(water_y-10, water_y+15)
        rw = random.randint(30, 60)
        rh = random.randint(20, 40)
        dr(d, rx, ry, rw, rh, mountain_near)
        dr(d, rx+5, ry+5, rw-10, rh-10, palette.get('rock_light', mountain_mid))

    # ===== 小船剪影（参考图中心元素）=====
    bx, by = W//2 - 30, water_y + 20
    # 船身
    dr(d, bx, by+8, 60, 12, (40, 30, 25, 255))
    dr(d, bx+5, by+6, 50, 4, (50, 40, 35, 255))
    # 船内人物剪影
    dr(d, bx+25, by-8, 8, 14, (30, 25, 20, 255))  # 身体
    dr(d, bx+23, by-14, 12, 8, (30, 25, 20, 255))  # 头
    # 鱼竿
    for i in range(18):
        dot(d, bx+30+i, by-14-int(i*0.4), (25, 20, 15, 255))
    # 鱼线
    for i in range(25):
        dot(d, bx+48, by-6+i, (200, 220, 240, 80))

    # ===== 水面倒影（参考图风格）=====
    # 天空颜色在水面的柔和倒影
    for y in range(water_y, water_y + 40):
        for x in range(0, W, 4):
            if random.random() < 0.15:
                rc = random.randint(0, 30)
                dot(d, x, y, (water_top[0]+rc, water_top[1]+rc, water_top[2]+rc, 60))

    return img


# ========== 衣服预览图（64x96 像素风）==========
def draw_cloth_preview(style, primary, secondary):
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    skin = (255, 220, 200, 255)
    hair = (200, 180, 160, 255)
    p = primary
    s = secondary
    pd = (max(0,p[0]-40), max(0,p[1]-40), max(0,p[2]-40), 255)
    pl = (min(255,p[0]+40), min(255,p[1]+40), min(255,p[2]+40), 255)

    # 通用人体基础
    # 头
    dr(d, 24, 4, 16, 16, skin)
    dr(d, 24, 4, 4, 16, (240,200,180,255))  # 阴影
    # 头发
    dr(d, 22, 2, 20, 8, hair)
    dr(d, 20, 6, 4, 12, hair)
    dr(d, 40, 6, 4, 12, hair)
    # 眼睛
    dr(d, 27, 10, 3, 3, (50,50,50,255))
    dr(d, 34, 10, 3, 3, (50,50,50,255))
    # 嘴
    dr(d, 30, 14, 4, 2, (200,120,120,255))

    # 腿部（通用）
    dr(d, 24, 56, 7, 28, skin)
    dr(d, 33, 56, 7, 28, skin)

    if style == 'underwear':
        # 白色内衣
        dr(d, 22, 20, 20, 12, p)
        dr(d, 22, 20, 20, 3, pl)   # 蕾丝边
        dr(d, 24, 32, 16, 10, p)   # 内裤
        dr(d, 24, 32, 16, 3, pl)
        # 红色心形装饰
        dr(d, 29, 24, 6, 4, s)
        dr(d, 30, 23, 2, 2, s)
        dr(d, 32, 23, 2, 2, s)

    elif style == 'dress':
        # 连衣裙
        dr(d, 22, 20, 20, 14, p)   # 上身
        dr(d, 22, 20, 20, 3, pl)   # 领口
        dr(d, 16, 34, 32, 26, p)   # 裙摆
        dr(d, 16, 34, 32, 3, pl)   # 裙摆边
        dr(d, 16, 56, 32, 4, pl)   # 裙底蕾丝
        dr(d, 30, 28, 4, 4, s)     # 腰带扣
        # 袖子
        dr(d, 18, 22, 4, 10, p)
        dr(d, 42, 22, 4, 10, p)

    elif style == 'pajamas':
        # 轻薄睡衣
        dr(d, 18, 18, 28, 36, p)   # 睡裙主体
        dr(d, 18, 18, 28, 4, pl)   # 领口蕾丝
        dr(d, 18, 50, 28, 4, pl)   # 裙摆蕾丝
        dr(d, 20, 20, 2, 8, s)     # 肩带
        dr(d, 42, 20, 2, 8, s)
        # 波浪裙摆
        dr(d, 16, 52, 8, 4, p)
        dr(d, 28, 54, 8, 4, p)
        dr(d, 40, 52, 8, 4, p)

    elif style == 'gothic':
        # 哥特：黑色连衣裙 + 红色点缀
        dr(d, 20, 18, 24, 16, p)   # 上身
        dr(d, 20, 18, 24, 4, pd)   # 尖领
        dr(d, 20, 22, 24, 2, s)    # 红色领口线
        dr(d, 14, 34, 36, 30, p)   # 裙摆
        dr(d, 14, 34, 36, 4, pd)   # 裙摆阴影
        dr(d, 14, 60, 36, 4, s)    # 红色裙底
        # 红色腰带+十字架
        dr(d, 20, 30, 24, 4, s)
        dr(d, 30, 26, 4, 8, s)
        # 黑色长袜
        dr(d, 24, 56, 7, 18, p)
        dr(d, 33, 56, 7, 18, p)
        dr(d, 24, 74, 16, 4, s)    # 红色袜边

    elif style == 'lolita':
        # 洛丽塔：粉色蓬蓬裙 + 白色蕾丝
        dr(d, 22, 18, 20, 14, pl)  # 白色上衣
        dr(d, 22, 18, 20, 3, s)    # 领口蕾丝
        dr(d, 12, 32, 40, 32, p)   # 粉色蓬蓬裙
        dr(d, 12, 32, 40, 4, s)    # 白色蕾丝边
        dr(d, 12, 60, 40, 4, s)    # 裙底蕾丝
        # 大蝴蝶结
        dr(d, 28, 22, 8, 6, s)
        dr(d, 26, 24, 4, 4, s)
        dr(d, 34, 24, 4, 4, s)
        # 白色长袜
        dr(d, 24, 56, 7, 20, pl)
        dr(d, 33, 56, 7, 20, pl)
        dr(d, 24, 76, 7, 2, s)
        dr(d, 33, 76, 7, 2, s)
        # 粉色鞋子
        dr(d, 24, 84, 7, 4, p)
        dr(d, 33, 84, 7, 4, p)

    elif style == 'maid':
        # 女仆：黑白
        dr(d, 20, 18, 24, 36, p)   # 黑色连衣裙
        dr(d, 22, 20, 20, 18, s)   # 白色围裙
        dr(d, 22, 20, 20, 3, (200,200,200,255))  # 围裙边
        dr(d, 28, 24, 8, 4, s)     # 围裙蝴蝶结
        # 白色头饰
        dr(d, 22, 0, 20, 6, s)
        dr(d, 24, 2, 4, 4, s)
        dr(d, 36, 2, 4, 4, s)
        # 白色袖口
        dr(d, 18, 22, 4, 4, s)
        dr(d, 42, 22, 4, 4, s)
        # 黑色长袜
        dr(d, 24, 56, 7, 18, p)
        dr(d, 33, 56, 7, 18, p)
        # 黑色鞋子
        dr(d, 24, 84, 7, 4, pd)
        dr(d, 33, 84, 7, 4, pd)

    elif style == 'swimsuit':
        # 泳装
        dr(d, 22, 20, 20, 26, p)   # 连体泳装
        dr(d, 22, 20, 20, 3, pl)   # 上边高光
        dr(d, 22, 42, 20, 4, pl)   # 腰边
        dr(d, 24, 20, 2, 8, s)     # 肩带
        dr(d, 38, 20, 2, 8, s)
        # 侧边条纹
        dr(d, 22, 26, 2, 14, s)
        dr(d, 40, 26, 2, 14, s)

    else:  # custom / default
        # 通用紫色渐变连衣裙
        dr(d, 22, 18, 20, 14, p)
        dr(d, 22, 18, 20, 3, pl)
        dr(d, 16, 32, 32, 28, p)
        dr(d, 16, 32, 32, 4, pl)
        dr(d, 16, 56, 32, 4, s)
        dr(d, 30, 26, 4, 4, s)
        # 袖子
        dr(d, 18, 20, 4, 10, p)
        dr(d, 42, 20, 4, 10, p)

    return img


def draw_bg_sea():
    """近海区 - 白天/黄昏，温暖蓝绿色调"""
    return draw_fishing_scene({
        'sky_top': (100, 160, 220),
        'sky_mid': (140, 190, 230),
        'sky_bot': (180, 210, 240),
        'mountain_far': (80, 120, 160),
        'mountain_mid': (60, 100, 140),
        'mountain_near': (40, 70, 100),
        'forest': (30, 55, 40),
        'water_top': (60, 130, 180),
        'water_bot': (30, 70, 110),
        'wave': (200, 230, 255),
        'sun': (520, 40, 25),
        'stars': False,
    })


def draw_bg_sea2():
    """远海区 - 日落，粉紫色调"""
    return draw_fishing_scene({
        'sky_top': (120, 100, 160),
        'sky_mid': (200, 140, 160),
        'sky_bot': (240, 180, 170),
        'mountain_far': (100, 80, 120),
        'mountain_mid': (80, 60, 100),
        'mountain_near': (60, 45, 80),
        'forest': (50, 35, 55),
        'water_top': (140, 100, 130),
        'water_bot': (80, 50, 80),
        'wave': (255, 220, 230),
        'sun': (320, 50, 30),
        'stars': False,
    })


def draw_bg_sea3():
    """深海区 - 夜晚，深蓝星空"""
    return draw_fishing_scene({
        'sky_top': (15, 20, 50),
        'sky_mid': (25, 35, 75),
        'sky_bot': (40, 50, 90),
        'mountain_far': (20, 25, 50),
        'mountain_mid': (15, 20, 40),
        'mountain_near': (10, 15, 30),
        'forest': (8, 12, 25),
        'water_top': (20, 35, 70),
        'water_bot': (10, 15, 35),
        'wave': (180, 210, 255),
        'sun': (520, 35, 20),
        'stars': True,
    })


def draw_bg_sea4():
    """神秘海域 - 极光，紫绿色调"""
    return draw_fishing_scene({
        'sky_top': (20, 25, 55),
        'sky_mid': (40, 35, 80),
        'sky_bot': (60, 50, 90),
        'mountain_far': (25, 30, 55),
        'mountain_mid': (20, 25, 45),
        'mountain_near': (15, 18, 35),
        'forest': (12, 15, 28),
        'water_top': (30, 40, 70),
        'water_bot': (15, 20, 40),
        'wave': (160, 255, 220),
        'sun': (520, 30, 18),
        'stars': True,
        'aurora': (80, 255, 180),
    })


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
    save(draw_bg_sea2(), 'bg_sea2.png')
    save(draw_bg_sea3(), 'bg_sea3.png')
    save(draw_bg_sea4(), 'bg_sea4.png')

    # 衣服预览图
    save(draw_cloth_preview('underwear', (255,240,245), (255,182,193)), 'cloth_underwear.png')
    save(draw_cloth_preview('dress', (103,232,249), (21,94,117)), 'cloth_dress.png')
    save(draw_cloth_preview('pajamas', (251,207,232), (157,23,77)), 'cloth_pajamas.png')
    save(draw_cloth_preview('gothic', (30,30,30), (200,50,50)), 'cloth_gothic.png')
    save(draw_cloth_preview('lolita', (255,180,200), (255,255,255)), 'cloth_lolita.png')
    save(draw_cloth_preview('maid', (40,40,40), (255,255,255)), 'cloth_maid.png')
    save(draw_cloth_preview('swimsuit', (60,130,200), (30,70,140)), 'cloth_swimsuit.png')
    save(draw_cloth_preview('custom', (168,85,247), (236,72,153)), 'cloth_custom.png')

    print("\nAll cute sprites generated!")
