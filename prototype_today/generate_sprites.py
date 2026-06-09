#!/usr/bin/env python3
"""
生成爆衣钓鱼王国 - 像素风格角色精灵图
水银灯(Suigintou) + 克鲁鲁(Krul Tepes) 哥特萝莉风格
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

def draw_pixel_line(draw, x1, y1, x2, y2, color, width=1):
    """Bresenham 画线"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        draw.rectangle([x1, y1, x1+width-1, y1+width-1], fill=color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_rect(draw, x, y, w, h, color):
    draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

def draw_rect_outline(draw, x, y, w, h, color, thickness=1):
    draw.rectangle([x, y, x+w-1, y+h-1], outline=color, width=thickness)

# ========== 调色板 ==========
PALETTE = {
    'skin_light': (255, 230, 220, 255),
    'skin_mid':   (240, 210, 195, 255),
    'skin_shadow':(220, 185, 170, 255),
    'hair_silver':(230, 230, 240, 255),
    'hair_white': (250, 250, 255, 255),
    'hair_shadow':(180, 180, 200, 255),
    'eye_red':    (220, 40, 60, 255),
    'eye_dark':   (160, 20, 40, 255),
    'eye_glow':   (255, 120, 140, 255),
    'dress_black':(35, 30, 45, 255),
    'dress_dark': (50, 45, 65, 255),
    'dress_light':(70, 65, 90, 255),
    'lace_purple':(180, 140, 200, 255),
    'lace_dark':  (120, 90, 140, 255),
    'ribbon_red': (200, 50, 70, 255),
    'gold':       (255, 215, 100, 255),
    'blush':      (255, 150, 160, 120),
    'mouth':      (180, 60, 80, 255),
    'black':      (20, 18, 28, 255),
    'white':      (255, 255, 255, 255),
    'outline':    (40, 35, 50, 255),
    'leg':        (240, 210, 200, 255),
    'leg_dark':   (220, 185, 175, 255),
    'sock_black': (45, 40, 55, 255),
    'sock_lace':  (160, 140, 180, 255),
}

