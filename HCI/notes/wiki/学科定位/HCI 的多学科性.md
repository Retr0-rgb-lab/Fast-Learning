---
tags:
  - HCI
  - 多学科
  - 跨学科
  - 学科协作
created: 2026-10-04
type: 知识点
aliases:
  - HCI 的多学科背景
  - Multidisciplinary HCI
domain: [人机交互, 认知心理学]
course: COMP3423 Human-Computer Interaction
lecture: [L01]
source: ["[Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)"]
---

# HCI 的多学科性

> **一句话**：HCI 不是一个学科，是**十个学科的协作面**——计算机科学、人工智能、工程、认知心理学、人体工程与人类因素、社会学、传播学、人类学、语言学、工业设计——**每一栏都配了一个具体例子，而其中至少两个例子证明：把某一项需求判断留给"计算机"或者"文化"，都会做错。**

课件 L01-b p37 把这十个学科列成一张清单，然后从 p38 到 p52 用**十四页**逐一给例子。L01-b p13（ACM SIGCHI 1982 的范围声明）和 p57（课程总结）给出"为什么必须多学科"的正式说法。原文见 [Introducing HCI 2](<../../raw/01 COMP3423 Introducing HCI 2 2026 09 05.pdf>)。

## 十个学科与它们各自的例子

| # | 学科 | 课件给的例子 | 这一栏提供的是 |
|---|---|---|---|
| 1 | **Computer science**（计算机科学） | RFID 病毒与 **RFID Guardian** 个人防火墙 | 硬件与协议层的**失效模式** |
| 2 | **Artificial intelligence**（人工智能） | Engelbart 1962《Augmenting Human Intellect》与 1968 年的工作站 | "机器该在哪一层帮上忙"的**历史判断** |
| 3 | **Engineering**（工程） | **Logitech MX Revolution** 滚轮鼠标 | 手感、**实现精度与耐久性** |
| 4 | **Cognitive psychology**（认知心理学） | 记忆过载导致的**四种坏密码** | 人的**记忆与注意**的硬限制 |
| 5 | **Ergonomics, human factors**（人体工程与人类因素） | **Maltron** 单手键盘、**PenAgain**、VR 步态识别服 | 身体尺寸、姿势、**负荷与安全边界** |
| 6 | **Sociology**（社会学） | 人们**如何建立社交网络** | 结构而非个体：网络、角色、**规范** |
| 7 | **Communication**（传播学） | 媒介线索谱 + 香农模型 + "工具与平台的类比模型" | 沟通的**通道、线索与信息形态** |
| 8 | **Anthropology**（人类学） | **来电显示在非西方文化中失效** | **在当地文化里什么算得体** |
| 9 | **Linguistics**（语言学） | 语音识别的**两种形态** | **符号系统**本身：说什么、谁在说 |
| 10 | **Industrial design**（工业设计） | **Duraflex** 防水键盘、**Bendi Board** 夜光键盘 | **物本身**：材质、外形、放置 |
| ＋ | 课件原文末尾还写了一个 **"&c"**（等等） | — | **清单是开放的**，不是十个封口 |

## 机器侧的四栏

### 1. 计算机科学：RFID 病毒与 RFID Guardian

**先看需求。** 课件 p38：*"US Department of Homeland Security wants driver's licenses with RFID tag that can be read from a distance to use for patrol at the US-Mexican border"*（美国国土安全部想要**带 RFID 标签的驾照**，能被**远距离读取**，用于美墨边境的巡逻）。配图是夜间边境上两名警员，其中一人正在读证件、另一人拿着笔记本电脑。课件随后用一行大字盖在照片上：**"But RFID tags can be reprogrammed!"**（但 RFID 标签**是可以被重新编程的**），并附了一张 RFID 天线标签的特写。

**这一栏贡献的就是这句"可以被重新编程"。**"能被远距离读"这个需求在计算机科学的视角下不只是"能不能读到"，而是"**读到的那个东西，本身还能不能被改**"。**可远距离读取 + 无源可写 = 一张能被伪造的通行证**，这是协议层的结论，不是需求文档能看出来的。

