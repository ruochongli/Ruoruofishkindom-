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

# === 3. Build nude with anatomical details ===
nude = arr.copy()

# Skin palette (8 tones)
HL = np.array([255, 225, 210], dtype=np.uint8)
LT = np.array([248, 205, 185], dtype=np.uint8)
BS = np.array([236, 182, 162], dtype=np.uint8)
M1 = np.array([225, 168, 148], dtype=np.uint8)
M2 = np.array([212, 152, 132], dtype=np.uint8)
SH = np.array([195, 132, 112], dtype=np.uint8)
DK = np.array([175, 110, 90],  dtype=np.uint8)
DP = np.array([155, 92, 75],   dtype=np.uint8)

# Nipple/areola
AR = np.array([205, 140, 130], dtype=np.uint8)
NP = np.array([185, 120, 110], dtype=np.uint8)

# Body outline per y
body_xs = {}
for y in range(h):
    xs = [cx for cx in range(w) if is_cloth[y,cx] and labeled[y,cx]==body_label]
    if xs:
        body_xs[y] = (min(xs), max(xs), sum(xs)/len(xs))

# === 4. Fill body with anatomical skin ===
for y in range(h):
    if y not in body_xs: continue
    left, right, center = body_xs[y]
    orig_w = right - left + 1
    
    # Nude width
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
    nl = max(0, nl)
    nr = min(w-1, nr)
    
    for x in range(nl, nr+1):
        dx = x - center
        dist_from_center = abs(dx) / max(nude_w/2, 1)
        
        # Determine base tone
        if 36 <= y <= 40:           # breasts
            if y == 36:
                if dist_from_center < 0.2:  tone = M2
                elif dist_from_center < 0.5: tone = LT
                else: tone = M1
            elif y == 37:
                nipple_dx = 3.5
                nipple_dist = min(abs(dx + nipple_dx), abs(dx - nipple_dx))
                if nipple_dist < 0.8:
                    tone = NP
                elif nipple_dist < 2.0:
                    tone = AR
                elif dist_from_center < 0.3:
                    tone = LT
                else:
                    tone = M1
            elif y == 38:
                nipple_dx = 3.5
                nipple_dist = min(abs(dx + nipple_dx), abs(dx - nipple_dx))
                if nipple_dist < 0.8: tone = NP
                elif nipple_dist < 2.0: tone = AR
                elif dist_from_center < 0.4: tone = BS
                else: tone = M2
            elif y == 39:
                if dist_from_center < 0.3: tone = M1
                else: tone = M2
            else:
                tone = M2
        elif 41 <= y <= 45:         # underboob / upper abdomen
            if y == 41:
                if dist_from_center < 0.3: tone = DK
                else: tone = M2
            elif y == 43:
                if dist_from_center < 0.2: tone = BS
                elif dist_from_center < 0.5: tone = M1
                else: tone = M2
            else:
                if dist_from_center < 0.5: tone = BS
                else: tone = M1
        elif 46 <= y <= 48:         # waist / navel
            if y == 46 and dist_from_center < 0.25:
                tone = DP
            elif dist_from_center < 0.3:
                tone = M2
            elif dist_from_center < 0.6:
                tone = M1
            else:
                tone = SH
        elif 49 <= y <= 52:         # lower belly / hip top
            if dist_from_center < 0.4: tone = BS
            elif dist_from_center < 0.7: tone = M1
            else: tone = SH
        elif 53 <= y <= 58:         # hips / upper thigh
            if dist_from_center < 0.3: tone = LT
            elif dist_from_center < 0.6: tone = BS
            else: tone = M2
        elif 59 <= y <= 65:         # mid thigh
            if dist_from_center < 0.25: tone = SH
            elif dist_from_center < 0.55: tone = BS
            else: tone = M1
        elif 66 <= y <= 70:         # lower thigh / knee upper
            if dist_from_center < 0.3: tone = M1
            elif dist_from_center < 0.6: tone = BS
            else: tone = M2
        elif 71 <= y <= 76:         # knee cap
            if y in (73, 74):
                if dist_from_center < 0.35: tone = HL
                else: tone = BS
            else:
                tone = M1
        elif 77 <= y <= 82:         # calf upper
            if dist_from_center < 0.3: tone = M1
            elif dist_from_center < 0.6: tone = BS
            else: tone = M2
        elif 83 <= y <= 88:         # calf lower / ankle
            if dist_from_center < 0.4: tone = M2
            else: tone = M1
        elif y >= 89:               # foot
            toe_idx = x - nl
            if toe_idx in [1, 3, 5]:
                tone = M2
            else:
                tone = BS
        elif 26 <= y <= 35:         # shoulders / upper chest
            if dist_from_center < 0.4: tone = HL
            else: tone = LT
        else:
            tone = BS
        
        # Blend with original brightness
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        bright = (r+g+b)/3.0
        
        if bright < 35:
            final = DK
        elif bright < 60:
            final = tuple(max(0, int(tone[i]) - 15) for i in range(3))
        elif bright > 110:
            final = tuple(min(255, int(tone[i]) + 12) for i in range(3))
        else:
            final = tuple(int(tone[i]) for i in range(3))
        
        nude[y, x, :3] = final
        nude[y, x, 3] = 255
    
    # Clear pixels outside nude body
    for x in range(left, right+1):
        if (x < nl or x > nr) and is_cloth[y,x] and labeled[y,x]==body_label:
            nude[y, x, 3] = 0

# Preserve original skin & hair
for y in range(h):
    for x in range(w):
        if is_skin[y, x] or is_hair[y, x]:
            nude[y, x, :3] = arr[y, x, :3]
            nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v5.png')
print('Saved v5')
