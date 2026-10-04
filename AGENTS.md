# AGENTS.md

本仓库是一个**纯笔记仓库**，没有代码、构建、测试或 CI。一级目录是**知识域**，每域是一门课或一个主题。所有内容都是给人读的 Obsidian 笔记。

---

## 并发工作（最容易犯的错，先读这条）

**多个 agent 会同时在不同知识域上工作。**你会看到别人的半成品：某个域目录结构刚建好、笔记只有几篇、linter 报几百条断链、git status 里有大量别的域的增删改。

- **只改你被指派的域。不要 `git add -A` / `git commit` / `git push`** —— 那会把别人没写完的内容一起提交。用户会统一提交。
- **不要顺手"修正"别的域**（哪怕它违反了下面的约定）。发现偏差记下来报告，不要动手。
- 没有 `.gitignore`，`.obsidian/`（尤其 `workspace.json`）和 `.soit/` 是**被跟踪的**，会持续产生噪声 diff。`git status` 里的这两项变化通常不是你的。
- remote `github.com/Retr0-rgb-lab/Fast-Learning`，分支 `main`，**无 CI、无 pre-commit hook** —— 没有任何自动检查会替你兜底，验证要自己跑。

---

## 目录约定

### 1. 域内结构：llm-wiki 两层

```
<Domain>/
├── notes/
│   ├── raw/     原始资料，通常是课堂 PDF 课件。只读，永不修改
│   └── wiki/    从课件知识点编译出的笔记 + index.md + log.md
│       ├── assets/   图片（若有）
│       └── <主题子目录>/
└── tools/       该域的检查脚本（若有）
```

- **`raw/` 放原始资料**（课堂 PDF 课件、论文原件）。**不可变。**
- **`wiki/` 放知识笔记**，在课件知识点之间建立网络（Obsidian 双链）。

### 2. 目录名不带任何数字

`wiki/` 下可以建子目录按主题划分，但**目录名不得含数字**（不要 `01-xxx`、`1_xxx`）。按主题命名以便长期扩展。

### 3. `index.md` / `log.md` 放 `notes/wiki/` 内

新写的域一律放 `notes/wiki/index.md`（MOC 索引）和 `notes/wiki/log.md`（沉淀日志）。

> **已知偏差**（不要顺手改）：`Software_Engineering/`、`Logic/` 的 index/log 在**域根目录**；`Math/` 用的是 `MOC.md` 且完全扁平、没有 `notes/` 分层；`Cybernetics/materials/` 存着 PDF 而 `notes/raw/` 里是一个 `.md`，与约定相反。

---

## 写笔记的约定

- **中文为主，术语中英对照**（便于对照课件和英文考试）。
- **每篇自足**：单独打开任何一篇都能读懂。不要写"如上例所示"这种依赖前文的省略。
- **场景不预设**（重要）：任何例子都要**从零完整解释**——样本是什么、任务是什么、每一步在做什么、为什么这么做。**不要预设读者已经知道某个场景。**课件里的例子不能只标一句"见课件 p42"。
- 课件页码只作**溯源标注**，不是理解的前提。
- 标记易错点用 `> [!warning]` callout。
- 跨主题的关联集中列在 `index.md`，不要每篇都重复一遍。

### frontmatter 契约

每篇 wiki 笔记都要有：

```yaml
---
tags: [...]                  # 必填，非空列表
domain: [学科, 子领域]        # 必填。单域归本域目录；跨域在 domain 里声明
created: YYYY-MM-DD
type: 知识点 | 知识地图 | 索引 | 复习
aliases: [...]               # 英文名、缩写、旧称（见下方"双链的坑"）
# 课程笔记：
course: COMP 4423 ...
lecture: [L3]
source: "[PDF 文件名](<../../raw/PDF 文件名>)"   # 相对本文件指向 notes/raw/
# 自学笔记：
来源: "自学（PyTorch / 深度学习）"
---
```