**再看对策。** 课件 p39 给出两个人和两件东西：**Melanie Rieback**，**Ubisec** 的研究员，在**阿姆斯特丹自由大学（VU University Amsterdam）发明了第一个 RFID 病毒**；她随后开发了 **RFID Guardian**，一个**个人防火墙**——它是一块**普通电路板，带两根天线和板载处理器**；它**拦截来自 RFID 读写器的信号**，像软件防火墙一样，**除非你希望那些信号到达你的 RFID，否则不放行**。课件给的场景是：**"比如你正通过海关的时候"**。

**把这两页连起来读**：一个计算机安全问题被发现，被转成一个**用户身边的物理装置**来解决，而它的开关逻辑直接对应"我现在是不是在过海关"这个情境。**这是"交互式系统"这个词最完整的一个实例。**
### 2. 人工智能：Engelbart 1962 与 1968

课件 p40 在 "Artificial intelligence" 这一栏只给了两行：**Douglas Engelbart（1962）"Augmenting Human Intellect: A Conceptual Framework"**（《增强人类智力：一个概念框架》），以及**1968 年实现了带鼠标、跨文档链接、复音键（chorded keyboard）的工作站**。**课件没给任何关于 AI 现状的评价**（课件未展开），可以确定的只是：Engelbart 那篇的贡献不是"造出了鼠标"，而是**先把目标定义成"增强人的智力"，再倒推需要什么样的机器**——在同期"机器翻译即将解决一切"的乐观气氛里，这是一个反向的目标设定。这条线的完整发展见 [[../交互的历史/Engelbart 与增强人类智力|Engelbart 与增强人类智力]]。

> [!note] 补充（课件外）
> 课件把 Engelbart 这条线与 AI 放在同一栏讨论，隐含的前提是"**AI 帮不上忙，因为要增强的对象是人**"。这个前提背后的历史背景（课件未提）：1950s 末到 1960s 初，机器翻译与机器感知领域刚经历一轮过度承诺，资助与乐观预期随后大幅回落。**这段历史不参与本笔记的论证，列在这里只为标明它是外部补充。**

### 3. 工程：MX Revolution 滚轮鼠标

课件 p41 在 "Engineering" 这一栏给的是 **Logitech MX Revolution 鼠标**，描述只有一句：***"Scroll through hundreds of pages with a simple flick of your finger"***（**手指简单一甩，就翻过几百页**）。

**这一栏提供的是"手感"和"造得出来吗"。**摆轮、加速度曲线、去惯性、轴承寿命——**这些是认知心理学给不出的，也不是工业设计能定的。**同一件产品里，工业设计决定它长什么样、认知心理学决定人为什么要甩一下、工程决定甩一下能翻几百页还不会坏。见同域《可用性工程就是软件工程》里同一只鼠标作为"试出来的设计"的类比。

### 4. 认知心理学：记忆过载长出四种坏密码

课件 p42 的原文：**"For instance, memory overload causes security issues"**（例如，**记忆过载会造成安全问题**）。四种坏密码逐条列了出来：

| # | 课件原文 | 中文 |
|---|---|---|
| 1 | Passwords too simple ('password') | 密码太简单（'password'） |
| 2 | Related to user self (birth date) | 和用户自身有关（生日） |
| 3 | Repeating same password everywhere | 到处重复用同一个密码 |
| 4 | Forgetting password (and account name) | 忘了密码（连用户名一起忘） |

课件的对策只有一句，而且是整页的重点：***"Programming routines to make up for user error"***（**写程序来替用户的差错兜底**）。**这一栏提供的是一条不可协商的硬限制**——"人的记忆容量有限"不是一个可以靠培训消化的建议，**它是一个会直接长成四种具体坏密码的机制**。四种坏密码里没有一种是"用户懒"：第 4 种（连用户名一起忘）恰恰是系统**要求人同时记住两个不相关的字符串**的产物。**所以对策只能落在"准确存储与回忆"这一格，也就是让机器去记**，这正是 [[人类与计算机的能力分工]] 准则一的应用。

