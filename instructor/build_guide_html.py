# -*- coding: utf-8 -*-
"""
강사 운영 가이드 단일 HTML 빌더
  instructor/GUIDE_*.md  ->  instructor/dist/instructor-guide.html   (standalone · 배포용)
                        ->  instructor/dist/artifact.html            (Artifact 게시용 fragment)

의존성 없음. python build_guide_html.py
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, 'dist')

SOURCES = [
    ('g0', 'GUIDE_0_overview.md', '개요', '전체 운영'),
    ('g1', 'GUIDE_1.md', '1', 'OT · 초기 설정'),
    ('g2', 'GUIDE_2.md', '2', '모델 · 핵심 명령어'),
    ('g3', 'GUIDE_3.md', '3', 'CLAUDE.md'),
    ('g4', 'GUIDE_4.md', '4', 'Skills'),
    ('g5', 'GUIDE_5.md', '5', 'SubAgents'),
    ('g6', 'GUIDE_6.md', '6', 'Hooks'),
    ('g7', 'GUIDE_7.md', '7', '캡스톤'),
]

TIMES = {
    'g0': '09:30~17:50', 'g1': '09:30~10:20', 'g2': '10:30~11:20', 'g3': '11:30~12:20',
    'g4': '14:00~14:50', 'g5': '15:00~15:50', 'g6': '16:00~16:50', 'g7': '17:00~17:50',
}

RUN_HEADER = ['시각', '분', '블록', '유형', '사용 파일']
WARN_WORDS = ('경고', '주의', '실패', '결손', '미제작', '미검증', '금지', '리스크', '반드시')


# ────────────────────────────────────────────────────────────── 인라인

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def render_link(text, href):
    m = re.fullmatch(r'GUIDE_(\d)(?:_overview)?\.md', href)
    if m:
        return '<a class="xref" href="#/g%s">%s</a>' % (m.group(1), text)
    if href.startswith(('http://', 'https://')):
        return '<a class="xlink" href="%s" target="_blank" rel="noopener">%s</a>' % (esc(href), text)
    # 저장소 상대경로 — standalone 배포 시 해석 불가하므로 경로 표기로 렌더
    return '<span class="path">%s</span>' % text


def inline(t):
    spans = []

    def keep(m):
        spans.append(m.group(1))
        return '\x00%d\x00' % (len(spans) - 1)

    t = re.sub(r'`([^`]+)`', keep, t)
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: render_link(m.group(1), m.group(2)), t)
    t = re.sub(r'\x00(\d+)\x00', lambda m: '<code>%s</code>' % esc(spans[int(m.group(1))]), t)
    return t


def split_row(line):
    line = line.strip().strip('|')
    cells = re.split(r'(?<!\\)\|', line)
    return [c.strip().replace('\\|', '|') for c in cells]


def slug_kind(v):
    v = v.replace(' ', '')
    if '통제' in v:
        return 'control'
    if '실습' in v:
        return 'lab'
    if '시연' in v:
        return 'demo'
    if '강의' in v:
        return 'talk'
    if '안내' in v:
        return 'brief'
    return 'none'


# ────────────────────────────────────────────────────────────── 블록 파서

class Doc(object):
    def __init__(self, gid):
        self.gid = gid
        self.out = []
        self.heads = []          # {id, level, text}
        self.run = []            # 타임라인 행
        self.n = 0

    def hid(self):
        self.n += 1
        return '%s-h%d' % (self.gid, self.n)


def render(md, gid):
    d = Doc(gid)
    lines = md.split('\n')
    i, N = 0, len(lines)

    while i < N:
        ln = lines[i]

        # ── 코드 펜스
        if ln.startswith('```'):
            lang = ln[3:].strip()
            i += 1
            buf = []
            while i < N and not lines[i].startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            body = esc('\n'.join(buf))
            if lang:
                d.out.append(
                    '<figure class="code"><span class="code-tag">%s</span><pre><code>%s</code></pre></figure>'
                    % (esc(lang), body))
            else:
                d.out.append('<figure class="board"><pre>%s</pre></figure>' % body)
            continue

        # ── 표
        if ln.startswith('|') and i + 1 < N and re.fullmatch(r'\|[\s:\-\|]+\|', lines[i + 1].strip()):
            head = split_row(ln)
            i += 2
            rows = []
            while i < N and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1

            if head == RUN_HEADER:
                d.run = rows
                d.out.append(runstrip(rows))

            th = ''.join('<th>%s</th>' % inline(c) for c in head)
            tb = ''.join(
                '<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in r)
                for r in rows)
            d.out.append('<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                         % (th, tb))
            continue

        # ── 인용 (대사 / 콜아웃)
        if ln.startswith('>'):
            buf = []
            while i < N and lines[i].startswith('>'):
                buf.append(lines[i][1:].lstrip() if len(lines[i]) > 1 else '')
                i += 1
            text = '\n'.join(buf).strip('\n')
            paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
            body = ''.join('<p>%s</p>' % inline(p.replace('\n', ' ')) for p in paras)
            first = text.lstrip()
            if first.startswith(('"', '“', '(')):
                d.out.append('<blockquote class="say"><span class="say-tag">대사</span>%s</blockquote>' % body)
            else:
                tone = 'warn' if any(w in text for w in WARN_WORDS) else 'note'
                d.out.append('<aside class="callout %s">%s</aside>' % (tone, body))
            continue

        # ── 목록
        if re.match(r'^\s*(?:-\s|\d+\.\s)', ln):
            ordered = bool(re.match(r'^\s*\d+\.\s', ln))
            items = []
            while i < N and re.match(r'^\s*(?:-\s|\d+\.\s)', lines[i]):
                items.append(re.sub(r'^\s*(?:-\s|\d+\.\s)', '', lines[i]))
                i += 1
            tag = 'ol' if ordered else 'ul'
            d.out.append('<%s>%s</%s>' % (tag, ''.join('<li>%s</li>' % inline(x) for x in items), tag))
            continue

        # ── 제목
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            lv = len(m.group(1))
            raw = m.group(2).strip()
            hid = d.hid()
            d.heads.append({'id': hid, 'level': lv, 'text': re.sub(r'[*`]', '', raw)})
            d.out.append(heading(lv, hid, raw))
            i += 1
            continue

        # ── 구분선
        if re.fullmatch(r'-{3,}', ln.strip()):
            d.out.append('<hr>')
            i += 1
            continue

        # ── 문단
        if ln.strip():
            buf = [ln]
            i += 1
            while i < N and lines[i].strip() and not re.match(r'^(#{1,6}\s|\||>|```|-{3,}$|\s*-\s|\s*\d+\.\s)', lines[i]):
                buf.append(lines[i])
                i += 1
            d.out.append('<p>%s</p>' % inline(' '.join(buf)))
            continue

        i += 1

    return d


def heading(lv, hid, raw):
    # H3 : "B1-1 · 강사 소개 및 OT (09:30~09:35 · 5분)"
    m = re.match(r'^(B\d-\d)\s*·\s*(.+?)\s*\((.+)\)\s*$', raw)
    if lv == 3 and m:
        return ('<h3 id="%s" class="block" data-block="%s">'
                '<span class="chip block-id">%s</span>'
                '<span class="block-name">%s</span>'
                '<span class="block-time">%s</span></h3>'
                % (hid, m.group(1), m.group(1), inline(m.group(2)), inline(m.group(3))))
    # H4 : "LAB_4-1 · dtc-explainer 손코딩 (5분)"
    m4 = re.match(r'^(LAB_[\d\-]+)\s*·\s*(.+?)(?:\s*\((.+)\))?\s*$', raw)
    if lv == 4 and m4:
        t = '<span class="block-time">%s</span>' % inline(m4.group(3)) if m4.group(3) else ''
        return ('<h4 id="%s" class="lab"><span class="chip lab-id">%s</span>'
                '<span class="block-name">%s</span>%s</h4>'
                % (hid, m4.group(1), inline(m4.group(2)), t))
    return '<h%d id="%s">%s</h%d>' % (lv, hid, inline(raw), lv)


def runstrip(rows):
    total = 0
    parts = []
    for r in rows:
        if len(r) < 4:
            continue
        try:
            mins = int(re.sub(r'\D', '', r[1]) or 0)
        except ValueError:
            mins = 0
        total += mins
        bm = re.match(r'^(B\d-\d)\s*(.*)$', r[2])
        bid = bm.group(1) if bm else ''
        label = bm.group(2).strip() if bm else r[2]
        parts.append(
            '<button class="rs" data-goto="%s" data-kind="%s" style="flex:%d 1 0">'
            '<span class="rs-at">%s</span>'
            '<span class="rs-label">%s</span>'
            '<span class="rs-min">%s분</span></button>'
            % (esc(bid), slug_kind(r[3]), max(mins, 2), esc(r[0]), inline(label), mins))
    return ('<div class="runstrip-wrap"><div class="runstrip-head">'
            '<span class="rs-title">런시트</span><span class="rs-total">총 %d분</span></div>'
            '<div class="runstrip">%s</div>'
            '<div class="rs-legend">'
            '<span data-kind="talk">강의</span><span data-kind="demo">시연</span>'
            '<span data-kind="lab">실습</span><span data-kind="brief">안내</span>'
            '<span data-kind="control">통제</span></div></div>'
            % (total, ''.join(parts)))


# ────────────────────────────────────────────────────────────── 문서 조립

def build():
    guides, index = [], []
    for gid, fn, num, topic in SOURCES:
        path = os.path.join(HERE, fn)
        if not os.path.exists(path):
            print('!! 없음:', fn, file=sys.stderr)
            sys.exit(1)
        md = io.open(path, encoding='utf-8').read()
        d = render(md, gid)
        title = d.heads[0]['text'] if d.heads else topic
        sections = [h for h in d.heads if h['level'] == 2]
        guides.append({
            'id': gid, 'num': num, 'topic': topic, 'title': title,
            'time': TIMES[gid], 'sections': sections, 'html': '\n'.join(d.out),
        })
        for h in d.heads:
            if h['level'] <= 4:
                index.append({'g': gid, 'i': h['id'], 't': h['text'], 'l': h['level']})

    nav = ''.join(
        '<li><button class="nav-item" data-go="%s">'
        '<span class="nav-num%s">%s</span>'
        '<span class="nav-body"><span class="nav-topic">%s</span>'
        '<span class="nav-time">%s</span></span></button>'
        '<ul class="nav-sub">%s</ul></li>'
        % (g['id'], ' is-ot' if g['num'] == '개요' else '', g['num'], esc(g['topic']), g['time'],
           ''.join('<li><button data-sec="%s" data-go="%s">%s</button></li>'
                   % (s['id'], g['id'], esc(re.sub(r'^\d+\.\s*', '', s['text']))) for s in g['sections']))
        for g in guides)

    panes = ''.join(
        '<section class="guide" id="%s" data-num="%s" data-topic="%s" data-time="%s" hidden>%s</section>'
        % (g['id'], esc(g['num']), esc(g['topic']), g['time'], g['html'])
        for g in guides)

    body = (SHELL
            .replace('{{NAV}}', nav)
            .replace('{{PANES}}', panes)
            .replace('{{INDEX}}', json.dumps(index, ensure_ascii=False)))

    os.makedirs(DIST, exist_ok=True)

    frag = '<title>강사 런시트</title>\n' + FONTS + '\n<style>\n' + CSS + '\n</style>\n' + body + '\n<script>\n' + JS + '\n</script>\n'
    io.open(os.path.join(DIST, 'artifact.html'), 'w', encoding='utf-8').write(frag)

    full = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>강사 런시트 — Claude Code 실무 교육</title>\n' + FONTS +
            '\n<style>\n' + CSS + '\n</style>\n</head>\n<body>\n' + body +
            '\n<script>\n' + JS + '\n</script>\n</body>\n</html>\n')
    out = os.path.join(DIST, 'instructor-guide.html')
    io.open(out, 'w', encoding='utf-8').write(full)

    print('가이드 %d편 · 표제 %d개' % (len(guides), len(index)))
    for g in guides:
        print('  %-4s %-16s %s  섹션 %d' % (g['num'], g['topic'], g['time'], len(g['sections'])))
    print('\n생성 : %s  (%.0f KB)' % (out, os.path.getsize(out) / 1024))


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;500;600&'
         'family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&display=swap">')


CSS = r"""
/* ══ 토큰 ── module_3/DESIGN.md 의 관제 콘솔 팔레트에서 파생 ══ */
:root{
  color-scheme:light;
  --ground:#F4F6FA;      --surface:#FFFFFF;     --raised:#EDF1F7;
  --line:#DCE2EC;        --line-soft:#E9EDF4;
  --ink:#141A26;         --ink-2:#3B4457;       --muted:#69738A;   --faint:#98A2B6;
  --accent:#1F63B8;      --accent-ink:#12457F;  --accent-soft:#E4EDF9;  --on-accent:#FFFFFF;
  --ok:#1F7A56;          --ok-soft:#E1F2EA;
  --warn:#9A6108;        --warn-soft:#FBF0DC;
  --danger:#B5382C;      --danger-soft:#FAE7E4;
  --info:#0B6E85;        --info-soft:#E0F0F4;
  --board-bg:#111725;    --board-ink:#D5DCEA;   --board-line:#2C3446;
  --shadow:0 1px 2px rgba(20,26,38,.05), 0 12px 28px -18px rgba(20,26,38,.35);
  --rail-w:288px;
  --sans:'IBM Plex Sans KR','Pretendard','Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  --mono:'IBM Plex Mono','D2Coding','Cascadia Mono',Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --ground:#0F1420;    --surface:#171D2B;     --raised:#1E2536;
    --line:#2A3245;      --line-soft:#212938;
    --ink:#E6EBF5;       --ink-2:#C3CBDA;       --muted:#8C97AD;   --faint:#6B7690;
    --accent:#4DA3FF;    --accent-ink:#8FC4FF;  --accent-soft:#16273D;  --on-accent:#0F1420;
    --ok:#35D07F;        --ok-soft:#122C22;
    --warn:#FFB547;      --warn-soft:#2E2416;
    --danger:#FF5F6D;    --danger-soft:#31191C;
    --info:#38C4DE;      --info-soft:#122A31;
    --board-bg:#0B101B;  --board-ink:#C7D0E0;   --board-line:#242C3D;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 14px 32px -18px rgba(0,0,0,.7);
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --ground:#0F1420;      --surface:#171D2B;     --raised:#1E2536;
  --line:#2A3245;        --line-soft:#212938;
  --ink:#E6EBF5;         --ink-2:#C3CBDA;       --muted:#8C97AD;   --faint:#6B7690;
  --accent:#4DA3FF;      --accent-ink:#8FC4FF;  --accent-soft:#16273D;  --on-accent:#0F1420;
  --ok:#35D07F;          --ok-soft:#122C22;
  --warn:#FFB547;        --warn-soft:#2E2416;
  --danger:#FF5F6D;      --danger-soft:#31191C;
  --info:#38C4DE;        --info-soft:#122A31;
  --board-bg:#0B101B;    --board-ink:#C7D0E0;   --board-line:#242C3D;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 14px 32px -18px rgba(0,0,0,.7);
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--sans); font-size:15px; line-height:1.72; font-weight:400;
  word-break:keep-all; overflow-wrap:anywhere;
}
button{font:inherit; color:inherit; background:none; border:0; cursor:pointer}
:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:4px}
@media (prefers-reduced-motion:reduce){ *{animation:none!important; transition:none!important} }

