---
tags:
  - HCI
  - 学科定位
  - 学科边界
  - 定义
created: 2026-10-04
type: 知识点
aliases:
  - HCI 的定义
  - HCI 学科边界
domain: [人机交互]
course: COMP3423 Human-Computer Interaction
lecture: [L01]
source: ["[Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>)", "[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)"]
---

# HCI-定义与学科边界

> **一句话**：HCI（human-computer interaction，人机交互）是**为人类使用而设计、实现、评估交互式计算系统**的学科；它的边界远宽于"界面设计"——用户旅程、组织内工作如何组织、任务如何分派、业务流程、算法，只要能改善用户体验，都归它管。

这一页要钉住两件事：**这门课管到哪儿为止**，以及**为什么"管界面"是误读**。素材取自课件 L01-a 的 p3（SIGCHI 1992 模型）、p16（为真实世界而计算）、p20–p24（订票流程与"HCI 不只是界面设计"）、p39（四个定义），以及 L01-b 的 p53–p54（这门学科实际在做哪三组活动）。课件原文见 [Introducing HCI 1](<../../raw/01 COMP3423 Introducing HCI 1 2026 08 27 1.pdf>)、[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)。

## 四个定义：同一学科的四个切面

课件 p39 一次给了四个定义，它们的差别不是措辞差别，而是**切的面不同**。

| # | 出处 | 原文要点 | 它把学科切在哪 |
|---|---|---|---|
| 1 | ACM SIGCHI Curricula for HCI | "…concerned with the **design, evaluation and implementation** of interactive computing systems for human use **and with the study of major phenomena surrounding them**." | 三个动词 + **还要研究围绕这些系统的主要现象** |
| 2 | CHI 1985 | "An **input language** for the user, an **output language** for the machine, and a **protocol for interaction**." | 交互的**三件套**：一门输入语言、一门输出语言、一个协议 |
| 3 | IBM Design Concepts | "It's simply the parts of the computer that you **see, hear, touch or talk to**. It is the set of all the things that allow you and your computer to communicate with each other." | **感官可及的外壳** |
| 4 | 课件未标注出处 | "A discipline concerned with the **design, implementation, and evaluation** of interactive computing systems for human use." | 一句话版，**最窄的那个** |

从这四句能读出四件事：

1. **三个动词是稳定的**：design、implementation、evaluation。#1 与 #4 词序不同（#1 是 design → evaluation → implementation，#4 是 design → implementation → evaluation），但集合完全一样。课件没有列出第四个动词。
2. **#1 最宽**。它比 #4 多出的半句是 *"and with the study of major phenomena surrounding them"*——**围绕系统的那些现象本身也在研究对象里**。
3. **#2 是最可操作的一种表述**：交互 = 用户的一套**输入语言** + 机器的一套**输出语言** + 两者之间的一个**协议**。这解释了 HCI 里"协议"一词的来路——它关心的不是像素，是**双方能不能对得上**。
4. **#3 最窄，而且窄得不对**。它把 HCI 说成"你看得见、听得见、摸得到、说得出得到的那部分"。这正是后面要推翻的读法。

> [!warning] 常见错误
> 别把 #3（IBM 那句）当学科定义背。它是四句里**唯一一句把学科缩成一堆硬件外壳的**，而它自己就印在一门明确讲"HCI 不只是界面设计"的课的 p39 上——课件列它是为了**对照**，不是采纳。考试问"HCI 是什么"，答案落在 design / implementation / evaluation 这三个动词上。

## SIGCHI 1992 的 HCI 模型：边界画在哪一层

课件 p3 印了一张 SIGCHI 1992 的 "Model of HCI"，结构是**三层横条，从上到下叠放**。

**第一层：Use and Context（使用与情境）**

- **U1** Social Organization and Work（社会组织与工作）
- **U2** Application Areas（应用领域）
- **U3** Human-Machine Fit and Adaptation（人机适配与适应）

**第二层：Human ｜ Computer（人 ｜ 计算机）**

| Human 一侧 | Computer 一侧 |
|---|---|
| **H1** Human Information Processing（人类信息加工） | **C1** Input and Output Devices（输入输出设备） |
| **H2** Language, Communication and Interaction（语言、沟通与交互） | **C2** Dialogue Techniques（对话技术） |
| **H3** Ergonomics（人体工程） | **C3** Dialogue Genre（对话体裁） |
| | **C4** Computer Graphics（计算机图形） |
| | **C5** Dialogue Architecture（对话架构） |

**第三层：Development Process（开发过程）**——四者成环：

