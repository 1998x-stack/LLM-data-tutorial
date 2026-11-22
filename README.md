# LLM Data Tutorial · 大语言模型预训练数据工程

> 从原始网页到可训练语料：面向研究生、数据工程师与 LLM 研究实践者的开放式课程知识库。

本项目围绕 **数据来源 → 正文抽取 → 规范化与过滤 → 去重 → 质量评估 → 数据混合 → Tokenization → 可复现训练数据** 建立系统化学习路径。课程不把“数据清洗”简化为若干 if-else，而是强调数据契约、来源追踪、论文证据、误差分析和受控实验。

## 当前版本

- 28 个课程模块，保留原有 01.html–28.html 章节入口。
- 首页支持全文搜索、知识分类筛选与标签筛选。
- 已深度重构：01–25，采用渐进式叙事、原创 SVG、交互练习、MathML 公式、可运行算法示例、单元测试和论文证据账本。
- 01–25 每篇重构文章维护独立 evidence/NN.json 证据清单。
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
| 质量、安全与评估 | 10–13、18 | 困惑度、教育质量分类器、LLM 标注、评测去污染、分层抽检与下游质量评估 |
| 数据组成与表示 | 14、19–20、22 | 文档/Token 配比、BPE、SentencePiece、词表成本、多语言 token premium、领域数据 |
| 系统与工具链 | 15–17、23–24 | Spark/Ray、Parquet/Arrow/Iceberg、DVC、数据血缘与可复现性、DataTrove、Dolma |
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
| 06 | URL 与域名过滤 | RFC 3986、URL 规范化、域名画像、审计策略 |
| 07 | 精确去重 | SHA-256、Bloom Filter、假阳性与精确索引 |
| 08 | MinHash 近邻去重 | Shingling、Jaccard、MinHash 定理、LSH Banding |
| 09 | 多粒度去重策略 | 行/段落/文档粒度、重复簇、跨 Crawl 消融 |
| 10 | 困惑度质量过滤 | Cross-Entropy、5-gram Kneser–Ney、KenLM、CCNet |
| 11 | 教育质量分类器 | FineWeb-Edu、Llama 3 合成标注、Snowflake Arctic Embed 回归器、阈值消融 |
| 12 | LLM 辅助数据标注 | Rubric、IAA、LLM-as-a-Judge 偏差、不确定性路由、蒸馏 |
| 13 | 评测集去污染 | GPT-3 word n-gram、Llama 2 token skipgram、T1–T4 污染 taxonomy |
| 14 | 多源数据混合配比 | 文档到 token 权重换算、DoReMi、RegMix、RegMix-D |
| 15 | 分布式数据处理架构 | Spark AQE、Ray Data streaming、Shuffle、Backpressure、幂等恢复 |
| 16 | 大规模数据存储 | Parquet row groups、Arrow 内存格式、Iceberg snapshots、对象存储与小文件治理 |
| 17 | 流水线可复现性 | DVC DAG、content hash、run manifest、依赖锁与输出指纹 |
| 18 | 数据质量评估体系 | DCLM / Dolma、质量维度、分层抽样、置信区间、受控下游评测 |
| 19 | Tokenization 与 BPE | pair frequency、merge ranks、byte-level BPE、SentencePiece、tiktoken |
| 20 | 词表设计与优化 | vocabulary × hidden size、embedding / softmax 成本、多语言 token premium |
| 21 | 合成数据生成 | Self-Instruct、Evol-Instruct、独立验证、来源追踪与模型坍缩边界 |
| 22 | 领域适配数据策略 | DAPT、TAPT、Continual Pretraining、Replay 与遗忘评估 |
| 23 | DataTrove 流水线实战 | Document、PipelineStep、Local/Slurm/Ray、任务恢复与 MinHash |
| 24 | Dolma 工具链全解析 | Dataset / Toolkit / Dolma 3、Tagger、Dedupe、Mixer、Tokens |
| 25 | 六大清洗范式对比 | 规则、统计、去重、分类器、LLM Judge、人工与下游实验 |
| 26 | 自动化数据准备系统 | Agent 编排、质量反馈与治理 |
| 27 | 在线数据选择与动态配比 | 课程学习、在线采样与动态调度 |
| 28 | 端到端综合实战 | 数据契约、流水线、验收与排障 |