def draw_female_gothic_base(dress_type='full', damaged=False):
    """
    绘制水银灯+克鲁鲁风格哥特萝莉像素角色
    画布: 64x96 像素
    """
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    p = PALETTE

    # 阴影层
    draw_rect(d, 20, 88, 28, 6, (0,0,0,40))

    # ===== 腿部 =====
    # 左腿
    draw_rect(d, 24, 64, 6, 22, p['leg'])
    draw_rect(d, 24, 64, 2, 22, p['leg_dark'])  # 阴影
    # 右腿
    draw_rect(d, 34, 64, 6, 22, p['leg'])
    draw_rect(d, 34, 64, 2, 22, p['leg_dark'])

    # 袜子（过膝袜）
    if dress_type != 'underwear':
        # 左袜
        draw_rect(d, 24, 70, 6, 16, p['sock_black'])
        # 袜口蕾丝
        draw_rect(d, 23, 70, 8, 3, p['sock_lace'])
        draw_rect(d, 24, 71, 1, 1, p['white'])
        draw_rect(d, 26, 71, 1, 1, p['white'])
        draw_rect(d, 28, 71, 1, 1, p['white'])
        # 右袜
        draw_rect(d, 34, 70, 6, 16, p['sock_black'])
        draw_rect(d, 33, 70, 8, 3, p['sock_lace'])
        draw_rect(d, 34, 71, 1, 1, p['white'])
        draw_rect(d, 36, 71, 1, 1, p['white'])
        draw_rect(d, 38, 71, 1, 1, p['white'])

    # ===== 鞋子 =====
    draw_rect(d, 23, 86, 8, 4, p['dress_black'])
    draw_rect(d, 33, 86, 8, 4, p['dress_black'])
    draw_rect(d, 24, 85, 2, 1, p['ribbon_red'])  # 鞋饰
    draw_rect(d, 34, 85, 2, 1, p['ribbon_red'])

    # ===== 身体/连衣裙 =====
    if dress_type == 'full':
        # 裙子主体（哥特式蓬蓬裙）
        # 裙子上部
        draw_rect(d, 22, 42, 20, 24, p['dress_black'])
        # 裙子下部展开
        draw_rect(d, 18, 58, 28, 14, p['dress_black'])
        # 裙摆褶皱
        draw_rect(d, 20, 60, 4, 10, p['dress_dark'])
        draw_rect(d, 30, 60, 4, 10, p['dress_dark'])
        draw_rect(d, 40, 60, 4, 10, p['dress_dark'])
        # 蕾丝花边
        for lx in range(18, 46, 4):
            draw_rect(d, lx, 70, 2, 3, p['lace_purple'])
        # 腰部丝带
        draw_rect(d, 22, 50, 20, 4, p['ribbon_red'])
        draw_rect(d, 30, 48, 4, 8, p['ribbon_red'])  # 蝴蝶结中间
        draw_rect(d, 26, 46, 4, 4, p['ribbon_red'])  # 蝴蝶结左
        draw_rect(d, 34, 46, 4, 4, p['ribbon_red'])  # 蝴蝶结右
        # 胸前装饰
        draw_rect(d, 30, 38, 4, 4, p['gold'])
        # 破损效果
        if damaged:
            # 裙子破洞
            draw_rect(d, 24, 52, 6, 6, p['skin_light'])
            draw_rect(d, 36, 58, 4, 4, p['skin_light'])
            draw_rect(d, 28, 64, 3, 3, p['skin_light'])
            # 破损边缘红线
            draw_rect(d, 23, 51, 2, 2, p['ribbon_red'])
            draw_rect(d, 31, 57, 2, 2, p['ribbon_red'])

    elif dress_type == 'damaged':
        # 严重破损，只剩部分裙子
        draw_rect(d, 22, 42, 20, 12, p['dress_black'])
        draw_rect(d, 18, 52, 10, 8, p['dress_black'])
        draw_rect(d, 36, 54, 10, 6, p['dress_black'])
        # 大量破洞露出皮肤
        draw_rect(d, 24, 44, 16, 14, p['skin_light'])
        draw_rect(d, 26, 54, 12, 10, p['skin_light'])
        # 破损边缘
        draw_rect(d, 22, 42, 3, 3, p['ribbon_red'])
        draw_rect(d, 38, 42, 3, 3, p['ribbon_red'])
        draw_rect(d, 20, 50, 2, 2, p['ribbon_red'])
        draw_rect(d, 40, 52, 2, 2, p['ribbon_red'])
        # 蕾丝残余
        draw_rect(d, 18, 58, 4, 3, p['lace_purple'])
        draw_rect(d, 42, 58, 4, 3, p['lace_purple'])

    elif dress_type == 'underwear':
        # 内衣状态（睡衣/轻薄）
        # 内衣上衣
        draw_rect(d, 24, 36, 16, 12, p['dress_light'])
        draw_rect(d, 24, 36, 16, 4, p['lace_purple'])
        # 内衣下装
        draw_rect(d, 26, 48, 12, 8, p['dress_light'])
        draw_rect(d, 26, 48, 12, 2, p['lace_purple'])
        # 透明感（用半透明像素模拟）
        for ux in range(26, 38, 2):
            for uy in range(40, 54, 2):
                draw_rect(d, ux, uy, 1, 1, (255,255,255,60))

    # ===== 手臂 =====
    # 左臂
    draw_rect(d, 14, 38, 6, 20, p['skin_light'])
    draw_rect(d, 14, 38, 2, 20, p['skin_shadow'])
    # 右臂
    draw_rect(d, 44, 38, 6, 20, p['skin_light'])
    draw_rect(d, 44, 38, 2, 20, p['skin_shadow'])

    # 袖子（泡泡袖）
    if dress_type != 'underwear':
        draw_rect(d, 12, 34, 10, 10, p['dress_black'])
        draw_rect(d, 42, 34, 10, 10, p['dress_black'])
        # 袖口蕾丝
        draw_rect(d, 12, 42, 10, 3, p['lace_purple'])
        draw_rect(d, 42, 42, 10, 3, p['lace_purple'])
    else:
        # 内衣状态露出手臂
        draw_rect(d, 14, 56, 6, 4, p['blush'])  # 轻微脸红在手臂？不，跳过

    # ===== 头部 =====
    # 脖子
    draw_rect(d, 30, 30, 4, 6, p['skin_shadow'])

    # 脸
    draw_rect(d, 22, 8, 20, 24, p['skin_light'])
    draw_rect(d, 22, 8, 20, 4, p['skin_light'])   # 额头
    draw_rect(d, 22, 8, 4, 24, p['skin_shadow'])  # 左脸阴影
    draw_rect(d, 38, 8, 4, 24, p['skin_mid'])     # 右脸亮部

    # 下巴尖（克鲁鲁风格的小尖脸）
    draw_rect(d, 26, 30, 12, 4, p['skin_light'])
    draw_rect(d, 28, 32, 8, 2, p['skin_light'])

    # ===== 眼睛（水银灯/克鲁鲁风格大红眼） =====
    # 左眼
    draw_rect(d, 24, 18, 8, 10, p['eye_red'])
    draw_rect(d, 24, 18, 8, 3, p['eye_dark'])   # 上眼线
    draw_rect(d, 26, 20, 4, 4, p['eye_glow'])   # 高光
    draw_rect(d, 24, 20, 2, 6, p['white'])      # 内侧高光
    # 右眼
    draw_rect(d, 34, 18, 8, 10, p['eye_red'])
    draw_rect(d, 34, 18, 8, 3, p['eye_dark'])
    draw_rect(d, 36, 20, 4, 4, p['eye_glow'])
    draw_rect(d, 34, 20, 2, 6, p['white'])

    # 眉毛（细长，有点高傲）
    draw_pixel_line(d, 24, 14, 30, 15, p['hair_shadow'], 1)
    draw_pixel_line(d, 36, 15, 42, 14, p['hair_shadow'], 1)

    # 嘴（小嘴，克鲁鲁式微笑或水银灯的冷漠）
    draw_rect(d, 30, 26, 4, 1, p['mouth'])
    # 嘴角微微上扬
    draw_rect(d, 29, 25, 1, 1, p['mouth'])
    draw_rect(d, 34, 25, 1, 1, p['mouth'])

    # 腮红（羞耻时会更明显，基础版轻微）
    draw_rect(d, 22, 22, 4, 4, p['blush'])
    draw_rect(d, 40, 22, 4, 4, p['blush'])

    # ===== 头发（水银灯风格银白长发） =====
    # 后发（长发及腰）
    draw_rect(d, 18, 6, 28, 12, p['hair_silver'])
    draw_rect(d, 16, 10, 4, 30, p['hair_silver'])
    draw_rect(d, 44, 10, 4, 30, p['hair_silver'])
    draw_rect(d, 14, 16, 4, 40, p['hair_silver'])
    draw_rect(d, 46, 16, 4, 40, p['hair_silver'])
    draw_rect(d, 12, 24, 4, 50, p['hair_silver'])
    draw_rect(d, 48, 24, 4, 50, p['hair_silver'])
    # 后发阴影
    draw_rect(d, 14, 20, 3, 30, p['hair_shadow'])
    draw_rect(d, 47, 20, 3, 30, p['hair_shadow'])

    # 头顶
    draw_rect(d, 20, 2, 24, 10, p['hair_white'])
    draw_rect(d, 18, 4, 28, 6, p['hair_silver'])

    # 刘海（M字型，哥特萝莉经典刘海）
    draw_rect(d, 22, 6, 20, 8, p['hair_silver'])
    draw_rect(d, 24, 8, 4, 6, p['hair_white'])
    draw_rect(d, 30, 8, 4, 6, p['hair_white'])
    draw_rect(d, 36, 8, 4, 6, p['hair_white'])
    # 刘海阴影
    draw_rect(d, 22, 10, 20, 2, p['hair_shadow'])

    # 呆毛（水银灯标志性翘起）
    draw_rect(d, 38, 0, 3, 4, p['hair_white'])
    draw_rect(d, 39, 0, 2, 2, p['hair_silver'])

    # 两侧鬓角
    draw_rect(d, 20, 12, 4, 16, p['hair_silver'])
    draw_rect(d, 40, 12, 4, 16, p['hair_silver'])
    draw_rect(d, 20, 20, 2, 10, p['hair_shadow'])
    draw_rect(d, 42, 20, 2, 10, p['hair_shadow'])

    # 头饰（克鲁鲁式小皇冠/蝴蝶结）
    # 黑色蝴蝶结
    draw_rect(d, 28, 2, 8, 4, p['dress_black'])
    draw_rect(d, 26, 1, 4, 4, p['dress_black'])
    draw_rect(d, 34, 1, 4, 4, p['dress_black'])
    # 蝴蝶结中心红宝石
    draw_rect(d, 30, 2, 4, 3, p['ribbon_red'])
    # 蕾丝装饰
    draw_rect(d, 27, 0, 2, 2, p['lace_purple'])
    draw_rect(d, 35, 0, 2, 2, p['lace_purple'])

    # ===== 项链 =====
    draw_rect(d, 28, 32, 8, 1, p['gold'])
    draw_rect(d, 31, 33, 2, 2, p['ribbon_red'])

    return img


