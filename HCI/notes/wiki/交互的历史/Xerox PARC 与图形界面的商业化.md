---
tags:
  - 交互历史
  - 图形用户界面
  - Xerox PARC
  - Apple Macintosh
  - 直接操纵
created: 2026-10-04
type: 知识点
aliases:
  - Alto to Macintosh
  - Alto 传承链
domain: [人机交互]
course: COMP3423 Human-Computer Interaction
lecture: [L01]
source: ["[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)"]
---

# Xerox PARC 与图形界面的商业化

> **一句话**：图形界面的想法不是被某一家公司**发明**的，而是被**一串机器接力做出来的** —— 1973 年 **Xerox PARC 的 Alto** 造出全部零件（本地处理器、位图显示、鼠标、窗口、菜单、滚动条、电子邮件、以太网），1981 年 **Xerox Star 8010** 第一次把它们**装成一台面向"商务人士"的商品**并第一次**用可用性工程（usability engineering）造**，1983 年 **Apple Lisa** 降价到 $10,000 却仍然失败，1984 年 **Apple Macintosh** 用**$2,500** 拿下市场 —— 前三台机器全部商业失败，第四台成功。

课件 L01 第 2 份 p27–p33。原文见 [Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)。

## 一条技术传承链

| 年份 | 机器 | 身份 | 商业结局 |
|---|---|---|---|
| 1973 | **Xerox Alto** | PARC 内部研发机，**所有零件一次到位** | 不是商品 |
| 1981 | **Xerox Star 8010** | 第一台面向"商务人士"的商用个人计算机；**第一个综合性 GUI**；**第一个基于可用性工程的系统** | 失败（$15,000） |
| 1983 | **Apple Lisa** | 承袭 Star 多数思想，$10,000，Macintosh 的前身 | 失败 |
| 1984 | **Apple Macintosh** | $2,500，"老想法，但做得好" | 成功 |

**这四行里最刺眼的事实是：唯一没失败的那台，用的是前面三台全部的"老想法"。** 变量不在技术，在价格、时机、开放性和生态。

## Xerox PARC 与 Alto（1973）

课件 p27 的条目在标签栏里写着一句定调的话：***Personal computing (GUI!)*** —— 个人计算（图形用户界面）。然后列出 Alto 的配置：

| 类别 | 课件原文 | 中文 |
|---|---|---|
| 计算 | *Alto Computer, a **personal workstation with local processor*** | **带本地处理器**的个人工作站 |
| 显示 | ***bit-mapped display***、*mouse* | **位图显示**、鼠标 |
| 界面 | *Modern graphical interfaces with **text and drawing editing, electronic mail, windows, menus, scrollbars, mouse selection**, etc.* | 现代图形界面：**文本与绘图编辑、电子邮件、窗口、菜单、滚动条、鼠标选择** |
| 网络 | ***Local area network (Ethernet), using shared resources*** | **局域网（以太网）**，用来**共享资源** |

**"local processor"（本地处理器）这一条是整台机器的定位。** 在此之前，用户坐在终端前，终端后面那台计算机是**别人的**。Alto 的处理器在**用户自己这台机器里** —— 这是"个人工作站"（personal workstation）与"分时终端"的分界线。

**"bit-mapped display"（位图显示）决定了画面怎么被改。** 字符终端的屏幕是一格一格字符单元，程序只能在字符格上写符号；**位图**意味着屏幕是一块可逐点寻址的画布。于是**窗口**（一块矩形区域可以独立持有自己的内容）、**绘图**（不是 ASCII 字符画，是真线真面）、**鼠标选择**（命中的是像素位置，不是第几行第几列）这三件事才成为可能。**界面从"文本的一维序列"变成"二维画布"，是这一行带来的根本变化。**

**"Local area network (Ethernet), using shared resources"常被跳读成"PARC 有网"。** 它的准确含义是：**打印机、存储、别的机器上的软件，都在网络后面，用户按共享资源来用** —— 而不是每台机器自己配齐。**这正是 1980 年代办公自动化的基础设施**，也是"个人计算"能成立的前提：一台机器不需要什么都有。

**然后是那个被单独标出来的细节：***"Display screen has **portrait orientation**"*** —— **显示屏是竖屏。**