/* ══ 셸 ══ */
.app{display:grid; grid-template-columns:var(--rail-w) minmax(0,1fr); min-height:100vh}

/* ══ 좌측 레일 ══ */
.rail{
  position:sticky; top:0; height:100vh; display:flex; flex-direction:column;
  background:var(--surface); border-right:1px solid var(--line); z-index:30;
}
.brand{padding:22px 20px 16px; border-bottom:1px solid var(--line-soft)}
.brand-mark{
  display:inline-flex; align-items:center; gap:7px;
  font-family:var(--mono); font-size:10.5px; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent);
}
.brand-mark::before{content:''; width:7px; height:7px; border-radius:50%; background:var(--accent)}
.brand h1{margin:8px 0 3px; font-size:19px; font-weight:600; letter-spacing:-.01em; line-height:1.3}
.brand p{margin:0; font-size:12.5px; color:var(--muted)}

.search{padding:14px 16px 10px}
.search input{
  width:100%; padding:8px 11px; font-size:13px; font-family:inherit;
  color:var(--ink); background:var(--raised);
  border:1px solid var(--line); border-radius:7px;
}
.search input::placeholder{color:var(--faint)}

.nav{flex:1; overflow-y:auto; padding:0 10px 20px}
.nav ul{list-style:none; margin:0; padding:0}
.nav > ul > li + li{margin-top:2px}
.nav-item{
  width:100%; display:flex; align-items:center; gap:11px;
  padding:9px 10px; border-radius:8px; text-align:left;
  border:1px solid transparent;
}
.nav-item:hover{background:var(--raised)}
.nav-item.on{background:var(--accent-soft); border-color:color-mix(in srgb, var(--accent) 26%, transparent)}
.nav-num{
  flex:none; width:26px; height:26px; display:grid; place-items:center;
  font-family:var(--mono); font-size:13px; font-weight:600; font-variant-numeric:tabular-nums;
  color:var(--muted); background:var(--raised); border:1px solid var(--line); border-radius:7px;
}
.nav-num.is-ot{width:auto; padding:0 8px; font-family:var(--sans); font-size:11px}
.nav-item.on .nav-num{background:var(--accent); border-color:var(--accent); color:var(--on-accent)}
.nav-body{display:flex; flex-direction:column; min-width:0; line-height:1.35}
.nav-topic{font-size:13.5px; font-weight:500}
.nav-item.on .nav-topic{color:var(--accent-ink)}
.nav-time{font-family:var(--mono); font-size:10.5px; color:var(--faint); font-variant-numeric:tabular-nums}