def draw_male_gothic_base(dress_type='full', damaged=False):
    """
    绘制哥特风格男性角色
    画布: 64x96 像素
    """
    W, H = 64, 96
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    p = PALETTE

    # 阴影
    draw_rect(d, 20, 88, 28, 6, (0,0,0,40))

    # 腿部（长裤）
    if dress_type != 'underwear':
        draw_rect(d, 24, 60, 7, 24, p['dress_black'])
        draw_rect(d, 34, 60, 7, 24, p['dress_black'])
        # 裤线
        draw_rect(d, 26, 62, 1, 20, p['dress_dark'])
        draw_rect(d, 36, 62, 1, 20, p['dress_dark'])
    else:
        # 内衣状态
        draw_rect(d, 24, 60, 7, 24, p['leg'])
        draw_rect(d, 34, 60, 7, 24, p['leg'])
        draw_rect(d, 24, 60, 2, 24, p['leg_dark'])
        draw_rect(d, 34, 60, 2, 24, p['leg_dark'])

    # 鞋子
    draw_rect(d, 23, 86, 9, 4, p['dress_black'])
    draw_rect(d, 33, 86, 9, 4, p['dress_black'])

    # 身体/外套
    if dress_type == 'full':
        # 长外套（哥特式）
        draw_rect(d, 20, 36, 24, 28, p['dress_black'])
        draw_rect(d, 18, 56, 28, 12, p['dress_black'])
        # 外套翻领
        draw_rect(d, 22, 38, 6, 16, p['dress_dark'])
        draw_rect(d, 36, 38, 6, 16, p['dress_dark'])
        # 衬衫（白色）
        draw_rect(d, 28, 36, 8, 14, p['white'])
        # 领结
        draw_rect(d, 30, 40, 4, 4, p['ribbon_red'])
        # 腰带
        draw_rect(d, 22, 54, 20, 3, p['gold'])
        # 纽扣
        draw_rect(d, 31, 44, 2, 2, p['gold'])
        draw_rect(d, 31, 48, 2, 2, p['gold'])
        if damaged:
            draw_rect(d, 26, 46, 5, 5, p['skin_light'])
            draw_rect(d, 34, 52, 4, 4, p['skin_light'])
            draw_rect(d, 25, 45, 2, 2, p['ribbon_red'])

    elif dress_type == 'damaged':
        draw_rect(d, 20, 36, 24, 12, p['dress_black'])
        draw_rect(d, 18, 46, 10, 8, p['dress_black'])
        draw_rect(d, 36, 48, 10, 6, p['dress_black'])
        draw_rect(d, 24, 42, 16, 14, p['skin_light'])
        draw_rect(d, 22, 38, 2, 2, p['ribbon_red'])
        draw_rect(d, 38, 38, 2, 2, p['ribbon_red'])

    elif dress_type == 'underwear':
        draw_rect(d, 24, 36, 16, 10, p['dress_light'])
        draw_rect(d, 26, 48, 12, 8, p['dress_light'])

    # 手臂
    draw_rect(d, 14, 36, 6, 22, p['skin_light'])
    draw_rect(d, 44, 36, 6, 22, p['skin_light'])
    if dress_type != 'underwear':
        draw_rect(d, 14, 36, 6, 8, p['dress_black'])
        draw_rect(d, 44, 36, 6, 8, p['dress_black'])

    # 头部
    draw_rect(d, 30, 30, 4, 6, p['skin_shadow'])
    # 脸（男性更方）
    draw_rect(d, 22, 8, 20, 24, p['skin_light'])
    draw_rect(d, 22, 8, 4, 24, p['skin_shadow'])
    draw_rect(d, 38, 8, 4, 24, p['skin_mid'])
    draw_rect(d, 24, 30, 16, 4, p['skin_light'])

    # 眼睛（男性更锐利）
    draw_rect(d, 25, 18, 7, 5, p['eye_red'])
    draw_rect(d, 25, 18, 7, 2, p['eye_dark'])
    draw_rect(d, 26, 19, 3, 2, p['white'])
    draw_rect(d, 36, 18, 7, 5, p['eye_red'])
    draw_rect(d, 36, 18, 7, 2, p['eye_dark'])
    draw_rect(d, 37, 19, 3, 2, p['white'])

    # 眉毛（更粗更锐利）
    draw_pixel_line(d, 24, 14, 31, 15, p['hair_shadow'], 2)
    draw_pixel_line(d, 35, 15, 42, 14, p['hair_shadow'], 2)

    # 嘴（冷漠/自信）
    draw_rect(d, 30, 26, 4, 1, p['mouth'])

    # 头发（银白短发，有点凌乱）
    draw_rect(d, 20, 2, 24, 10, p['hair_silver'])
    draw_rect(d, 18, 6, 4, 20, p['hair_silver'])
    draw_rect(d, 42, 6, 4, 20, p['hair_silver'])
    draw_rect(d, 16, 10, 4, 16, p['hair_silver'])
    draw_rect(d, 44, 10, 4, 16, p['hair_silver'])
    # 刘海
    draw_rect(d, 22, 6, 20, 6, p['hair_white'])
    draw_rect(d, 24, 8, 4, 4, p['hair_shadow'])
    draw_rect(d, 36, 8, 4, 4, p['hair_shadow'])
    # 呆毛
    draw_rect(d, 38, 0, 3, 3, p['hair_white'])

    return img


