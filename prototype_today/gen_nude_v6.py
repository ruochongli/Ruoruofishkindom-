from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

# === 1. Layer separation ===
mask = arr[:,:,3] > 0
is_hair = np.zeros((h, w), dtype=bool)
is_skin = np.zeros((h, w), dtype=bool)
is_cloth = np.zeros((h, w), dtype=bool)

for y in range(h):
    for x in range(w):
        if not mask[y, x]: continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        bright = (r+g+b)/3.0
        if y < 25 and bright > 200:
            is_hair[y, x] = True
        elif 130 < bright < 200 and r > 180 and r > b + 10:
            is_skin[y, x] = True
        else:
            is_cloth[y, x] = True

# === 2. Find body cloth component ===
labeled = np.zeros((h, w), dtype=np.int32)
label = 0
for y in range(h):
    for x in range(w):
        if not is_cloth[y, x] or labeled[y, x] > 0: continue
        label += 1
        stack = [(y, x)]
        labeled[y, x] = label
        while stack:
            cy, cx = stack.pop()
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = cy+dy, cx+dx
                if 0<=ny<h and 0<=nx<w and is_cloth[ny,nx] and labeled[ny,nx]==0:
                    labeled[ny,nx] = label
                    stack.append((ny,nx))

body_label = None
max_size = 0
for i in range(1, label+1):
    size = np.sum(labeled==i)
    coords = np.argwhere(labeled==i)
    cy = np.mean(coords[:,0])
    cx = np.mean(coords[:,1])
    if size > max_size and 15 <= cx <= 50 and cy > 10:
        max_size = size
        body_label = i

print(f'Body label: {body_label}, size: {max_size}')

# === 3. Skin palette ===
HL = np.array([255, 228, 212], dtype=np.uint8)
LT = np.array([250, 210, 192], dtype=np.uint8)
BS = np.array([240, 190, 170], dtype=np.uint8)
M1 = np.array([228, 175, 155], dtype=np.uint8)
M2 = np.array([215, 160, 140], dtype=np.uint8)
SH = np.array([200, 140, 120], dtype=np.uint8)
DK = np.array([180, 118, 98],  dtype=np.uint8)
DP = np.array([160, 100, 82],   dtype=np.uint8)

# Nipple/areola - more saturated pinker tones
AR = np.array([210, 150, 138], dtype=np.uint8)  # areola
NP = np.array([195, 130, 120], dtype=np.uint8)  # nipple darker

nude = arr.copy()

# Body outline per y
body_xs = {}
for y in range(h):
    xs = [cx for cx in range(w) if is_cloth[y,cx] and labeled[y,cx]==body_label]
    if xs:
        body_xs[y] = (min(xs), max(xs), sum(xs)/len(xs))

# === 4. Fill body ===
for y in range(h):
    if y not in body_xs: continue
    left, right, center = body_xs[y]
    orig_w = right - left + 1
    
    # Nude width with curves
    if 36 <= y <= 40:       nude_w = orig_w + 1
    elif 41 <= y <= 45:     nude_w = orig_w - 1
    elif 46 <= y <= 50:     nude_w = orig_w - 2
    elif 51 <= y <= 56:     nude_w = orig_w
    elif 57 <= y <= 68:     nude_w = orig_w - 1
    elif 69 <= y <= 76:     nude_w = orig_w - 1
    elif 77 <= y <= 88:     nude_w = orig_w - 1
    else:                   nude_w = orig_w
    
    nude_w = max(6, min(nude_w, orig_w + 1))
    nl = int(center - nude_w/2)
    nr = nl + nude_w - 1
    nl = max(0, nl); nr = min(w-1, nr)
    
    for x in range(nl, nr+1):
        dx = x - center
        dist = abs(dx) / max(nude_w/2, 1)
        
        # Get original brightness
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        bright = (r+g+b)/3.0
        
        is_nipple_area = False
        
        # === ANATOMICAL TONE ===
        if 36 <= y <= 40:           # breasts
            nipple_dx = 3.0
            nipple_dist = min(abs(dx + nipple_dx), abs(dx - nipple_dx))
            if y == 37 and nipple_dist < 0.9:
                tone = NP; is_nipple_area = True
            elif y == 37 and nipple_dist < 2.2:
                tone = AR; is_nipple_area = True
            elif y == 38 and nipple_dist < 0.8:
                tone = NP; is_nipple_area = True
            elif y == 38 and nipple_dist < 2.0:
                tone = AR; is_nipple_area = True
            elif dist < 0.25:
                tone = LT
            elif dist < 0.55:
                tone = BS
            else:
                tone = M1
        elif 41 <= y <= 45:         # underboob / upper belly
            if y == 41 and dist < 0.35:
                tone = DK
            elif y == 43 and dist < 0.3:
                tone = M1
            else:
                tone = M2
        elif 46 <= y <= 49:         # waist / navel
            if y == 47 and dist < 0.3:
                tone = DP  # navel
            elif dist < 0.3:
                tone = M2
            elif dist < 0.6:
                tone = M1
            else:
                tone = SH
        elif 50 <= y <= 53:         # lower belly
            if dist < 0.35:
                tone = BS
            elif dist < 0.65:
                tone = M1
            else:
                tone = M2
        elif 54 <= y <= 58:         # hips
            if dist < 0.3:
                tone = LT
            elif dist < 0.6:
                tone = BS
            else:
                tone = M2
        elif 59 <= y <= 65:         # mid thigh
            if dist < 0.25:
                tone = SH
            elif dist < 0.55:
                tone = BS
            else:
                tone = M1
        elif 66 <= y <= 70:         # lower thigh / knee upper
            if dist < 0.3:
                tone = M1
            elif dist < 0.6:
                tone = BS
            else:
                tone = M2
        elif 71 <= y <= 76:         # knee
            if y in (73, 74) and dist < 0.35:
                tone = HL
            elif dist < 0.4:
                tone = BS
            else:
                tone = M1
        elif 77 <= y <= 82:         # calf
            if dist < 0.3:
                tone = M1
            elif dist < 0.6:
                tone = BS
            else:
                tone = M2
        elif 83 <= y <= 88:         # ankle
            if dist < 0.4:
                tone = M2
            else:
                tone = M1
        elif y >= 89:               # foot
            toe_idx = x - nl
            tone = M2 if toe_idx in [1,3,5] else BS
        elif 26 <= y <= 35:         # shoulders / upper chest
            if dist < 0.4:
                tone = HL
            else:
                tone = LT
        else:
            tone = BS
        
        # === BRIGHTNESS BLEND (skip for nipple/areola) ===
        if is_nipple_area:
            final = tuple(int(tone[i]) for i in range(3))
        elif bright < 35:
            final = tuple(int(DP[i]) for i in range(3))
        elif bright < 60:
            final = tuple(max(0, int(tone[i]) - 12) for i in range(3))
        elif bright > 100:
            final = tuple(min(255, int(tone[i]) + 10) for i in range(3))
        else:
            final = tuple(int(tone[i]) for i in range(3))
        
        nude[y, x, :3] = final
        nude[y, x, 3] = 255
    
    # Clear outside
    for x in range(left, right+1):
        if (x < nl or x > nr) and is_cloth[y,x] and labeled[y,x]==body_label:
            nude[y, x, 3] = 0

# Preserve skin & hair
for y in range(h):
    for x in range(w):
        if is_skin[y, x] or is_hair[y, x]:
            nude[y, x, :3] = arr[y, x, :3]
            nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v6.png')
print('Saved v6')
