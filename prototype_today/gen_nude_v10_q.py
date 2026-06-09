from PIL import Image
import numpy as np

img = Image.open('sprite_f_q.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

nude = arr.copy()

# === SKIN PALETTE (v9 refined) ===
SKIN = {
    'hl': (255, 228, 212),
    'lt': (251, 217, 196),
    'bs': (254, 208, 188),
    'm1': (236, 179, 149),
    'sh': (211, 142, 123),
    'dk': (175, 110, 90),
    'dp': (155, 92, 75),
}

NIP = (180, 115, 105)
ARO = (200, 140, 130)

CENTER = 32

def is_skin_pixel(r, g, b, bright):
    """Detect exposed skin (face, neck, hands)."""
    return (bright > 140 and r > 170 and g > 120 and b > 90 and r > b + 10)

for y in range(h):
    for x in range(w):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        
        # HEAD: keep
        if y < 25:
            continue
        
        # NECK: keep, add collarbone
        if y in (25, 26):
            dx = abs(x - CENTER)
            if y == 25 and dx == 4:
                nude[y, x, :3] = SKIN['hl']
            continue
        
        # HANDS (exposed skin in original): keep
        if is_skin_pixel(r, g, b, bright):
            continue
        
        dx = abs(x - CENTER)
        
        # === TORSO (y=27-55) ===
        if 27 <= y <= 55:
            if 36 <= y <= 39:       # breasts
                nipple_dist = min(abs(x - 28), abs(x - 36))
                if nipple_dist == 0:
                    tone = NIP
                elif nipple_dist <= 2:
                    tone = ARO
                elif dx < 3:
                    tone = SKIN['hl']
                elif dx < 5:
                    tone = SKIN['lt']
                else:
                    tone = SKIN['bs']
            elif 40 <= y <= 42:     # underboob
                tone = SKIN['sh'] if dx < 3 else SKIN['m1']
            elif y == 43:           # waist + navel
                tone = SKIN['dp'] if dx == 0 else (SKIN['sh'] if dx < 3 else SKIN['m1'])
            elif 44 <= y <= 46:     # lower waist
                tone = SKIN['m1'] if dx < 3 else SKIN['bs']
            elif 47 <= y <= 50:     # hips
                if dx < 3:
                    tone = SKIN['lt']
                elif dx < 6:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['m1']
            elif 51 <= y <= 53:     # upper thigh / hip bottom
                if dx < 3:
                    tone = SKIN['bs']
                elif dx < 6:
                    tone = SKIN['m1']
                else:
                    tone = SKIN['sh']
            elif y in (54, 55):     # lower thigh / hand area
                tone = SKIN['sh'] if dx < 3 else SKIN['bs']
            elif 27 <= y <= 30:     # upper chest
                if dx < 3:
                    tone = SKIN['hl']
                elif dx < 6:
                    tone = SKIN['lt']
                else:
                    tone = SKIN['m1']
                if y in (27, 28) and dx == 5:
                    tone = SKIN['hl']
            elif 31 <= y <= 35:     # mid chest
                if dx < 3:
                    tone = SKIN['lt']
                elif dx < 6:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['m1']
            else:
                tone = SKIN['bs']
            
            # Brightness blend
            if bright < 30:
                final = SKIN['dp']
            elif bright < 55:
                final = tuple(max(0, c - 12) for c in tone)
            elif bright > 90:
                final = tuple(min(255, c + 8) for c in tone)
            else:
                final = tone
            
            nude[y, x, :3] = final
            nude[y, x, 3] = 255
        
        # === LEGS (y=56-95): no cropping, just recolor ===
        elif y >= 56:
            if 56 <= y <= 62:       # upper thigh
                if dx < 3:
                    tone = SKIN['sh']
                elif dx < 6:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['m1']
            elif 63 <= y <= 68:     # mid thigh
                if dx < 3:
                    tone = SKIN['sh']
                elif dx < 6:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['m1']
            elif 69 <= y <= 73:     # knee
                if y in (70, 71) and dx < 3:
                    tone = SKIN['hl']
                elif dx < 3:
                    tone = SKIN['sh']
                else:
                    tone = SKIN['bs']
            elif 74 <= y <= 80:     # calf
                if dx < 3:
                    tone = SKIN['sh']
                elif dx < 5:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['m1']
            elif 81 <= y <= 85:     # ankle
                if dx < 3:
                    tone = SKIN['m1']
                elif dx < 5:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['sh']
            else:                   # foot
                # Use actual pixel position relative to leg cluster
                tone = SKIN['sh'] if dx < 2 else SKIN['bs']
            
            if bright < 30:
                final = SKIN['dp']
            elif bright < 55:
                final = tuple(max(0, c - 10) for c in tone)
            elif bright > 90:
                final = tuple(min(255, c + 6) for c in tone)
            else:
                final = tone
            
            nude[y, x, :3] = final
            nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_f_q_stage5_v10.png')
print('Saved v10')