### 5. 人体工程与人类因素：一只手、一支笔、一件 VR 服

课件 p43 在 "Ergonomics/human factors" 这一栏并列给了三件东西：**Maltron Single Handed Ergonomic Keyboard**（**Maltron 单手人体工程键盘**）、**Pacific Writing Instruments: The PenAgain**（**PenAgain** 笔），以及 *"Ergonomics" of a **virtual reality gait-recognition suit** in human-factors research*（人类因素研究中一件**虚拟现实步态识别服**的"人体工程"）。**三件里各有一层别家给不出的判据。**

- **Maltron**：标准键盘要求十指回到原位，单手键盘把这个要求整个取消。这不只是"更舒服"，**"取消了一条对人的要求"才是人因学的做法**。
- **PenAgain**：把笔的重心移到虎口可支撑的位置，减少长时间握持的静态肌负荷——判据是**疲劳出现在哪里**。
- **VR 步态识别服**：问的是"**穿着它的人能不能在虚拟环境里正常走路而不摔倒**"。**人因在这里不是"坐着舒不舒服"，而是"在系统设定的物理约束下会不会失去平衡"**——它是安全边界，不是舒适度。

## 社会侧的五栏

### 6. 社会学：人们如何建立社交网络

课件 p44 只给了一个短语：**"How people establish social networks"**（人们**如何建立社交网络**），配一张社交网络关系的图示。**课件没有展开**（这一栏的展开全部缺席），但这句短语的位置很关键：**它问的是"网络如何形成"，不是"某个人想加谁"。**前者是结构问题——角色、位置、互惠、边界；后者是功能问题。**在设计"加好友""分享给同事"这类功能时，只有社会学的问法会先问"这个人在这张网络里是什么位置"。**这一域的展开见 [[../情境与文化/情境与文化-知识地图|情境与文化]]。

### 7. 传播学：一条按"线索多少"排的媒介谱，附两个模型

课件 p45 的主图把通信媒介排成**从线索最少到线索最多**的一列：

> Ads / Flyers / Posters　→　E-mail / Texting / Letters　→　Social media　→　(Mobile) phone / Walkie-talkie　→　Video-conference / Avatars　→　**Face to face**

图上方单独挂着 **Social robots（社交机器人）**，并分成两支：**Remote controlled**（遥控）与 **AI driven**（AI 驱动）；两个向下的箭头把这两支分别指回谱上靠后的位置。谱下方是那条注记，全部照录：

> *"**More cues** to face to face communication in the medium → **supposedly** lead to better communication and interpersonal relationship"*
> （媒介中**越接近面对面沟通的线索越多** → **据说**会带来更好的沟通与人际关系）

**注意课件自己写的是 "supposedly"（据说），不是断言。**这一栏交付给 HCI 的**不是一个结论，而是一个待验证的假设**——而一个待验证的假设，正好是可以拿来指导设计的工具：**每加一种线索（语音、画面、身体在场、可回应的节奏），沟通质量就可能往上走一格。**

**同一页底部还有两个模型，都出自这一栏。**

**(a) 香农的通用通信模型**（Shannon's general communication model）——五个方框单向相连，箭头上标的是**消息与信号的区别**：

$$
\underbrace{\text{INFORMATION SOURCE}}_{\text{信息源}}\ \xrightarrow{\ \text{MESSAGE}\ }\ \underbrace{\text{TRANSMITTER}}_{\text{发射端}}\ \xrightarrow{\ \text{SIGNAL}\ }\ \underbrace{\text{CHANNEL}}_{\text{信道}}\ \xrightarrow{\ \text{SIGNAL}\ }\ \underbrace{\text{RECEIVER}}_{\text{接收端}}\ \xrightarrow{\ \text{MESSAGE}\ }\ \underbrace{\text{DESTINATION}}_{\text{目的端}}
$$