def draw_npc_lily():
    """NPC 莉莉 - 粉色系可爱风格"""
    W, H = 48, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    p = PALETTE

    # 基础比例
    draw_rect(d, 20, 50, 20, 10, (0,0,0,30))  # 阴影

    # 腿
    draw_rect(d, 22, 40, 5, 18, p['skin_light'])
    draw_rect(d, 30, 40, 5, 18, p['skin_light'])
    # 袜子
    draw_rect(d, 22, 48, 5, 10, (255,200,220,255))
    draw_rect(d, 30, 48, 5, 10, (255,200,220,255))

    # 裙子（粉色）
    draw_rect(d, 20, 30, 18, 16, (255,180,200,255))
    draw_rect(d, 18, 38, 22, 8, (255,180,200,255))
    draw_rect(d, 20, 32, 18, 2, (255,150,180,255))

    # 上身
    draw_rect(d, 22, 18, 14, 14, (255,220,230,255))
    draw_rect(d, 26, 22, 6, 4, (255,150,180,255))  # 领结

    # 手臂
    draw_rect(d, 16, 20, 5, 14, p['skin_light'])
    draw_rect(d, 37, 20, 5, 14, p['skin_light'])

    # 头
    draw_rect(d, 22, 4, 14, 16, p['skin_light'])
    draw_rect(d, 22, 4, 3, 16, p['skin_shadow'])

    # 眼睛（蓝绿色）
    draw_rect(d, 24, 10, 4, 5, (100,200,180,255))
    draw_rect(d, 30, 10, 4, 5, (100,200,180,255))
    draw_rect(d, 25, 11, 2, 2, p['white'])
    draw_rect(d, 31, 11, 2, 2, p['white'])

    # 嘴
    draw_rect(d, 27, 16, 4, 1, p['mouth'])

    # 头发（粉色双马尾）
    draw_rect(d, 20, 2, 18, 8, (255,160,180,255))
    draw_rect(d, 14, 6, 6, 20, (255,160,180,255))
    draw_rect(d, 38, 6, 6, 20, (255,160,180,255))
    draw_rect(d, 12, 12, 4, 16, (255,140,160,255))
    draw_rect(d, 42, 12, 4, 16, (255,140,160,255))
    # 刘海
    draw_rect(d, 22, 4, 14, 4, (255,180,200,255))

    # 蝴蝶结
    draw_rect(d, 16, 4, 4, 4, (255,100,140,255))
    draw_rect(d, 38, 4, 4, 4, (255,100,140,255))

    return img