$$
D1\ \text{（设计方法）}\ \longrightarrow\ D2\ \text{（实现技术与工具）}\ \longrightarrow\ D3\ \text{（评估技术）}\ \longrightarrow\ D4\ \text{（示例系统与案例研究）}\ \longrightarrow\ D1
$$

同一页上半部分就是**本门课自己的课程编号表**，讲次与编号一一对应：

| 讲次 | 主题 | 对应模型编号 |
|---|---|---|
| 1 | Use and context | U1–3 |
| 2 | Human information processing | H1 |
| 3 | Visual perception and computer graphics | H1, C4 |
| 4 | Language, communication, and dialogue techniques | H2, C2, 3, 5 |
| 5 | Ergonomics, I/O devices, haptics, sound | H3, C1 |
| ~~—~~ | ~~Design approaches and implementation~~（课件里已被划掉） | ~~D1–2~~ |
| 6 | Evaluation techniques and example systems | D3–4 |

**这张图本身就否定了"HCI = 界面设计"**：模型最外层的第一格是 **U1 Social Organization and Work**——**社会组织与工作在 1992 年就和"应用领域""人机适配"并排放在最外圈**。学科的外壳装的是社会，不是屏幕。

## 边界顶开：一张被代理渠道注销的已付款机票

L01-a p24 是一句反问：*"Given this example, is HCI just about interface design?"* 答案就在下一行：*"No, HCI also is concerned with the **customer journey, organization of work, task delegation, business processes, the algorithms**; anything to improve the user experience."*

它反问所指的 "this example"，是 p20–p23 一次第一人称的亲身经历（**2018 年 8 月**）。链条完整摊开：

1. 通过 **Expedia** 订并付清了一张 **KLM** 的经济舱机票。
2. 想用 KLM 自家里程（Flying Blue）升舱，于是上 **KLM 官网**操作。**网站上根本不存在"用里程支付"这个选项。**
3. 于是中止这次会话，并**假定原预订仍然有效**（升舱没付款，所以没生效）。
4. 写信问 KLM 为什么不能用他们自己的里程升舱。KLM 回复解释为什么不可能，理由"随便什么"。
5. **登机前 30 小时**在线值机，**整张预订已被取消**。
6. 打电话给 KLM，当场修复了这次取消。**幸好还剩 1 个座位**——否则就得改天走。
7. KLM 事后说明：是 **Expedia 取消了预订，因为票是在 Expedia 买的**；**KLM 处理不了代理售出的票**。

课件 p24 把责任逐条落到四家：

- **Flying Blue（里程体系）** 本该说明不能用里程升舱；
- **KLM 网站** 本该向代理方查询票是否由代理售出，并**对做不到的请求提前警告**；
- **Expedia** 本该把预订状态的变化通知客户；
- **KLM 处理不了 Expedia 的票属于业务流程问题，不该由客户承担**。

**这四条里没有一条是"把按钮做大"。** 故障点分布在里程规则、跨机构数据查询、状态通知、内部流程四处，正好逐项对应那句"用户旅程 / 组织内工作 / 任务分派 / 业务流程 / 算法"。更完整的案例处理见 [[../情境与文化/界面背后的组织与文化|界面背后的组织与文化]]。

## 为真实世界而计算：脏活才是 HCI 的战场

L01-a p16 的论点是：**逻辑形式取决于你相信世界是什么样**。课件用洗发水里的维生素 B 演示。

**（1）民间推理是肯定前件（modus ponens）**

$$
\begin{array}{ll}
A \to B & \text{规则：维生素 B 对头发好}\\
A & \text{事实：这瓶洗发水含维生素 B}\\
\therefore\ B & \text{所以它对我的头发好}
\end{array}
$$

课件在这一行旁边明确标注：**经验上为假的结论（empirically false conclusion）**。

**（2）假的根源在真值条件（iff）被写成了蕴含**

$$
\begin{array}{ll}
A \to B\ \text{实为}\ \mathrm{iff} & \text{维生素 B 是从营养酵母这类食物中被代谢得来}\ \Longleftrightarrow\ \text{它对我的头发有益}\\
\text{而洗发水里的维生素 B} & \text{没有被代谢（\emph{Shampoo is not metabolized}}）\\
\therefore\ \neg B & \text{洗发水里的维生素 B 对我的头发没有作用}
\end{array}
$$

**（3）所以代码的形状跟着你的信念走**

课件原话：*"Therefore, Python syntax depends on your beliefs as a coder."*

```python
# 民间信念：只要含维生素 B 就算
if (condition): code1 else: code2

# 列表推导式里同一个信念
[on_true] if [expression] else [on_false]
```