**竖屏这件事决定了整个界面的隐喻。** 一块竖着的屏幕，比例接近一页纸（一张纸竖着拿的样子）。**于是"文档""页""桌面上的纸张"这套说法在竖屏上是字面成立的** —— 屏幕上真的有一张"纸"，可以摊开、可以对齐、可以叠起来。**这套隐喻后来原封不动地被搬到了横向的 CRT 显示器上，再搬到今天的屏幕里**，尽管它们的比例早已不匹配。

> [!note] 补充（课件外）
> 课件只写了"竖屏"这个事实，**没有解释为什么**。按史实，Alto 配的是 8½×11 英寸的竖式画布，这个"和纸一样大"的规格正是上面那套隐喻的字面来源。**竖屏的显示器后来在办公与出版场景反而更顺手**，这也解释了为什么下一页的 Star 8010 能赢下"桌面出版"这块市场。

### 课件顺手做了一次点名

p28 整页是一道 quiz：*"Quiz item!! Raise your hand if you know who it is. Have you ever heard of:"*，然后列了七个名字 —— **Ed McCreight、Chuck Thacker、Butler Lampson、Bob Sproull、Dave Boggs、Steve Wozniak、Steve Jobs**。p29 紧接着是 Xerox PARC (1973) 的图片，**并给了一个 1973 年的小型系统硬件展重聚页面网址**（`sphs73reunion.org`）。

**这七个名字的排列方式本身就是信息**：前五个是 PARC 那台机器背后的研究者，第六第七是把它推向大众的两个人（乔布斯从 PARC 看到界面，沃兹尼亚克造出机器）。**课件要传达的是"发明者与推广者不是同一批人"** —— 而这两批人在 1970 年代**在公众视野里都不存在**。

## Xerox Star 8010（1981）：第一个综合性 GUI

课件 p30 把 Star 8010 标为 ***Personal computing (commercialised)*** —— **个人计算（商业化）**。两条总纲：*"First commercial personal computer for **"business professionals**""*（第一台面向**"商务人士"**的商用个人计算机），*"First **comprehensive** GUI, using many ideas developed at Xerox PARC"*（第一个**综合性**图形界面，用了大量在 Xerox PARC -developed 的想法）。**注意引号里的 "business professionals"** —— 课件加引号是在提示：1981 年这台机器瞄准的是**企业里的办公人员**，不是程序员，不是爱好者。

八个设计要点（课件原文）：

| # | 课件原文 | 中文 | 它替掉了什么 |
|---|---|---|---|
| 1 | *familiar conceptual model (**simulated desktop**)* | 熟悉的概念模型（**模拟桌面**） | 抽象的命令行。屏幕上放的是你桌面上已有的东西 |
| 2 | *promoted **recognising/pointing** rather than **remembering/typing*** | 提倡**识别与指点**，而不是**记忆与打字** | 记住语法并准确击键 |
| 3 | *property sheets to specify **appearance/behaviour of objects*** | 用**属性表**指定对象的**外观与行为** | 去猜某个对象的默认设置 |
| 4 | *what you see is what you get (**WYSIWYG**)* | 所见即所得 | "所见非所得"：排版命令在另一层才生效 |
| 5 | *small set of **generic commands** that could be used throughout the system* | 一小组**贯穿全系统的通用命令** | 每个软件各发明一套操作 |
| 6 | *high degree of **consistency and simplicity*** | 高度的**一致性与简单性** | 同类操作在各处表现不同 |
| 7 | ***modeless interaction*** | **无模式交互** | 交互有"模式"（编辑模式 / 命令模式），换个动作要先切模式 |
| 8 | *limited amount of **user customisation*** | **有限的用户定制** | 各人改出各人的系统，界面因人而异 |

**第 2 条是这八条里唯一一条可以被测量验证的：识别与指点（recognising/pointing）取代记忆与打字（remembering/typing）。** 前面那一代界面要求用户**先记住**要敲什么、再准确**敲**出来；这一代只要求用户**看出**对的对象、再**指**它。前者考核记忆，后者考核知觉 —— **这是整个 HCI 里"用识别代替回忆"这条主张最早、最完整的一次表述。**

**第 7 条 modeless（无模式）也需要说清。** "模式"指**系统所处的状态**：同样一个按键或一次点击，在不同状态下含义不同，用户必须先知道自己现在在哪个模式里才能操作。**无模式 = 操作的后果只取决于你操作了什么，不取决于系统当时处于什么状态。** 这一条今天仍是评价文字编辑器、图形工具、甚至表单界面的标准之一。

