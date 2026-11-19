import re, os, sys, subprocess, shutil, html
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out+'/media', exist_ok=True)
for f in os.listdir(src+'/image'):
    if not f.endswith('COVER.jpg'): shutil.copy(src+'/image/'+f, out+'/media/'+f)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:50]
BOOK='AI Governance: From Strategy to Execution (IAPP, 1st ed.)'
heads={'_11-A-Head':'h2','_12-B-Head':'h3','_13-C-Head':'h4','_14-D-Head':'h5','_90-End-NOTES-Header':'h2'}
files=[('AIGP_1E-FM_EPUB','00-front-matter','Front matter (About, Preface, Introduction)',None,'')]
for i in range(1,17): files.append((f'AIGP_1E-Chapter_{i}',None,None,i,''))
files.append(('AIGP_1E-BM','99-back-matter','Back matter',None,''))
index=[]
for base,fname,title,num,_ in files:
    t=open(f'{src}/{base}.xhtml',encoding='utf8').read()
    authors=''
    if num:
        title=re.sub('<[^>]+>','',re.search(r'class="_02-Chap-Title[^"]*"[^>]*>(.*?)</p>',t,re.S).group(1)).strip()
        title=html.unescape(title)
        m=re.search(r'class="_02-Chap-author[^"]*"[^>]*>(.*?)</p>',t,re.S)
        authors=html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else ''
        fname=f'ch{num:02d}-{slug(title)}'
        t=re.sub(r'<p[^>]*class="_01-Chap-Num[^"]*"[^>]*>.*?</p>','',t,flags=re.S)
        t=re.sub(r'<p[^>]*class="_02-Chap-Title[^"]*"[^>]*>.*?</p>',f'<h1>Chapter {num}: {html.escape(title)}</h1>',t,flags=re.S)
    for c,h in heads.items():
        t=re.sub(r'<p([^>]*)class="'+c+r'[^"]*"([^>]*)>(.*?)</p>',lambda m:f'<{h}>'+re.sub(r'</?a[^>]*>','',m.group(3))+f'</{h}>',t,flags=re.S)
    # endnote refs -> superscript text, drop anchors
    t=re.sub(r'<a[^>]*class="_idEndnoteLink[^"]*"[^>]*>(.*?)</a>',r'<sup>\1</sup>',t,flags=re.S)
    t=re.sub(r'<a[^>]*class="_idEndnoteAnchor[^"]*"[^>]*>(.*?)</a>',r'\1',t,flags=re.S)
    t=re.sub(r'<a id="[^"]*"\s*/?>(</a>)?','',t)
    t=t.replace('src="image/','src="media/')
    # endnotes: li -> numbered paragraphs
    t=re.sub(r'<li[^>]*id="endnote-[^"]*"[^>]*>\s*<p[^>]*>(.*?)</p>\s*</li>',lambda m:'<p>'+re.sub(r'^\s*(<span>)?(\d+)(</span>)?\s*(&#9;|\t)',r'<b>\2.</b> ',m.group(1).strip())+'</p>',t,flags=re.S)
    t=re.sub(r'<ol[^>]*>((?:\s*<p>.*?</p>)+)\s*</ol>',r'\1',t,flags=re.S)
    # single-cell boxes -> blockquotes
    def box(m):
        inner=m.group(0)
        if len(re.findall(r'<td',inner))==1:
            c=re.search(r'<td[^>]*>(.*)</td>',inner,re.S).group(1)
            c=re.sub(r'^\s*<p[^>]*>(.*?)</p>',r'<p><b>\1</b></p>',c,count=1,flags=re.S)
            return '<blockquote>'+c+'</blockquote>'
        return inner
    t=re.sub(r'<table.*?</table>',box,t,flags=re.S)
    p=subprocess.run(['pandoc','-f','html','-t','gfm','--wrap=none'],input=t,capture_output=True,text=True)
    md=p.stdout
    md=re.sub(r'<(/?)(span|div)[^>]*>','',md)
    md=re.sub(r'\n{3,}','\n\n',md)
    fm=f'---\ntitle: "{title}"\nsource: "{BOOK}"\noriginal: "../../originals/AI Governance From Strategy to Execution.epub"\n'
    if num: fm+=f'chapter: {num}\nauthors: "{authors}"\n'
    fm+='tags: [source-text, aigp-book]\n---\n\n'
    if not num: md=f'# {title}\n\n'+md
    open(f'{out}/{fname}.md','w',encoding='utf8').write(fm+md)
    index.append((fname,title,num,authors))
import json; json.dump(index,open(out+'/.index.json','w'))
print('\n'.join(f'{f}  {len(open(out+"/"+f+".md").read())//1000}k' for f,*_ in index))
