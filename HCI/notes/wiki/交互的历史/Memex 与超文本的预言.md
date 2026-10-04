---
tags:
  - 交互历史
  - 超文本
  - 信息检索
  - Memex
  - Vannevar Bush
created: 2026-10-04
type: 知识点
aliases:
  - Memex
  - Memory Extender
  - As We May Think
domain: [人机交互]
course: COMP3423 Human-Computer Interaction
lecture: [L01]
source: ["[Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>)"]
---

# Memex 与超文本的预言

> **一句话**：1945 年 Vannevar Bush 在《As We May Think》里诊断出的瓶颈**不是"存不下"，而是"用不上"** —— *"publication has been extended far beyond our present ability to make the real use of the record"*（出版物的增长已远远超出我们真正利用这些记录的能力）；他为此设想的机器 **Memex（Memory Extender，记忆延伸器）** 是一台以**缩微胶片**为存储、以**关键词索引与交叉引用**为检索、以**链式链接**为组织方式的个人外部记忆 —— **它从未被造出来**，但**超文本（hypertext）与万维网（WWW）都是它的直系后代**。

课件 L01 第 1 份 p51–p53。原文见 [Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>)。课件在这一段开头就把定性写了：*"Intellectual foundations laid by Vannevar Bush (1945)"*。

## 他诊断的是哪一个问题

课件 p51 整页只有四行，但问题提得非常干净：

- 载体：*"As we may think" article in **Atlantic Monthly*** —— 1945 年发表在《大西洋月刊》上的文章《As We May Think》；
- 病灶：*"Identified the **information storage and retrieval** problem: **new knowledge does not reach the people who could benefit from it**"* —— 他指出**信息存储与检索**问题，**新知识到不了那些能从中受益的人手里**；
- 原句：*"**publication has been extended far beyond our present ability to make the real use of the record**"*。

**这句话的结构值得拆开看，因为它决定了后面五项设想为什么长那样。**

| 成分 | 说的是什么 |
|---|---|
| publication has been extended | **产出端已经爆炸** —— 文献、记录、报告的产生速度远超以往 |
| far beyond our present ability | 但**利用端没有跟上** |
| to make real use of **the record** | 卡住的是**记录本身的使用**，不是记录的产生 |

**所以病根不在"存"，在"取"和"用"。**记录已经海量地存在了（缩微胶片、卡片目录、图书馆），问题是没有任何一个人能在需要的时候把相关的那几条从整个藏量里拽出来。Bush 举的隐含例子就是**一个研究者自己的书架** —— 他读过的每篇文章都是活的知识，但只有靠记忆里的偶然联想才找得回来；**联想是随机触发的，不可预约**。

> [!warning] 常见错误
> 不要把 Memex 讲成"最早的计算机"或"信息技术的开端"。课件的定性是 **"Intellectual foundations"（智识基础）** —— Bush 贡献的是**一个问题陈述加一份设想清单**，不是一台机器。Memex **从来没有被造出来**（下一节有课件原话）。

## Memex 是什么：五项设想

课件 p52 把 Memex 标为 **Memory Extender（记忆延伸器）**，副标题是 *"Conceiving Hypertext and the World Wide Web"*（构想超文本与万维网），然后给了五条：

| # | 课件原文 | 这条在解决什么 |
|---|---|---|
| 1 | *"Device where individuals store all personal **books, records, communications**"* | **收全**：一个人的全部藏书、记录、往来信件都归这台机器管。范围是"个人的全部"，不是"机构的收藏" |
| 2 | *"Items retrieved rapidly through **indexing, keywords, cross references**,..."* | **快取**：靠**索引、关键词、交叉引用**迅速取回。这是针对上一节那个"用不上"的正面回答 |
| 3 | *"Can **annotate text with margin notes, comments**,..."* | **可批注**：能在正文**页边写笔记、加评论**。材料从此不再只读 |
| 4 | *"Can construct and save a **trail (chain of links)** through the material"* | **可串链**：能把查阅过程**构造成一条穿过材料的链并把它存下来**。一次思考的路径本身成为可复用的对象 |
| 5 | *"Acts as an **external memory**"* | **是外部记忆**：不是工具，是**人的记忆的延长** |