.nav-sub{display:none; margin:2px 0 8px 37px!important; padding-left:11px!important; border-left:1px solid var(--line)}
.nav-item.on + .nav-sub{display:block}
.nav-sub button{
  display:block; width:100%; text-align:left; padding:4px 8px; border-radius:6px;
  font-size:12.5px; color:var(--muted); line-height:1.45;
}
.nav-sub button:hover{background:var(--raised); color:var(--ink)}
.nav-sub button.on{color:var(--accent-ink); font-weight:500}

.rail-foot{padding:12px 16px; border-top:1px solid var(--line-soft); display:flex; gap:8px}
.rail-foot button{
  flex:1; padding:6px 8px; font-size:11.5px; color:var(--muted);
  border:1px solid var(--line); border-radius:7px; background:var(--raised);
}
.rail-foot button:hover{color:var(--ink); border-color:var(--accent)}

/* ══ 스테이지 ══ */
.stage{min-width:0; display:flex; flex-direction:column}
.topbar{
  position:sticky; top:0; z-index:20; display:flex; align-items:center; gap:14px;
  padding:0 34px; height:62px;
  background:color-mix(in srgb, var(--ground) 88%, transparent);
  backdrop-filter:saturate(1.4) blur(10px);
  border-bottom:1px solid var(--line);
}
.tb-num{
  font-family:var(--mono); font-size:11px; font-weight:600; letter-spacing:.1em;
  padding:4px 9px; border-radius:6px; color:var(--accent-ink); background:var(--accent-soft);
}
.tb-title{font-size:15.5px; font-weight:600; letter-spacing:-.01em}
.tb-time{
  margin-left:auto; font-family:var(--mono); font-size:12.5px; color:var(--muted);
  font-variant-numeric:tabular-nums;
}
.menu-btn{display:none; padding:6px 10px; border:1px solid var(--line); border-radius:7px; font-size:13px}

