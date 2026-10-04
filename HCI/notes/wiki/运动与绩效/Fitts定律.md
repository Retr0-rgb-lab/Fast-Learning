---
tags:
  - Fitts定律
  - 运动控制
  - 信息论
created: 2026-10-04
type: 知识点
aliases:
  - Fitts' law
  - 费茨定律
domain: [人机交互, 认知心理学]
course: COMP3423 Human-Computer Interaction
lecture: [L01, L02]
source: ["[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)", "[Human Part 2](<../../raw/02 COMP3423 Human Part 2 2026 09 20.pdf>)"]
---

# Fitts定律

> **一句话**：把人（的手指、鼠标光标、眼动）移到目标区域上所需的时间，是「**到目标的距离 ÷ 目标大小**」的函数 —— 距离越远、目标越小，花的时间越长；课件把它压成一句口号：**控件越宽、离指针越近，越容易点中**。形式化只有一行：$T = a + b\log_2(2D/W)$。

这一页是 [[../人类信息加工/人类信息处理器模型|人类信息处理器模型]]「输出 · 运动（Motor）」那一格的全部理论。课件主体在 Human Part 2 p26–p36，另有一道考题在 Introducing HCI 2 p58–p59。原文见 [Human Part 2](<../../raw/02 COMP3423 Human Part 2 2026 09 20.pdf>)、[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)。

## 人物、定律与公式：Fitts 1954 年说了什么

**人物**：**Prof. Paul Morris Fitts**。课件给的履历只有三句 —— 美国空军**中校**（Lieutenant-colonel of the US Air Force）、**美国空军人类工程处处长**（Head of US Air Force Human Engineering Division）、后来在**俄亥俄州立大学**（Ohio State U）和**密歇根大学**（U of Michigan）当教授。**这个履历本身就是论点的出处**：一个管空军人机工程的人，要的是"驾驶员在几秒内把操纵杆打到位"这种可测量的数，不是"手感好不好"。

**定律（1954）**，课件原话：

> *"Fitts' law (1954) states that the amount of time required for a person to move a pointer to a target area (e.g., finger to button) is a function of **the distance to the target divided by the size of the target**. Thus, the longer the distance and the smaller the target's size, the longer it takes."*

课件紧接着给它定位：*"Thus, Fitts' Law relates to the **Efficiency of system performance**"* —— 它讲的是**系统绩效的效率**，不涉及感知、记忆或问题解决。

**它建模的动作**（课件 p29 逐条列出）：是**人的运动的一个模型**；预测**从起始位置快速移动到目标区域**所需的时间；建模的是**指向（pointing）这个动作**。而且**真实世界与计算机两侧都能用**：真实世界用**手、手指，甚至眼动追踪（eye tracking）**；计算机上用**鼠标或摇杆**。课件 p26 的配图正是一架 **Spitfire 战斗机**的驾驶舱操纵杆 —— 那是"真实世界"那一侧的物证。

**口号**（课件 p29 单独排成大字的一句）：*"**The wider an interface widget and the closer it is to the pointer, the easier to hit it**"* —— 控件越宽、离指针越近，越容易点中。

**公式**：

$$
T \;=\; a \;+\; b\,\log_2\!\left(\frac{2D}{W}\right)
$$

| 符号 | 课件给的定义 | 物理意义 |
|---|---|---|
| $T$ | *movement time* | 移动时间：从出发到停在目标上的时间 |
| $D$ | *distance to the target* | 到目标的**距离** |
| $W$ | *width of the target (how big it is)* | 目标的**宽度** |
| $a$、$b$ | *empirically determined constants* | 两条**经验确定**的常数 |

## 模型来源：把人的运动系统当成一条信息通道

课件 p30 给了四条，全部是关于**这个模型站在什么理论上的**：

- **基于 Shannon 的信息系统理论**（*Shannon's theory of information systems*）；
- **人的运动系统被建模成一条用来传输信息的通道**（*modelled as channel used to transmit information*）；
- **任务有一定的难度，用 bit 计**；
- **通道有一定的带宽，用秒/bit 计**。

