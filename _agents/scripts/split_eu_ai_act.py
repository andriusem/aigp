import re, os, sys
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
raw = open(src, encoding='utf8').read().split('\n')
# strip page furniture, collect footnotes per page
junk = re.compile(r'^(\d+/144|ELI: http://data\.europa\.eu/eli/reg/2024/1689/oj|EN|OJ L, 12\.7\.2024)$')
fn = re.compile(r'^\(\d+\)\s+(OJ |Regulation|Directive|Council|Commission|Decision|Position|Judgment|Recommendation|Opinion|Interinstitutional)')
lines, notes = [], []
page = []
def flush():
    # trailing footnotes of a page
    i = len(page)
    while i > 0 and (fn.match(page[i-1]) or (page[i-1] and not page[i-1].startswith('(') and i>1 and any(fn.match(x) for x in page[max(0,i-4):i-1]) and page[i-1][:1].islower())):
        i -= 1
    j = i
    # only treat as footnotes if block starts with a footnote line
    while j < len(page) and not fn.match(page[j]): j += 1
    body, foot = page[:j], page[j:]
    lines.extend(body)
    if foot: lines.append('\x00FN ' + ' '.join(x.strip() for x in foot))
for l in raw:
    l = l.rstrip().replace('`', '')
    if junk.match(l.strip()):
        if page: flush(); page.clear()
        continue
    page.append(l)
flush()

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60]
start = next(i for i,l in enumerate(lines) if l.strip()=='HAVE ADOPTED THIS REGULATION:')
annex0 = next(i for i,l in enumerate(lines) if l.strip()=='ANNEX I')

def reflow(block):
    b=[x.strip() for x in block]
    keep=[]
    for k,x in enumerate(b):
        if not x:
            prev=next((y for y in reversed(keep) if y),'')
            nxt=next((y for y in b[k+1:] if y),'')
            if prev and nxt[:1].islower() and not prev.endswith(('.',';',':')): continue
        keep.append(x)
    block=keep
    paras, cur = [], ''
    for l in block:
        s = l.strip()
        if s.startswith('\x00FN '):
            paras.append(('fn', s[4:])); continue
        if not s:
            if cur and re.fullmatch(r'\d+\.', cur): continue
            if cur: paras.append(('p', cur)); cur = ''
            continue
        newp = re.match(r'^(\(\w{1,5}\)|—|–|\d+\.)(\s|$)', s) and not (cur and re.fullmatch(r'\d+\.', cur))
        if newp and cur: paras.append(('p', cur)); cur = s
        else: cur = (cur + ' ' + s).strip() if cur else s
        if cur.endswith('-') and not cur.endswith(' -'): pass
    if cur: paras.append(('p', cur))
    return paras

# --- articles
arts = []; chapter = section = ''
i = start + 1; n = 1
cur = None
while i < annex0:
    s = lines[i].strip()
    if re.fullmatch(r'CHAPTER [IVXL]+', s):
        j=i+1
        while not lines[j].strip(): j+=1
        chapter = 'Chapter ' + s.split()[1] + ': ' + re.sub(r'\b(ai|eu)\b', lambda m:m.group(1).upper(), lines[j].strip().lower().capitalize()); section = ''; i = j+1; continue
    if re.fullmatch(r'SECTION \d+', s):
        j=i+1
        while not lines[j].strip(): j+=1
        section = s.capitalize() + ': ' + lines[j].strip(); i = j+1; continue
    if s == f'Article {n}':
        cur = {'n': n, 'title': lines[i+1].strip(), 'chapter': chapter, 'section': section, 'body': []}
        arts.append(cur); n += 1; i += 2; continue
    if cur: cur['body'].append(lines[i])
    i += 1
assert len(arts) == 113, len(arts)
afile = {a['n']: f"art-{a['n']:03d}-{slug(a['title'])}" for a in arts}

# --- annexes
roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII']
anx = []; idxs = []
for r in roman:
    idxs.append(next(i for i in range(annex0, len(lines)) if lines[i].strip()==f'ANNEX {r}'))
for k, r in enumerate(roman):
    a, b = idxs[k], idxs[k+1] if k+1 < len(roman) else len(lines)
    body = lines[a+1:b]
    # title: lines until first blank
    t = []
    while body and not body[0].strip(): body.pop(0)
    while body and body[0].strip(): t.append(body.pop(0).strip())
    title = ' '.join(t)
    anx.append({'r': r, 'k': k+1, 'title': title, 'body': body})
xfile = {x['r']: f"annex-{x['k']:02d}-{slug(x['title'])}" for x in anx}

link_art = re.compile(r'\bArticles? (\d+)((?:\(\d+\))*(?:\([a-z]+\))*)')
EXTW=('Regulation','Directive','Decision','the Charter','the TEU','the TFEU','the Treaty','Council','Commission','Protocol')
def is_ext(tail):
    tail=tail[:70]; i=tail.find(' of ')
    if i<0: return False
    pre=tail[:i]
    if len(pre.split())>6 or any(c in pre for c in '.;:'): return False
    return tail[i+4:].startswith(EXTW)
def linkify(t, here=None):
    if here == 'recital':
        return re.sub(r'\bAnnex (XIII|XII|XI|IX|X|VIII|VII|VI|IV|V|III|II|I)\b(?! to)', lambda m: f'[Annex {m.group(1)}]({xfile[m.group(1)]}.md)', t)
    def ra(m):
        num = int(m.group(1))
        if is_ext(m.string[m.end():m.end()+90]): return m.group(0)
        if num in afile and num != here:
            return f'[Article {num}{m.group(2)}]({afile[num]}.md)' if m.group(0).startswith('Article ') else f'Articles [{num}{m.group(2)}]({afile[num]}.md)'
        return m.group(0)
    t = link_art.sub(ra, t)
    t = re.sub(r'\bAnnex (XIII|XII|XI|IX|X|VIII|VII|VI|IV|V|III|II|I)\b(?! to)', lambda m: f'[Annex {m.group(1)}]({xfile[m.group(1)]}.md)', t)
    return t