.scroll{flex:1; padding:34px 34px 96px}
.guide{max-width:920px; margin:0 auto}
.guide[hidden]{display:none}

/* ══ 본문 타이포 ══ */
.guide h1{display:none}
.guide h2{
  margin:52px 0 18px; padding-top:20px; border-top:1px solid var(--line);
  font-size:20px; font-weight:600; letter-spacing:-.015em; text-wrap:balance;
  scroll-margin-top:86px;
}
.guide > h2:first-of-type{margin-top:8px; border-top:0; padding-top:0}
.guide h3{
  margin:34px 0 14px; font-size:16.5px; font-weight:600; letter-spacing:-.01em;
  text-wrap:balance; scroll-margin-top:86px;
}
.guide h3.block{
  display:flex; flex-wrap:wrap; align-items:baseline; gap:10px;
  padding:10px 14px; background:var(--surface);
  border:1px solid var(--line); border-left:3px solid var(--accent); border-radius:9px;
}
.guide h4{margin:26px 0 10px; font-size:14.5px; font-weight:600; scroll-margin-top:86px}
.guide h4.lab{display:flex; flex-wrap:wrap; align-items:baseline; gap:9px}
.chip{
  font-family:var(--mono); font-size:11px; font-weight:600; letter-spacing:.04em;
  padding:2px 7px; border-radius:5px; white-space:nowrap;
}
.block-id{color:var(--on-accent); background:var(--accent)}
.lab-id{color:var(--info); background:var(--info-soft)}
.block-name{flex:1 1 auto; min-width:0}
.block-time{font-family:var(--mono); font-size:11.5px; font-weight:400; color:var(--muted); font-variant-numeric:tabular-nums}