**中间那三步全是 signal，signal 在两端才变成 message。**这就是 HCI 那句"输入语言 / 输出语言 / 协议"的传播学版本：**协议管的是中间那段，两端的 message 才是人和人真正交换的东西。**

**(b) 工具与平台的类比模型**（*Analogical model for tools and platforms*）——五个剪影单向相连，**箭头上标的编号和词完全不同**：

$$
\underbrace{\text{DESIGNER}}_{\text{设计者}}\ \xrightarrow{\ \text{① INFORMATION}\ }\ \underbrace{\text{TOOL}}_{\text{工具}}\ \xrightarrow{\ \text{② DATA}\ }\ \underbrace{\text{PHYSICAL MEDIUM}}_{\text{物理媒介}}\ \xrightarrow{\ \text{② DATA}\ }\ \underbrace{\text{PLATFORM}}_{\text{平台}}\ \xrightarrow{\ \text{③ INFORMATION}\ }\ \underbrace{\text{USER}}_{\text{用户}}
$$

**读法：设计者交给工具的是信息（意图）；工具与物理媒介之间、以及物理媒介与平台之间流动的全是数据；只有到了平台→用户那一步，才重新变回信息。**也就是说，**整条链上被反复折腾的是数据，端点上才存在"意义"**——这正好解释了 HCI 为什么不能只做界面：**设计的产物是信息，但系统里流的是数据，而"变成信息"这件事只在最后一步发生。**

### 8. 人类学：来电显示在非西方文化中失效

课件用了**三页、三种素材**讲同一件事，分量逐步加重。**p46：一张诺基亚手机 + 一个气泡"Hi Bert"。** 页面标题 "Calling-line identification"，下面一行结论 **"Non-Western cultures may dislike this"**（非西方文化可能**不喜欢**这个功能）。引用的研究是：Konkka, K. (2003). *Indian needs. Cultural end-user research in Mombai*，收在 Lindholm, C., Keinonen, T., & Kiljander, H. (Eds.), *Mobile Usability. How Nokia Changed the Face of the Mobile Phone*（pp. 97–111），New York, London: McGraw-Hill。**"Hi Bert" 这三个字就是全部的论证**：来电显示让人**按名字打招呼**，而按名打招呼预设了"我认识你"；在一种**打招呼方式不是由亲疏关系决定**的文化里，这个功能**默认替你做了一次自我介绍式的亲昵**。

**p47：同一部手机 + 一张印度的苦行僧（sadhu）照片 + 一个黄色气泡"Hi Sandjai" + 一个红叉**（同一篇引文）。**这次红叉指向的不是来电显示，是"用名字称呼"这个动作本身**——对一个宗教苦行者直呼其名（音译自 Sandeep）**不成立**。**能显示姓名不等于应该使用姓名。**这一层比 p46 更狠：**p46 是"这个功能可能让人不舒服"，p47 是"这个功能可能做出一个在该文化里不可接受的行为"。**

**p48：只有一句标题 "Who's underneath?"**（底下是谁？），配图是同一部手机上的邮件/联系人列表（可见 "New messages (1)"、若干条 "meeting …"、以及 "To-Do items"）。**课件没有解释这句话问的是来电人还是联系人条目**（课件未展开）——但它把问题摆在了那里：**一个显示出来的名字，在当地文化里到底唯一地指向谁？**

### 9. 语言学：语音识别的两种形态

课件 p52 的这一栏讲的是一个功能有两种完全不同的实现目标。原文：**"Two forms of speech recognition"**（语音识别的两种形态）：

| 形态 | 原文 | 它回答的问题 | 失败的样子 |
|---|---|---|---|
| ① | **Converts spoken words to machine-readable input (text)** —— 把说出的话转成机器可读**输入**（文本） | **说了什么？**（转写） | 词转错了，但人还是同一个人 |
| ② | **Identifies the speaker according to acoustic input (voice verification)** —— 根据声学**输入**识别**说话人**（**声纹验证**） | **是谁？**（验证） | 词全对，但认错了人 |