把 Shannon 的通信要素与 Fitts 的模型要素逐项对上：

| Shannon 的通信要素 | Fitts 模型里的对应物 | 单位 |
|---|---|---|
| 要传的消息 | 一次指向任务 | — |
| 消息本身的量 | 难度指数 **ID** | bit |
| 传输通道 | **人的运动系统**（以及设备） | — |
| 通道带宽 | 斜率 **$b$** | 秒/bit |

三句话必须记住：**大脑是信源、肌肉是信宿** —— 指向不是"手自己知道要去哪"，而是大脑把一条关于方向和距离的信息发给肌肉执行；**任务难度用 bit 计**；**通道带宽用秒/bit 计**。带宽的**倒数**就是每秒能传多少 bit，那正是绩效指数，见 [[难度指数与绩效指数]]。

**"宽度比"就是 ID 的定义**（课件 p30 的任务示意图）：

- 鼠标指针离目标 **$A$ 个像素（或 bit）** —— 这个 $A$ 叫 **amplitude（幅度）**；
- 目标是 **$W$ 个像素宽** —— 课件在图上把这个容差标注为 **tolerance（容差）**；
- **Index of Difficulty（难度指数，ID）**给出这个任务的难度（单位 **bit**），**同时取决于 $A$ 和 $W$**。

**ID 的三种写法**（课件 p31）：**原始式** $ID = \log_2(2A/W)$（*Original equation*）；**Shannon 式改写** $ID = \log_2(A/W + 1)$，或 $ID = \log_2(A/W + 0.5)$（课件注明 **when ID < 3 bits**）。三者的差别**只在那个常数**。因为 $\log_2(2x) = 1 + \log_2 x$，原始式比"裸"的 $\log_2(A/W)$ 恒定多 **1 bit**；Shannon 式把常数挪到**对数里面**（$+1$ 或 $+0.5$），使 $A \ll W$ 时 ID 仍有正值、不会掉到负数。三种写法只有在**几何差异很小（$ID$ 很小）的任务**上才会明显分家 —— 这就是课件特地点明「$ID<3$ bit 时用 $+0.5$」的原因。

> [!warning] 常见错误
> $W$ 是**目标宽度**，不是"指针到目标的距离"。距离是 $D$（或任务图里的 $A$）。把 $W$ 误读成距离，整条公式的量纲就没了：$\frac{2D}{W}$ 必须是无量纲比值。

## 为什么是对数：四条理由

课件用三页（p31–p34）专门讲这一节，页标题都是 **"Why a Logarithm?"**。四条理由各有各的性质：① 是运动本身的性质，② 是理论来源，③ 是数据拟合的结果，④ 是 ①③ 的数学后果。

**① 速度-准确权衡（speed-accuracy tradeoff）**

课件原话：*"When you try to move quickly to a target, it's harder to be accurate. If the target is farther away (D increases) or smaller (W decreases), it gets harder. **But the difficulty doesn't increase linearly; it increases more slowly as you keep making things harder**."*

拆开是两半：**$D$ 变大或 $W$ 变小都会让数就变大**（难度上升），**但上升得越来越慢**。这正是对数的形状 —— 线性会让任务成本按同样比例爆炸，对数把它压住了。

**② 信息论（information theory）**

课件原话：*"Paul Fitts was inspired by Shannon's information theory (like how much information can be sent through a noisy channel). He saw pointing as a process of '**transmitting information** from brain to muscles. **The logarithm comes from the way information capacity is calculated in bits**."*

关键在于：**信息量以 bit 计算，而 bit 与"可区分的选项数"之间是对数关系** —— 要区分 $N$ 种可能，需要的信息量是 $\log_2 N$ bit。指向任务正是一个多选一问题："该打中哪一个目标"。对数因此不是拟合出来的修辞，而是**信息计量的定义本身**。

**③ 经验拟合（empirical fit）**

课件原话：*"Fitts plotted how long it took people to point at targets of various sizes and distances. Found that **a logarithmic relationship fits the data better than linear**."*