.guide p{margin:0 0 14px; max-width:74ch}
.guide ul,.guide ol{margin:0 0 16px; padding-left:20px; max-width:74ch}
.guide li{margin:3px 0}
.guide li::marker{color:var(--faint)}
.guide hr{margin:34px 0; border:0; border-top:1px solid var(--line-soft)}
.guide strong{font-weight:600; color:var(--ink)}
.guide code{
  font-family:var(--mono); font-size:.875em; padding:1px 5px; border-radius:4px;
  background:var(--raised); border:1px solid var(--line-soft); color:var(--ink-2);
}
.path{
  font-family:var(--mono); font-size:.875em; color:var(--muted);
  border-bottom:1px dotted var(--faint);
}
a.xref,a.xlink{color:var(--accent-ink); text-decoration:none; border-bottom:1px solid color-mix(in srgb,var(--accent) 40%,transparent)}
a.xref:hover,a.xlink:hover{border-bottom-color:var(--accent)}

/* ══ 런시트 스트립 ══ */
.runstrip-wrap{
  margin:0 0 22px; padding:14px 16px 12px;
  background:var(--surface); border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow);
}
.runstrip-head{display:flex; align-items:baseline; gap:10px; margin-bottom:10px}
.rs-title{font-family:var(--mono); font-size:10.5px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--muted)}
.rs-total{margin-left:auto; font-family:var(--mono); font-size:11.5px; color:var(--faint); font-variant-numeric:tabular-nums}
.runstrip{display:flex; gap:5px; align-items:stretch}
.rs{
  min-width:0; padding:9px 10px 8px; text-align:left; border-radius:8px;
  background:var(--raised); border:1px solid var(--line); border-top:3px solid var(--faint);
  display:flex; flex-direction:column; gap:2px; transition:transform .12s ease, border-color .12s ease;
}
.rs:hover{transform:translateY(-2px); border-color:var(--accent)}
.rs-at{font-family:var(--mono); font-size:11.5px; font-weight:600; font-variant-numeric:tabular-nums; color:var(--ink)}
.rs-label{font-size:11.5px; line-height:1.35; color:var(--muted); overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical}
.rs-min{margin-top:auto; font-family:var(--mono); font-size:10px; color:var(--faint); font-variant-numeric:tabular-nums}
.rs[data-kind="talk"]{border-top-color:var(--accent)}
.rs[data-kind="demo"]{border-top-color:var(--info)}
.rs[data-kind="lab"]{border-top-color:var(--ok)}
.rs[data-kind="brief"]{border-top-color:var(--faint)}
.rs[data-kind="control"]{border-top-color:var(--danger)}
.rs-legend{display:flex; flex-wrap:wrap; gap:14px; margin-top:11px; padding-top:10px; border-top:1px solid var(--line-soft)}
.rs-legend span{display:inline-flex; align-items:center; gap:5px; font-size:11px; color:var(--muted)}
.rs-legend span::before{content:''; width:12px; height:3px; border-radius:2px; background:var(--faint)}
.rs-legend span[data-kind="talk"]::before{background:var(--accent)}
.rs-legend span[data-kind="demo"]::before{background:var(--info)}
.rs-legend span[data-kind="lab"]::before{background:var(--ok)}
.rs-legend span[data-kind="control"]::before{background:var(--danger)}

