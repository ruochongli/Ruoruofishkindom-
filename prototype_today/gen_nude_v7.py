from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

# Start from blank canvas
nude = np.zeros((h, w, 4), dtype=np.uint8)

# Colors
SKIN = {
    'hl': (255, 228, 212),  # highlight
    'lt': (248, 210, 192),
    'bs': (238, 190, 170),
    'm1': (225, 175, 155),
    'm2': (212, 160, 140),
    'sh': (195, 140, 118),
    'dk': (175, 118, 98),
    'dp': (155, 100, 82),
    'nip': (190, 125, 115),  # nipple
    'aro': (205, 145, 135),  # areola
}

def setp(x, y, col):
    if 0 <= x < w and 0 <= y < h:
        nude[y, x, :3] = col
        nude[y, x, 3] = 255

def line(y, x1, x2, col):
    for x in range(max(0, x1), min(w, x2+1)):
        setp(x, y, col)

def grad(y, x1, x2, cols):
    """Fill line with gradient from cols[0] to cols[1]"""
    n = x2 - x1 + 1
    if n <= 0: return
    c1, c2 = np.array(cols[0]), np.array(cols[1])
    for i, x in enumerate(range(max(0, x1), min(w, x2+1))):
        t = i / max(n-1, 1)
        col = tuple(int(c1[j] + (c2[j]-c1[j])*t) for j in range(3))
        setp(x, y, col)

def oval(cx, cy, rw, rh, col):
    for dy in range(-rh, rh+1):
        for dx in range(-rw, rw+1):
            if (dx/rw)**2 + (dy/rh)**2 <= 1.0:
                setp(cx+dx, cy+dy, col)

# ===== HEAD (keep from original) =====
for y in range(25):
    for x in range(w):
        if arr[y, x, 3] > 0:
            nude[y, x] = arr[y, x]

# ===== NECK =====
line(25, 29, 34, SKIN['dk'])
line(26, 29, 34, SKIN['m2'])
line(27, 28, 35, SKIN['m2'])
line(28, 28, 35, SKIN['m1'])
line(29, 28, 35, SKIN['bs'])
line(30, 28, 35, SKIN['lt'])
line(31, 29, 34, SKIN['hl'])

# ===== SHOULDERS / COLLAR =====
line(32, 22, 24, SKIN['m2'])
line(32, 25, 37, SKIN['lt'])
line(32, 38, 40, SKIN['m2'])
line(33, 21, 23, SKIN['m1'])
line(33, 24, 38, SKIN['bs'])
line(33, 39, 41, SKIN['m1'])

# ===== UPPER CHEST =====
line(34, 20, 22, SKIN['sh'])
line(34, 23, 39, SKIN['lt'])
line(34, 40, 42, SKIN['sh'])

line(35, 21, 23, SKIN['m1'])
line(35, 24, 38, SKIN['bs'])
line(35, 39, 41, SKIN['m1'])

# ===== BREASTS =====
# Row 36: breast top
line(36, 22, 24, SKIN['sh'])
line(36, 25, 28, SKIN['lt'])
line(36, 29, 33, SKIN['dk'])
line(36, 34, 37, SKIN['lt'])
line(36, 38, 41, SKIN['sh'])

# Row 37: nipple row
line(37, 22, 23, SKIN['m1'])
line(37, 24, 25, SKIN['nip'])
line(37, 26, 27, SKIN['aro'])
line(37, 28, 33, SKIN['dk'])
line(37, 34, 35, SKIN['aro'])
line(37, 36, 37, SKIN['nip'])
line(37, 38, 39, SKIN['m1'])

# Row 38: breast bottom
line(38, 23, 24, SKIN['m2'])
line(38, 25, 26, SKIN['aro'])
line(38, 27, 29, SKIN['m1'])
line(38, 30, 31, SKIN['dk'])
line(38, 32, 34, SKIN['m1'])
line(38, 35, 36, SKIN['aro'])
line(38, 37, 38, SKIN['m2'])

# Row 39: underboob
line(39, 24, 25, SKIN['sh'])
line(39, 26, 28, SKIN['m2'])
line(39, 29, 32, SKIN['dk'])
line(39, 33, 35, SKIN['m2'])
line(39, 36, 37, SKIN['sh'])