这里的因果方向值得注意：**先有数据，后有对数**。Fitts 测量人们指向各种尺寸、各种距离目标所花的时间，把数据画出来，发现**对数关系比线性更贴合数据**。理由 ② 提供了事后解释，理由 ③ 提供了选择依据。

**④ 倍增/减半效应（doubling/halving effect）**

课件原话：*"The logarithm means that **doubling the distance or halving the width increases the difficulty by a fixed amount**"*：

- **距离 $D$ 翻倍，log 项增加 1**；
- **宽度 $W$ 减半，log 项也增加 1**；
- *"Making it twice as hard doesn't make users take twice as long, **but just a little bit**."*

数学上就是 $\log_2(2x)=1+\log_2 x$ 与 $\log_2(x/2)=\log_2 x-1$。**几何上"翻倍"只换来难度上固定的 1 bit。**

课件 p34 的收束句（这一节的中心）：

> *"The logarithm captures the **diminishing returns** in movement time as tasks get harder, **matching both theory and experiment**."* —— 对数捕捉的是**边际递减**（diminishing returns），并且**同时对上理论与实验**。

## 速度-准确权衡，以及为什么要做训练

课件 p35 把权衡写成两条对称的话：**更快就更毛糙**（*Faster is sloppier / inaccurate*），**更慢就更精确**（*Slower is precise / accurate*）。但课件立刻加了一条限制：

> *"**Whether speed of reaction leads to reduced accuracy depends on the task and the user.**"*

—— **"为了求快而牺牲准确"是否真的发生，取决于任务和用户。** 这句话否掉了"快必然不准"这种一刀切的说法，也是训练这件事存在的理由：

> *"That is why you do training: **fast + accurate**."*

**训练的作用不是让人放弃速度，而是把权衡曲线整体推到"又快又准"那个角上。** 课件给了两个被当作例证的对象：

- **Fafa Yim**，**Logitech 职业战队队长**，打《**英雄联盟**》（League of Legends）。课件 p36 的照片说明只有三个词：***fast and accurate***。
- **Spitfire 战斗机的驾驶舱操纵杆**（课件 p26 配图）。飞行员要在极短时间内把操纵杆打到某个位置，而打偏的代价是物理的。

> [!tip] 类比
> 这两个对象的共同结构是**高风险 + 高重复**：职业选手和战斗机飞行员每天在同一个动作上做上千次。这正是训练能改动回归常数 $a$ 和 $b$ 的条件，见 [[难度指数与绩效指数]]。

## 一个隐患：$W$ 是像素，但人感知的是视角

课件把 $W$ 明确定义为**像素宽度**（*"Target is W pixels wide"*）。但**人不是按像素感知的** —— 人感知到的是**视角**，即目标在视野里张开的角度。这条缝隙有两个后果：

1. **同一个按钮换到不同屏幕密度上，像素宽度不变、视角变了。** $W$ 的像素值没动，算出来的 ID 也没动，但用户**看见**的东西变了。
2. **$W$ 小到一定程度后，人眼察觉不到尺寸的进一步变化** —— 再缩小不改变视角，也就不改变感知难度。**在 ID 上它还在继续变差，在人的知觉上它已经不差了。**

视角如何度量、以及"大小恒常性"（size constancy）为什么成立，见 [[../知觉与视觉/视角度量与大小恒常性|视角度量与大小恒常性]]。

## 考题复盘：Fitts 定律与"胖手指综合征"

课件 Introducing HCI 2 p58 给出一道 **Exam Sample Item**，题目类目标成 **"Insight"**：

> **How is Fitts' Law related to the fat-finger syndrome (i.e., Japanese stock broker)?**

**"胖手指综合征"说的是哪一种失误**：在触屏上，用**手指**去点屏幕，手指落点的误差远大于鼠标光标的落点误差，于是**看起来很小的误按**会变成**真实的下单动作**。课件没有复述案情，只把它当作"指针很宽"的极端情形 —— 而这正是它要考的东西。

四个选项（原文照录，答案在 p59 勾在 **D**）：

