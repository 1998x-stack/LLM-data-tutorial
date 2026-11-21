# LLM Data Tutorial · 大语言模型预训练数据工程

> 从原始网页到可训练语料：面向研究生、数据工程师与 LLM 研究实践者的开放式课程知识库。

本项目围绕 **数据来源 → 正文抽取 → 规范化与过滤 → 去重 → 质量评估 → 数据混合 → Tokenization → 可复现训练数据** 建立系统化学习路径。课程不把“数据清洗”简化为若干 if-else，而是强调数据契约、来源追踪、论文证据、误差分析和受控实验。

## 当前版本

- 28 个课程模块，保留原有 01.html–28.html 章节入口。
- 首页支持全文搜索、知识分类筛选与标签筛选。
- 首批深度重构：01–05，采用渐进式叙事、原创 SVG、交互练习、MathML 公式和论文引用。
- 每篇重构文章维护独立 evidence/NN.json 证据清单。
- courses.json 是唯一课程元数据源；courses-data.js 是离线首页使用的生成文件。
- 纯静态站点，直接打开 index.html 即可浏览，无需构建服务或第三方 CDN。

## 快速开始

    git clone https://github.com/1998x-stack/LLM-data-tutorial.git
    cd LLM-data-tutorial
    open index.html              # macOS
    # 或直接用浏览器打开 index.html

如果希望通过本地 HTTP 服务检查相对路径：

    python3 -m http.server 8000
    # 浏览器访问 http://localhost:8000

## 知识架构

| 分类 | 模块 | 主要问题 |
|---|---:|---|
| 基础与全景 | 01 | 训练语料工程的系统边界、数据契约与研究锚点 |
| 数据采集与提取 | 02–03 | Common Crawl 归档定位、WARC/WAT/WET、正文抽取 |
| 规范化与过滤 | 04–06 | 语言识别、URL 策略、启发式过滤 |
| 去重与相似性 | 07–09 | 精确去重、MinHash、LSH、多粒度重复 |
| 质量、安全与评估 | 10–13、18 | 困惑度、教育质量、LLM 标注、去污染、质量评估 |
| 数据组成与表示 | 14、19–20、22 | 数据混合、Tokenization、词表、领域数据 |
| 系统与工具链 | 15–17、23–24 | 分布式处理、存储、可复现性、DataTrove、Dolma |
| 前沿与自动化 | 21、25–27 | 合成数据、数据范式、自动化编排、在线选择 |
| 综合实战 | 28 | 从原始数据到可复现训练语料的端到端工程 |

完整标签体系见 docs/taxonomy.md。

## 章节目录

| # | 模块 | 核心主题 |
|---|---|---|
| 01 | LLM 数据工程全景 | 数据生产链路、数据契约、里程碑论文与消融方法 |
| 02 | Common Crawl 数据采集 | WARC/WAT/WET、URL Index、Range 请求、warcio |
| 03 | 网页正文提取 | DOM、boilerplate removal、Trafilatura、精确率与召回率 |
| 04 | 语言识别与过滤 | fastText、阈值校准、多语言路由 |
| 05 | 启发式规则过滤 | C4、FineWeb、规则消融与误杀分析 |
| 06 | URL 与域名过滤 | blocklist、域名统计、来源策略 |
| 07 | 精确去重 | 哈希、Bloom Filter、文档与段落粒度 |
| 08 | MinHash 近邻去重 | Jaccard、签名、LSH |
| 09 | 多粒度去重策略 | 行级、段落级、文档级与跨快照去重 |
| 10 | 困惑度质量过滤 | n-gram LM、CCNet、困惑度边界 |
| 11 | 教育质量分类器 | FineWeb-Edu、合成标注、分类器 |
| 12 | LLM 辅助数据标注 | 评分协议、蒸馏、偏差审计 |
| 13 | 评测集去污染 | n-gram、MinHash、污染检测 |
| 14 | 多源数据混合配比 | 来源权重、采样与 token 分布 |
| 15 | 分布式数据处理架构 | Spark、Ray、分区与容错 |
| 16 | 大规模数据存储 | Parquet、Arrow、压缩与冷热分层 |
| 17 | 流水线可复现性 | 数据版本、配置哈希、血缘与审计 |
| 18 | 数据质量评估体系 | 质量指标、人工抽检、下游消融 |
| 19 | Tokenization 与 BPE | Byte-level BPE、分词与 token 预算 |
| 20 | 词表设计与优化 | 词表规模、覆盖率、推理成本 |
| 21 | 合成数据生成 | Self-Play、数据增强、模型坍缩 |
| 22 | 领域适配数据策略 | 代码、科学、医学与多语言 |
| 23 | DataTrove 流水线实战 | 模块化数据处理与可复现配置 |
| 24 | Dolma 工具链全解析 | 开放语料、数据整理与工具链 |
| 25 | 数据清洗范式比较 | 规则、模型、混合与数据选择 |
| 26 | 自动化数据准备系统 | Agent 编排、质量反馈与治理 |
| 27 | 在线数据选择与动态配比 | 课程学习、在线采样与动态调度 |
| 28 | 端到端综合实战 | 数据契约、流水线、验收与排障 |