**第 8 条"limited customisation"是一条克制的设计决策，值得单独看。** 前面七条都在给能力，第八条却在**收**。理由在第 6 条里：定制越多，一致性越难保证。**课件把它写成一条正面设计要点，说明 1981 年的设计者已经知道"给用户自由"和"系统一致"会互相打架。**

### 它是第一个按可用性工程造出来的系统

课件 p31 另起一条：***First system based upon usability engineering***（第一个基于**可用性工程**的系统），下面四个环节是设计过程：

| 环节 | 课件原文 |
|---|---|
| 1 | ***inspired design*** —— 有灵感的设计 |
| 2 | ***extensive paper prototyping and usage analysis*** —— 大量**纸面原型**与**使用分析** |
| 3 | ***usability testing with potential users*** —— 让**潜在用户**做**可用性测试** |
| 4 | ***iterative refinement of interface*** —— 对界面做**迭代式精修** |

**这四步就是今天的可用性工程流程的原样。** 关键在第 2 步的 **paper prototyping（纸面原型）**：在造出电子机器之前，先用纸和笔把界面画出来、在纸上走一遍流程。这条之所以能成立，是因为 1981 年的机器**极其昂贵**（$15,000），不可能靠"多造几台试"来迭代。

**所以这张表是本页最反讽的部分**：**第一个把可用性工程做全套的系统，也是第一个把用户研究做到这个程度的系统，然后它商业失败了。**失败的五条原因见 [[先驱者与定居者]]。

## Apple Lisa（1983）

课件 p32 把 Lisa 放在 "The user becomes important (1980–87)" 这一段里，条目只有四条：

- *based upon **many ideas in the Star*** —— 基于 **Star 里的许多想法**；
- *predecessor of **Macintosh*** —— **Macintosh 的前身**；
- *somewhat cheaper (**$10,000**)* —— **便宜一些：$10,000**；
- *commercial failure as well* —— **同样商业失败**。

**$15,000 → $10,000 是降价 33%，但结果从"失败"变成"同样失败"。** 课件用 **"somewhat cheaper"（便宜一些）** 这个说法，就是在提醒这条降价**不够**。三年之后再降到 $2,500 才算跨过门槛。

**Lisa 的失败还留给了 Macintosh 一份账单**：它是 Macintosh 的**前身**，而下一页列出的 Macintosh 成功原因里有一条就是 *"corrected mistakes of Lisa"*（**修正了 Lisa 的错误**）。

> [!tip] 类比
> 把 Star 8010、Lisa、Macintosh 想成一次连续的三次试射：第一次打靶，靶纸画得最准、瞄具调得最细，但站得太远（$15,000）；第二次往前走了一大步（$10,000），但还是没到能命中的距离；第三次既往前走了（$2,500），**又承认了前两次的经验已经成熟**（"old ideas but well done"），才命中。**中间两次的失败不是浪费，它们是第三次能做到"不必要做先锋"的前提。**

## Apple Macintosh（1984）

课件 p33 的第一条判语先立正：***"old ideas" but well done!*** —— **"老想法"，但做得好！** **课件在认可这台机器之前，先否定了它的原创性。** 这正是传承链的收口。

然后是成功原因，共七条（课件原文）：

| # | 课件原文 | 中文 |
|---|---|---|
| 1 | *sharp pricing (**$2,500**)* | 定价锐利：**$2,500** |
| 2 | *did not need to **trail blaze*** | **不必再做先锋** |
| 3 | *corrected mistakes of Lisa; **"mature" ideas*** | 修正了 Lisa 的错误；想法已经**"成熟"** |
| 4 | *market now **ready*** | 市场**已经准备好了** |
| 5 | *developer's toolkit **encouraged 3rd party non-Apple software*** | **开发者工具包**鼓励**第三方的非 Apple 软件** |
| 6 | *interface guidelines **encouraged consistency between applications*** | **界面指南**促成**应用之间的一致性** |
| 7 | *domination in **desktop publishing** because of **affordable laser printer** and excellent graphics* | 在**桌面出版**上称霸，靠的是**可负担的激光打印机**和优秀的图形 |

**第 1、2、3、4 条是一组：它们全部在说"你不用再冒险了"。** $2,500 让普通公司买得起；不用再开路，所以可以把资源全花在做好上；前人的错误已经被别人付过学费；市场已经成熟。**这四条里没有一条是技术突破。**

