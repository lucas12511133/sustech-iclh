from html.parser import HTMLParser
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import re

T = {
 '生命科学与大健康创新中心 · 南方科技大学生命科学学院':'Innovative Center for Life Science and Health · SUSTech',
 '依托南方科技大学生命科学学院，推动前沿研究、产学研协同与复合型人才培养。':'A center at SUSTech School of Life Sciences connecting frontier research, industry partnerships and interdisciplinary talent development.',
 '跳至正文':'Skip to content', '南方科技大学生命科学学院':'SUSTech School of Life Sciences', '南方科技大学':'SUSTech',
 '联系我们':'Contact us', '学院导航':'School navigation', '关于我们':'About', '院系导航':'Departments', '师资队伍':'Faculty', '教育教学':'Education', '科学研究':'Research', '新闻动态':'News',
 '展开学院导航':'Open school navigation', '收起学院导航':'Close school navigation', '首页':'Home', '科学研究 · 科研创新平台':'Research · Research Platforms',
 '生命科学与大健康创新中心':'Innovative Center for Life Science and Health', '生命科学与大健康':'Innovative Center for', '创新中心':'Life Science and Health',
 '以生命科学之基，筑大健康之未来':'Advancing life science. Building a healthier future.', '了解中心':'Explore the center', '南方科技大学校园实景':'SUSTech campus',
 '页内导航':'On this page', '中心概况':'Overview', '核心团队':'Leadership', '中心职能':'Our Work', '建设进展':'Partnerships', '重点项目':'Projects', '联系合作':'Contact',
 '立足生命科学':'Rooted in life science', '连接研究与应用':'Connecting research with application',
 '以学科交叉为基础，以真实需求为牵引，':'Bringing disciplines together to address real needs.',
 '推动生命科学创新走向大健康应用。':'Turning life science innovation into applications for health.',
 '生命科学与大健康创新中心（ICLH）依托南方科技大学生命科学学院，结合结构生物学、神经科学、合成生物学等前沿学科优势，建设集技术转化、学术传播与复合型人才培养于一体的平台。':'Based in the School of Life Sciences at Southern University of Science and Technology, the Innovative Center for Life Science and Health (ICLH) draws on strengths in structural biology, neuroscience and synthetic biology. It brings technology translation, academic exchange and interdisciplinary education together in one platform.',
 '面向粤港澳大湾区科技创新与深圳生物医药、健康产业发展需求，中心推动高校研究与产业实践相互连接，构建协同的“产学研用”创新生态。':'Responding to innovation priorities in the Guangdong–Hong Kong–Macao Greater Bay Area and the needs of Shenzhen’s biomedical and health industries, the center connects university research with industry practice across research, education and application.',
 '了解中心职能':'Explore our work', '让前沿探索':'Turning discovery', '回应生命健康需求':'into health solutions',
 '促进科研成果转化':'Advance research translation', '拓展跨学科合作':'Expand interdisciplinary collaboration', '培养复合型创新人才':'Develop interdisciplinary innovators',
 '访问张明杰教授主页（新标签页）':'Visit Mingjie Zhang’s profile (opens in a new tab)', '张明杰院士':'Professor Mingjie Zhang', '创新中心主任':'Director', '张明杰':'Mingjie Zhang',
 '讲席教授 · 中国科学院院士':'Chair Professor · Member of the Chinese Academy of Sciences', '研究方向':'Research interests', '分子生物学与生物化学':'Molecular biology and biochemistry', '结构生物学 · 神经生物学':'Structural biology · Neurobiology',
 '访问王宇教授主页（新标签页）':'Visit Rowan Wang’s profile (opens in a new tab)', '王宇教授':'Professor Rowan Wang', '创新中心副主任':'Deputy Director', '王宇':'Rowan Wang',
 '教授 · 商学院、生命科学学院双聘':'Professor · Joint appointment in the Business School and School of Life Sciences', '数学建模 · 数据分析':'Mathematical modeling · Data analysis', '随机过程 · 系统优化':'Stochastic processes · Systems optimization',
 '构建产学研用协同体系':'Connecting research, education and industry', '四项中心职能':'Four areas of work',
 '前沿转化研究':'Translational Research', '前沿转化':'Translational', '研究':'Research', '产学研协同枢纽':'Industry–University Partnerships', '产学研':'Industry', '协同枢纽':'Partnerships',
 '复合型人才培养':'Interdisciplinary Talent Development', '复合型':'Talent', '人才培养':'Development', '跨学科科研合作':'Interdisciplinary Research Collaboration', '跨学科':'Interdisciplinary', '科研合作':'Collaboration',
 '产学研用':'Science to impact', '协同创新':'Working together', '点击环形板块，了解中心职能':'Select a segment to explore our work',
 '科学发现与应用探索':'Scientific discovery and translation',
 '聚焦结构生物学、合成生物学、细胞治疗、神经科学与生物医学工程，支持具有明确转化潜力的早期研究。':'We support early-stage research with clear translational potential in structural biology, synthetic biology, cell therapy, neuroscience and biomedical engineering.',
 '产学研用 · 协同创新':'Research, education and industry working together',
 '产业需求与科研能力对接':'Matching industry needs with research expertise',
 '挖掘企业技术需求，匹配学院科研成果，推动校企联合实验室、横向课题与技术评估孵化。':'We identify industry challenges and connect them with research from the school, supporting joint laboratories, industry-sponsored projects, technology assessment and incubation.',
 '课堂学习与真实实践结合':'Connecting learning with real-world practice',
 '通过创新创业课程、企业实践与横向课题，让学生理解行业问题，参与研发过程，探索成果创业。':'Entrepreneurship courses, industry placements and sponsored research help students understand practical challenges, contribute to R&D and explore research-based ventures.',
 '不同学科共同解决问题':'Different disciplines, shared research questions',
 '围绕“生命科学＋X”组织联合攻关，以种子项目和联合课题支持交叉方向的探索性研究。':'Through “Life Sciences + X” collaborations, we bring researchers together across disciplines and support exploratory work through seed projects and joint research.',
 '上一项中心职能':'Previous area of work', '下一项中心职能':'Next area of work',
 '在合作与实践中推进创新':'Advancing innovation through partnership', '战略合作':'Strategic partnerships',
 '连接临床资源与工程技术，拓展生命健康应用场景。':'Connecting clinical resources with engineering expertise to explore new health applications.',
 '重庆小米熊儿童医院合作现场':'Partnership event with Chongqing Xiaomixiong Children’s Hospital', '儿童健康 · 临床协同':'Child health · Clinical collaboration',
 '重庆小米熊儿童医院有限公司':'Chongqing Xiaomixiong Children’s Hospital Co., Ltd.',
 '合作面向儿童全生命周期健康。未来拟整合高校科研优势与企业临床资源，围绕儿童脑发育、脑疾病干预与认知健康开展联合研究。':'This partnership focuses on health throughout childhood. Planned collaboration will combine university research expertise with clinical resources to study brain development, interventions for brain disorders and cognitive health in children.',
 '深圳市荣益电子科技有限公司合作现场':'Partnership event with Shenzhen Rongyi Electronic Technology', '医工交叉 · 健康应急':'Medical engineering · Emergency response',
 '深圳市荣益电子科技有限公司':'Shenzhen Rongyi Electronic Technology Co., Ltd.',
 '结合低空监测、远距离巡检、应急投送与智能数据采集技术，探索公共卫生应急、户外健康救援及区域人群健康监测等合作场景。':'The collaboration explores public health emergency response, outdoor rescue and population health monitoring, drawing on low-altitude monitoring, remote inspection, emergency delivery and intelligent data collection.',
 '把真实行业问题':'Bringing real industry challenges', '带进课堂':'into the classroom',
 '创新创业课程围绕真实案例展开，邀请行业实践者分享经验，帮助学生理解技术、资源、约束与决策。':'Our innovation and entrepreneurship courses use real cases and insights from industry practitioners to help students understand technology, resources, constraints and decision-making.',
 '从行业判断，到个人成长。':'Developing industry judgment and personal direction.',
 '行业实践者分享真实案例':'An industry practitioner discussing a real case', '真实案例':'Real cases', '课堂中的行业与技术讨论':'Classroom discussion of industry and technology', '行业视野':'Industry perspectives', '创新创业课程交流':'Discussion in an entrepreneurship course', '职业启发':'Career insights',
 '跨越学科边界':'Across disciplines', '探索健康新可能':'Exploring new possibilities for health', '睿鹰急救天眼项目指挥平台场景':'Command platform for the Ruiying Emergency Eye project',
 '01 / 应急救援':'01 / Emergency response', '生命科学 × 智慧应急':'Life sciences × Intelligent emergency response', '睿鹰急救天眼':'Ruiying Emergency Eye',
 '构建人、机、车空地协同急救网络，面向心脏骤停等紧急场景，探索提升院前急救响应能力。':'The project brings people, aerial systems and ground vehicles together in a coordinated emergency response network, exploring ways to improve prehospital care for cardiac arrest and other emergencies.',
 '围绕“黄金四分钟”的救援需求，补齐复杂场景下的急救短板，为公共应急体系提供技术支撑。':'It addresses the critical first four minutes of cardiac arrest response and seeks to close gaps in complex rescue settings, providing technical support for public emergency services.',
 '了解项目方向':'Explore the research', '以空地协同网络连接现场响应与应急指挥，推动技术研发与实际救援场景结合。':'An integrated air–ground network connects on-site response with emergency command, linking technology development to practical rescue needs.',
 'LLPS 支架蛋白组合设计项目示意':'Overview of the LLPS scaffold protein design project', '02 / 合成生物学':'02 / Synthetic biology',
 'LLPS 支架蛋白组合设计与优化':'LLPS Scaffold Protein Design and Optimization', '放大 LLPS 项目示意图':'Enlarge the LLPS project diagram', '查看大图':'View diagram', '生命科学 × 计算设计':'Life sciences × Computational design',
 '面向环境鲁棒性的':'Environmentally Robust', '高效 LLPS 支架蛋白':'LLPS Scaffold Protein', '组合设计与优化':'Design and Optimization',
 '探索对细胞类型、表达波动和环境扰动不敏感的凝聚体设计原则。':'The project explores principles for designing condensates that remain robust across cell types, variations in expression and environmental perturbations.',
 '面向人工无膜细胞器、反应通路分区、信号调控、细胞工厂与治疗性细胞工程等应用方向。':'Potential applications include artificial membraneless organelles, pathway compartmentalization, signaling regulation, cell factories and therapeutic cell engineering.',
 'LLPS 即液–液相分离。项目关注支架蛋白组合在不同环境中的稳定表现，探索更具适应性的设计方法。':'LLPS stands for liquid–liquid phase separation. The research studies how scaffold protein combinations perform across environments and explores more adaptable design strategies.',
 'AI 驱动 RNA 药物研发平台流程示意':'Workflow for AI-driven RNA drug discovery', '03 / 创新药物':'03 / Drug discovery', 'AI 驱动的 RNA 药物研发':'AI-Driven RNA Drug Discovery', '放大 RNA 药物研发示意图':'Enlarge the RNA drug discovery diagram',
 '生命科学 × 人工智能':'Life sciences × Artificial intelligence', 'AI 驱动的':'AI-Driven', 'RNA 药物研发':'RNA Drug Discovery',
 '南方科技大学生命科学学院陈炜教授、王泽峰教授科研团队，探索 AI 驱动的 RNA 创新药物研发平台。':'Research teams led by Professors Wei Chen and Zefeng Wang at SUSTech School of Life Sciences are exploring an AI-driven platform for RNA drug discovery.',
 '运用人工智能大模型开展 RNA 序列优化、分子筛选与递送系统设计，连接靶点挖掘、分子设计、LNP 递送优化与临床前验证。':'The platform uses large AI models for RNA sequence optimization, molecular screening and delivery system design, linking target discovery, molecular design, lipid nanoparticle (LNP) delivery optimization and preclinical validation.',
 '围绕 RNA 药物研发链路，结合计算方法与实验研究，探索提高分子设计和递送优化效率。':'Combining computational approaches with experimental research, the project explores ways to improve molecular design and delivery optimization throughout the RNA drug discovery process.',
 '共探生命科学':'Shaping the future', '与大健康的未来':'of life science and health',
 '欢迎围绕产业需求、学术研究与成果转化开展交流。':'We welcome discussions on industry needs, academic research and research translation.',
 '产业合作':'Industry partnerships', '学术合作':'Academic collaboration', '资本合作':'Investment partnerships', '联系与合作':'Contact and collaboration', '学院官方联系入口':'School of Life Sciences contact',
 '深圳市南山区学苑大道 1088 号':'1088 Xueyuan Avenue, Nanshan District, Shenzhen', '南方科技大学生物楼':'Biology Building, SUSTech', '前往学院联系页面':'Visit the school contact page',
 '南方科技大学 · 生命科学学院':'SUSTech · School of Life Sciences', '学院首页':'School homepage', '科研创新平台':'Research platforms', '返回顶部':'Back to top', '关闭大图':'Close enlarged diagram',
}