```python
# 有依据的信念：必须是「含维生素 B」AND/OR「来自食物」
if (cond1 AND/OR cond2) AND/OR (cond3 AND/OR cond4): code1 else: code2
```

**从"含 B"到"含 B 且来自食物"，条件从一个变成四个，还带上 AND/OR 的组合。** 这多出来的负担不是语法洁癖，是真实世界的模糊性。

课件把这套负担列成一句话加一张清单：*"Computing for the real world means you have to deal with **conditional truth, epistemics, semantics, meaning, pragmatics** — the messy empirical world. Therefore, **research precedes computing**."*

| 该对付的脏活 | 在洗发水例子里对应什么 |
|---|---|
| 条件真值（conditional truth） | 蕴含 vs 双向蕴含：谁在主张"当且仅当" |
| 认知论（epistemics） | 结论在经验上为假 |
| 语义（semantics） | "维生素 B"指哪一支——食物代谢来的，还是洗发水里的 |
| 意义（meaning）、语用（pragmatics） | 瓶身印的字和实际成分不是一回事 |

> [!warning] 常见错误
> 这一页不是在讲 Python 语法糖。它讲的是**需求的起点不是"用户想要什么"，而是"这个世界怎么运作"**——后者只能靠研究得到，所以课件说 **research precedes computing**（研究先于计算）。把它读成"先调研再写代码"就丢掉了力度：原话的意思是**没有研究，你的代码形式本身就是错的**（`if (condition)` 就是错的信念写出来的错形式）。

## 这门学科实际在做哪几组活动

L01-b p53–p54 把 design / implementation / evaluation 三个动词展开成可操作的清单。

| 组 | 课件标题 | 具体动作 |
|---|---|---|
| 1 | **Understanding users and their tasks**（理解用户及其任务） | 任务中心的设计（task-centred system design）：**列出任务样例**；用**任务中心走查（task-centred walk-through）**评估设计 |
| 2 | **Designing with the user**（与用户一起设计） | 用户中心设计与**原型（prototype）**；与用户共同设计的方法；**低保真与中保真原型**；**纸面原型（paper prototyping）**；**用用户评估系统与界面**：评估在设计中的角色、**观察人们使用系统以发现（界面）问题**、走查式用户测试 |
| 3 | **Designing visual interfaces**（设计视觉界面） | 日常物品的设计：**什么样的视觉设计才有效**；**超越屏幕的设计**：表征与隐喻（representations and metaphors）；图形屏幕设计：界面控件在屏幕上的**位置** |
| 4 | **Principles of design**（设计原则） | 设计原则、指南、**可用性启发式（usability heuristics）**；**用指南来设计并发现可用性问题**；**Fitts 定律**——控件越宽、离指针越近，越容易命中 |

第 1、2 组正对着模型最外层的 "Use and Context"：**先搞清用户和任务，再和用户一起做**。第 3、4 组对着 C4（计算机图形）与 D1（设计方法）。第 4 组那三条"原则/指南/启发式"说明：这一行的人不靠灵感，靠可复用的检查表——而检查表上的 Fitts 定律就是本课后面一整个讲次（H3、C1）的内容。

## 一句话收束

> HCI = **设计 + 实现 + 评估**三个动词的学科，1992 年的模型最外圈第一格写的是"社会组织与工作"；四个定义里最窄的那句（IBM 的"看得见听得到摸得到说得出"）恰恰是课件要推翻的那句。**判断某个问题是不是 HCI 的问题，只需问一句：这个故障能不能只靠改界面解决？不能——就是它的地界。**

## 相关笔记

- **本域枢纽**：[[学科定位-知识地图]] — 本域的论证骨架与四篇详细笔记的入口就在这一页定下的边界里
- **本域**：[[HCI 的多学科性]] — 回答"哪十个学科来协作完成上面那三组活动"，是本文档边界的执行层
- **本域**：[[可用性工程就是软件工程]] — 用项目超支的账，给出"为什么这条边界值得单开一门课"
- **本域**：[[可用性即销量]] — 用真实灾难说明边界顶得太窄会付什么代价
- **跨域**：[[../情境与文化/界面背后的组织与文化|界面背后的组织与文化]] — "用户旅程 / 业务流程 / 任务分派"这一层的完整案例处理
- **跨域**：[[../交互的历史/交互方式的八个阶段|交互方式的八个阶段]] — 边界本身随硬件与媒介的移动而移动，"输出语言"每换一次就变一次
- **跨域**：[[../运动与绩效/Fitts定律|Fitts定律]] — 第 4 组活动里那条"最常被直接考"的设计原则，它属于第二层的 H3 侧
