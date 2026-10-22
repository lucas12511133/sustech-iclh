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
# Faithful translations of the supplied poster text.
T.update({
  "使命与愿景": "Mission and Vision",
  "随着粤港澳大湾区国际科技创新中心建设加速，生命科学领域正迎来产学研深度融合的历史性机遇。": "As the Guangdong–Hong Kong–Macao Greater Bay Area accelerates the development of an international science and technology innovation center, life sciences face a historic opportunity for deeper integration of industry, universities and research.",
  "南方科技大学生命科学学院在张明杰院长领导下，已形成结构生物学、神经科学、合成生物学等前沿学科优势。": "Under the leadership of Dean Mingjie Zhang, the School of Life Sciences at Southern University of Science and Technology has established strengths in frontier disciplines including structural biology, neuroscience and synthetic biology.",
  "为响应国家“创新驱动发展”战略，对接深圳市“20+8”产业集群规划（生物医药与健康产业集群），打造集技术转化、学术传播与复合型人才培养于一体的枢纽平台，实现打破传统学术与产业壁垒，构建高效协同的“产学研用”一体化创新生态，显著提升南方科技大学生命科学院在生命健康、生物医药等前沿领域的科技创新策源力、产业影响力及复合型人才培养水平。": "In response to the national innovation-driven development strategy and Shenzhen’s “20+8” industrial cluster plan for biomedicine and health, the center builds a hub integrating technology translation, academic exchange and interdisciplinary talent development. It breaks down traditional barriers between academia and industry and creates an efficient, coordinated innovation ecosystem connecting industry, universities, research and application, significantly strengthening the school’s capacity to generate scientific and technological innovation, its industrial influence and its development of interdisciplinary talent in life, health, biomedicine and other frontier fields.",
  "构建高效协同的": "Building an efficient, coordinated",
  "“产学研用”一体化创新生态": "innovation ecosystem connecting industry, universities, research and application",
  "技术转化": "Technology translation",
  "学术传播": "Academic exchange",
  "复合型人才培养": "Interdisciplinary talent development",
  "构建产学研闭环": "Closing the loop between industry, universities and research",
  "聚焦五大方向": "Five research directions",
  "聚焦结构生物学、合成生物学、细胞治疗、神经科学、生物医学工程五大方向；设“种子基金”支持具有明确转化潜力的早期研究。": "The five focus areas are structural biology, synthetic biology, cell therapy, neuroscience and biomedical engineering. A seed fund supports early-stage research with clear translational potential.",
  "需求挖掘与匹配": "Identifying and matching needs",
  "需求挖掘与匹配：深入企业调研，精准识别技术痛点；梳理学院科研成果，主动向企业推送。联合攻关平台：组织校企联合实验室、横向课题技术评估与孵化。": "Identifying and matching needs: conduct in-depth company research to pinpoint technical challenges, review the school’s research outputs and actively introduce them to companies. Joint research platforms: organize university–industry laboratories, technology assessment and incubation for industry-sponsored projects.",
  "课程与项目": "Courses and projects",
  "复合型人才培养基地": "Interdisciplinary Talent Development Base",
  "课程与项目：开设创新创业课程，与成功企业家面对面交流；实习与实践：建立企业实习基地网络；学生深度参与中心横向课题研发全过程；创业辅导、种子资金、孵化空间，支持师生基于中心成果创业。": "Courses and projects: offer innovation and entrepreneurship courses and face-to-face exchanges with successful entrepreneurs. Internships and practice: establish a network of company internship bases and involve students deeply in the full R&D process of the center’s industry-sponsored projects. Entrepreneurship guidance, seed funding and incubation space support faculty and students in launching ventures based on the center’s research outputs.",
  "“生命科学 + X”联合攻关": "“Life Sciences + X” joint research",
  "多领域跨学科科研合作": "Interdisciplinary Research Across Multiple Fields",
  "打破学院内学科壁垒，组建“生命科学 + X”联合攻关团队。以种子项目 / 联合课题形式，支持交叉方向的探索性研究。实现多领域跨学科的科研合作。": "Break down disciplinary barriers within the school and form “Life Sciences + X” joint research teams. Support exploratory interdisciplinary research through seed projects and joint projects, enabling research collaboration across multiple fields.",
  "成果转化": "Research Translation",
  "战略资金引进": "Strategic Funding",
  "已为学院引进战略资金合作": "Strategic funding partnerships have been secured for the school",
  "儿童全生命周期健康服务": "Health services throughout childhood",
  "深耕儿童垂直大健康领域，聚焦0-18岁儿童全生命周期健康服务，是西南地区极具特色的儿童大健康医疗服务机构。": "Specializing in children’s health, the company focuses on full-lifecycle health services for children aged 0–18 and is a distinctive pediatric healthcare provider in Southwest China.",
  "医工交叉深度合作": "In-depth medical–engineering collaboration",
  "专注低空安防领域的研发、生产、销售工作。未来，企业将与大健康创新中心开展医工交叉深度合作，发挥无人机低空监测等技术优势，赋能各大健康应用场景。": "The company specializes in R&D, production and sales in low-altitude security. It will undertake in-depth medical–engineering collaboration with the health innovation center, drawing on drone-based low-altitude monitoring and other technical strengths to enable a range of health applications.",
  "创新创业课程": "Innovation and Entrepreneurship Courses",
  "真正的收获，不是聆听一段光鲜的成功故事，而是穿透故事表象，看见事件背后的权衡取舍。": "The real benefit comes not from hearing a glamorous success story, but from looking beyond the narrative to understand the trade-offs behind events.",
  "从行业判断落地到个人成长，依托真实案例，理解资源、约束、风险与选择。": "Translate industry judgment into personal growth, using real cases to understand resources, constraints, risks and choices.",
  "国际视野": "International Perspectives",
  "学会用更系统的方式理解行业、技术、人，以及每一次决策。": "Learn to understand industry, technology, people and every decision more systematically.",
  "这套分析思维可以迁移复用，面对复杂问题，独立判断，支撑长期成长。": "This analytical way of thinking can be transferred and reused to make independent judgments on complex problems and support long-term growth.",
  "跨学科合作项目": "Interdisciplinary Collaborative Projects",
  "构建人机车空地协同急救网络，抢抓心脏骤停黄金四分钟，": "Build a coordinated air–ground emergency response network connecting people, aircraft and vehicles, making the most of the critical first four minutes after cardiac arrest,",
  "补齐复杂场景院前急救短板，赋能公共应急体系，用科技守护群众生命安全。": "close gaps in prehospital emergency care in complex settings, strengthen public emergency services and use technology to protect lives.",
  "建立对细胞类型、表达波动和环境扰动不敏感的凝聚体设计原则，": "Establish design principles for condensates that are insensitive to cell type, expression fluctuations and environmental perturbations,",
  "服务于人工无膜细胞器、反应通路分区、信号调控、细胞工厂与治疗性细胞工程。": "serving artificial membraneless organelles, reaction pathway compartmentalization, signaling regulation, cell factories and therapeutic cell engineering.",
  "该项目系南方科技大学生命科学学院的陈炜教授、王泽峰教授科研团队研发，打造 AI 驱动的 RNA 创新药物研发平台，": "Developed by the research teams of Professors Wei Chen and Zefeng Wang at SUSTech School of Life Sciences, this project creates an AI-driven platform for innovative RNA drug discovery,",
  "项目运用人工智能大模型完成 RNA 序列优化、分子筛选与递送系统设计，打通靶点挖掘、分子设计、LNP 递送优化到临床前验证的研发链路。": "using large AI models to perform RNA sequence optimization, molecular screening and delivery system design, and connecting the R&D pipeline from target discovery and molecular design through LNP delivery optimization to preclinical validation.",
  "构建人机车空地协同急救网络，抢抓心脏骤停黄金四分钟，补齐复杂场景院前急救短板，赋能公共应急体系，用科技守护群众生命安全。": "Build a coordinated air–ground emergency response network connecting people, aircraft and vehicles; make the most of the critical first four minutes after cardiac arrest; close gaps in prehospital emergency care in complex settings; strengthen public emergency services; and use technology to protect lives.",
  "建立对细胞类型、表达波动和环境扰动不敏感的凝聚体设计原则，服务于人工无膜细胞器、反应通路分区、信号调控、细胞工厂与治疗性细胞工程。": "Establish design principles for condensates that are insensitive to cell type, expression fluctuations and environmental perturbations, serving artificial membraneless organelles, reaction pathway compartmentalization, signaling regulation, cell factories and therapeutic cell engineering.",
  "该项目系南方科技大学生命科学学院的陈炜教授、王泽峰教授科研团队研发，打造 AI 驱动的 RNA 创新药物研发平台，项目运用人工智能大模型完成 RNA 序列优化、分子筛选与递送系统设计，打通靶点挖掘、分子设计、LNP 递送优化到临床前验证的研发链路。": "Developed by the research teams of Professors Wei Chen and Zefeng Wang at SUSTech School of Life Sciences, this project creates an AI-driven platform for innovative RNA drug discovery. It uses large AI models to perform RNA sequence optimization, molecular screening and delivery system design, connecting the R&D pipeline from target discovery and molecular design through LNP delivery optimization to preclinical validation.",
  "查看完整原文": "Read the full description",
  "合作入口": "Collaboration",
  "课程筑基 · 项目落地 · 战略合作": "Courses as a foundation · Project implementation · Strategic partnerships"
})
T.update({"复合型人才": "Interdisciplinary Talent", "培养基地": "Development Base", "多领域跨学科": "Across Disciplines"})
T.update({
  "构建人机车空地协同急救网络，抢抓心脏骤停黄金四分钟。": "Build a coordinated air–ground emergency response network connecting people, aircraft and vehicles, making the most of the critical first four minutes after cardiac arrest.",
  "补齐复杂场景院前急救短板，赋能公共应急体系，用科技守护群众生命安全。": "Close gaps in prehospital emergency care in complex settings, strengthen public emergency services and use technology to protect lives.",
  "建立对细胞类型、表达波动和环境扰动不敏感的凝聚体设计原则。": "Establish design principles for condensates that are insensitive to cell type, expression fluctuations and environmental perturbations.",
  "服务于人工无膜细胞器、反应通路分区、信号调控、细胞工厂与治疗性细胞工程。": "Serve artificial membraneless organelles, reaction pathway compartmentalization, signaling regulation, cell factories and therapeutic cell engineering.",
  "该项目系南方科技大学生命科学学院的陈炜教授、王泽峰教授科研团队研发，打造 AI 驱动的 RNA 创新药物研发平台。": "Developed by the research teams of Professors Wei Chen and Zefeng Wang at SUSTech School of Life Sciences, this project creates an AI-driven platform for innovative RNA drug discovery.",
  "项目运用人工智能大模型完成 RNA 序列优化、分子筛选与递送系统设计，打通靶点挖掘、分子设计、LNP 递送优化到临床前验证的研发链路。": "The project uses large AI models to perform RNA sequence optimization, molecular screening and delivery system design, connecting the R&D pipeline from target discovery and molecular design through LNP delivery optimization to preclinical validation.",
  "项目介绍": "Project description"
})
T.update({
  "核心成员": "Core Members",
  "讲席教授、中国科学院院士": "Chair Professor, Member of the Chinese Academy of Sciences",
  "教授（商学院、生命科学学院双聘）": "Professor (joint appointment in the Business School and School of Life Sciences)",
  "结构生物学、神经生物学": "Structural biology, neurobiology",
  "数学建模、数据分析": "Mathematical modeling, data analysis",
  "随机过程、系统优化": "Stochastic processes, systems optimization",
  "人机车空地协同急救网络": "Coordinated air–ground emergency response network",
  "五大方向": "Five research directions",
  "企业·转化": "Enterprise · Translation",
  "跨学科·联合攻关": "Interdisciplinary · Joint research",
  "投资·孵化": "Investment · Incubation"
})
T.update({'高效 LLPS 支架蛋白':'Efficient LLPS Scaffold Protein'})
T.update({
  "个人简介": "Biography",
  "讲席教授，生命科学学院院长，中国科学院院士，香港科学院创院院士。": "Chair Professor; Dean of the School of Life Sciences; Member of the Chinese Academy of Sciences; Founding Member of the Hong Kong Academy of Sciences.",
  "2003年获香港裘槎基金会优秀学者奖；2006年获国家自然科学奖二等奖；2011年获何梁何利基金科学与技术奖，同年当选为中国科学院院士；2015年当选为香港科学院创院院士；2021年获谈家桢生命科学成就奖。": "He received the Outstanding Scholar Award from the Croucher Foundation in Hong Kong in 2003 and the Second Prize of the State Natural Science Award in 2006. In 2011, he received the Ho Leung Ho Lee Foundation Prize for Science and Technology and was elected to the Chinese Academy of Sciences. He became a Founding Member of the Hong Kong Academy of Sciences in 2015 and received the Tan Jiazhen Life Science Achievement Award in 2021.",
  "从事运营管理相关研究，已在商科国际顶级UTD期刊上发表论文10篇，现任Production and Operations Management的Senior Editor以及Decision Sciences的Associate Editor，荣获浙江省科学技术进步奖三等奖，所著决策咨询专报于国务院办公厅录用、政策研究报告获浙江省委书记批示。": "His research focuses on operations management. He has published 10 papers in leading international business journals on the UTD list. He currently serves as Senior Editor of Production and Operations Management and Associate Editor of Decision Sciences. He received the Third Prize of the Zhejiang Provincial Science and Technology Progress Award. His decision-making advisory report was accepted by the General Office of the State Council, and his policy research report received written comments from the Secretary of the CPC Zhejiang Provincial Committee.",
  "入选国家级海外高层次人才引进计划青年特聘专家、广东省珠江人才计划青年拔尖人才、深圳市鹏城孔雀计划特聘教授等。": "He has been selected as a young distinguished expert under the national overseas high-level talent recruitment program, a leading young talent under Guangdong’s Pearl River Talent Program, and a distinguished professor under Shenzhen’s Pengcheng Peacock Program, among other honors."
})
T.update({'项目合作':'Project Partnerships'})
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
# Preserve ring label positions so the center does not cover English text.
en=re.sub(r'<script name="language-redirect"></script>','',en)
en=en.replace('<link rel="stylesheet" href="hero.css">','').replace('</head>','<link rel="stylesheet" href="hero.css"></head>')
(root/'en.html').write_text(en,encoding='utf-8')
print('English page generated; all Chinese text nodes and attributes translated.')