T.update({'前往学院联系页面 ↗':'Visit the school contact page ↗','学院首页 ↗':'School homepage ↗','查看大图 ↗':'View diagram ↗','科研创新平台 ↗':'Research platforms ↗','返回顶部 ↑':'Back to top ↑'})
root=Path(__file__).parent/'dist'
zh=(root/'index.html').read_text(encoding='utf-8-sig')
zh=zh.replace('href="https://bio.sustech.edu.cn/index/languages/lang/en.html" lang="en">EN ↗</a>', 'href="en.html" lang="en" hreflang="en" data-language-switch>EN</a>')
zh=zh.replace('script.js?v=cycle1','script.js?v=bilingual1')
if 'name="language-redirect"' not in zh:
    zh=zh.replace('</head>', '<link rel="alternate" hreflang="en" href="en.html"><script name="language-redirect">if(/^en(?:-|$)/i.test(new URLSearchParams(location.search).get("lang")||"")){location.replace("en.html"+location.hash)}</script></head>')
(root/'index.html').write_text(zh,encoding='utf-8')

class Translate(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=False); self.out=[]; self.in_script=False; self.missing=set()
    def translate(self,s):
        if not re.search(r'[\u4e00-\u9fff]',s): return s
        key=s.strip(); result=T.get(key)
        if result is None: self.missing.add(key); return s
        return s[:len(s)-len(s.lstrip())]+result+s[len(s.rstrip()):]
    def handle_decl(self,s): self.out.append('<!'+s+'>')
    def handle_starttag(self,tag,attrs):
        if tag=='script': self.in_script=True
        output=[]
        for k,v in attrs:
            if tag=='html' and k=='lang': v='en'
            elif v is not None:
                v=self.translate(v)
                if k=='href':
                    if v=='en.html': v='index.html'
                    elif v.startswith('https://bio.sustech.edu.cn/'):
                        u=urlsplit(v); q=dict(parse_qsl(u.query)); q['lang']='en-us'; v=urlunsplit((u.scheme,u.netloc,u.path,urlencode(q),u.fragment))
                    elif v=='https://www.sustech.edu.cn/': v='https://www.sustech.edu.cn/en/'
                    elif 'www.sustech.edu.cn/zh/faculties/rowan-wang.html' in v: v=v.replace('/zh/','/en/')
                if k=='src' or k=='data-image':
                    v=v.replace('assets/image12.png','assets/llps-en.svg').replace('assets/image13.png','assets/rna-en.svg')
                if 'data-language-switch' in dict(attrs) and k in ('lang','hreflang'): v='zh-CN'
                if tag=='link' and dict(attrs).get('rel')=='alternate' and k=='hreflang': v='zh-CN'
            output.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
        self.out.append('<'+tag+(' '+' '.join(output) if output else '')+'>')
        if tag=='head': pass
    def handle_endtag(self,tag):
        if tag=='script': self.in_script=False
        if tag=='head': self.out.append('<link rel="stylesheet" href="english.css?v=1">')
        self.out.append('</'+tag+'>')
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs); self.out[-1]=self.out[-1][:-1]+'/>'
    def handle_data(self,s):
        if self.in_script: return  # The language redirect belongs only to the Chinese entry.
        s=self.translate(s)
        self.out.append(escape(s))
    def handle_entityref(self,s): self.out.append('&'+s+';')
    def handle_charref(self,s): self.out.append('&#'+s+';')
    def handle_comment(self,s): self.out.append('<!--'+s+'-->')

p=Translate(); p.feed(zh)
if p.missing: raise SystemExit('Missing translations: '+repr(sorted(p.missing)))
en=''.join(p.out).replace('data-language-switch>EN</a>','data-language-switch>中文</a>')
en=en.replace('<h1 id="hero-title">Innovative Center for<br>Life Science and Health</h1>','<h1 id="hero-title">Innovative Center for<br>Life Science and Health</h1>')
en=en.replace('<p class="hero-en" lang="en">Innovative Center for Life Science and Health</p>','<p class="hero-en" lang="en">School of Life Sciences · SUSTech</p>')
en=en.replace('x="367"','x="350"').replace('x="133"','x="150"')
en=re.sub(r'<script name="language-redirect"></script>','',en)
en=en.replace('<link rel="stylesheet" href="hero.css">','').replace('</head>','<link rel="stylesheet" href="hero.css"></head>')
(root/'en.html').write_text(en,encoding='utf-8')
print('English page generated; all Chinese text nodes and attributes translated.')
