from PIL import Image
import numpy as np

img = Image.open('sprite_elf.png').convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

nude = arr.copy()

# === Color classification ===
# Based on detailed per-row analysis of sprite_elf.png
# Skin tones: warm, medium brightness (appears on face, neck, hands)
# Dress: dark grays/blacks (y=27-49)
# Leggings/boots: dark purple-browns (y=56-95)
# Hair: very bright (y<25)

SKIN_TONES = {
    'face_light': (254, 208, 188),
    'face_mid':   (251, 217, 196),
    'face_shadow': (236, 179, 149),
    'neck':       (211, 142, 123),
    'hand':       (254, 208, 188),
}

# Nipple/areola
NIP = (185, 120, 110)
ARO = (200, 140, 130)

for y in range(h):
    for x in range(w):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        bright = (r+g+b)/3.0
        
        # === HEAD (y<25): keep original ===
        if y < 25:
            continue
        
        # === NECK/HAND (y=25-26, 50-55): keep original skin ===
        if y in (25, 26) or (50 <= y <= 55):
            # These are already skin tones in original, keep them
            continue
        
        # === DRESS (y=27-49): replace with skin ===
        if 27 <= y <= 49:
            # Check if this pixel is cloth (dark) or already skin
            # Skin pixels in this region have bright > 140 and warm tone
            is_skin_pixel = (bright > 140 and r > 170 and g > 120 and b > 90 and r > b + 15)
            
            if is_skin_pixel:
                continue  # keep existing skin (rare in dress area)
            
            # Map dress color to skin based on brightness
            center = 32  # approximate body center
            dx = abs(x - center)
            
            # Determine skin tone by position within body
            if y <= 30:       # upper chest / shoulders
                if dx < 3:    tone = SKIN_TONES['face_light']
                elif dx < 6:  tone = SKIN_TONES['face_mid']
                else:         tone = SKIN_TONES['face_shadow']
            elif y <= 35:     # chest area
                if dx < 2:    tone = SKIN_TONES['face_shadow']  # sternum shadow
                elif dx < 5:  tone = SKIN_TONES['face_light']
                else:         tone = SKIN_TONES['face_mid']
            elif y == 36:     # nipple row
                nipple_dist = min(abs(x - 28), abs(x - 36))
                if nipple_dist < 1:   tone = NIP
                elif nipple_dist < 3: tone = ARO
                elif dx < 3:          tone = SKIN_TONES['face_light']
                else:                 tone = SKIN_TONES['face_mid']
            elif y == 37:     # nipple row lower
                nipple_dist = min(abs(x - 28), abs(x - 36))
                if nipple_dist < 1:   tone = NIP
                elif nipple_dist < 2: tone = ARO
                elif dx < 3:          tone = SKIN_TONES['face_mid']
                else:                 tone = SKIN_TONES['face_shadow']
            elif y <= 40:     # underboob
                if dx < 3:    tone = SKIN_TONES['face_shadow']
                else:         tone = SKIN_TONES['face_mid']
            elif y <= 43:     # waist
                if y == 42 and dx < 2:
                    tone = (165, 95, 78)  # navel
                elif dx < 3:  tone = SKIN_TONES['face_shadow']
                else:         tone = SKIN_TONES['face_mid']
            elif y <= 46:     # lower belly
                if dx < 3:    tone = SKIN_TONES['face_light']
                else:         tone = SKIN_TONES['face_mid']
            else:             # hip top
                if dx < 3:    tone = SKIN_TONES['face_light']
                else:         tone = SKIN_TONES['face_shadow']
            
            # Blend with original brightness for texture
            if bright < 30:
                final = (160, 95, 78)
            elif bright < 60:
                final = tuple(max(0, c - 15) for c in tone)
            elif bright > 90:
                final = tuple(min(255, c + 10) for c in tone)
            else:
                final = tone
            
            nude[y, x, :3] = final
        
        # === LEGS (y=56-95): replace socks/boots with skin ===
        elif y >= 56:
            # Check if skin (rare) or cloth
            is_skin_pixel = (bright > 140 and r > 170 and g > 120 and b > 90)
            if is_skin_pixel:
                continue
            
            center = 32
            dx = abs(x - center)
            
            if y <= 62:       # upper thigh
                if dx < 2:    tone = SKIN_TONES['face_shadow']
                elif dx < 5:  tone = SKIN_TONES['face_mid']
                else:         tone = SKIN_TONES['face_shadow']
            elif y <= 68:     # mid thigh
                if dx < 2:    tone = SKIN_TONES['face_shadow']
                elif dx < 5:  tone = SKIN_TONES['face_mid']
                else:         tone = SKIN_TONES['face_shadow']
            elif y <= 74:     # knee area
                if y in (70, 71) and dx < 3:
                    tone = SKIN_TONES['face_light']  # knee cap
                elif dx < 2:  tone = SKIN_TONES['face_shadow']
                else:         tone = SKIN_TONES['face_mid']
            elif y <= 82:     # calf
                if dx < 2:    tone = SKIN_TONES['face_shadow']
                elif dx < 4:  tone = SKIN_TONES['face_mid']
                else:         tone = SKIN_TONES['face_shadow']
            elif y <= 88:     # ankle
                if dx < 2:    tone = SKIN_TONES['face_shadow']
                else:         tone = SKIN_TONES['face_mid']
            else:             # foot
                toe_idx = x - (center - 4)
                if toe_idx in [1, 3, 5]:
                    tone = SKIN_TONES['face_shadow']
                else:
                    tone = SKIN_TONES['face_mid']
            
            # Blend
            if bright < 30:
                final = (155, 90, 75)
            elif bright < 60:
                final = tuple(max(0, c - 12) for c in tone)
            elif bright > 90:
                final = tuple(min(255, c + 8) for c in tone)
            else:
                final = tone
            
            nude[y, x, :3] = final

Image.fromarray(nude, 'RGBA').save('sprite_elf_nude_v8.png')
print('Saved v8')