/* ══ 대사 · 콜아웃 ══ */
.say{
  position:relative; margin:0 0 18px; padding:16px 20px 14px 22px;
  background:var(--surface); border:1px solid var(--line);
  border-left:3px solid var(--accent); border-radius:0 10px 10px 0;
}
.say-tag{
  position:absolute; top:-9px; left:16px; padding:1px 8px;
  font-family:var(--mono); font-size:10px; font-weight:600; letter-spacing:.1em;
  color:var(--on-accent); background:var(--accent); border-radius:4px;
}
.say p{margin:0 0 10px; color:var(--ink-2); line-height:1.8}
.say p:last-child{margin-bottom:0}

.callout{margin:0 0 18px; padding:12px 16px; border-radius:9px; border:1px solid var(--line)}
.callout p{margin:0 0 8px; font-size:14px}
.callout p:last-child{margin-bottom:0}
.callout.note{background:var(--raised); border-left:3px solid var(--muted)}
.callout.warn{background:var(--warn-soft); border-left:3px solid var(--warn); border-color:color-mix(in srgb,var(--warn) 26%,transparent)}

/* ══ 판서 · 코드 ══ */
.board{
  margin:0 0 18px; padding:16px 18px; border-radius:10px;
  background:var(--board-bg); border:1px solid var(--board-line);
  overflow-x:auto;
}
.board pre{
  margin:0; font-family:var(--mono); font-size:12.5px; line-height:1.62;
  color:var(--board-ink); white-space:pre;
}
.code{
  position:relative; margin:0 0 18px; padding:16px 18px 14px; border-radius:10px;
  background:var(--raised); border:1px solid var(--line); overflow-x:auto;
}
.code-tag{
  position:absolute; top:8px; right:12px;
  font-family:var(--mono); font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:var(--faint);
}
.code pre{margin:0; white-space:pre}
.code code{
  display:block; padding:0; background:none; border:0;
  font-family:var(--mono); font-size:12.5px; line-height:1.68; color:var(--ink-2);
}

