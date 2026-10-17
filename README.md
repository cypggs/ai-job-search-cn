<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="200">
</p>

# AI Job Search 中国求职版

*跑在你自己机器上的 AI 求职助手。*

[English README](README_EN.md) | **中文 README**

[![CI](https://github.com/cypggs/ai-job-search-cn/actions/workflows/ci.yml/badge.svg)](https://github.com/cypggs/ai-job-search-cn/actions/workflows/ci.yml)

一个基于 [Claude Code](https://claude.com/claude-code) 的 AI 求职框架：fork 本仓库、填写个人档案，然后让 Claude 帮你评估职位匹配度、定制中文简历、撰写求职信、准备面试。

本项目 fork 自 [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search)（丹麦求职框架），并针对**中国求职环境**做了深度适配：

- **中文简历 / 求职信 LaTeX 模板**（`cv/chinese/main.tex`、`cover_letters/chinese/cover.tex`），基于 `ctex` + moderncv，符合国内 HR 的阅读习惯
- **中国市场专属档案字段**：求职意向、期望薪资（支持 `20k-30k·14薪` 式报价）、当前薪资、工作年限、到岗时间、政治面貌 / 籍贯 / 民族（国企事业单位可选）、微信号
- **中国职场文化评估维度**：996 / 大小周、五险一金、试用期条款、国企 vs 外企 vs 互联网公司的匹配度，都会进入职位匹配评分
- **国内招聘平台抓取策略**：BOSS 直聘、拉勾、猎聘、智联招聘、前程无忧反爬严格，默认采用 WebSearch + 手动粘贴职位描述的方式，不硬刚反爬
- 同时保留原框架全部国际化能力：英文简历模板、LinkedIn / freehire CLI 工具、外企与出海岗位投递

> 说明：这是一个独立的开源项目，与 Anthropic 无隶属、背书、赞助或维护关系。文中提及 Anthropic 和 Claude Code 仅用于描述本工具链。

## 它真的有用吗？

原项目作者 Mads Lorentzen 是一名地球物理学家，2025 年底被裁员后用这个框架跑完了自己的整个求职流程——69 份定制申请、20 场一面、1 个签约 offer，2026 年 6 月入职 AI 工程师岗位。这个中国版保留了同一套 `/scrape`、`/apply`、`/interview` 工作流。

## 工作流程

```
/setup          /scrape              /apply <链接或粘贴的JD>
  |                |                     |
  v                v                     v
填写个人档案   搜索国内招聘平台        评估职位匹配度
                 |                     |
                 v                     v
             按匹配度展示职位      起草中文简历 + 求职信
                 |                     |
                 v                     v
             挑选职位             审阅 agent 交叉评审
             进入 /apply          -> 修改 -> 产出最终 PDF
```

### 与原版相比，中国版多了什么

| 场景 | 原版（丹麦版） | 本 fork（中国版） |
|------|--------------|------------------|
| 简历语言 | 英文 moderncv 模板 | 中文 ctex 模板 + 英文模板并存，按 JD 语言自动选择 |
| 薪资口径 | 年薪（丹麦克朗） | 月薪 `k`、`*薪`（13薪/14薪）、总包，评估时自动换算对比 |
| 职位信息源 | 丹麦四大招聘站 + LinkedIn | BOSS直聘/拉勾/猎聘/智联/51job（WebSearch）+ LinkedIn/外企 |
| 档案字段 | 姓名/电话/邮箱 | 增加微信号、政治面貌、籍贯、到岗时间、工作年限 |
| 文化评估 | 工会、休假 | 996/大小周、五险一金、试用期、通勤 |

## 环境要求

- [Claude Code](https://claude.com/claude-code) CLI（需要 Claude Pro/Max/Team 订阅或 API 额度）
- Python 3.10+
- [Bun](https://bun.sh)（仅在使用门户 CLI 工具时需要；国内求职默认用 WebSearch，可跳过）
- LaTeX 发行版（`lualatex` + `xelatex`）：macOS 推荐 [MacTeX](https://tug.org/mactex/)，Windows 推荐 [MiKTeX](https://miktex.org/)，Linux `sudo apt install texlive-full`
- **中文字体**：模板用 `ctex` 宏包自动检测系统字体——macOS 自带苹方/华文，Windows 用 SimHei/SimSun，Linux 需 `sudo apt install fonts-noto-cjk`
- 可选：`pip install pypdf`（`/apply` 的 ATS 文本层检查用）

## 快速开始

### 1. Fork 并克隆

```bash
gh repo fork cypggs/ai-job-search-cn --clone
cd ai-job-search-cn
```

> ⚠️ **Fork 默认是公开仓库**，而 `/setup` 会把你的个人信息（姓名、电话、期望薪资）写入会被 git 跟踪的文件。如果只是自己用，建议复制到一个**私有仓库**并把这个仓库设为 `upstream`（方法见 [SETUP.md](SETUP.md) 第 8 节）。

### 2. 安装工具（可选）

```bash
python3 tools/install_portal_clis.py
```

国内求职默认走 WebSearch，这步可跳过；如需 LinkedIn / freehire CLI 或想用 `/add-portal` 自建平台工具再装。

### 3. 填写档案

```bash
claude
# 在 Claude Code 中运行：
/setup
```

`/setup` 支持三种方式：读取 `documents/` 文件夹（简历 PDF、证书等）、直接粘贴一份简历、或对话式访谈。中国版会额外询问：期望薪资（月薪/年薪/几薪）、目标城市、是否接受 996/大小周、是否投递国企（需要政治面貌等字段）。

### 4. 搜索职位

```bash
/scrape
```

针对国内平台执行 WebSearch，按匹配度展示结果。国内平台反爬严格，结果可能只有标题和摘要——**更推荐直接复制 JD 全文**：

```bash
/apply [粘贴完整职位描述]
```

职位太多看不过来？先跑 `/rank`，让框架批量打分、排出优先级短名单。

### 5. 投递

```bash
/apply https://www.zhipin.com/job/xxxxxxxx.html
```

链接抓不到就直接粘 JD。中文版职位会自动生成**中文简历和中文求职信 PDF**（英文 JD 则用英文模板）。

完整流程：解析 JD → 匹配度评估（含 996/五险一金等中国维度）→ 起草简历+求职信 → 独立审阅 agent 交叉评审 → 编译 PDF 并逐页检查（页数、孤行、字体、中文字体渲染）→ ATS 文本层关键词核验 → 产出最终文件。

## 全部命令

| 命令 | 用途 |
|------|------|
| `/setup` | 初始化/更新个人档案（`--section search` 只更新搜索配置） |
| `/scrape` | 搜索新职位、去重、快速匹配评估（`broad` 跑全部类目，`health` 检查平台 CLI 健康度） |
| `/rank` | 对抓取结果批量打分排序，生成优先短名单 |
| `/apply` | 核心投递工作流：评估→起草→评审→编译→ATS 检查 |
| `/outcome` | 记录投递结果（面试/offer/拒信），自动归档材料；`followup` 提醒久未回复的投递 |
| `/interview` | 基于已投递的档案生成面试准备包 + 模拟面试 |
| `/upskill` | 分析你的技能与目标职位的差距，生成学习计划 |
| `/expand` | 从 GitHub/作品集等公开资料扩充档案中的技能 |
| `/html-report` | 生成自包含 HTML 求职看板（离线可用，投了多少、漏斗转化率一目了然） |
| `/add-template` | 注册自定义简历/求职信模板（LaTeX、Typst 等） |
| `/add-portal` | 为某个招聘平台生成搜索 CLI 技能（有反爬的平台会自动降级为 WebSearch 建议） |
| `/reset` | 清空个人档案重新开始 |

另有 `/gmail-sync`、`/notion-sync`（同步到 Gmail / Notion）。**注意**：这两项依赖对 Google / Notion 的网络访问，在中国大陆网络环境下可能无法直接使用；核心的 `/scrape`、`/apply`、`/html-report` 均不依赖外部服务。

## 中国求职实战建议

框架是通用的，但国内求职有几个本地要点，配合使用效果最佳：

- **内推为王**：国内大厂简历筛选高度依赖内推。`/scrape` 的高匹配职位会附带 LinkedIn 人脉搜索链接；对国内公司，可以同步在**脉脉、LinkedIn、校友群**里找目标公司的员工内推——同样一句话，内推的转化率远高于海投。
- **JD 直接粘贴最靠谱**：BOSS 直聘等平台的职位页几乎必然触发反爬，复制 JD 全文粘贴给 `/apply` 是最稳定的信息输入方式，框架对粘贴文本的处理与 URL 完全等价。
- **警惕培训贷/招转培**：`/scrape` 和 `/rank` 会对"同一职位多城市重复发布"等异常模式给出提示，但国内求职仍需自行甄别要求入职前缴费、"带薪培训"后返还等骗局。
- **背调意识**：国内入职普遍有背景调查，`/apply` 的事实核查机制（所有经历必须能在档案中找到出处）恰好保证了简历内容与背调材料一致——不要为了好看虚构经历。
- **薪资谈判**：档案里填好当前薪资和期望薪资后，评估职位时会自动对比 JD 报价（自动识别 `20k-30k·14薪` 这类口径并换算），帮你快速判断值不值得聊。

## 目录结构

```
ai-job-search-cn/
├── CLAUDE.md                     # 个人档案 + 工作流规则（/setup 自动填充）
├── cv/chinese/main.tex           # 中文简历模板（ctex + moderncv）
├── cover_letters/chinese/        # 中文求职信模板（ctexart）
├── .claude/commands/             # 12 个斜杠命令定义
├── .claude/skills/               # 核心技能定义（评估框架、写作风格、面试准备）
├── .agents/skills/               # 门户搜索 CLI（LinkedIn、freehire、丹麦 demo）
├── tools/                        # 校验与辅助脚本（PDF 检查、布局检查、lint）
├── documents/                    # 个人材料（简历原件、证书、历史投递）
└── job_search_tracker.csv        # 投递追踪表
```

## 与上游保持同步

上游迭代很快。本 fork 已同步至上游最新版本（291 个上游提交，含 `/interview`、`/notion-sync`、PDF 布局自动校验、`/rank` 大改、免费内推链接生成等）。之后想继续跟进上游：

```bash
python3 tools/check_upstream_updates.py   # 预览上游更新会影响你哪些个性化文件
python3 tools/upstream_triage.py          # 把落后的提交分成"值得看"和"可跳过"
```

详见 [SETUP.md](SETUP.md) 第 8 节。

## 致谢

- 原作者 [Mads Lorentzen](https://github.com/MadsLorentzen) 及 [上游项目](https://github.com/MadsLorentzen/ai-job-search)
- [Mikkel Krogholm](https://github.com/mikkelkrogsholm) 的招聘 CLI 技能
- 基于 [Claude Code](https://claude.com/claude-code) 构建

## License

MIT
