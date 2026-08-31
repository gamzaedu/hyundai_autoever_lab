# -*- coding: utf-8 -*-
"""
Clawd 원본 에셋 -> 가이드북용 경량 에셋 변환

  assets/clawd/emotes/*.gif  ->  guide/assets/img/*.gif   (크롭 + 축소 + 팔레트화)
  assets/clawd/poses/*.png   ->  guide/assets/img/*.png   (합성용 회색 발판 제거 + 크롭)

주의 — Pillow 의 ImageSequence.Iterator 는 GIF 의 disposal 처리를 이미 끝낸
프레임을 돌려준다. 여기에 직접 alpha_composite 로 이전 프레임을 또 겹치면
날아가는 입자(음표·색종이)가 지워지지 않고 누적되어 번진다. 절대 하지 말 것.
"""
import os, sys
from collections import deque
from PIL import Image, ImageSequence

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC  = os.path.join(ROOT, 'assets', 'clawd')
DST  = os.path.join(ROOT, 'guide', 'assets', 'img')

EMOTES   = ['photo', 'coding', 'reading', 'painting', 'listening', 'exercise', 'birthday']
GIF_SIZE = 140
OCCUPANCY = 0.40      # 이 비율 이상의 프레임에 존재하는 픽셀 = 캐릭터 본체
PAD       = 0.14      # 본체 bbox 여백


def frames_of(path):
    """프레임을 RGBA 로 그대로 읽는다 (누적 합성 금지)"""
    im = Image.open(path)
    out, dur = [], []
    for fr in ImageSequence.Iterator(im):
        out.append(fr.convert('RGBA'))
        dur.append(fr.info.get('duration', 60))
    return out, dur, im.size


def body_box(frames, size):
    """
    전 프레임 합집합 bbox 를 쓰면 멀리 날아가는 입자까지 포함되어
    캐릭터가 지나치게 작아진다. 대부분의 프레임에 존재하는 픽셀만으로 bbox 를 잡는다.
    """
    w, h = size
    need = max(1, int(len(frames) * OCCUPANCY))
    count = [0] * (w * h)
    for f in frames:
        a = f.split()[3].load()
        for y in range(h):
            base = y * w
            for x in range(w):
                if a[x, y] > 24:
                    count[base + x] += 1
    L, T, R, B = w, h, 0, 0
    for y in range(h):
        base = y * w
        for x in range(w):
            if count[base + x] >= need:
                if x < L: L = x
                if x > R: R = x
                if y < T: T = y
                if y > B: B = y
    if R <= L or B <= T:                       # 안전망 : 합집합 bbox 로 대체
        L, T, R, B = w, h, 0, 0
        for f in frames:
            b = f.getbbox()
            if b:
                L, T, R, B = min(L, b[0]), min(T, b[1]), max(R, b[2]), max(B, b[3])
    side = max(R - L, B - T)
    pad  = int(side * PAD) + 2
    side += pad * 2
    cx, cy = (L + R) // 2, (T + B) // 2
    L = max(0, min(w - side, cx - side // 2))
    T = max(0, min(h - side, cy - side // 2))
    return (L, T, L + side, T + side)


def to_palette(img):
    """알파를 인덱스 63 투명색으로 옮긴 팔레트 이미지"""
    alpha = img.split()[3]
    q = img.convert('RGB').quantize(colors=63, method=Image.MEDIANCUT)
    q.paste(63, alpha.point(lambda v: 255 if v < 128 else 0).convert('1'))
    pal = q.getpalette()
    pal[63 * 3:63 * 3 + 3] = [0, 0, 0]
    q.putpalette(pal)
    return q


def build_gif(name, every=1):
    src = os.path.join(SRC, 'emotes', f'clawd-{name}.gif')
    frames, durs, size = frames_of(src)
    box = body_box(frames, size)
    out, od = [], []
    for i, (f, d) in enumerate(zip(frames, durs)):
        if i % every:
            continue
        out.append(to_palette(f.crop(box).resize((GIF_SIZE, GIF_SIZE), Image.NEAREST)))
        od.append(d * every)
    dst = os.path.join(DST, f'clawd-{name}.gif')
    out[0].save(dst, save_all=True, append_images=out[1:], duration=od, loop=0,
                disposal=2, transparency=63, optimize=True)
    return box, len(out), os.path.getsize(dst)


def strip_stage(im):
    """회색/흰색이면서 이미지 테두리와 이어진 덩어리 = 사진 합성용 발판 -> 제거"""
    w, h = im.size
    px = im.load()

    def achro(x, y):
        r, g, b, a = px[x, y]
        return a <= 10 or max(r, g, b) - min(r, g, b) <= 30

    seen = [[False] * h for _ in range(w)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if achro(x, y) and not seen[x][y]:
                seen[x][y] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if achro(x, y) and not seen[x][y]:
                seen[x][y] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[nx][ny] and achro(nx, ny):
                seen[nx][ny] = True; q.append((nx, ny))
    for x in range(w):
        for y in range(h):
            if seen[x][y]:
                px[x, y] = (0, 0, 0, 0)
    return im


def build_poses():
    import glob
    n = 0
    for p in sorted(glob.glob(os.path.join(SRC, 'poses', '*.png'))):
        im = strip_stage(Image.open(p).convert('RGBA'))
        bb = im.getbbox()
        if not bb:
            continue
        im = im.crop(bb)
        w, h = im.size
        s = 220 / max(w, h)
        if s < 1:
            im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.NEAREST)
        im.save(os.path.join(DST, os.path.basename(p)), optimize=True)
        n += 1
    return n


if __name__ == '__main__':
    every = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    os.makedirs(DST, exist_ok=True)
    total = 0
    for nm in EMOTES:
        box, nf, sz = build_gif(nm, every)
        total += sz
        print(f'  {nm:10s} box={box} {nf:3d}f {sz // 1024:3d}KB')
    print(f'  GIF 합계 {total // 1024}KB')
    print(f'  포즈 PNG {build_poses()}개')