**第 5、6 条是生态。** 前一条让**别人**愿意给这台机器写软件（工具包降低了移植成本），后一条保证这些软件**看起来和用起来是一致的**（界面指南 = Star 8010 那八条设计要点的行业化版本）。**Star 8010 自己能做到"高度一致"，是因为它上面只跑它自己；Macintosh 要做到一致，只能靠一套公开的规范。** 这是从造机器到造生态的差别。

**第 7 条解释了一个课件没细说的市场事实**：Macintosh 的统治地位**不在通用办公，而在桌面出版**，而它靠的是**可负担的激光打印机**。**也就是说，决定这台机器命运的外部因素是打印机，不是处理器。**

### 课件当场提出的反问

p33 的最后三行，标题是 *"However:"*，下面只有一句：

> ***Pull to Trash to eject?*** —— **拖进废纸篓以弹出？**

**这是一道课堂提问，不是一道判断题。** 它的取意是**直接操纵范式自己的破绽**：整套 GUI 教用户"**指到目标上**就完成操作"（recognising/pointing），可一旦出现一个**不能指向的目标**（一个硬件设备、一张光盘、一张存储卡），这套范式就断了 —— 用户被训练出的直觉是"点它会有反应"，而这里"点它"没有意义。**课件把这个问题直接甩在成功那一页的末尾，意思是：卖得最成功的那台机器也没有解决范式本身的问题。**

> [!warning] 常见错误
> **三件事不要混：**
> 1. **Alto 不是商品**，它是研发机，课件从头到尾没写它卖过。商用化的起点是 **1981 年的 Star 8010**。
> 2. **Star 8010 与 Macintosh 不是同一台机器的两代**。中间还隔着 **Lisa（1983）**。课件明确说 Lisa 是"based upon many ideas in the Star"、是"predecessor of Macintosh"、**并且同样失败**。
> 3. **"第一个 GUI"有三种说法，别选错**：课件给 **SketchPad（1963）** 判的是"graphical user interface"的**构想**（见 [[个人计算的预言者们]]），给 **Star 8010（1981）** 判的是 **first comprehensive GUI**（第一个**综合性** GUI），给 **Macintosh（1984）** 判的是**"老想法但做得好"**。**三句都不等于"第一台 GUI 计算机"。**

## 一句话收束

> **Alto（1973）造出全部零件**（本地处理器 + 位图显示 + 鼠标 + 窗口/菜单/滚动条 + 以太网共享资源，竖屏是那套"文档"隐喻的字面来源）→ **Star 8010（1981）** 第一次把它们做成商品并第一次全套跑**可用性工程**，$15,000 卖不动 → **Lisa（1983）** $10,000，"同样失败" → **Macintosh（1984）** $2,500，**不技术创新、只做生态与定价**，成了；而课件在成功那一页的末尾当场追问 **"Pull to Trash to eject?"** —— 直接操纵范式在**指不到的东西**上断了。

## 相关笔记

- **枢纽**：[[交互的历史-知识地图]] — 这条链是这个域"从概念到商品"的主干
- **总纲**：[[交互方式的八个阶段]] — 第四段（图形显示）与第五段（微处理器）正是在 1973–1984 这十一年里合成一台机器
- **源头**：[[个人计算的预言者们]] — Alto 用上的那些想法，SketchPad、Dynabook、Computer Lib 在 1963–1974 年已经想过了
- **失败为什么**：[[先驱者与定居者]] — Star 8010 的五条失败原因和四条教训
- **另一条同代线**：[[Engelbart 与增强人类智力]] — 1968 年那台工作站的鼠标、文档间链接、弦式键盘，是 Alto 之前同一问题的另一批答案
- **同一个问题**：[[Memex 与超文本的预言]] — Star 8010 的"属性表""WYSIWYG""通用命令"背后，仍是 Memex 那套"让材料可被检索与改造"的企图
- **跨域**：[[../学科定位/可用性工程就是软件工程|可用性工程就是软件工程]] — Star 8010 的纸面原型 + 用户测试 + 迭代，就是这一页所说的可用性工程的四步
- **跨域**：[[../知觉与视觉/格式塔原则|格式塔原则]] — "模拟桌面"为什么看一眼就会用，是因为它把图元按接近性、相似性、包围这些原则组织好了