ELI = 'http://data.europa.eu/eli/reg/2024/1689/oj'
SRC = 'Regulation (EU) 2024/1689 (EU AI Act), OJ L, 12.7.2024'
def render(paras, here=None):
    o, f = [], []
    for kind, txt in paras:
        if kind == 'fn': f.append(txt); continue
        txt = linkify(txt, here)
        if re.match(r'^\d+\.\s', txt): o.append(f'**{txt.split(" ",1)[0]}** {txt.split(" ",1)[1]}')
        elif re.match(r'^\(\w{1,5}\)\s', txt): o.append('- ' + txt)
        else: o.append(txt)
    md = ''
    for k, p in enumerate(o):
        sep = '\n' if (p.startswith('- ') and k and o[k-1].startswith('- ')) else '\n\n'
        md += (sep if k else '') + p
    if f: md += '\n\n---\n*Footnotes on this page of the Official Journal:* ' + ' '.join(f)
    return md + '\n'

for a in arts:
    fm = f'---\ntitle: "Article {a["n"]}: {a["title"]}"\nsource: "{SRC}"\neli: {ELI}\narticle: {a["n"]}\nchapter: "{a["chapter"]}"\n' + (f'section: "{a["section"]}"\n' if a['section'] else '') + 'tags: [source-text, eu-ai-act]\n---\n\n'
    nav = f'*{a["chapter"]}' + (f' · {a["section"]}' if a['section'] else '') + '* · [Index](00-index.md)'
    prev = f'[← Article {a["n"]-1}]({afile[a["n"]-1]}.md)' if a['n'] > 1 else ''
    nxt = f'[Article {a["n"]+1} →]({afile[a["n"]+1]}.md)' if a['n'] < 113 else ''
    open(f'{out}/{afile[a["n"]]}.md','w',encoding='utf8').write(fm + f'# Article {a["n"]}: {a["title"]}\n\n{nav}\n\n' + render(reflow(a['body']), a['n']) + f'\n{prev}  {nxt}\n')
for x in anx:
    fm = f'---\ntitle: "Annex {x["r"]}: {x["title"]}"\nsource: "{SRC}"\neli: {ELI}\nannex: "{x["r"]}"\ntags: [source-text, eu-ai-act]\n---\n\n'
    open(f'{out}/{xfile[x["r"]]}.md','w',encoding='utf8').write(fm + f'# Annex {x["r"]}: {x["title"]}\n\n[Index](00-index.md)\n\n' + render(reflow(x['body'])))

# recitals
rec = lines[:start]
w0 = next(i for i,l in enumerate(rec) if l.strip()=='Whereas:')
rmd, cur, num = [], [], 0
seq = rec[w0+1:]
for idx, l in enumerate(seq):
    s = l.strip()
    m = re.match(r'^\((\d+)\)(\s+(.*))?$', s)
    ok = False
    if m and int(m.group(1)) == num+1:
        if m.group(3): ok = True
        else:
            k = idx+1
            while k < len(seq) and not seq[k].strip(): k += 1
            nx = seq[k].strip() if k < len(seq) else ''
            ok = not re.match(r'^\(\d+\)', nx) and not re.match(r'^(OJ |Regulation \(|Directive |Council |Commission |Position |Decision |Judgment )', nx)
    if ok:
        if num: rmd.append((num, cur))
        num += 1; cur = [m.group(3)] if m.group(3) else []; continue
    cur.append(l)
rmd.append((num, cur))
body = ''
for k, c in rmd:
    body += f'## Recital {k}\n\n' + render(reflow(c), 'recital') + '\n'
open(f'{out}/recitals.md','w',encoding='utf8').write(f'---\ntitle: "EU AI Act: recitals (1–{num})"\nsource: "{SRC}"\neli: {ELI}\ntags: [source-text, eu-ai-act]\n---\n\n# EU AI Act: recitals (1–{num})\n\nThe recitals explain the purpose and reasoning behind the articles. They are not binding but guide interpretation. [Index](00-index.md)\n\n' + body)

# index
ix = f'---\ntitle: "EU AI Act: index"\nsource: "{SRC}"\neli: {ELI}\ntags: [source-text, eu-ai-act, index]\n---\n\n# EU AI Act (Regulation (EU) 2024/1689)\n\nText as published in the Official Journal on 12 July 2024 ({ELI}), split one file per article. Later amendments (such as the Digital Omnibus) are **not** included. Only the Official Journal version is authentic.\n\n- [Recitals 1–{num}](recitals.md)\n'
ch = sec = None
for a in arts:
    if a['chapter'] != ch: ch = a['chapter']; sec = None; ix += f'\n## {ch}\n\n'
    if a['section'] and a['section'] != sec: sec = a['section']; ix += f'\n**{sec}**\n\n'
    ix += f'- [Article {a["n"]}: {a["title"]}]({afile[a["n"]]}.md)\n'
ix += '\n## Annexes\n\n' + ''.join(f'- [Annex {x["r"]}: {x["title"]}]({xfile[x["r"]]}.md)\n' for x in anx)
open(f'{out}/00-index.md','w',encoding='utf8').write(ix)
print(len(arts), 'articles,', len(anx), 'annexes,', num, 'recitals')