def draw_npc_hein():
    """NPC 海恩 - 冷酷帅哥风格"""
    W, H = 48, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)
    p = PALETTE

    draw_rect(d, 20, 50, 20, 10, (0,0,0,30))

    # 腿
    draw_rect(d, 22, 40, 5, 18, p['dress_black'])
    draw_rect(d, 30, 40, 5, 18, p['dress_black'])

    # 上身（深色外套）
    draw_rect(d, 20, 24, 18, 20, (60,60,80,255))
    draw_rect(d, 26, 26, 6, 8, p['white'])
    draw_rect(d, 28, 28, 2, 2, p['gold'])

    # 手臂
    draw_rect(d, 16, 24, 5, 16, (60,60,80,255))
    draw_rect(d, 37, 24, 5, 16, (60,60,80,255))

    # 头
    draw_rect(d, 22, 4, 14, 16, p['skin_light'])
    draw_rect(d, 22, 4, 3, 16, p['skin_shadow'])

    # 眼睛（深蓝）
    draw_rect(d, 24, 10, 4, 5, (80,120,200,255))
    draw_rect(d, 30, 10, 4, 5, (80,120,200,255))
    draw_rect(d, 25, 11, 2, 2, p['white'])
    draw_rect(d, 31, 11, 2, 2, p['white'])

    # 嘴
    draw_rect(d, 27, 16, 4, 1, p['mouth'])

    # 头发（深蓝/黑色短发）
    draw_rect(d, 20, 2, 18, 8, (40,50,80,255))
    draw_rect(d, 18, 6, 5, 14, (40,50,80,255))
    draw_rect(d, 35, 6, 5, 14, (40,50,80,255))
    draw_rect(d, 22, 4, 14, 4, (60,70,100,255))

    return img


