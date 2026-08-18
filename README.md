# 🤖 LLM数据工程 · 从入门到精通

> 📘 28章 实战体系 · 交互式 HTML 课程

> **English TL;DR:** A 28-chapter, all-Chinese hands-on course on **LLM data engineering** — the pipeline that turns raw web text into high-quality pretraining corpora. Follows the six milestone papers (C4, CCNet, The Pile, RefinedWeb, FineWeb/EDU, Dolma) across four phases: acquisition → cleaning → dedup/filtering → mixing & pipeline (DataTrove/Dolma). HTML-visualized, zero-install, open `index.html` to read.

## 📖 课程简介

数据是 LLM 的燃料。本课程系统讲解 **LLM 预训练数据的完整工程链路**：从 Common Crawl 原始爬取，经正文提取、语言/规则/URL 过滤、精确与近邻（MinHash）去重、困惑度与教育质量筛选，到 tokenization、词表设计、合成数据、多源配比与可复现流水线，最终落地为 DataTrove / Dolma 的端到端实战。全程以 6 篇里程碑论文为锚点，从原理到工程逐块落地。

### 四大主题阶段

| 阶段 | 章节 | 核心 |
|------|------|------|
| **采集与提取** | 01–03 | WARC/WAT/WET、trafilatura 正文提取 |
| **清洗与去重** | 04–10 | 规则/语言/URL 过滤、SHA-1 + MinHash、多粒度去重 |
| **质量与配比** | 11–14 | 教育质量分类器、LLM 标注、评测去污染、多源混合 |
| **流水线与实战** | 15–28 | 分布式处理、可复现性、BPE、合成数据、DataTrove/Dolma、自动化数据准备 |

## 🚀 快速开始

无需安装任何依赖，直接用浏览器打开 `index.html` 即可在线阅读全部章节：

```bash
open index.html   # macOS
# 或在浏览器中直接打开 index.html
```

## 📚 核心论文（随课提供 PDF）

| 论文 | 对应章节 |
|------|---------|
| [The Pile](pdfs/The_Pile.pdf)（22 来源多语料） | 14 |
| [C4 / T5](pdfs/C4_T5.pdf)（启发式清洗范式） | 05 |
| [RefinedWeb](pdfs/RefinedWeb.pdf)（规模化清洗） | 05–06 |
| [CCNet](pdfs/CCNet.pdf)（困惑度分级） | 10 |
| [FineWeb](pdfs/FineWeb.pdf)（数据集复现） | 05 / 11 / 20 |
| [Dolma](pdfs/Dolma.pdf)（8 步清洗基线） | 09, 13, 24 |

## 📖 章节目录

| # | 章节 | 核心主题 |
|---|------|----------|
| 01 | LLM数据工程概述 | 数据驱动的LLM革命、六篇里程碑论文全景、清洗流水线总览 |
| 02 | Common Crawl 数据采集 | WARC/WAT/WET格式、S3开放数据访问、warcio解析实战 |
| 03 | 网页正文提取 | trafilatura提取、HTML噪声消除、提取方案对比 |
| 04 | 语言识别与过滤 | fastText 176语言、置信度阈值设计、多语料配比 |
| 05 | 启发式规则过滤 | C4经典规则集、FineWeb规则扩展、规则设计与迭代 |
| 06 | URL与域名过滤 | Blocklist构建、SEO垃圾识别、域名下采样 |
| 07 | 精确去重 | SHA-1哈希去重、Bloom Filter、段落级 vs 文档级 |
| 08 | MinHash 近邻去重 | Jaccard相似度、MinHash签名、LSH分桶优化 |
| 09 | 多粒度去重策略 | 行/段/文档级、跨语料全局去重、Dolma三级去重 |
| 10 | 困惑度质量过滤 | KenLM、CCNet三分法、困惑度局限 |
| 11 | 教育质量分类器 | fastText分类器、FineWeb-Edu方法论、部署 |
| 12 | LLM辅助数据标注 | 评分prompt、知识蒸馏、标注偏差 |
| 13 | 评测集去污染 | n-gram重叠检测、污染处理、Dolma实践 |
| 14 | 多源数据混合配比 | The Pile 22源、2026惯例配比、上/下采样 |
| 15 | 分布式数据处理 | Spark/Dask/Ray对比、分区、容错 |
| 16 | 大规模数据存储 | 分层存储、Parquet/Arrow、zstd压缩 |
| 17 | 流水线可复现性 | DVC数据版本、确定性清洗、元数据追踪 |
| 18 | 数据质量评估体系 | 内部指标、代理任务评测、人工抽检 |
| 19 | Tokenization 与 BPE | Byte-level BPE、SentencePiece、中文分词 |
| 20 | 词表设计优化 | 词表大小权衡、扩展、推理效率 |
| 21 | 合成数据生成 | Self-Play、数据增强、模型坍缩风险 |
| 22 | 领域适配数据 | 代码清洗、医学适配、多语言平衡 |
| 23 | DataTrove 流水线实战 | 模块化清洗、FineWeb复现、Spark运行 |
| 24 | Dolma 工具链全解析 | 8步数据管线、3万亿语料、混合配方 |
| 25 | 六大清洗范式对比 | 进化树、范式选择、FLUX |
| 26 | 自动化数据准备 | DataEvolver、Agent驱动编排、多样性约束 |
| 27 | 在线选择与动态配比 | 课程学习调度、FLUX、80/20混合 |
| 28 | 综合实战项目 | 完整流水线、验收标准、排障 |

## 📂 项目结构

```text
LLM-data-tutorial/
├── index.html      # 课程主入口
├── 01.html ~ 28.html   # 章节正文
├── courses.json    # 课程元数据
├── theme.css       # 统一主题
└── pdfs/           # 6 篇里程碑论文 PDF
```

## 🎯 前置知识与适合人群

- 适合：对 LLM 预训练数据好奇的数据工程师 / ML 工程师 / 研究者
- 建议具备：Python 基础 + 基本数据处理概念。无需 GPU

## ✨ 课程特色

- **六篇里程碑论文贯穿**：以 C4 / The Pile / RefinedWeb / CCNet / FineWeb / Dolma 为锚点
- **28 章完整闭环**：采集 → 清洗 → 去重 → 质量 → 配比 → 流水线
- **工程向**：DataTrove / Dolma 实战、分布式、可复现性
- **即开即用**：纯静态 HTML，无构建、无服务器

---
*本课程由 `LLM-data-tutorial/` 项目维护。*