## 仓库结构

    LLM-data-tutorial/
    ├── AGENTS.md                 # 代理协作与质量门禁
    ├── README.md
    ├── index.html                # 可搜索、可筛选的课程首页
    ├── 01.html ... 28.html       # 章节入口；01–25 已深度重构；26–28 待迁移
    ├── courses.json              # 课程元数据唯一事实源
    ├── courses-data.js           # 离线首页生成数据
    ├── theme.css                 # 首页与章节共享设计系统
    ├── assets/diagrams/          # 原创 SVG 图解
    ├── evidence/                 # 每章 claim → source → locator 证据账本
    ├── docs/                     # 架构、标签、写作、证据和 QA 规范
    ├── scripts/                  # 元数据构建与站点验证
    ├── tests/                    # 离线目录、内容完整性与算法测试
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
- [FineWeb-Edu Dataset Card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- [FineWeb-Edu Classifier](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier)
- [LLM-as-a-Judge · MT-Bench](https://arxiv.org/abs/2306.05685)
- [Inter-Annotator Agreement in NLP · AACL 2026](https://aclanthology.org/2026.aacl-long.27/)
- [GPT-3 · Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- [Llama 2 · Dataset Contamination](https://arxiv.org/abs/2307.09288)
- [Benchmark Contamination Review · GEM 2026](https://aclanthology.org/2026.gem-main.50/)
- [DoReMi · NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/dcba6be91359358c2355cd920da3fcbd-Abstract-Conference.html)
- [Data Mixing Laws · ICLR 2025](https://arxiv.org/abs/2403.16952)
- [RegMix · ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5f67d864aae6115374fed7beddd119e0-Abstract-Conference.html)
- [RegMix-D · Findings AACL 2026](https://aclanthology.org/2026.findings-aacl.84/)
- [Apache Parquet Format Specification](https://github.com/apache/parquet-format)
- [Apache Arrow Format](https://arrow.apache.org/docs/format/Intro.html)
- [Apache Iceberg Specification](https://iceberg.apache.org/spec/)
- [Amazon S3 strong consistency](https://aws.amazon.com/s3/consistency/)
- [DVC · Defining Pipelines](https://doc.dvc.org/user-guide/pipelines/defining-pipelines)
- [DVC · Reproduce Pipelines](https://doc.dvc.org/command-reference/repro)
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [Data Statements for NLP · TACL](https://aclanthology.org/Q18-1041/)
- [DataComp-LM · NeurIPS 2024](https://arxiv.org/abs/2406.11794)
- [Dolma · ACL 2024](https://aclanthology.org/2024.acl-long.840/)
- [BPE · Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/)
- [SentencePiece](https://arxiv.org/abs/1808.06226)
- [OpenAI tiktoken](https://github.com/openai/tiktoken)
- [GPT-2 tokenizer documentation](https://huggingface.co/docs/transformers/model_doc/gpt2)
- [Llama 3 tokenizer design](https://ai.meta.com/blog/meta-llama-3/)
- [Tokenizer Choice For LLM Training](https://arxiv.org/abs/2310.08754)
- [Explaining and Mitigating Crosslingual Tokenizer Inequities · NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/5b91cefbfa52340af2f16f249572dc76-Paper-Conference.pdf)
- [TokLens · ACL 2026 SRW](https://aclanthology.org/2026.acl-srw.18/)
- [Self-Instruct · ACL 2023](https://aclanthology.org/2023.acl-long.754/)
- [WizardLM / Evol-Instruct](https://arxiv.org/abs/2304.12244)
- [Orca · Microsoft Research](https://www.microsoft.com/en-us/research/publication/orca-progressive-learning-from-complex-explanation-traces-of-gpt-4/)
- [Phi-4 Technical Report](https://www.microsoft.com/en-us/research/publication/phi-4-technical-report/)
- [AI models collapse when trained on recursively generated data · Nature 2024](https://www.nature.com/articles/s41586-024-07566-y)
- [Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413)
- [Don’t Stop Pretraining · ACL 2020](https://aclanthology.org/2020.acl-main.740/)
- [TiC-LM · ACL 2025](https://aclanthology.org/2025.acl-long.1551/)
- [Continual Learning of LLMs · ACM Computing Surveys 2025](https://doi.org/10.1145/3735633)
- [Hugging Face DataTrove](https://github.com/huggingface/datatrove)
- [AI2 Dolma Toolkit](https://github.com/allenai/dolma)
- [Dolma 3 datasets and recipes](https://github.com/allenai/dolma3)
- [AI2 Dolma documentation](https://docs.allenai.org/training_data/dolma/)
- [LLM Data Auditor · 2026](https://arxiv.org/abs/2601.17717)
- [ByT5 · TACL](https://doi.org/10.1162/tacl_a_00461)
- [Apache Spark documentation](https://spark.apache.org/docs/latest/)
- [Ray Data documentation](https://docs.ray.io/en/latest/data/)
- [Common Crawl documentation](https://commoncrawl.org/get-started)
- [RFC 3986 · URI Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986)
- [Deduplicating Training Data Makes Language Models Better · ACL 2022](https://aclanthology.org/2022.acl-long.577/)
- [Broder · On the Resemblance and Containment of Documents](https://doi.org/10.1109/SEQUEN.1997.666900)
- [Bloom Filter false-positive analysis · NIST](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=903775)
- [fastText language identification](https://fasttext.cc/docs/en/language-identification)
- [Trafilatura documentation](https://trafilatura.readthedocs.io/en/stable/)

## 设计原则

本项目借鉴 Olah-style 的渐进式解释方式与 Annotated Transformer 的代码注释教学方法，但所有文章文字、SVG、示例和布局均独立创作。我们不复制第三方图示、文章段落或品牌资产。

## License / Data provenance

课程代码、原创图示和文档的许可应以仓库根目录的 LICENSE（若存在）为准。引用的数据集、模型和第三方语料分别遵守各自的许可、使用条款与隐私约束。数据源公开可访问不等于其中所有内容都可自由再分发。


## Latest quality follow-up

- [Versioned-tool and evidence-ledger audit (2026-11-22)](docs/versioned-tool-followup-2026-11.md): DataTrove v0.10.1 / Dolma Toolkit v1.2.1 source pins, Dolma JSONL and token-index corrections, and strict evidence validation.
