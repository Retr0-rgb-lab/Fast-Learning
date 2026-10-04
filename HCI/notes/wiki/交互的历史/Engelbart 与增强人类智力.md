---
tags:
  - 交互历史
  - 增强人类智力
  - Douglas Engelbart
  - 鼠标
  - 协同工作
created: 2026-10-04
type: 知识点
aliases:
  - Augmenting Human Intellect
  - Douglas Engelbart
domain: [人机交互]
course: COMP3423 Human-Computer Interaction
lecture: [L01]
source: ["[Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>)", "[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)"]
---

# Engelbart 与增强人类智力

> **一句话**：Douglas Engelbart 的诊断不是"计算机还不够快"，而是**"世界在变复杂、问题在变紧迫，但人集体处理复杂与紧迫问题的能力没有按同样速度增长"** —— 既然**人**是瓶颈，那要增强的就是**人的智力**（augmenting human intellect），而不是替换掉人；他 1962 年给出的定义里三个动词全是关于**人**的：*approach*（接近问题情境）、*gain comprehension to suit his particular needs*（获得**符合自身需要**的理解）、*derive solutions*（导出解）。

课件 L01 第 1 份 p54–p58（1950 年代的诊断、1962 年 SRI 报告、1964 年第一只鼠标），第 2 份"Multidisciplinary"一节里 1968 年工作站那两行。原文见 [Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>) 与 [Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)。

## 问题：问题在长，人没有

课件 p54 整页是 Engelbart 1950 年代的一段自述引文，四句话，逻辑是一根链：

> *"...The world is getting **more complex**, and problems are getting **more urgent**. These must be dealt with **collectively**. However, **human abilities to deal collectively with complex / urgent problems are not increasing as fast as these problems**. If you could do something to improve human capability to deal with these problems, then you'd really contribute something basic."*
> —— 世界变得更复杂，问题变得更紧迫；这些问题必须**集体地**处理。**然而人类集体处理复杂／紧迫问题的能力，并没有跟问题一起以同样的速度增长。**如果你能做点什么来改善人类处理这些问题的能力，那你就在贡献一件根本性的东西。

**这段话里被大多数笔记漏掉的是"collectively"（集体地）这两次出现。** 他说的瓶颈不是某个人的算力、记忆力或注意力，而是**一群人协同处理复杂问题的能力**。所以他的方案落点必然是**协作**而不是**个人效率** —— 这一点决定了后来 NLS（Augmentation Research Center）那条线的形态。

**"not increasing as fast as these problems"（没有和问题长得一样快）是一个关于增长率的说法。** 注意它的精确形式：他没说人的能力**停滞**，也没说在**下降**，而是说**问题的增速超过了人的增速**。这个差距即使人均能力每年都在提高，也依然存在 —— 这才是"必须做点什么"的论证。

**最后那句"contribute something basic（贡献一件根本性的东西）"是动机，不是主张。** 他没说这很容易，也没说这已经在做。

## 1962 年的定义：augment 不是 replace

课件 p56–p57 整整两页（内容重复）给的是 SRI 报告 **《A Conceptual Framework for Augmenting Human Intellect》（SRI Report, 1962）** 的定义原文，课件给出网址 `http://www.1962paper.org/web.html`。定义分两句：

> *"**By augmenting man's intellect we mean** increasing the capability of a man to **approach** a complex problem situation, **gain comprehension to suit his particular needs**, and to **derive solutions** to problems. One objective is to develop **new techniques, procedures, and systems** that will better **adapt people's basic information-handling capabilities** to the needs, problems, and progress of society."*

**拆成三个层次看：**

| 层次 | 原文关键词 | 谁是主语 |
|---|---|---|
| **目标函数** | *increasing the capability of **a man*** | **人**。被增加的是"一个人的能力"，不是系统的吞吐 |
| **三个动作** | approach / gain comprehension to suit his particular needs / derive solutions | 全是**人**做的动作；机器没有出现在这三个动词里 |
| **手段** | *new techniques, procedures, and systems* that **adapt people's basic information-handling capabilities** | 新的技术、流程与**系统**。系统是**适配器**，人是它适配的对象 |

