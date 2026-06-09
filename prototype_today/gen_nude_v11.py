from PIL import Image
import numpy as np

img = Image.open('sprite_f.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

nude = arr.copy()

SKIN = {
    'hl': (255, 228, 212), 'lt': (251, 217, 196), 'bs': (254, 208, 188),
    'm1': (236, 179, 149), 'sh': (211, 142, 123), 'dk': (175, 110, 90), 'dp': (155, 92, 75),
}
NIP = (180, 115, 105)
ARO = (200, 140, 130)
CENTER = 32

def body_width(y):
    """Body+arms width at each row. Dress frills beyond this are cropped."""
    widths = {
        27: 28, 28: 28, 29: 28, 30: 28,
        31: 26, 32: 26, 33: 26, 34: 26, 35: 26,
        36: 24, 37: 24, 38: 24,
        39: 24, 40: 24, 41: 24, 42: 24,
        43: 22, 44: 22, 45: 22, 46: 22,
        47: 24, 48: 24, 49: 26, 50: 28,
        51: 28, 52: 28, 53: 30, 54: 30, 55: 30,
        56: 26, 57: 24,
    }
    return widths.get(y, None)  # None = no crop (legs)

def is_exposed_skin(r, g, b, bright):
    return (bright > 140 and r > 170 and g > 120 and b > 90 and r > b + 10)

for y in range(h):
    for x in range(w):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
        bright = (r + g + b) / 3.0
        
        # HEAD
        if y < 25:
            continue
        
        # NECK
        if y in (25, 26):
            dx = abs(x - CENTER)
            if y == 25 and dx == 4:
                nude[y, x, :3] = SKIN['hl']
            continue
        
        # Exposed skin (face, neck, hands) - keep regardless of body width
        if is_exposed_skin(r, g, b, bright):
            continue
        
        dx = abs(x - CENTER)
        bw = body_width(y)
        
        # === UPPER BODY (y=27-57): crop to body width ===
        if bw is not None:
            nl = CENTER - bw // 2
            nr = nl + bw
            if not (nl <= x < nr):
                nude[y, x, 3] = 0
                continue
            
            # Skin tone mapping (v9 refined)
            if 36 <= y <= 39:
                nipple_dist = min(abs(x - 28), abs(x - 36))
                if nipple_dist == 0: tone = NIP
                elif nipple_dist <= 2: tone = ARO
                elif dx < 3: tone = SKIN['hl']
                elif dx < 5: tone = SKIN['lt']
                else: tone = SKIN['bs']
            elif 40 <= y <= 42:
                tone = SKIN['sh'] if dx < 3 else SKIN['m1']
            elif y == 43:
                tone = SKIN['dp'] if dx == 0 else (SKIN['sh'] if dx < 3 else SKIN['m1'])
            elif 44 <= y <= 46:
                tone = SKIN['m1'] if dx < 3 else SKIN['bs']
            elif 47 <= y <= 50:
                if dx < 3: tone = SKIN['lt']
                elif dx < 6: tone = SKIN['bs']
                else: tone = SKIN['m1']
            elif 51 <= y <= 53:
                if dx < 3: tone = SKIN['bs']
                elif dx < 6: tone = SKIN['m1']
                else: tone = SKIN['sh']
            elif y in (54, 55):
                tone = SKIN['sh'] if dx < 3 else SKIN['bs']
            elif 27 <= y <= 30:
                if dx < 3: tone = SKIN['hl']
                elif dx < 6: tone = SKIN['lt']
                else: tone = SKIN['m1']
                if y in (27, 28) and dx == 5: tone = SKIN['hl']
            elif 31 <= y <= 35:
                if dx < 3: tone = SKIN['lt']
                elif dx < 6: tone = SKIN['bs']
                else: tone = SKIN['m1']
            else:
                tone = SKIN['bs']
            
            if bright < 30: final = SKIN['dp']
            elif bright < 55: final = tuple(max(0, c - 12) for c in tone)
            elif bright > 90: final = tuple(min(255, c + 8) for c in tone)
            else: final = tone
            
            nude[y, x, :3] = final
            nude[y, x, 3] = 255
        
        # === LEGS (y=58+): no crop, preserve original silhouette ===
        else:
            if 58 <= y <= 62:
                if dx < 3: tone = SKIN['sh']
                elif dx < 6: tone = SKIN['bs']
                else: tone = SKIN['m1']
            elif 63 <= y <= 68:
                if dx < 3: tone = SKIN['sh']
                elif dx < 6: tone = SKIN['bs']
                else: tone = SKIN['m1']
            elif 69 <= y <= 73:
                if y in (70, 71) and dx < 3: tone = SKIN['hl']
                elif dx < 3: tone = SKIN['sh']
                else: tone = SKIN['bs']
            elif 74 <= y <= 80:
                if dx < 3: tone = SKIN['sh']
                elif dx < 5: tone = SKIN['bs']
                else: tone = SKIN['m1']
            elif 81 <= y <= 85:
                if dx < 3: tone = SKIN['m1']
                elif dx < 5: tone = SKIN['bs']
                else: tone = SKIN['sh']
            else:
                tone = SKIN['sh'] if dx < 2 else SKIN['bs']
            
            if bright < 30: final = SKIN['dp']
            elif bright < 55: final = tuple(max(0, c - 10) for c in tone)
            elif bright > 90: final = tuple(min(255, c + 6) for c in tone)
            else: final = tone
            
            nude[y, x, :3] = final
            nude[y, x, 3] = 255

Image.fromarray(nude, 'RGBA').save('sprite_f_stage5_v11.png')
print('Saved v11')
