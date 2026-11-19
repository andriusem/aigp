import subprocess, re, os, sys
pdf, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
def page(n, layout=False):
    a=['pdftotext','-f',str(n),'-l',str(n)]+(['-layout'] if layout else [])+[pdf,'-']
    t=subprocess.run(a,capture_output=True,text=True).stdout
    lines=[l for l in t.split('\n') if not re.search(r'©\s*OECD 2022|OECD FRAMEWORK FOR THE CLASSIFICATION OF AI SYSTEMS', l)]
    return '\n'.join(lines)
def reflow(t):
    paras=[]; cur=''
    for l in t.split('\n'):
        s=l.strip()
        if not s:
            if cur: paras.append(cur); cur=''
            continue
        if re.match(r'^(•|-|\d+\.)\s', s) and cur: paras.append(cur); cur=s; continue
        if cur.endswith('-') and not cur.endswith(' -'): cur=cur[:-1]+s
        else: cur=(cur+' '+s).strip()
    if cur: paras.append(cur)
    out=[]
    for p in paras:
        p=re.sub(r'^•\s*','- ',p)
        if re.fullmatch(r'\d{1,3}',p): continue
        out.append(p)
    return '\n\n'.join(out)
SECS=[('00-summary','Abstract and executive summary',[3,6,7]),
('01-overview','1. Overview and goal of the framework',range(16,25)),
('02-people-and-planet','2. Classification framework: People & Planet',range(25,30)),
('03-economic-context','2. Classification framework: Economic Context',range(30,35)),
('04-data-and-input','2. Classification framework: Data & Input',range(35,42)),
('05-ai-model','2. Classification framework: AI Model',range(42,50)),
('06-task-and-output','2. Classification framework: Task & Output',range(50,55)),
('07-applying-the-framework','3. Applying the framework (credit scoring, AlphaGo Zero, manufacturing, GPT-3)',range(55,66)),
('08-next-steps','4. Next steps',range(66,68)),
('09-annexes-a-b','Annex A (sample AI applications by sector) and Annex B (AI adoption per industry)',range(68,72))]
SRC='OECD (2022), OECD Framework for the Classification of AI Systems, OECD Digital Economy Papers No. 323, https://doi.org/10.1787/cb6d9eca-en'
idx=[]
for fn,title,pages in SECS:
    body=''
    for n in pages:
        lay=page(n,True)
        body+=f'## Page {n}\n\n'+reflow(page(n))+'\n\n'
        if re.search(r'^\s*Table \d+\.', lay, re.M) or n==18:
            body+='<details><summary>Layout view of page '+str(n)+' (tables)</summary>\n\n```text\n'+lay.strip('\n')+'\n```\n\n</details>\n\n'
    pr=f'pp. {list(pages)[0]}–{list(pages)[-1]}' if len(list(pages))>1 else f'p. {list(pages)[0]}'
    fm=f'---\ntitle: "{title}"\nsource: "{SRC}"\noriginal: "../../originals/oecd-framework.pdf"\npages: "{pr}"\ntags: [source-text, oecd-classification]\n---\n\n'
    open(f'{out}/{fn}.md','w',encoding='utf8').write(fm+f'# {title}\n\n*{pr}* · [Index](00-index.md) · [PDF](../../originals/oecd-framework.pdf#page={list(pages)[0]})\n\n'+body)
    idx.append((fn,title,pr))
ix=f'---\ntitle: "OECD Framework for the Classification of AI Systems: index"\nsource: "{SRC}"\ntags: [source-text, oecd-classification, index]\n---\n\n# OECD Framework for the Classification of AI Systems (2022)\n\n{SRC}. 80 pages. Reading copy split by section, with page headings (`## Page N`) for citation; pages with tables also have a layout view. French and German summaries and the acknowledgement/membership annexes are left out. Original: [PDF](../../originals/oecd-framework.pdf). © OECD 2022, used under the OECD terms and conditions: local only.\n\n'
ix+=''.join(f'- [{t}]({f}.md) ({p})\n' for f,t,p in idx)
open(f'{out}/00-index.md','w',encoding='utf8').write(ix)
print('\n'.join(f'{f}: {len(open(out+"/"+f+".md").read())//1000}k' for f,_,_ in idx))
