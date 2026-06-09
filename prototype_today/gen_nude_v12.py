from PIL import Image
import numpy as np

img = Image.open('sprite_f.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

nude = np.zeros((h, w, 4), dtype=np.uint8)

# Copy head
nude[:25, :, :] = arr[:25, :, :]

SKIN = {
    'hl': (255, 228, 212), 'lt': (251, 217, 196), 'bs': (254, 208, 188),
    'm1': (236, 179, 149), 'sh': (211, 142, 123), 'dk': (175, 110, 90), 'dp': (155, 92, 75),
}
NIP = (180, 115, 105)
ARO = (200, 140, 130)
CENTER = 32

# Neck: keep original, enhance collarbone
for y in (25, 26):
    for x in range(w):
        if arr[y, x, 3] > 0:
            nude[y, x, :] = arr[y, x, :]
            if y == 25 and abs(x - CENTER) == 4:
                nude[y, x, :3] = SKIN['hl']

# === ANATOMICALLY CORRECT TORSO (y=27-57) ===
# Drawn from scratch. Shape: shoulders wide -> breasts -> waist narrow -> hips wide -> thighs
# Includes arms hanging at sides.
TORSO = {
    27: (20, 44),   # shoulders
    28: (19, 45),
    29: (18, 46),   # shoulders widest
    30: (18, 46),
    31: (19, 45),   # upper chest
    32: (20, 44),
    33: (20, 44),
    34: (19, 45),   # breast upper
    35: (18, 46),   # breast
    36: (18, 46),   # breast fullest
    37: (19, 45),
    38: (20, 44),   # breast lower
    39: (20, 44),   # underbust
    40: (21, 43),
    41: (22, 42),   # waist
    42: (22, 42),
    43: (21, 43),
    44: (21, 43),
    45: (22, 42),   # waist narrowest
    46: (21, 43),   # hips upper
    47: (20, 44),
    48: (19, 45),
    49: (18, 46),   # hips widest
    50: (19, 45),
    51: (20, 44),   # upper thigh / crotch
    52: (21, 43),
    53: (22, 42),
    54: (23, 41),
    55: (24, 40),   # transition to legs
    56: (24, 40),
    57: (24, 40),
}

for y, (left, right) in TORSO.items():
    for x in range(left, right):
        dx = abs(x - CENTER)
        
        # Skin tone by anatomical region
        if 36 <= y <= 39:       # breasts
            nipple_dist = min(abs(x - 28), abs(x - 36))
            if nipple_dist == 0: tone = NIP
            elif nipple_dist <= 2: tone = ARO
            elif dx < 3: tone = SKIN['hl']
            elif dx < 5: tone = SKIN['lt']
            else: tone = SKIN['bs']
        elif 40 <= y <= 42:     # underboob
            tone = SKIN['sh'] if dx < 3 else SKIN['m1']
        elif y == 43:           # waist + navel
            tone = SKIN['dp'] if dx == 0 else (SKIN['sh'] if dx < 3 else SKIN['m1'])
        elif 44 <= y <= 46:     # lower waist / hip upper
            tone = SKIN['m1'] if dx < 3 else SKIN['bs']
        elif 47 <= y <= 50:     # hips
            if dx < 3: tone = SKIN['lt']
            elif dx < 6: tone = SKIN['bs']
            else: tone = SKIN['m1']
        elif 51 <= y <= 53:     # upper thigh / groin
            if dx < 3: tone = SKIN['bs']
            elif dx < 6: tone = SKIN['m1']
            else: tone = SKIN['sh']
        elif y in (54, 55):     # lower thigh transition
            tone = SKIN['sh'] if dx < 3 else SKIN['bs']
        elif 27 <= y <= 30:     # shoulders / upper chest
            if dx < 3: tone = SKIN['hl']
            elif dx < 6: tone = SKIN['lt']
            else: tone = SKIN['m1']
            if y in (27, 28) and dx == 5: tone = SKIN['hl']
        elif 31 <= y <= 35:     # mid chest
            if dx < 3: tone = SKIN['lt']
            elif dx < 6: tone = SKIN['bs']
            else: tone = SKIN['m1']
        else:
            tone = SKIN['bs']
        
        nude[y, x, :3] = tone
        nude[y, x, 3] = 255

# === LEGS (y=58-95): preserve original silhouette, recolor ===
for y in range(58, h):
    for x in range(w):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        dx = abs(x - CENTER)
        
        # Exposed skin on legs (keep original - e.g. if any skin shows through stockings)
        if bright > 140 and r > 170 and g > 120 and b > 90 and r > b + 10:
            nude[y, x, :] = arr[y, x, :]
            continue
        
        if 58 <= y <= 62:       # upper thigh
            if dx < 3: tone = SKIN['sh']
            elif dx < 6: tone = SKIN['bs']
            else: tone = SKIN['m1']
        elif 63 <= y <= 68:     # mid thigh
            if dx < 3: tone = SKIN['sh']
            elif dx < 6: tone = SKIN['bs']
            else: tone = SKIN['m1']
        elif 69 <= y <= 73:     # knee
            if y in (70, 71) and dx < 3: tone = SKIN['hl']
            elif dx < 3: tone = SKIN['sh']
            else: tone = SKIN['bs']
        elif 74 <= y <= 80:     # calf
            if dx < 3: tone = SKIN['sh']
            elif dx < 5: tone = SKIN['bs']
            else: tone = SKIN['m1']
        elif 81 <= y <= 85:     # ankle
            if dx < 3: tone = SKIN['m1']
            elif dx < 5: tone = SKIN['bs']
            else: tone = SKIN['sh']
        else:                   # foot
            toe_idx = x - 24  # approximate left foot start
            if toe_idx in [1, 3, 5]:
                tone = SKIN['sh']
            else:
                tone = SKIN['bs']
        
        if bright < 30: final = SKIN['dp']
        elif bright < 55: final = tuple(max(0, c - 10) for c in tone)
        elif bright > 90: final = tuple(min(255, c + 6) for c in tone)
        else: final = tone
        
        nude[y, x, :3] = final
        nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_f_stage5_v12.png')
print('Saved v12')