/* ══ 표 ══ */
.tbl{margin:0 0 20px; overflow-x:auto; border:1px solid var(--line); border-radius:10px; background:var(--surface)}
.tbl table{border-collapse:collapse; width:100%; font-size:13.5px}
.tbl th,.tbl td{
  padding:9px 13px; text-align:left; vertical-align:top;
  border-bottom:1px solid var(--line-soft); font-variant-numeric:tabular-nums;
}
.tbl th{
  font-size:11px; font-weight:600; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted); background:var(--raised); white-space:nowrap;
  border-bottom:1px solid var(--line);
}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:color-mix(in srgb, var(--accent) 5%, transparent)}
.tbl td code{white-space:nowrap}

/* ══ 검색 ══ */
.results{max-width:920px; margin:0 auto}
.results[hidden]{display:none}
.res-head{font-size:12.5px; color:var(--muted); margin-bottom:14px}
.res{
  display:block; width:100%; text-align:left; padding:11px 14px; margin-bottom:6px;
  background:var(--surface); border:1px solid var(--line); border-radius:9px;
}
.res:hover{border-color:var(--accent)}
.res-where{font-family:var(--mono); font-size:10.5px; letter-spacing:.08em; color:var(--accent-ink); display:block; margin-bottom:2px}
.res-what{font-size:14px}
.res mark{background:color-mix(in srgb,var(--accent) 24%,transparent); color:inherit; border-radius:3px; padding:0 2px}

/* ══ 반응형 ══ */
@media (max-width:1080px){ .scroll{padding:26px 22px 80px} .topbar{padding:0 22px} }
@media (max-width:900px){
  .app{grid-template-columns:1fr}
  .rail{
    position:fixed; inset:0 auto 0 0; width:min(88vw,var(--rail-w));
    transform:translateX(-100%); transition:transform .22s ease;
  }
  .rail.open{transform:none; box-shadow:0 0 0 100vmax rgba(10,14,22,.45)}
  .menu-btn{display:block}
  .runstrip{flex-wrap:wrap}
  .rs{flex:1 1 132px!important}
}

