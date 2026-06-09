from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

nude = arr.copy()

# Original skin tones from the sprite (extracted from exposed skin areas)
SKIN = {
    'hl': (255, 228, 212),   # highlight
    'lt': (251, 217, 196),   # light (face/neck)
    'bs': (254, 208, 188),   # base (hands)
    'm1': (236, 179, 149),   # mid
    'sh': (211, 142, 123),   # shadow
    'dk': (175, 110, 90),    # deep shadow
    'dp': (155, 92, 75),     # darkest
}

# Enhanced nipple/areola
NIP = (180, 115, 105)
ARO = (200, 140, 130)

# Body center (from original sprite analysis)
CENTER = 32

def body_width(y):
    """Return approximate body width at each y-level based on original sprite."""
    # Measured from sprite_elf.png analysis
    widths = {
        25: 12, 26: 12,
        27: 18, 28: 18, 29: 20, 30: 20, 31: 20, 32: 20, 33: 18,
        34: 16, 35: 14, 36: 14, 37: 14, 38: 16, 39: 16, 40: 16,
        41: 16, 42: 16, 43: 16, 44: 16, 45: 16, 46: 18, 47: 18,
        48: 20, 49: 20, 50: 20, 51: 20, 52: 20, 53: 20, 54: 20, 55: 20,
        56: 18, 57: 18, 58: 18, 59: 18, 60: 18, 61: 18, 62: 18,
        63: 18, 64: 18, 65: 18, 66: 18, 67: 18, 68: 18,
        69: 18, 70: 18, 71: 18, 72: 18, 73: 18, 74: 18, 75: 18,
        76: 18, 77: 18, 78: 18, 79: 18, 80: 18, 81: 18, 82: 18,
        83: 18, 84: 18, 85: 18, 86: 18, 87: 18, 88: 18,
        89: 18, 90: 18, 91: 18, 92: 18, 93: 18, 94: 18, 95: 16,
    }
    return widths.get(y, 18)

for y in range(h):
    for x in range(w):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        bright = (r+g+b)/3.0
        
        # HEAD: keep original
        if y < 25:
            continue
        
        # NECK: keep original skin, enhance shading
        if y in (25, 26):
            # Already skin in original, but add collarbone hint at y=25
            dx = abs(x - CENTER)
            if y == 25 and dx == 4:
                nude[y, x, :3] = SKIN['hl']  # collarbone highlight
            continue
        
        # Check if pixel is already exposed skin (hands, rare skin patches)
        is_exposed_skin = (bright > 140 and r > 170 and g > 120 and b > 90 and r > b + 10)
        if is_exposed_skin:
            continue
        
        # === DRESS / TORSO (y=27-55) ===
        if 27 <= y <= 55:
            bw = body_width(y)
            dx = abs(x - CENTER)
            
            # Apply nude body shape: slightly narrower waist, subtle breast
            if 36 <= y <= 42:       # breast area
                if dx <= 3:
                    bw = bw + 1   # breasts slightly wider than dress
            elif 43 <= y <= 48:     # waist
                if dx <= 3:
                    bw = bw - 1   # waist slightly narrower
            
            nl = CENTER - bw // 2
            nr = nl + bw
            if not (nl <= x < nr):
                nude[y, x, 3] = 0  # make transparent
                continue
            
            # Determine skin tone by anatomical position
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
                if dx < 3:
                    tone = SKIN['sh']
                else:
                    tone = SKIN['m1']
            elif y == 43:           # waist + navel
                if dx == 0:
                    tone = SKIN['dp']  # navel
                elif dx < 3:
                    tone = SKIN['sh']
                else:
                    tone = SKIN['m1']
            elif 44 <= y <= 46:     # lower waist
                if dx < 3:
                    tone = SKIN['m1']
                else:
                    tone = SKIN['bs']
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
                if dx < 3:
                    tone = SKIN['sh']
                else:
                    tone = SKIN['bs']
            elif 27 <= y <= 30:     # upper chest / shoulders
                if dx < 3:
                    tone = SKIN['hl']
                elif dx < 6:
                    tone = SKIN['lt']
                else:
                    tone = SKIN['m1']
                # Collarbone hint at y=27-28
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
            
            # Blend with original brightness for texture
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
        
        # === LEGS (y=56-95) ===
        elif y >= 56:
            bw = body_width(y)
            dx = abs(x - CENTER)
            
            # Leg gap in upper thigh
            if 56 <= y <= 65:
                if dx < 2:
                    bw = bw - 2  # gap between thighs
            
            nl = CENTER - bw // 2
            nr = nl + bw
            if not (nl <= x < nr):
                nude[y, x, 3] = 0
                continue
            
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
            elif 69 <= y <= 73:     # knee cap
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
            elif 81 <= y <= 85:     # lower calf / ankle
                if dx < 3:
                    tone = SKIN['m1']
                elif dx < 5:
                    tone = SKIN['bs']
                else:
                    tone = SKIN['sh']
            else:                   # foot
                toe_idx = x - nl
                if toe_idx in [1, 3, 5]:
                    tone = SKIN['sh']
                else:
                    tone = SKIN['bs']
            
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

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v9.png')
print('Saved v9')