def draw_boss():
    """绘制一个像素风格的海兽BOSS"""
    W, H = 80, 64
    img = create_image(W, H)
    d = ImageDraw.Draw(img)

    # 深海怪物 - 章鱼/乌贼风格
    colors = {
        'body': (80, 40, 120, 255),
        'body_light': (120, 60, 160, 255),
        'eye': (255, 80, 80, 255),
        'eye_glow': (255, 200, 200, 255),
        'tentacle': (100, 50, 140, 255),
    }

    # 身体
    draw_rect(d, 20, 10, 40, 30, colors['body'])
    draw_rect(d, 25, 12, 30, 20, colors['body_light'])

    # 大眼睛
    draw_rect(d, 30, 16, 20, 14, colors['eye'])
    draw_rect(d, 34, 19, 6, 6, colors['eye_glow'])
    draw_rect(d, 32, 18, 3, 3, (255,255,255,255))

    # 触手
    for i, tx in enumerate([10, 18, 26, 50, 58, 66]):
        draw_rect(d, tx, 38, 6, 20 - i*2, colors['tentacle'])
        draw_rect(d, tx+1, 56, 4, 4, colors['body'])

    # 斑点
    draw_rect(d, 22, 14, 4, 4, colors['body_light'])
    draw_rect(d, 52, 20, 4, 4, colors['body_light'])
    draw_rect(d, 28, 32, 3, 3, colors['body_light'])
    # 眼睛高光
    draw_rect(d, 32, 18, 3, 3, (255,255,255,255))

    return img


def draw_bg_cabin():
    """船舱背景 - 像素风格"""
    W, H = 340, 400
    img = create_image(W, H, (25, 20, 35, 255))
    d = ImageDraw.Draw(img)

    # 木地板
    for y in range(320, H, 8):
        draw_rect(d, 0, y, W, 4, (60, 45, 35, 255))
        draw_rect(d, 0, y+4, W, 4, (50, 38, 30, 255))

    # 墙壁
    draw_rect(d, 0, 0, W, 320, (35, 30, 50, 255))
    # 墙壁纹理
    for x in range(0, W, 20):
        draw_rect(d, x, 0, 1, 320, (40, 35, 55, 255))

    # 窗户（圆形，哥特式）
    draw_rect(d, 120, 40, 100, 120, (20, 18, 30, 255))
    draw_rect(d, 125, 45, 90, 110, (15, 25, 50, 255))
    # 窗框
    draw_rect(d, 165, 45, 4, 110, (60, 55, 45, 255))
    draw_rect(d, 125, 95, 90, 4, (60, 55, 45, 255))
    # 星星
    draw_rect(d, 140, 60, 2, 2, (255, 255, 220, 255))
    draw_rect(d, 180, 75, 2, 2, (255, 255, 220, 255))
    draw_rect(d, 155, 110, 2, 2, (255, 255, 220, 255))

    # 床
    draw_rect(d, 20, 240, 80, 60, (50, 40, 60, 255))
    draw_rect(d, 20, 240, 80, 15, (70, 55, 75, 255))
    draw_rect(d, 25, 255, 70, 40, (80, 60, 90, 255))
    draw_rect(d, 25, 255, 70, 8, (100, 80, 110, 255))

    # 衣橱
    draw_rect(d, 240, 180, 80, 120, (55, 45, 35, 255))
    draw_rect(d, 242, 182, 36, 116, (65, 55, 45, 255))
    draw_rect(d, 282, 182, 36, 116, (65, 55, 45, 255))
    draw_rect(d, 278, 182, 4, 116, (45, 38, 30, 255))

    # 地毯
    draw_rect(d, 100, 300, 140, 20, (80, 40, 60, 255))
    draw_rect(d, 105, 302, 130, 16, (70, 35, 50, 255))

    return img


