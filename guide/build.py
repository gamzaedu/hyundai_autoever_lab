# -*- coding: utf-8 -*-
"""
단일 HTML 실습가이드 빌더
  template.html + assets/ -> dist/*.html (외부 참조 0개, 완전 오프라인)

치환 규칙
  {{IMG:파일명}}   -> data:image/...;base64,...        (CSS url() 안에서 1회만 쓸 때)
  {{FONT:파일명}}  -> data:font/woff2;base64,...        (문서에 실제 쓰인 글자만 서브셋)
  {{IMGCSS}}      -> .i-<슬러그>{background-image:...; aspect-ratio:W/H} 규칙 묶음

같은 이미지를 여러 곳에서 쓰는 경우 <img src> 를 쓰면 base64 가 그 횟수만큼 중복된다.
-> 마크업에서는 class="bg i-<슬러그>" 로 참조하고, 실제 데이터는 {{IMGCSS}} 에 1회만 넣는다.
"""
import base64, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(HERE, 'template.html')
IMG  = os.path.join(HERE, 'assets', 'img')
FONT = os.path.join(HERE, 'assets', 'font')
DIST = os.path.join(HERE, 'dist')

MIME = {'.png': 'image/png', '.gif': 'image/gif', '.svg': 'image/svg+xml'}

# 서브셋에 항상 포함할 글자 (JS가 동적으로 생성하는 문자열 등)
EXTRA_CHARS = (
    '0123456789'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    r'''.,:;!?%/\-–—+=*&#@()[]{}<>"'`~^|_$'''
    '완료복사됨실패진행중잠김해금레벨점수총점등급획득남은개'
    '전설의클로드트레이너목줄을자유롭게다루는고수충분히잘했어요우와아직태초마을이야'
)


def slug(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def collect_chars(html: str) -> str:
    """템플릿에서 화면에 실제 노출되는 글자 수집 (태그·주석 제거 후 전체)"""
    t = re.sub(r'<script[\s\S]*?</script>', ' ', html)
    t = re.sub(r'<style[\s\S]*?</style>', ' ', t)
    t = re.sub(r'<!--[\s\S]*?-->', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    # 스크립트가 만드는 문자열도 놓치지 않도록 원본 전체를 추가로 포함
    return ''.join(sorted(set(t + html + EXTRA_CHARS)))


def subset_font(path: str, text: str) -> bytes:
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont
    opts = Options()
    opts.flavor = 'woff2'
    opts.desubroutinize = True
    opts.layout_features = ['*']
    opts.drop_tables += ['DSIG']
    opts.notdef_outline = True
    f = TTFont(path, fontNumber=0)
    ss = Subsetter(options=opts)
    ss.populate(text=text)
    ss.subset(f)
    buf = io.BytesIO()
    f.flavor = 'woff2'
    f.save(buf)
    return buf.getvalue()


def main():
    with open(TPL, encoding='utf-8') as fp:
        html = fp.read()

    chars = collect_chars(html)
    report = []
    # 클래스 스캔은 base64 주입 전(원본 템플릿)에 해둔다
    used = set(re.findall(r'\bi-([a-z0-9-]+)\b', html))

    # --- 폰트 ---
    def font_sub(m):
        name = m.group(1)
        src = os.path.join(FONT, name)
        data = subset_font(src, chars)
        report.append(('FONT', name, os.path.getsize(src), len(data)))
        return 'data:font/woff2;base64,' + base64.b64encode(data).decode()

    html = re.sub(r'\{\{FONT:([^}]+)\}\}', font_sub, html)

    # --- 이미지 CSS 클래스 (중복 제거) ---
    #     마크업의 class="bg i-<슬러그>" 를 스캔해 실제로 쓰인 것만 규칙 생성
    rules, seen = [], set()
    for fn in sorted(os.listdir(IMG)):
        s = slug(fn)
        if s not in used or s in seen:
            continue
        seen.add(s)
        path = os.path.join(IMG, fn)
        with open(path, 'rb') as fp:
            data = fp.read()
        mime = MIME[os.path.splitext(fn)[1].lower()]
        b64 = base64.b64encode(data).decode()
        ratio = ''
        if not fn.lower().endswith('.svg'):
            from PIL import Image as _I
            with _I.open(path) as _im:
                ratio = f'aspect-ratio:{_im.size[0]}/{_im.size[1]};'
        rules.append(f'.i-{s}{{{ratio}background-image:url("data:{mime};base64,{b64}")}}')
        report.append(('IMGCSS', fn, len(data), len(data)))
    missing = used - seen
    if missing:
        print('!! assets/img 에 없는 이미지 클래스:', sorted(missing), file=sys.stderr)
        sys.exit(1)
    if html.count('{{IMGCSS}}') != 1:
        print(f'!! {{{{IMGCSS}}}} placeholder 가 {html.count("{{IMGCSS}}")}개 — 정확히 1개여야 함', file=sys.stderr)
        sys.exit(1)
    html = html.replace('{{IMGCSS}}', '\n'.join(rules))

    # --- 이미지 (CSS url() 직접 삽입용) ---
    def img_sub(m):
        name = m.group(1)
        src = os.path.join(IMG, name)
        with open(src, 'rb') as fp:
            data = fp.read()
        report.append(('IMG', name, len(data), len(data)))
        mime = MIME[os.path.splitext(name)[1].lower()]
        return f'data:{mime};base64,' + base64.b64encode(data).decode()

    html = re.sub(r'\{\{IMG:([^}]+)\}\}', img_sub, html)

    # --- 검증: 외부 참조가 남아있으면 실패 ---
    leaks = re.findall(r'(?:src|href)\s*=\s*["\'](https?:|//)', html)
    if leaks:
        print('!! 외부 참조 발견:', leaks, file=sys.stderr)
        sys.exit(1)
    if '{{' in html:
        print('!! 미치환 placeholder:', re.findall(r'\{\{[^}]+\}\}', html)[:5], file=sys.stderr)
        sys.exit(1)

    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, 'claude-levelup-guide.html')
    with open(out, 'w', encoding='utf-8') as fp:
        fp.write(html)

    print(f'수집 글자수 : {len(chars)}')
    for kind, name, a, b in report:
        print(f'  {kind:5s} {name:26s} {a//1024:5d}KB -> {b//1024:5d}KB')
    print(f'\n생성 : {out}  ({os.path.getsize(out)/1024/1024:.2f} MB)')


if __name__ == '__main__':
    main()