- `source` 里的相对路径要按笔记所在深度算（`wiki/<子目录>/X.md` 用 `../../raw/`）。
- **`domain:` 是硬要求**（llm-wiki-ingest 纪律）。目前 `Computer_Vision` 和 `HCI` 全量落实；`Cybernetics` / `Software_Engineering` / `Web_Development` 尚未补齐 —— **你改到哪个域就补哪个域，不要跨域批量改。**

---

## Obsidian 双链的四个坑

这些会造成**静默损坏**：链接看起来正常，实际解析到错误的页。

1. **`[[X]]` 按 basename 解析，不是按路径。** 移动或重命名文件**不会**破坏链接 —— 所以可以自由重组目录。但反过来：**两个文件同名会被静默歧义**。

2. **真实文件名优先于 alias。** 如果 A 的 `aliases:` 恰好等于 B 的**真实文件名**，那么 `[[该名字]]` 全部解析到 B，A 的这个 alias 永远不生效。仓库里真实发生过（`nn.Linear 输出与 logits.md` 的 alias 撞上了 `Logits、Softmax 与 argmax.md`）。**不要用另一个页面的文件名当 alias。**

3. **`[[folder/Note]]` 路径前缀链接在 Obsidian 里合法**，但只按 basename 扫描的脚本会误报。linter 接受它，但新写的笔记优先用纯 basename。

4. **改名前先查入链。** 靠 `aliases:` 一次性兼容旧名，**不要跨文件做 find-replace**。

---

## 图片

**图片一律由用户提供。你的职责是整理和落位，不要自己生成。**

不要用文生图模型，也不要用 HTML/SVG 等方式自己画技术图。

拿到用户给的图片后：

- 放进 `<Domain>/notes/wiki/assets/`，文件名用中文描述性命名
- **一律用 `![[文件名.png]]` 内嵌，禁止相对路径**（`![](../../图片/x.png)`）。相对路径在任何一次移动后都会断
- 插进笔记里语义正确的位置（不是随便丢在文末）
- 用 `mmx vision describe --image <路径>` 核对图的内容与该处正文的说法是否一致，不一致先问用户，别硬塞
- 跑该域 linter —— 它会检查 `assets/` 里的图是否都被引用、引用是否可达

目前全仓库图片引用已全部是 wikilink 内嵌（相对路径为 0），别引入例外。

---

## 验证

**没有 CI，改完必须自己跑检查。**

```bash
python3 <Domain>/tools/<domain>_lint.py     # 默认 wiki 根 = 脚本同级 notes/wiki，也可传参指定
```

报告四项，**通过标准是全部为 0**：

| 指标 | 含义 |
|---|---|
| 断链 unresolved | 有链接指向不存在的页 |
| 孤儿页 no-inbound | 没有任何入链的笔记（进不来，等于没写） |
| 歧义 basename | 同名多文件，链接会解析歧义 |
| alias 遮蔽真实页 | alias 撞上别的真实文件名，该 alias 永不生效 |

> **两个 linter 已分叉**：`Computer_Vision/tools/cv_lint.py` 与 `HCI/tools/hci_lint.py` 是同一工具的两个 fork，**HCI 版更新**（多了 alias 遮蔽检测和域内/跨域链接计数）。**CV 版的 docstring 仍写着"别名优先"，那是错的**（真实 Obsidian 是文件名优先）—— 它只是代码修对了、注释没改。
> **给新域建 linter 时复制 HCI 版**，只改默认路径。理想状态是合并成一份共享脚本，目前还没有。

**结构改动后必须重跑并对比数字**：断链和孤儿数应当下降。另外注意 linter 会**跳过代码块和行内代码**（Python 的 `[[2.0, 1.0]]` 这类嵌套列表不是 wikilink）。

---

## 收尾

改动一个域后：

1. 跑该域的 linter，确认四项全 0
2. 在该域的 `notes/wiki/log.md` 追加一行：日期 / 做了什么 / 来源
3. **不要 commit**（见"并发工作"）