| 选项 | 原文 | 判断 | 依据 |
|---|---|---|---|
| A | Stress worsens performance | ✅ 对 | 压力降低表现，因此更容易出错 |
| B | Fitts reckons with the **width ratio** between pointer and interface widget | ✅ 对 | 关键是**指针与控件之间的宽度比**，不是控件宽度本身 |
| C | The **logarithmic distribution** for fat fingers differs from, for instance, mouse pointers | ❌ 错 | 见下 |
| D | **A and B are correct** | ✅ **正解** | — |

课件 p59 的答案页原话：

> *"Fitts: The wider an interface widget and the closer it is to the pointer, the easier to hit it - **particularly when the pointer is wide as well (fat finger)**. So it's about the **pointer-to-target width ratio**, not target width alone. **And yes, people make more errors under stress**."*

拆成两句：**① 胖手指之所以要命，是因为指针本身很宽。** 口号里"更容易点中"的条件是控件宽、离得近；指针越宽，同样距离和同样控件宽度下**有效容差越小**，所以公式里起作用的是**比值**。**② 压力确实会让人更容易出错。**

**C 为什么是干扰项** —— 它说的"胖手指的对数分布与鼠标指针不同"，与这条定律的**全部前提**冲突：

1. 如果对数分布随指针类型而变，那么**一条公式就不能评估任意设备** —— 换一种指针就要重推一套系数，定律的通用价值当场消失。
2. 从模型内部看，**对数来自信息论**：指向任务的信息量以 bit 计，而这与用手指还是用鼠标**无关**。手指只是把有效宽度改小了一点，从而把 ID 推高了一点，**对数的形式没变**。
3. 课件强调的是 **width ratio（比值）**，不是**分布形状**。C 谈形状，A、B 谈比值与压力 —— 只有 A、B 是这条定律真正解释得了的东西。

> [!note] 课件在这一页给了什么、没给什么
> 课件 p22 给了这些**事实**：涉事机构是 **瑞穗证券（Mizuho Securities）**；画面是**社长福田真孝（Makoto Fukuda）**在记者会上鞠躬道歉；起因是在**新上市的小型招聘公司 J-Com Co.** 的股票上**下了一笔巨额错误订单**；后果有三条 —— **东京证券交易所的公信力受损**、**竞争对手 NTT（一家软件公司）股价上涨 11%**、**瑞穗交易亏损 US$331,000,000**。
> 课件**没有**给的：年份、下单量的具体数字、以及是哪家分行。
> 课件自己的判语是 *"this problem was merely about small buttons, stress, money loss, and losing face"* —— 它把这个案例定位成"指针很宽"加"压力"这两个因素的极端演示，后果的严重性是**第三根支柱**。完整案情见 [[../学科定位/可用性即销量|可用性即销量]]。

## 一句话收束

> 指向时间是 $\frac{\text{距离}}{\text{大小}}$ 的对数函数：因为快就不准，所以想又快又准就得练；因为一翻倍只买到一个 bit，所以做得更难不会让用户慢一倍。

## 相关笔记

- **本域**：[[运动与绩效-知识地图]] — 本域的 MOC，三个符号（ID / $b$ / IP）的分工表与复习路线都在那里
- **本域**：[[难度指数与绩效指数]] — 把本页公式里的 $a$、$b$ 拆出来，$IP=1/b$ 就是那条通道的带宽
- **本域**：[[反应时与行为时间尺度]] — 这里的 $T$ 只是"移动时间"，从接收刺激到完成动作还要算上反应时
- **上游**：[[../人类信息加工/人类信息处理器模型|人类信息处理器模型]] — 本页是它「输出 · 运动（Motor）」那一格的理论
- **跨域**：[[../知觉与视觉/视角度量与大小恒常性|视角度量与大小恒常性]] — $W$ 是像素，人感的是视角，这条缝隙在这里闭合
- **跨域**：[[../学科定位/人类与计算机的能力分工|人类与计算机的能力分工]] — "快 vs 准"这个权衡为什么是分工问题，不只是界面问题
- **跨域**：[[../学科定位/可用性即销量|可用性即销量]] — 瑞穗证券"胖手指"事件是 ID 算错的下游后果
- **枢纽**：[[HCI-自测题库]] — 本页末尾那道"胖手指"考题的完整选项与勾选位置
