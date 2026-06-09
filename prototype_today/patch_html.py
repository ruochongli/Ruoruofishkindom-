#!/usr/bin/env python3
"""Patch index.html to use pixel art sprites and beautify UI"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ========== 1. Add pixel-art CSS ==========
css_addition = '''
  /* Pixel art rendering */
  .pixel-img { image-rendering: pixelated; image-rendering: crisp-edges; }
  .char-canvas {
    background: url('bg_cabin.png') center/cover no-repeat !important;
    image-rendering: pixelated;
  }
  .creation-preview {
    background: url('bg_cabin.png') center/cover no-repeat !important;
    image-rendering: pixelated;
  }
  .creation-title {
    font-size: 26px;
    text-align: center;
    margin-bottom: 20px;
    color: #fff;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    letter-spacing: 2px;
  }
  .panel-box {
    background: rgba(20, 15, 35, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }
  .cabin-slot {
    background: rgba(30, 25, 45, 0.7) !important;
    border: 2px dashed rgba(168, 85, 247, 0.2) !important;
  }
  .cabin-slot:hover {
    border-color: rgba(168, 85, 247, 0.5) !important;
    background: rgba(50, 40, 70, 0.5) !important;
  }
  .sea-card {
    background: rgba(20, 25, 50, 0.8) !important;
    border: 2px solid rgba(80, 120, 200, 0.2) !important;
  }
  .shop-item {
    background: rgba(25, 20, 40, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
  }
  .cloth-card {
    background: rgba(25, 20, 40, 0.8) !important;
    border: 2px solid transparent !important;
  }
  .cloth-card.selected {
    border-color: #f5576c !important;
    background: rgba(245, 87, 108, 0.15) !important;
    box-shadow: 0 0 12px rgba(245, 87, 108, 0.2);
  }
  .btn-primary {
    background: linear-gradient(135deg, #a855f7, #ec4899) !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
  }
  .btn-game:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  }
  .hp-bar-fill {
    background: linear-gradient(90deg, #ef4444, #f87171, #fca5a5) !important;
  }
  .shame-bar-fill {
    background: linear-gradient(90deg, #4ade80, #facc15, #f87171, #a855f7) !important;
  }
  .dur-bar-fill { border-radius: 4px; }
'''

html = html.replace('</style>', css_addition + '\n</style>')

# ========== 2. Add sprite preloading ==========
preload_js = '''
// ===== Sprite Preloading =====
const SPRITES = {};
function loadSprite(name, src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => { SPRITES[name] = img; resolve(); };
    img.onerror = () => { console.warn('Failed to load sprite:', src); resolve(); };
    img.src = src;
  });
}
let spritesReady = false;
async function preloadSprites() {
  await Promise.all([
    loadSprite('f', 'sprite_f.png'),
    loadSprite('f_damaged', 'sprite_f_damaged.png'),
    loadSprite('f_broken', 'sprite_f_broken.png'),
    loadSprite('f_underwear', 'sprite_f_underwear.png'),
    loadSprite('m', 'sprite_m.png'),
    loadSprite('m_damaged', 'sprite_m_damaged.png'),
    loadSprite('m_underwear', 'sprite_m_underwear.png'),
    loadSprite('lily', 'sprite_lily.png'),
    loadSprite('hein', 'sprite_hein.png'),
    loadSprite('boss', 'sprite_boss.png'),
  ]);
  spritesReady = true;
  console.log('All sprites loaded');
}
preloadSprites();
'''

# Insert before "// ========================"
html = html.replace('// ========================\n// 数据', preload_js + '\n// ========================\n// 数据')

# ========== 3. Replace drawCharacterOnContext ==========
new_draw_func = '''function drawCharacterOnContext(c, w, h, t, isPreview) {
  if (!spritesReady) {
    // Fallback: draw loading text
    c.fillStyle = '#fff';
    c.font = '14px sans-serif';
    c.textAlign = 'center';
    c.fillText('Loading sprites...', w/2, h/2);
    return;
  }

  // Determine sprite based on gender and damage state
  const gender = charData.gender === 'female' ? 'f' : 'm';
  let spriteKey = gender;

  if (!isPreview && player.dur) {
    const cloth = CLOTHES[selectedCloth];
    const maxTotal = cloth.maxDur.top + cloth.maxDur.bottom + cloth.maxDur.legs;
    const curTotal = player.dur.top + player.dur.bottom + player.dur.legs;
    const brokenRatio = 1 - (curTotal / maxTotal);
    if (brokenRatio > 0.6) {
      spriteKey = gender + '_underwear';
    } else if (brokenRatio > 0.3) {
      spriteKey = gender + '_broken';
    } else if (brokenRatio > 0.1) {
      spriteKey = gender + '_damaged';
    }
  }

  const sprite = SPRITES[spriteKey] || SPRITES[gender];
  if (!sprite) return;

  // Breath animation (bob up and down)
  const breathY = Math.sin(t * 2) * 4;
  const scale = Math.min(w / 64, h / 96) * 0.75;
  const bw = 64 * scale;
  const bh = 96 * scale;
  const bx = (w - bw) / 2;
  const by = (h - bh) / 2 + breathY + 20;

  c.imageSmoothingEnabled = false;
  c.drawImage(sprite, bx, by, bw, bh);

  // Blink overlay (simulate blinking with semi-transparent rect over eyes)
  const blink = Math.sin(t * 3) > 0.95;
  if (blink) {
    c.fillStyle = 'rgba(255,230,220,0.7)';
    const eyeW = bw * 0.18;
    const eyeH = bh * 0.06;
    const eyeY = by + bh * 0.19;
    c.fillRect(bx + bw * 0.32, eyeY, eyeW, eyeH);
    c.fillRect(bx + bw * 0.52, eyeY, eyeW, eyeH);
  }

  // Blush overlay based on shame
  if (!isPreview && player.shame > 20) {
    const blushAlpha = Math.min(player.shame / 100, 0.5);
    c.fillStyle = `rgba(255, 100, 120, ${blushAlpha})`;
    const blushR = bw * 0.12;
    c.beginPath();
    c.ellipse(bx + bw * 0.22, by + bh * 0.28, blushR, blushR * 0.7, 0, 0, Math.PI * 2);
    c.fill();
    c.beginPath();
    c.ellipse(bx + bw * 0.78, by + bh * 0.28, blushR, blushR * 0.7, 0, 0, Math.PI * 2);
    c.fill();
  }

  // Damage indicator lines
  if (!isPreview) {
    const cloth = CLOTHES[selectedCloth];
    const maxTotal = cloth.maxDur.top + cloth.maxDur.bottom + cloth.maxDur.legs;
    const curTotal = player.dur.top + player.dur.bottom + player.dur.legs;
    const brokenRatio = 1 - (curTotal / maxTotal);
    if (brokenRatio > 0.2) {
      c.strokeStyle = '#ef4444';
      c.lineWidth = 2;
      c.setLineDash([5, 5]);
      c.beginPath();
      c.moveTo(bx + bw * 0.2, by + bh * 0.55);
      c.lineTo(bx + bw * 0.5, by + bh * 0.65);
      c.stroke();
      c.setLineDash([]);
    }
  }
}'''

# Find and replace the old drawCharacterOnContext function
pattern = r'function drawCharacterOnContext\(c, w, h, t, isPreview\) \{[\s\S]*?^\}'
html = re.sub(pattern, new_draw_func, html, flags=re.MULTILINE, count=1)

# ========== 4. Add background images to game screens ==========
# Sea background
html = html.replace(
    '<div id="seaScreen" class="hidden">',
    '<div id="seaScreen" class="hidden" style="background: url(\'bg_sea.png\') center/cover no-repeat; border-radius: 16px; padding: 16px;">'
)

# City background  
html = html.replace(
    '<div id="cityScreen" class="hidden">',
    '<div id="cityScreen" class="hidden" style="background: url(\'bg_city.png\') center/cover no-repeat; border-radius: 16px; padding: 16px;">'
)

# ========== 5. Update crew avatar to use pixel sprites ==========
# Replace emoji avatar with sprite image in crew panel
html = html.replace(
    '<div class="crew-avatar">💕</div>',
    '<img id="crewAvatar" class="crew-avatar pixel-img" src="sprite_lily.png" style="width:48px;height:64px;image-rendering:pixelated;">'
)

# ========== 6. Add sprite to NPC interactions ==========
# In the battle/NPC sections where NPCs are referenced, we can add small sprites
# This is a simple enhancement - replace the 💕 emoji in battle logs with nothing
# (logs are text-based, so we keep them as is for now)

# ========== 7. Update title style ==========
html = html.replace(
    '<h1>🎣 爆衣钓鱼王国</h1>',
    '<h1 style="text-shadow: 0 0 20px rgba(168,85,247,0.5), 0 2px 4px rgba(0,0,0,0.3); font-size: 32px;">🎣 爆衣钓鱼王国</h1>'
)

# ========== 8. Update shop item emoji size and style ==========
# Make shop items look more like game inventory
html = html.replace(
    '.shop-item-emoji { font-size: 28px; margin-bottom: 4px; }',
    '.shop-item-emoji { font-size: 28px; margin-bottom: 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); }'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML patched successfully!")