# Row 40: upper abs
line(40, 25, 27, SKIN['m1'])
line(40, 28, 33, SKIN['sh'])
line(40, 34, 36, SKIN['m1'])

# ===== WAIST (narrowest) =====
line(41, 26, 28, SKIN['bs'])
line(41, 29, 32, SKIN['m2'])
line(41, 33, 35, SKIN['bs'])

line(42, 26, 28, SKIN['lt'])
line(42, 29, 32, SKIN['m1'])
line(42, 33, 35, SKIN['lt'])

line(43, 27, 29, SKIN['bs'])
line(43, 30, 31, SKIN['dp'])  # navel
line(43, 32, 34, SKIN['bs'])

line(44, 26, 28, SKIN['lt'])
line(44, 29, 32, SKIN['m1'])
line(44, 33, 35, SKIN['lt'])

line(45, 26, 28, SKIN['bs'])
line(45, 29, 32, SKIN['m2'])
line(45, 33, 35, SKIN['bs'])

line(46, 25, 28, SKIN['m1'])
line(46, 29, 32, SKIN['sh'])
line(46, 33, 36, SKIN['m1'])

line(47, 25, 28, SKIN['bs'])
line(47, 29, 32, SKIN['m2'])
line(47, 33, 36, SKIN['bs'])

# ===== HIPS =====
line(48, 24, 28, SKIN['lt'])
line(48, 29, 32, SKIN['bs'])
line(48, 33, 37, SKIN['lt'])

line(49, 23, 28, SKIN['bs'])
line(49, 29, 32, SKIN['m1'])
line(49, 33, 38, SKIN['bs'])

line(50, 22, 28, SKIN['m1'])
line(50, 29, 32, SKIN['sh'])
line(50, 33, 39, SKIN['m1'])

line(51, 22, 28, SKIN['bs'])
line(51, 29, 32, SKIN['m2'])
line(51, 33, 39, SKIN['bs'])

line(52, 22, 28, SKIN['m1'])
line(52, 29, 32, SKIN['sh'])
line(52, 33, 39, SKIN['m1'])

# ===== THIGHS (with gap) =====
line(53, 22, 28, SKIN['bs'])
line(53, 29, 32, SKIN['dk'])
line(53, 33, 39, SKIN['bs'])

line(54, 22, 28, SKIN['lt'])
line(54, 29, 32, SKIN['sh'])
line(54, 33, 39, SKIN['lt'])

line(55, 22, 28, SKIN['bs'])
line(55, 29, 32, SKIN['m2'])
line(55, 33, 39, SKIN['bs'])

line(56, 22, 28, SKIN['m1'])
line(56, 29, 32, SKIN['sh'])
line(56, 33, 39, SKIN['m1'])

line(57, 22, 28, SKIN['bs'])
line(57, 29, 32, SKIN['m1'])
line(57, 33, 39, SKIN['bs'])

line(58, 22, 28, SKIN['m2'])
line(58, 29, 32, SKIN['sh'])
line(58, 33, 39, SKIN['m2'])

line(59, 22, 28, SKIN['sh'])
line(59, 29, 32, SKIN['dk'])
line(59, 33, 39, SKIN['sh'])

line(60, 22, 28, SKIN['m1'])
line(60, 29, 32, SKIN['sh'])
line(60, 33, 39, SKIN['m1'])

line(61, 22, 28, SKIN['bs'])
line(61, 29, 32, SKIN['m2'])
line(61, 33, 39, SKIN['bs'])

line(62, 22, 28, SKIN['m1'])
line(62, 29, 32, SKIN['sh'])
line(62, 33, 39, SKIN['m1'])

line(63, 22, 28, SKIN['sh'])
line(63, 29, 32, SKIN['dk'])
line(63, 33, 39, SKIN['sh'])

line(64, 22, 28, SKIN['m2'])
line(64, 29, 32, SKIN['sh'])
line(64, 33, 39, SKIN['m2'])

line(65, 22, 28, SKIN['bs'])
line(65, 29, 32, SKIN['m1'])
line(65, 33, 39, SKIN['bs'])

line(66, 22, 28, SKIN['m1'])
line(66, 29, 32, SKIN['sh'])
line(66, 33, 39, SKIN['m1'])

