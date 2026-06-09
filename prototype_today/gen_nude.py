from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

gray = np.mean(arr[:,:,:3].astype(int), axis=2)
mask = arr[:,:,3] > 0

# Classify pixels
is_hair = np.zeros((h, w), dtype=bool)
is_skin = np.zeros((h, w), dtype=bool)
is_cloth = np.zeros((h, w), dtype=bool)

for y in range(h):
    for x in range(w):
        if not mask[y, x]:
            continue
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        if y < 25 and bright > 200:
            is_hair[y, x] = True
        elif 130 < bright < 200 and r > 180 and r > b + 10:
            is_skin[y, x] = True
        else:
            is_cloth[y, x] = True

# Connected components on cloth
labeled = np.zeros((h, w), dtype=np.int32)
label = 0
for y in range(h):
    for x in range(w):
        if not is_cloth[y, x] or labeled[y, x] > 0:
            continue
        label += 1
        stack = [(y, x)]
        labeled[y, x] = label
        while stack:
            cy, cx = stack.pop()
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < h and 0 <= nx < w and is_cloth[ny, nx] and labeled[ny, nx] == 0:
                    labeled[ny, nx] = label
                    stack.append((ny, nx))

body_labels = []
for i in range(1, label + 1):
    comp_mask = labeled == i
    size = np.sum(comp_mask)
    coords = np.argwhere(comp_mask)
    cy = np.mean(coords[:, 0])
    cx = np.mean(coords[:, 1])
    if size >= 30 and 15 <= cx <= 50 and cy > 10:
        body_labels.append(i)
        print(f'Body comp {i}: size={size}, center=({cx:.1f},{cy:.1f})')

# Refined skin palette
HL = (255, 220, 205)
LT = (245, 195, 175)
BS = (235, 175, 155)
MD = (220, 155, 135)
SH = (200, 130, 110)
DK = (180, 110, 90)

nude = arr.copy()

# Precompute center x for each y
y_centers = {}
for y in range(h):
    xs = [cx for cx in range(w) if is_cloth[y, cx] and labeled[y, cx] in body_labels]
    if xs:
        y_centers[y] = sum(xs) / len(xs)
    else:
        y_centers[y] = w / 2

def get_skin(y, x):
    cx = y_centers.get(y, w/2)
    dx = x - cx
    
    # Shoulders / upper chest (y ~ 26-35)
    if 26 <= y <= 35:
        if abs(dx) <= 3 and y >= 32:
            return HL
        elif abs(dx) <= 6:
            return LT
        else:
            return HL
    
    # Breasts / upper torso (y ~ 36-42)
    if 36 <= y <= 42:
        if abs(dx) <= 2:
            return DK  # cleavage shadow
        elif abs(dx) <= 5:
            return LT  # breast
        elif abs(dx) <= 8:
            return MD  # breast outer
        else:
            return MD
    
    # Mid torso / waist (y ~ 43-49)
    if 43 <= y <= 49:
        if abs(dx) <= 2 and y in (46, 47):
            return DK  # navel area
        elif abs(dx) <= 4:
            return MD  # waist
        else:
            return SH  # hip shadow
    
    # Lower torso / hips (y ~ 50-55)
    if 50 <= y <= 55:
        if abs(dx) <= 3:
            return LT
        elif abs(dx) <= 6:
            return MD
        else:
            return SH
    
    # Upper legs / thighs (y ~ 56-70)
    if 56 <= y <= 70:
        if abs(dx) <= 2:
            return SH  # inner thigh shadow
        elif abs(dx) <= 5:
            return BS
        else:
            return MD
    
    # Knees (y ~ 71-78)
    if 71 <= y <= 78:
        if y in (74, 75) and abs(dx) <= 4:
            return LT  # knee cap highlight
        elif abs(dx) <= 3:
            return SH
        else:
            return MD
    
    # Lower legs / calves (y ~ 79-86)
    if 79 <= y <= 86:
        if abs(dx) <= 2:
            return SH
        elif abs(dx) <= 5:
            return BS
        else:
            return MD
    
    # Ankles / feet (y ~ 87-95)
    if y >= 87:
        if y >= 91:
            return BS
        else:
            return MD
    
    return BS

for y in range(h):
    for x in range(w):
        if not is_cloth[y, x]:
            continue
        if labeled[y, x] not in body_labels:
            continue
        
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        base = get_skin(y, x)
        
        if bright < 40:
            nude[y, x, :3] = DK
        elif bright < 70:
            nude[y, x, :3] = tuple(max(0, c - 12) for c in base)
        elif bright < 100:
            nude[y, x, :3] = base
        else:
            nude[y, x, :3] = tuple(min(255, c + 12) for c in base)

# Navel: explicit dark pixels
for y in [46, 47]:
    cx = int(y_centers.get(y, w/2))
    for dx in [-1, 0, 1]:
        nx = cx + dx
        if 0 <= nx < w and is_cloth[y, nx] and labeled[y, nx] in body_labels:
            nude[y, nx, :3] = DK

# Toe separation at bottom
for y in [93, 94]:
    xs = [cx for cx in range(w) if is_cloth[y, cx] and labeled[y, cx] in body_labels]
    if len(xs) >= 6:
        for i, x in enumerate(xs):
            if i in [2, 4]:
                nude[y, x, :3] = SH

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v3.png')
print('Saved: sprite_elf_nude_v3.png')