**第 4 条是整份清单里最超前、也最被低估的一条。** 前三条（收全、快取、批注）今天任何一个笔记软件都有；第 4 条说的是：**你查 A 时顺手点进 B、B 又指向 C，这条 A→B→C 的路径本身有信息量，它值得被命名、保存、复用**。这正是超文本区别于传统超链接的地方 —— 链接不是终点，是**路径**。

课件最后补了一句否决性的事实：

> *"Bush's Memex idea was based on **microfilm records** but **not implemented**"* —— 基于**缩微胶片**记录，但**没有实现**。

## Memex 长什么样：五块硬件

课件 p53 用一张结构图给 Memex 配了五块部件（标题写的是 *Memex (1945) (**forerunner of WWW**)*，括号里直接写着"万维网的前身"）：

| 部件 | 课件原文 | 干什么 |
|---|---|---|
| 输入平板 | *"**Tablet** for user input (notes)"* | 用来输入**笔记**的平板 |
| 两台投影机 | *"Two projectors: **one for images, one for text** (cross references)"* | **一台投影图像、一台投影文字**，两者做**交叉引用** |
| 控制面板 | *"**User control panel** for bookmarks, hyperlinks, and **automated search**"* | **书签、超链接、自动化检索**三样都在这块面板上 |
| 通信 | *"Content can be **uploaded to other Memex machines**"* | 内容可以**上传到别的 Memex 机器** |
| 存储 | *"Information (text, images) on **microfilm**"* | 文字与图像信息**存在缩微胶片上** |

**这张图里藏着 Memex 的技术命运。** 五块部件里有三块 —— **缩微胶片存储、两台胶片投影机、一台输入用的平板** —— 全部是**光机设备**，没有一样是电子的。也就是说：这个设计里没有 CPU，没有可编程逻辑，检索靠的是**胶片索引机械 + 人手翻找 + 投影**。**"自动检索"要在这套硬件上实现，只能做成机械索引或预存轨道。**

**两台投影机的设计是这套方案里最聪明的一步。** 为什么需要**两台**？因为文字和图像在缩微胶片上是**分开存放**的两卷。画面上要同时显示"这段文字"和"这幅图"，并且**从文字能跳到图、从图能跳回文字** —— 交叉引用需要一个常驻的、被两台机器同时照亮的**工作面**。这个"两块内容 + 一个可切换的工作面"的结构，正是后来双屏、和后来超文本里"节点 + 窗口"的雏形。

**"Content can be uploaded to other Memex machines"是全套设想的收口。** 前四条讲的是一个人和他的材料怎么组织；这一条讲**人和人怎么连** —— 你的记忆库可以并入别人的记忆库。课件把这块写进硬件图，说明在 Bush 的构想里，Memex 从一开始就是**联网的**，不是单机。

## 为什么它没有实现

课件给的理由是它基于**缩微胶片**，并且直说 **not implemented**。课件**没有展开**为什么，本页不补。**但把 p53 那五块硬件按"它能做什么／做不到什么"分开，原因就浮出来了 —— 下表是本页据硬件图推出的推论，不是课件原文：**

| 在 1945 年它能做的 | 在 1945 年它做不到的 |
|---|---|
| 缩微拍摄：把一整套书缩成胶片，密度极高、成本极低 | **索引只能是机械的** —— 胶片线性排列，取一条内容只能沿索引轨找 |
| 双投影：文字与图像可以并排对照 | **投影是一次性的**，不像屏幕那样能随时刷新、能在原处改 |
| 人工查阅：人翻页、拉片、按键 | **"自动检索"没有电子器件可依**，只能做成预存轨道或索引机械 |
| 上传：把胶片寄给对方的 Memex | **内容不能被程序改写** —— 胶片是原件，涂改不了 |