**"to suit his particular needs"（符合他个人的需要）这半句最容易被跳过。** 它明确否认了"给所有人一套统一的最优流程"这种思路 —— 增强的目标函数里带着**个人差异**这一项。

**"adapt people's ... capabilities to the needs"（把人的信息处理能力适配到需求上）把主客关系摆正了。** 是**能力去适配需求**，不是**需求去适配能力**。这一句正是课件 L01-a p63 那句总结（"system tending to human needs"）的 1962 年版本。

> [!warning] 常见错误
> **"augment"是"增强"不是"取代"。**课件的定义从头到尾没有一处提到自动化掉人，也没有把"更好的机器"当成目标。考试里如果答成"Engelbart 认为要用计算机取代人的某些能力"，方向就反了 —— 他要增强的那个对象就是人本身。同理，**报告标题不要写成"自动化"**：第 1 份课件写 *A Conceptual Framework for Augmenting Human Intellect*，第 2 份课件写 *Augmenting Human Intellect: A Conceptual Framework*（词序相反），两者指同一份 1962 年 SRI 报告。

## 1950 年代他就看见的两种场景

课件 p55 是 Engelbart 另一段回忆，形态是**两幅画面**。第一幅关于**屏幕与符号**：

> *"...I had the image of sitting at a **big CRT screen** with all kinds of symbols, **new and different symbols, not restricted to our old ones**. The computer **could be manipulated**, and you could be **operating all kinds of things to drive the computer**..."*
> —— 想象自己坐在一块**大 CRT 屏幕**前，上面有各种各样的符号，**新的、不同的符号，不受我们老符号的限制**；计算机可以被**操纵**，你可以通过**操作各种东西来驱动计算机**。

第二幅关于**同事与协同**：

> *"...I also had a clear picture that one's **colleagues could be sitting in other rooms** with **similar work stations**, **tied to the same computer complex**, and could be **sharing and working and collaborating very closely**. And also the assumption that there'd be a lot of **new skills, new ways of thinking** that would evolve."*
> —— 我还清楚地想象到：**同事们坐在别的房间里**、用**相似的工作站**、**连到同一个计算机系统**上，可以**极紧密地共享、协作**；并且还会有大量**新技能、新的思考方式**演化出来。

**这两幅画面对应后来系统里两个真实存在的部分**，而且都是 1950 年代就画出来的：

| 1950 年代的想象 | 落地成什么 |
|---|---|
| 大 CRT 屏、**新符号**、**可操纵** | 位图显示 + 窗口 + 图标 + 鼠标（**直接操纵**这一整套） |
| 同事在**别的房间**、**同一台计算机**、**紧密协作** | 共享文件系统、窗口系统、远程共享显示 |

**第三句"新技能、新的思考方式会演化出来"是这段引文里最 HCI 的一句。** 它意味着：界面改变之后，**人会跟着变** —— 新的符号体系会催生新的工作方法。这不是一个关于工具的判断，是一个关于**人与工具互相塑形**的判断。

## 1964 年的第一只鼠标

课件 p58 整页只有三行：

- *Douglas Engelbart (**1964**)*；
- ***First mouse***；
- *"Gamers, pay tribute!"*（游戏玩家们，致以敬意 —— 课件自己加的一句玩笑）

**这一页的信息量在年份上。** 1964 年鼠标就已经存在，**比它后来进商品晚了二十年**。课件在下一页（p59）专门用 Hertz 的"没用的实验"来解释这种时间差 —— 也就是说，**鼠标本身正是"先驱者"型的发明**。

> [!tip] 类比
> 第一只鼠标在 1964 年和第一台 Macintosh 在 1984 年之间的 20 年，是**"技术做出来了"和"技术被选中了"之间**的距离。这段距离里通常没有技术障碍 —— 阻塞它的是成本、时机、以及**没人知道该怎么用它**（直接操纵的交互范式要等到图形界面整机才成立）。

## 1968 年的工作站

L01 第 2 份在"Multidisciplinary"一节把 Engelbart 列进**人工智能（Artificial intelligence）**那一条下，给了两行：

