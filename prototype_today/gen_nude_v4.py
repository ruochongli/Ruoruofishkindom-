from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

# Separate hair/skin/cloth
mask = arr[:,:,3] > 0
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

# Build body outline per y-level from cloth pixels
body_outline = {}  # y -> (left_x, right_x, center_x)
for y in range(h):
    xs = [cx for cx in range(w) if is_cloth[y, cx] and labeled[y, cx] in body_labels]
    if xs:
        body_outline[y] = (min(xs), max(xs), (min(xs) + max(xs)) / 2)

# Skin palette
HL = (255, 220, 205)  # highlight
LT = (248, 200, 180)  # light
BS = (235, 175, 155)  # base
MD = (220, 155, 135)  # mid shadow
SH = (200, 130, 110)  # shadow
DK = (175, 105, 85)   # deep shadow

nude = arr.copy()

# For each y-level, compute the "nude body" width based on anatomy
# The sprite is roughly front-facing with slight angle
for y in range(h):
    if y not in body_outline:
        continue
    left, right, center = body_outline[y]
    orig_width = right - left + 1
    
    # Compute nude body width & offset based on region
    if 36 <= y <= 42:       # breasts: wider than clothes
        nude_width = orig_width + 2
        offset = -1
    elif 43 <= y <= 48:     # waist: narrower than clothes
        nude_width = orig_width - 2
        offset = 1
    elif 49 <= y <= 56:     # hips: wider than waist, same or slightly wider than clothes
        nude_width = orig_width
        offset = 0
    elif 57 <= y <= 70:     # thighs: gradually narrower
        nude_width = orig_width - 1
        offset = 0
    elif 71 <= y <= 78:     # knees: slightly wider (knee caps)
        nude_width = orig_width
        offset = 0
    elif 79 <= y <= 90:     # calves: narrower
        nude_width = orig_width - 1
        offset = 0
    elif y >= 91:           # feet: narrow
        nude_width = orig_width - 1
        offset = 0
    else:                   # shoulders/upper torso
        nude_width = orig_width
        offset = 0
    
    # Keep within reasonable bounds
    nude_width = max(6, min(nude_width, orig_width + 2))
    
    # New body bounds
    new_left = int(center - nude_width / 2) + offset
    new_right = new_left + nude_width - 1
    new_left = max(0, new_left)
    new_right = min(w - 1, new_right)
    
    # Fill the nude body pixels
    for x in range(new_left, new_right + 1):
        dx = x - center
        
        # Determine skin tone by anatomical region
        if 36 <= y <= 42:           # breasts
            if abs(dx) <= 1:
                tone = DK          # cleavage / sternum shadow
            elif abs(dx) <= 3:
                tone = LT          # breast top (light)
            elif abs(dx) <= 5:
                tone = BS          # breast body
            else:
                tone = MD          # breast outer shadow
        elif 43 <= y <= 48:         # waist
            if abs(dx) <= 1 and y == 46:
                tone = DK          # navel
            elif abs(dx) <= 2:
                tone = MD          # waist shadow (indent)
            else:
                tone = BS
        elif 49 <= y <= 56:         # hips / lower belly
            if abs(dx) <= 1:
                tone = LT          # belly center
            elif abs(dx) <= 3:
                tone = BS
            else:
                tone = SH          # hip outer shadow
        elif 57 <= y <= 65:         # upper thigh
            if abs(dx) <= 1:
                tone = SH          # inner thigh shadow
            elif abs(dx) <= 3:
                tone = BS
            else:
                tone = MD          # outer thigh
        elif 66 <= y <= 70:         # mid thigh
            if abs(dx) <= 1:
                tone = SH
            elif abs(dx) <= 3:
                tone = BS
            else:
                tone = MD
        elif 71 <= y <= 75:         # knee cap
            if abs(dx) <= 2:
                tone = HL          # knee highlight
            elif abs(dx) <= 4:
                tone = BS
            else:
                tone = MD
        elif 76 <= y <= 78:         # below knee
            tone = BS
        elif 79 <= y <= 86:         # calf
            if abs(dx) <= 1:
                tone = SH
            else:
                tone = BS
        elif 87 <= y <= 90:         # ankle
            tone = MD
        elif y >= 91:               # foot
            if (x - new_left) % 2 == 0:
                tone = MD          # toe hint
            else:
                tone = BS
        elif 26 <= y <= 35:         # shoulders / upper chest (below neck)
            if abs(dx) <= 3:
                tone = HL
            else:
                tone = LT
        else:
            tone = BS
        
        # Blend with original brightness variation for texture
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        
        if bright < 40:
            final = DK
        elif bright < 70:
            final = tuple(max(0, c - 10) for c in tone)
        elif bright > 120:
            final = tuple(min(255, c + 10) for c in tone)
        else:
            final = tone
        
        nude[y, x, :3] = final
        nude[y, x, 3] = 255
    
    # Clear any original cloth pixels that are now outside the nude body
    for x in range(left, right + 1):
        if x < new_left or x > new_right:
            if is_cloth[y, x] and labeled[y, x] in body_labels:
                nude[y, x, 3] = 0  # make transparent

# Preserve original skin pixels (face, hands, neck)
for y in range(h):
    for x in range(w):
        if is_skin[y, x]:
            nude[y, x, :3] = arr[y, x, :3]
            nude[y, x, 3] = 255

# Preserve hair
for y in range(h):
    for x in range(w):
        if is_hair[y, x]:
            nude[y, x, :3] = arr[y, x, :3]
            nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v4.png')
print('Saved: sprite_elf_nude_v4.png')