**这张表给出的判断是：Memex 的每一项功能都绑死在光机媒介上，而这个选择不可撤销。** 一旦选定了缩微胶片作为存储介质，"自动检索"就永远只能做到机械水平；后来真正普及的电子存储走的是完全不同的路线。**所以这不是工程拖延，是选错了路** —— 它是一份思想清单，不是一份工程规格。课件未展开 1945 年之后的存储技术发展，本页也不补。

> [!note] 补充（课件外）
> 按史实，Bush 本人在 1938 年前后就在设计一种基于缩微胶片的机械检索设备（Rapid Selector），并在 1945 年前后制成原型演示；它同样从未投入实用。**这个背景解释了 p52 那句 "not implemented" 的分量** —— 不是"来不及造"，而是"造了也不合用"。

## 它是超文本和万维网的前身

课件给这页下的定性有两处，都很硬：

1. p52 副标题：*"Conceiving **Hypertext** and the **World Wide Web**"*；
2. p53 标题：*"Memex (1945) (**forerunner of WWW**)"*。

**三处设计直接对上了后来的万维网**：

| Memex（1945） | 万维网里的对应物 |
|---|---|
| 以关键词索引取回（p52 第 2 条） | URL 寻址 + 搜索引擎 |
| 交叉引用（p52 第 2 条 / p53 双投影机） | **超链接 `<a href>`** |
| 链式链接的 trail（p52 第 4 条） | 一条由超链接串成的**阅读路径** |
| 内容可上传到别的 Memex（p53） | 文档上传到服务器 / 发布到网络 |
| 作为外部记忆（p52 第 5 条） | 个人知识库、笔记系统 |

> [!warning] 常见错误
> **不要把"前身"读成"发明"。**Bush 发明的是**问题意识与设想清单**，不是超链接这个机制本身 —— 超链接、交叉引用、关键词检索在他之前就存在（图书馆目录、卡片索引、缩微胶片索引早就在用）。Memex 的贡献是**第一次把它们组织成一套面向"个人思考过程"的整体设计**，并明确提出要保存**路径**。考试里正确的表述是"forerunner（前身）／思想基础"，不是"the inventor of hypertext"。

## 一句话收束

> Bush 1945 诊断的瓶颈是**记录已经爆炸、但没人能真正用上它**；Memex 给出的五项设想（收全 / 索引快取 / 页边批注 / 保存链接链 / 充当外部记忆）建立在一套**全光机**的缩微胶片硬件上，因此**从未实现**，但**超文本与万维网继承的是这套问题定义，而不是这套硬件**。

## 相关笔记

- **枢纽**：[[交互的历史-知识地图]] — 1945 年这条线是这个域里最早的一根支柱
- **总纲**：[[交互方式的八个阶段]] — 批处理那个阶段制造了"记录爆炸但用不上"的局面，Memex 是它的直接回应
- **同代同题**：[[Licklider 与人机共生]] — 他的短期目标第 4 条 *large scale information storage and retrieval* 与 Memex 是同一个问题的两种提法
- **同代不同题**：[[Engelbart 与增强人类智力]] — Bush 想的是怎么**存和取**知识，Engelbart 想的是怎么**加工和协同**知识
- **结局**：[[先驱者与定居者]] — 一份从未实现的设想为什么仍能定义后来的四十年
- **跨域**：[[../人类信息加工/问题空间与目标状态|问题空间与目标状态]] — Memex 保存"链"，等于把**走过的路径**本身变成可复用的表征
- **跨域**：[[../人类信息加工/类比推理|类比推理]] — Bush 描述的那个痛点（联想随机触发、不可预约）正是类比推理的自动化方向
- **跨域**：[[../情境与文化/界面背后的组织与文化|界面背后的组织与文化]] — "个人记忆库之间可以互相上传"这条设定，把知识从机构的公共品改写成个人资产