课件在同一页还列了 **Large Language Models（GPT、DeepSeek）**（页面来源标注 *Adapted from Statistical Methods for Speech Recognition, F. Jelinek*），以及四个产品：**Siri、Alexa、Google Assistant、Cortana**。**这一栏提供的是"符号系统"的分层**：同一个"语音"输入，**先要决定它是被翻译成符号（文本），还是被用来辨认符号的来源（身份）**，而这两种用法对系统的要求完全相反——**转写要求系统听得准，身份验证要求系统分得开。**

### 10. 工业设计：Duraflex 防水键盘与 Bendi Board 夜光键盘

课件 p53 这一栏给的是两件**物**：**Duraflex Comfort 键盘**（新版）**能抗水、抗酒精，抗其他消毒液，包括更"烈"的清洁用品**（产品文案是 "Stash it in your bag"，塞进包里就行）；**Bendi Board** **在黑暗中会发光**（lights up in the dark）。**这一栏的判据是"这个东西本身在环境里成不成立"。**一个在办公室里的键盘通常不为"被水淋到"设计，而"抗水、抗酒精、抗消毒液"这三个词连在一起指向的是**一个会被带到医院、厨房、车间、户外被清洗的物**——**"抗消毒液"不是"更防水"，它是一个关于"这东西将被用在哪里"的判断。**Bendi Board 会发光指向的则是"暗环境"这个使用条件：它没说"更好看"或"更省电"，**它说的是这个物在一个具体环境里自己解决了可及性问题。**这是工业设计与可用性工程交叉的地方：**可及性有时候靠改变物本身解决，不靠提示用户开灯。**

## 越界的那个例子：深水埗的竹架搭棚工

课件 p50 是"人类学"这一栏里最有分量的一页。页面上方是一句引语：

> *"What I will not have is that **some Californian nerd** decides how **my bamboo scaffolder in Sham Shui Po** is going to operate his telephone."*
> （我不能容忍的是：**某个加州极客**来决定**我在深水埗的竹架搭棚**该怎么用他的电话。）

页面下方是一张真人在**香港深水埗**的竹棚架上作业的照片，照片上叠着两个气泡：

- 左边一个粉色气泡来自一个**盘腿而坐、面前放着笔记本电脑的男人**，说的是：**"Relax, I often do the lotus position, so I know Asian culture"**（放轻松，我经常打坐，所以我懂亚洲文化）。课件这张图的意思很明确：**这是一个自称懂亚洲文化的"加州极客"式的形象。**
- 右边一个绿色气泡来自**搭棚工人本人**，说的是一句**粤语**：

> 「**電話根本就冇用。我需要用對手做嘢，唔想分心。**」
> （译文：**电话根本没用。我要用双手干活，不想分心。**）

**这一页的分量在于它同时否定了两个假设。**

**第一个被否定的是"用户想要这个功能"。**一个每天攀在竹架上、靠双手作业的人，**电话根本不在他的需求里**——来电显示对他不是"不好用"，是**这个动作在他所处的物理处境中毫无意义**。他的手就是他的工作器具，手机会分散他唯一不能分心的东西。

**第二个被否定的是"我懂你的文化"。**盘腿打坐的男人说自己懂亚洲文化，而**真在亚洲干活的这位，用一句粤语直接把话头掐断了**。**这就是人类学这一栏交付给 HCI 的东西：一个外部的、能自我宣称"我懂"的观察者，其资格本身要被验证，而验证的方法只有一种——让被观察的人用自己的语言把话说完。**

**这页也把"谁在决定"摆到了台面上。**引语里的动词是 **decides**（决定）——主语是"某个加州极客"。**功能列表、界面默认值、隐含的使用场景，全都是这个"决定"的产物。**当一个功能被默认设计成"接到来电时按名字打招呼"时，真正做出这个决定的人不在现场。