## 仓库结构

    LLM-data-tutorial/
    ├── AGENTS.md                 # 代理协作与质量门禁
    ├── README.md
    ├── index.html                # 可搜索、可筛选的课程首页
    ├── 01.html ... 28.html       # 章节入口；首批 01–05 深度重构
    ├── courses.json              # 课程元数据唯一事实源
    ├── courses-data.js           # 离线首页生成数据
    ├── theme.css                 # 首页与章节共享设计系统
    ├── assets/diagrams/          # 原创 SVG 图解
    ├── evidence/                 # 每章 claim → source → locator 证据账本
    ├── docs/                     # 架构、标签、写作、证据和 QA 规范
    ├── scripts/                  # 元数据构建与站点验证
    ├── tests/                    # 离线目录与内容完整性测试
    └── .github/workflows/        # 自动质量检查

## 内容生产规范

每篇文章遵循：问题与误区 → 最小心智模型 → 机制与公式 → 工程示例 → 证据与消融 → 失败模式 → 交互练习 → 参考资料。

详细规范：
- docs/article-authoring.md
- docs/evidence-policy.md
- docs/quality-gates.md
- docs/architecture.md

## 验证

    python3 scripts/build_course_data.py --check
    python3 scripts/validate_site.py
    python3 -m unittest discover -s tests -v
    node --test tests/offline-catalog.test.cjs

检查范围包括课程数据一致性、章节路径、内部链接、HTML 语义结构、SVG XML、证据账本和首页筛选逻辑。浏览器级截图与交互检查需要真实 Chromium 环境；若 CI 未执行，不应宣称已通过。

## 研究资料锚点

- [T5 / C4 · JMLR](https://jmlr.org/papers/v21/20-074.html)
- [CCNet · LREC 2020](https://aclanthology.org/2020.lrec-1.494/)
- [The Pile · arXiv](https://arxiv.org/abs/2101.00027)
- [RefinedWeb · arXiv](https://arxiv.org/abs/2306.01116)
- [FineWeb · NeurIPS 2024](https://arxiv.org/abs/2406.17557)
- [Dolma · ACL 2024](https://aclanthology.org/2024.acl-long.840/)
- [Common Crawl documentation](https://commoncrawl.org/get-started)
- [fastText language identification](https://fasttext.cc/docs/en/language-identification)
- [Trafilatura documentation](https://trafilatura.readthedocs.io/en/stable/)

## 设计原则

本项目借鉴 Olah-style 的渐进式解释方式与 Annotated Transformer 的代码注释教学方法，但所有文章文字、SVG、示例和布局均独立创作。我们不复制第三方图示、文章段落或品牌资产。

## License / Data provenance

课程代码、原创图示和文档的许可应以仓库根目录的 LICENSE（若存在）为准。引用的数据集、模型和第三方语料分别遵守各自的许可、使用条款与隐私约束。数据源公开可访问不等于其中所有内容都可自由再分发。