# ===== KNEES =====
line(67, 22, 28, SKIN['sh'])
line(67, 29, 32, SKIN['hl'])
line(67, 33, 39, SKIN['sh'])

line(68, 22, 28, SKIN['m1'])
line(68, 29, 32, SKIN['lt'])
line(68, 33, 39, SKIN['m1'])

line(69, 22, 28, SKIN['bs'])
line(69, 29, 32, SKIN['m2'])
line(69, 33, 39, SKIN['bs'])

line(70, 22, 28, SKIN['m1'])
line(70, 29, 32, SKIN['sh'])
line(70, 33, 39, SKIN['m1'])

# ===== CALVES =====
line(71, 22, 28, SKIN['bs'])
line(71, 29, 32, SKIN['m2'])
line(71, 33, 39, SKIN['bs'])

line(72, 22, 28, SKIN['m1'])
line(72, 29, 32, SKIN['sh'])
line(72, 33, 39, SKIN['m1'])

line(73, 22, 28, SKIN['bs'])
line(73, 29, 32, SKIN['m2'])
line(73, 33, 39, SKIN['bs'])

line(74, 22, 28, SKIN['sh'])
line(74, 29, 32, SKIN['dk'])
line(74, 33, 39, SKIN['sh'])

line(75, 22, 28, SKIN['m1'])
line(75, 29, 32, SKIN['sh'])
line(75, 33, 39, SKIN['m1'])

line(76, 22, 28, SKIN['bs'])
line(76, 29, 32, SKIN['m2'])
line(76, 33, 39, SKIN['bs'])

line(77, 22, 28, SKIN['m1'])
line(77, 29, 32, SKIN['sh'])
line(77, 33, 39, SKIN['m1'])

line(78, 22, 28, SKIN['sh'])
line(78, 29, 32, SKIN['dk'])
line(78, 33, 39, SKIN['sh'])

line(79, 22, 28, SKIN['m2'])
line(79, 29, 32, SKIN['sh'])
line(79, 33, 39, SKIN['m2'])

line(80, 22, 28, SKIN['bs'])
line(80, 29, 32, SKIN['m1'])
line(80, 33, 39, SKIN['bs'])

line(81, 22, 28, SKIN['m1'])
line(81, 29, 32, SKIN['sh'])
line(81, 33, 39, SKIN['m1'])

line(82, 22, 28, SKIN['sh'])
line(82, 29, 32, SKIN['dk'])
line(82, 33, 39, SKIN['sh'])

line(83, 22, 28, SKIN['m2'])
line(83, 29, 32, SKIN['sh'])
line(83, 33, 39, SKIN['m2'])

line(84, 22, 28, SKIN['bs'])
line(84, 29, 32, SKIN['m1'])
line(84, 33, 39, SKIN['bs'])

line(85, 22, 28, SKIN['m1'])
line(85, 29, 32, SKIN['sh'])
line(85, 33, 39, SKIN['m1'])

# ===== FEET =====
line(86, 22, 28, SKIN['sh'])
line(86, 29, 32, SKIN['dk'])
line(86, 33, 39, SKIN['sh'])

line(87, 22, 28, SKIN['m2'])
line(87, 29, 32, SKIN['sh'])
line(87, 33, 39, SKIN['m2'])

line(88, 22, 28, SKIN['bs'])
line(88, 29, 32, SKIN['m1'])
line(88, 33, 39, SKIN['bs'])

line(89, 22, 28, SKIN['m1'])
line(89, 29, 32, SKIN['sh'])
line(89, 33, 39, SKIN['m1'])

line(90, 22, 28, SKIN['sh'])
line(90, 29, 32, SKIN['dk'])
line(90, 33, 39, SKIN['sh'])

line(91, 22, 28, SKIN['dk'])
line(91, 29, 32, SKIN['sh'])
line(91, 33, 39, SKIN['dk'])

line(92, 22, 28, SKIN['dp'])
line(92, 29, 32, SKIN['dk'])
line(92, 33, 39, SKIN['dp'])

# Ground shadow
line(93, 20, 41, (0,0,0))
line(94, 22, 39, (0,0,0))

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v7.png')
print('Saved v7')