## 为什么必须是十个学科：两处正式说法

**说法一，ACM SIGCHI 1982（L01-b p13）。** 那一年课件用一整页印了 SIGCHI 的范围声明，同页还列了三个期刊（*International Journal of Man-Machine Studies* 1969 起、*International Journal of Human-Computer Studies*、*ACM Transactions on Computer-Human Interaction*）：

> *"The scope of SIGCHI consists of the study of the **human-computer interaction process** and includes research and development efforts leading to the **design and evaluation of user interfaces**. The focus of SIGCHI is on **how people communicate and interact with computer systems**."*

**"how people communicate and interact" 这半句，需要传播学、语言学和社会学同时在场才写得完。**

**说法二，课程总结（L01-b p57）。** 一句更直接的：

> *"**Various disciplines should collaborate** if a computer system wants to be **fit for human use**: computer science, social science and psychology, ergonomics, and interaction design."*
> （如果一个计算机系统想**适合人类使用**，**各个学科应当协作**。）

注意这句总结把十个压成了**四类**：**计算机科学 / 社会科学与心理学 / 人体工程 / 交互设计**——对应 SIGCHI 1992 模型最外层的 "Use and Context"、中间的 "Human ｜ Computer"、和最下面的 "Development Process"。**十个学科是这四类的展开，不是十个独立的方向。**

> [!warning] 常见错误
> 别把"多学科"读成"什么都沾一点"。**这十个学科每一个都在本页配了具体的、别的学科答不出来的问题。**判断某个问题归哪一栏，标准是"**这栏的方法能给出答案**"，不是"这个话题听起来很相关"。**"人走路会不会摔倒"是人体工程，"两个人怎么打招呼"是人类学，"这个功能用户想不想要"是社会学——三者的研究方法完全不同，不能互相替代。**

## 一句话收束

> HCI 的十个学科各自带一个例子进来：**计算机科学带来"RFID 标签可以被重新编程"，人工智能带来 Engelbart 1962 的"要增强的是人"，工程带来一甩手翻几百页的手感，认知心理学带来记忆过载长出的四种坏密码，人体工程带来单手键盘与 VR 里会不会摔倒，社会学带来网络而非个体，传播学带来"线索越多据说沟通越好"这个待验证假设，人类学带来"Hi Sandjai"这个红叉和深水埗那句"电话根本就冇用"，语言学带来语音识别的两种形态，工业设计带来抗消毒剂的键盘和夜里会发光的板。**

## 相关笔记

- **本域枢纽**：[[学科定位-知识地图]] — 本页是"论据层 3：划边界"的执行面，要与同域的"HCI-定义与学科边界"配套读
- **本域**：[[HCI-定义与学科边界]] — SIGCHI 1992 模型的三层结构，就是这十个学科的组织方式；SIGCHI 1982 的范围声明也在那里对照
- **本域**：[[人类与计算机的能力分工]] — 认知心理学那一栏的记忆过载，在能力分工表上有一个精确的落点（"准确存储与回忆"归机器）
- **本域**：[[可用性工程就是软件工程]] — 工程那一栏的 MX Revolution 滚轮鼠标，是"快速原型、用户测试"在硬件上的对应物
- **本域**：[[可用性即销量]] — "安全与隐私"那一档后果，RFID 可重写与人脸识别绕过是同一结构
- **跨域**：[[../交互的历史/Engelbart 与增强人类智力|Engelbart 与增强人类智力]] — 人工智能那一栏例子的完整版本，从 1962 的框架到 1968 的工作站
- **跨域**：[[../情境与文化/情境与文化-知识地图|情境与文化]] — 社会学与人类学这两栏在本域另一侧的展开，包括深水埗那个例子的更完整语境
- **跨域**：[[../人类信息加工/人类信息加工-知识地图|人类信息加工]] — 认知心理学那一栏的系统展开