/* ══ 인쇄 ══ */
@media print{
  .rail,.topbar,.runstrip-wrap,.rail-foot,.search{display:none!important}
  .app{display:block} .scroll{padding:0}
  .guide{display:block!important; max-width:none; page-break-after:always}
  .guide h1{display:block; font-size:22px; margin:0 0 16px}
  .say,.tbl,.board,.code,.callout{break-inside:avoid}
  body{background:#fff; color:#000; font-size:11pt}
}
"""


SHELL = r"""
<div class="app">
  <aside class="rail" id="rail">
    <div class="brand">
      <span class="brand-mark">Instructor Run Sheet</span>
      <h1>강사 운영 가이드</h1>
      <p>Claude Code 실무 교육 · 1일 7교시</p>
    </div>
    <div class="search">
      <input id="q" type="search" placeholder="제목 · 블록 검색" autocomplete="off" aria-label="검색">
    </div>
    <nav class="nav" aria-label="교시"><ul>{{NAV}}</ul></nav>
    <div class="rail-foot">
      <button id="theme">테마 전환</button>
      <button id="print">전체 인쇄</button>
    </div>
  </aside>

  <main class="stage">
    <header class="topbar">
      <button class="menu-btn" id="menu" aria-label="목차 열기">목차</button>
      <span class="tb-num" id="tbNum">개요</span>
      <span class="tb-title" id="tbTitle">전체 운영</span>
      <span class="tb-time" id="tbTime">09:30~17:50</span>
    </header>
    <div class="scroll" id="scroll">
      <div class="results" id="results" hidden></div>
      {{PANES}}
    </div>
  </main>
</div>
<script id="idx" type="application/json">{{INDEX}}</script>
"""


JS = r"""
(function(){
  var IDX = JSON.parse(document.getElementById('idx').textContent);
  var panes = [].slice.call(document.querySelectorAll('.guide'));
  var items = [].slice.call(document.querySelectorAll('.nav-item'));
  var scroll = document.getElementById('scroll');
  var results = document.getElementById('results');
  var q = document.getElementById('q');
  var rail = document.getElementById('rail');
  var META = {};
  panes.forEach(function(p){ META[p.id] = {num:p.dataset.num, topic:p.dataset.topic, time:p.dataset.time}; });

  function show(gid, secId){
    if(!META[gid]) gid = 'g0';
    results.hidden = true;
    panes.forEach(function(p){ p.hidden = (p.id !== gid); });
    items.forEach(function(b){ b.classList.toggle('on', b.dataset.go === gid); });
    document.querySelectorAll('.nav-sub button').forEach(function(b){
      b.classList.toggle('on', b.dataset.sec === secId);
    });
    var m = META[gid];
    document.getElementById('tbNum').textContent = m.num === '개요' ? '개요' : m.num + '교시';
    document.getElementById('tbTitle').textContent = m.topic;
    document.getElementById('tbTime').textContent = m.time;
    rail.classList.remove('open');
    if(secId){
      var el = document.getElementById(secId);
      if(el){ el.scrollIntoView({block:'start', behavior:'smooth'}); return; }
    }
    window.scrollTo(0,0);
  }

  function route(){
    var h = (location.hash || '#/g0').replace(/^#\//,'').split('/');
    show(h[0] || 'g0', h[1]);
  }
  window.addEventListener('hashchange', route);

  document.addEventListener('click', function(e){
    var nav = e.target.closest('[data-go]');
    if(nav){
      location.hash = '#/' + nav.dataset.go + (nav.dataset.sec ? '/' + nav.dataset.sec : '');
      return;
    }
    var rs = e.target.closest('.rs');
    if(rs){
      var pane = rs.closest('.guide');
      var h3 = pane.querySelector('h3[data-block="' + rs.dataset.goto + '"]');
      if(h3) h3.scrollIntoView({block:'start', behavior:'smooth'});
      return;
    }
    var xref = e.target.closest('a.xref');
    if(xref){ e.preventDefault(); location.hash = xref.getAttribute('href').slice(1); }
  });

  document.getElementById('menu').addEventListener('click', function(){ rail.classList.toggle('open'); });
  document.getElementById('print').addEventListener('click', function(){
    panes.forEach(function(p){ p.hidden = false; });
    window.print();
    setTimeout(route, 400);
  });

  /* 테마 */
  var root = document.documentElement;
  try{ var saved = localStorage.getItem('runsheet-theme'); if(saved) root.setAttribute('data-theme', saved); }catch(e){}
  document.getElementById('theme').addEventListener('click', function(){
    var cur = root.getAttribute('data-theme');
    var sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = cur ? (cur === 'dark' ? 'light' : 'dark') : (sysDark ? 'light' : 'dark');
    root.setAttribute('data-theme', next);
    try{ localStorage.setItem('runsheet-theme', next); }catch(e){}
  });

  /* 검색 */
  function esc(s){ return s.replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
  q.addEventListener('input', function(){
    var v = q.value.trim();
    if(v.length < 2){ results.hidden = true; route(); return; }
    var re = new RegExp(v.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'), 'gi');
    var hits = IDX.filter(function(h){ return re.test(h.t); }).slice(0, 60);
    panes.forEach(function(p){ p.hidden = true; });
    results.hidden = false;
    results.innerHTML = '<p class="res-head">"' + esc(v) + '" — ' + hits.length + '건</p>' +
      (hits.length ? hits.map(function(h){
        var m = META[h.g];
        var label = m.num === '개요' ? '개요' : m.num + '교시 · ' + m.topic;
        return '<button class="res" data-go="' + h.g + '" data-sec="' + h.i + '">' +
               '<span class="res-where">' + esc(label) + '</span>' +
               '<span class="res-what">' + esc(h.t).replace(re, function(x){ return '<mark>' + x + '</mark>'; }) + '</span></button>';
      }).join('') : '<p class="res-head">일치하는 항목 없음</p>');
  });

  route();
})();
"""


if __name__ == '__main__':
    build()