def draw_bg_city():
    """城市背景"""
    W, H = 640, 480
    img = create_image(W, H, (80, 120, 160, 255))
    d = ImageDraw.Draw(img)

    # 天空渐变（手动）
    for y in range(0, 200):
        c = int(80 + y * 0.4)
        draw_rect(d, 0, y, W, 1, (c, c+40, c+80, 255))

    # 地面
    draw_rect(d, 0, 300, W, 180, (60, 80, 60, 255))
    # 石板路
    for x in range(0, W, 40):
        for y in range(300, H, 20):
            draw_rect(d, x, y, 38, 18, (70, 90, 70, 255))

    # 建筑（哥特式）
    for bx in [50, 200, 380, 520]:
        bw = 100
        bh = 180
        by = 300 - bh
        draw_rect(d, bx, by, bw, bh, (50, 50, 70, 255))
        draw_rect(d, bx+5, by+10, bw-10, bh-20, (60, 60, 80, 255))
        # 尖顶
        draw_rect(d, bx+40, by-40, 20, 40, (50, 50, 70, 255))
        draw_rect(d, bx+45, by-50, 10, 10, (50, 50, 70, 255))
        # 窗户
        for wy in range(by+20, by+bh-20, 30):
            draw_rect(d, bx+20, wy, 20, 20, (30, 30, 50, 255))
            draw_rect(d, bx+60, wy, 20, 20, (30, 30, 50, 255))

    return img


def draw_bg_sea():
    """海域背景"""
    W, H = 640, 480
    img = create_image(W, H, (10, 20, 50, 255))
    d = ImageDraw.Draw(img)

    # 深海渐变
    for y in range(0, H):
        c = int(10 + y * 0.15)
        draw_rect(d, 0, y, W, 1, (c//2, c, c+20, 255))

    # 气泡
    import random
    random.seed(42)
    for _ in range(30):
        bx = random.randint(0, W-4)
        by = random.randint(50, H-10)
        draw_rect(d, bx, by, 3, 3, (200, 230, 255, 100))

    # 海底岩石
    for rx in [0, 100, 250, 400, 550]:
        rh = random.randint(30, 60)
        draw_rect(d, rx, H-rh, 80, rh, (20, 25, 40, 255))
        draw_rect(d, rx+10, H-rh+10, 60, rh-20, (30, 35, 50, 255))

    return img


# ========== 主程序 ==========
if __name__ == '__main__':
    print("Generating pixel art sprites...")

    # 女性角色
    save(draw_female_gothic_base('full', False), 'sprite_f.png')
    save(draw_female_gothic_base('full', True), 'sprite_f_damaged.png')
    save(draw_female_gothic_base('damaged', False), 'sprite_f_broken.png')
    save(draw_female_gothic_base('underwear', False), 'sprite_f_underwear.png')

    # 男性角色
    save(draw_male_gothic_base('full', False), 'sprite_m.png')
    save(draw_male_gothic_base('full', True), 'sprite_m_damaged.png')
    save(draw_male_gothic_base('underwear', False), 'sprite_m_underwear.png')

    # NPC
    save(draw_npc_lily(), 'sprite_lily.png')
    save(draw_npc_hein(), 'sprite_hein.png')

    # BOSS
    save(draw_boss(), 'sprite_boss.png')

    # 背景
    save(draw_bg_cabin(), 'bg_cabin.png')
    save(draw_bg_city(), 'bg_city.png')
    save(draw_bg_sea(), 'bg_sea.png')

    print("\nAll sprites generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
