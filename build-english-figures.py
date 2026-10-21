from pathlib import Path
import base64
from html import escape

assets=Path(__file__).parent/'dist'/'assets'
font=base64.b64encode((assets/'Exo2-Regular.ttf').read_bytes()).decode()
def document(title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img" aria-label="{escape(title)}"><defs><style>@font-face{{font-family:Exo2;src:url(data:font/ttf;base64,{font})}}text{{font-family:Exo2,Arial,sans-serif;fill:#173d41}}.label{{font-size:24px}}.small{{font-size:20px;fill:#56787c}}.white{{fill:white}}.flow{{stroke:#18bfc5;stroke-width:3;fill:none;marker-end:url(#arrow)}}</style><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#18bfc5"/></marker></defs><rect width="1200" height="680" fill="#f7fbfb"/><text x="60" y="66" font-size="31">{escape(title)}</text>{body}<text x="60" y="648" class="small">ICLH · School of Life Sciences · SUSTech</text></svg>'''

llps='''<text x="60" y="111" class="small">Design principles for condensates across changing conditions</text>
<g class="label" text-anchor="middle"><rect x="60" y="155" width="320" height="84" rx="8" fill="#e1f2f2"/><text x="220" y="205">Cell type</text><rect x="440" y="155" width="320" height="84" rx="8" fill="#e1f2f2"/><text x="600" y="205">Expression variation</text><rect x="820" y="155" width="320" height="84" rx="8" fill="#e1f2f2"/><text x="980" y="205">Environmental perturbation</text></g>
<path d="M220 239V280H600V310M600 239V310M980 239V280H600" class="flow"/>
<rect x="180" y="316" width="840" height="100" rx="10" fill="#18bfc5"/><text x="600" y="358" text-anchor="middle" font-size="29" class="white">Robust scaffold protein combinations</text><text x="600" y="389" text-anchor="middle" font-size="22" class="white">Liquid–liquid phase separation (LLPS)</text>
<path d="M600 416V462" class="flow"/><text x="600" y="498" text-anchor="middle" class="label">Potential applications</text>
<text x="600" y="542" text-anchor="middle" class="small">Membraneless organelles · Pathway compartmentalization · Signaling regulation</text><text x="600" y="577" text-anchor="middle" class="small">Cell factories · Therapeutic cell engineering</text>'''
(assets/'llps-en.svg').write_text(document('LLPS Scaffold Protein Design and Optimization',llps),encoding='utf-8')

rna='''<text x="60" y="111" class="small">Connecting computational design with experimental research</text>
<rect x="60" y="155" width="1080" height="75" rx="8" fill="#18bfc5"/><text x="600" y="202" text-anchor="middle" font-size="27" class="white">AI models for RNA sequence optimization, screening and delivery design</text>
<g text-anchor="middle"><rect x="60" y="295" width="235" height="155" rx="8" fill="#e1f2f2"/><text x="177" y="337" font-size="20" fill="#18bfc5">01</text><text x="177" y="378" class="label">Target</text><text x="177" y="411" class="label">discovery</text>
<rect x="342" y="295" width="235" height="155" rx="8" fill="#e1f2f2"/><text x="459" y="337" font-size="20">02</text><text x="459" y="378" class="label">RNA molecular</text><text x="459" y="411" class="label">design</text>
<rect x="624" y="295" width="235" height="155" rx="8" fill="#e1f2f2"/><text x="741" y="337" font-size="20">03</text><text x="741" y="378" class="label">LNP delivery</text><text x="741" y="411" class="label">optimization</text>
<rect x="906" y="295" width="235" height="155" rx="8" fill="#e1f2f2"/><text x="1023" y="337" font-size="20">04</text><text x="1023" y="378" class="label">Preclinical</text><text x="1023" y="411" class="label">validation</text></g>
<path d="M295 372H333M577 372H615M859 372H897" class="flow"/>
<text x="60" y="521" class="small">LNP: lipid nanoparticle</text><text x="60" y="559" class="small">Research teams led by Professors Wei Chen and Zefeng Wang</text>'''
(assets/'rna-en.svg').write_text(document('AI-Driven RNA Drug Discovery',rna),encoding='utf-8')
print('English research diagrams generated.')