- *"Douglas Engelbart (1962) **"Augmenting Human Intellect: A Conceptual Framework**"*（引 1962 年那份报告）；
- *"**In 1968, workstation with a mouse, links across documents, chorded keyboard**"* —— 1968 年的工作站已有**鼠标、文档间的链接（links across documents）、弦式键盘（chorded keyboard）**。

**这一行是 1962 年那份定义的第一批实物证据，四样东西同时出现：**

1. **鼠标** —— "operating all kinds of things to drive the computer"（p55 那句"操纵"）；
2. **文档间的链接** —— Memex 的交叉引用与链接链（[[Memex 与超文本的预言]]）变成了真的功能；
3. **弦式键盘** —— 一组键同时按下代表一个命令，用来**缩短高频命令的输入成本**（今天 Ctrl+这一类组合键的直系祖先）；
4. **一台工作站** —— 每人有自己的屏幕，而不是轮流用主机终端。

**注意第 3 样。** 课件把它列在"鼠标、文档链接"之间，不是随手排的：这三样加起来的共同点是**都在减少"从想法到动作"的转换成本**，而不是在增加功能。具体地说：

| 这三样各自替掉了什么 | 转换成本降在哪一步 |
|---|---|
| **鼠标** | 从**回忆命令串**变成**指向目标**。不用记住"选中"该敲什么 |
| **文档间的链接** | 从**抄下编号、再检索一次**变成**直接跳过去**。不用离开当前上下文 |
| **弦式键盘** | 从**逐字符击键**变成**一组键同时按下**。高频动作的击键次数被压缩 |

**这正是 1962 年定义里 *"better adapt people's basic information-handling capabilities"* 的具体落法** —— 三样都是**适配人的信息处理方式**，没有一样是替人做判断。

> [!note] 补充（课件外）
> 1968 年那次演示通常被称为 **"Mother of All Demos"**，演示内容包含 NLS 的文字编辑、窗口、鼠标、版本控制、协同与视频会议。课件这两行是从那份演示里挑出的三项设备特征。**课件未展开演示的具体过程**，本页也不补。

> [!warning] 常见错误
> **别把"增强人类智力"当成一句口号。**它有 1962 年的正式定义、有 1968 年的实物证据、有 1964 年的一个具体零件。把这一页只记成"Engelbart 发明了鼠标"就把最重的那部分丢了 —— 鼠标只是那套方案里最晚被大众认识的那一件。

## 一句话收束

> Engelbart 的论证链是"**问题增速 > 人的能力增速 → 且问题必须集体处理 → 所以要增强人（增强智力、而不是替换人）→ 手段是新的技术、流程与系统，让能力去适配需求**"；这套设想的第一批实物是 1964 年的鼠标和 1968 年那台同时具备**鼠标、文档间链接、弦式键盘**的工作站。

## 相关笔记

- **枢纽**：[[交互的历史-知识地图]] — 1962 年这份报告是这个域"为什么要做 HCI"论证的源头
- **总纲**：[[交互方式的八个阶段]] — 第四、五阶段（图形显示、微处理器）正是这一页两幅画面落地的地方
- **同代同题**：[[Memex 与超文本的预言]] — Bush 谈怎么存和取知识，Engelbart 谈怎么加工和协同知识
- **同代分歧**：[[Licklider 与人机共生]] — Licklider 1960 年就说人与机应当紧耦合成为**合伙关系**，比 Engelbart 更激进
- **那台工作站的最终归宿**：[[Xerox PARC 与图形界面的商业化]] — 1968 年的键盘、鼠标、链接在 1970 年代被 PARC 接过去重做成整机
- **结局**：[[先驱者与定居者]] — Engelbart 自己的系统在商业上是什么下场，课件没讲，但机制在这一页已经齐了
- **跨域**：[[../学科定位/人类与计算机的能力分工|人类与计算机的能力分工]] — "augment 而非 replace"是分工问题的历史答案
- **跨域**：[[../人类信息加工/人类信息处理器模型|人类信息处理器模型]] — "新技能、新思考方式会演化"对应模型里"学习与长期记忆"那一段
