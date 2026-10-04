---
tags: [索引, MOC, WD]
course: COMP3421
---

# Web 应用开发知识库 · COMP3421 MOC

> 香港理工大学 **COMP3421 Web Application Design and Development** 课程知识库。
> 按**主题**组织（不按讲次），全部笔记通过 Obsidian **双链（wikilink）**互联。
> **每篇笔记都是自足的** —— 单独打开任何一篇都能读懂。

> [!important] 第一次来，先读这一篇
> [[课程场景与阅读约定]] —— 交代了课程的原始资料在哪、本库覆盖到第几周、笔记里那些"示例站""课程调色板"是怎么来的。**不读它直接进主题，读到中途会觉得某些话没有来由。**

## 使用方式

- **按主题浏览** → 看下面的 [[#八大主题]]
- **零散复习** → 直接打开 `notes/wiki/<主题>/` 下任意一篇，每篇末尾的「关联」列出它的邻居
- **查原始出处** → 笔记顶部的出处行指向 `notes/raw/` 里的 6 份 PPTX
- **看连接** → [[#跨主题的关键连接]]，跨目录、单独值得记的线索都收在这里

## 八大主题

### 全栈概览 · The Big Picture（Week 1）

回答"一个网页请求从敲下地址到看见页面，中间到底发生了什么"。

- [[Web应用与客户端-服务器模型]] — **客户端—服务器模型**、一对多、双方唯一的共同语言是 HTTP
- [[三层架构]] — **浏览器 / 服务器 / 数据库**三层，客户端↔服务器走 HTTP、服务器↔数据库走 SQL
- [[HTTP与URL]] — 请求与响应的**解剖结构**、URL 六个组成部分各自的职责
- [[后端技术栈]] — Node.js → Express → REST/CRUD → WebSocket/SPA/部署（Week 1 概览层级）
- [[性能与可扩展性]] — 缓存、CDN、HTTP/2；以及**大型网站的五层架构**与"每块独立扩容"
- [[课程路线图]] — Week 1–13 每周建什么，Week 13 结束时会什么

### HTML 标记 · The Structure（Week 2）

回答"HTML 管什么、不管什么"。

- [[HTML是什么]] — 结构而非外观、浏览器如何渲染、发展史与 living standard
- [[元素与标签语法]] — **一个元素五部分**、成对与 void 标签、嵌套与缩进、完整文档骨架
- [[属性]] — `name="value"`，以及 CSS 与 JavaScript 都要靠它**抓元素**
- [[文本语义]] — 标题层级、`<strong>`/`<em>` 的**语义**用法、空白折叠
- [[链接与图像]] — `<a>` 的 `href` 各种形态、`<img>` 必须写 `alt`、`<picture>` 响应式图像
- [[图像映射]] — `usemap` + `<area>`，rect/circle/poly 三种形状与坐标读法
- [[列表与表格]] — ul/ol/dl，表格只用于数据、`rowspan`/`colspan`
- [[表单与输入]] — `action` + `method`、input 的类型与属性
- [[表单验证与可访问性]] — `label for`、浏览器**免 JS** 的原生校验、`fieldset`
- [[媒体元素]] — `controls` 一个属性带来播放器、`<source>` 格式回退
- [[SVG矢量图形]] — 用标记描述图形、viewBox 坐标系、path 命令、SMIL/CSS 动画
- [[容器与语义化]] — div vs span、block vs inline、语义化容器与 landmark
- [[DOM与开发者工具]] — HTML 变成**活的树**、节点家族、Elements 与 Console

### CSS 基础 · Styling the Web（Week 3）

回答"一条声明由什么组成，以及颜色的单位、字体的写法"。

- [[样式声明与内联]] — `property: value;` 这一个模式，以及 `style` 属性的一次性
- [[颜色表示法]] — **命名 / hex / rgb() / hsl() 四种写法**，以及课程调色板
- [[透明度与叠加层]] — `rgba()` 的 alpha、`opacity`、scrim 与 caption
- [[长度与单位]] — 绝对单位、相对单位、**`em` vs `rem`**、视口单位
- [[文本与字体]] — 文本对齐装饰间距、`font-family` 回退栈、`font` 简写、`@font-face`
- [[继承]] — **文本属性流下去，盒属性留在原地**

### CSS 选择器与层叠 · Selectors & Cascade（Week 4 上）

回答"规则怎么找到元素、两条规则打架时谁赢"。

- [[CSS引入方式]] — 内联样式的四个问题，**外链 / 内嵌 / 行内**三种引入
- [[规则结构与选择器分类]] — rule-set 的形状，**五类选择器**总表
- [[简单选择器]] — 元素、id、class、通配符；**class vs id**
- [[组合选择器]] — 分组、后代 `A B`、子代 `A > B`、相邻 `A + B`、通用兄弟 `A ~ B`
- [[属性选择器]] — `[attr]`、`^=`、`$=`、`*=`
- [[伪类与伪元素]] — 状态伪类（**LVHA 顺序**）、结构伪类、伪元素；`:` 是状态 `::` 是部分
- [[层叠与优先级]] — **来源顺序**、**优先级 (0,0,1) 计分**、`!important`

### 盒模型 · Box Model（Week 4 下）

回答"一个元素在页面上占据的那块地方由什么组成"。

- [[盒模型五层]] — **每个元素都是一个盒子**，content/padding/border/margin/background
- [[边框与圆角]] — border 的三要素、1–4 值的顺时针顺序、`border-radius` 的几何本质
- [[内外边距]] — padding 会被绘制、margin 永不绘制、**margin collapsing**
- [[尺寸与盒模型计算]] — `width` 指什么由 `box-sizing` 决定、**margin 居中**、`max-width`
- [[背景与混合模式]] — 背景六属性与简写、`mix-blend-mode`
- [[图像精灵]] — 一张图多个画面、`background-position` 取格、`steps()` 播帧

### 布局与定位 · Layout（Week 5 上）

回答"盒子怎么摆"。

- [[常规流]] — 不写任何 `position` 时浏览器做的事
- [[定位方式]] — **static / relative / absolute / fixed / sticky** 五值对照，偏移的符号规律
- [[层叠顺序与z-index]] — 谁盖住谁、z-index 只在层叠上下文内比较
- [[Flexbox]] — **一根轴**上的布局（自学页）
- [[Grid]] — **行列两维**布局（自学页）
- [[响应式与媒体查询]] — viewport、流式布局、`@media`、**移动优先**

### 动效与其他 CSS · Motion & Misc（Week 5 下）

回答"怎么动起来，以及收尾用的那些属性"。

- [[变换transform]] — 移动/旋转/缩放/倾斜，**不引起重排**、不占额外空间
- [[过渡transition]] — 把状态突变变成渐变、计时函数、`transition: all` 的坑
- [[关键帧动画]] — `@keyframes` 配方 + `animation` 运行、多段停靠点、`steps()`
- [[动效与可访问性]] — `prefers-reduced-motion`：**去掉运动，不是去掉意思**
- [[CSS变量]] — `--name` 定义、`var()` 读取、作用域与主题切换
- [[阴影]] — `box-shadow` 五个值、focus ring 与 inset
- [[display与隐藏]] — 外部盒类型、**隐藏元素的三种方式对比**
- [[图标]] — 图标字体 / 内联 SVG / 图片文件，各自的代价

### 色彩理论 · Colour Theory（Tutorial 1）

回答"颜色怎么来的、怎么配、怎么不瞎"。

- [[色彩成因]] — **减色**（颜料）与**加色**（光），为什么屏幕和打印机对不上
- [[色轮与三大参数]] — 色相/饱和度/明度，**HSV 与 HSL 的第三个通道不一样**
- [[配色方案]] — **七种**在色轮上取点的几何规则，以及各自何时出错
- [[对比度与可读性]] — **对比度是算出来的数**、AA/AAA 阈值、颜色不能是唯一信息载体

## 跨主题的关键连接

这些连接跨越目录，是复习时最值得单独记的线索：

| 连接 | 说明 |
|---|---|
| [[元素与标签语法]] → [[CSS引入方式]] | HTML 的 `style` 属性是 CSS 的**最差放法**，也是理解 CSS 存在理由的起点 |
| [[属性]] ↔ [[简单选择器]] | `class` / `id` 是 HTML 留给 CSS 和 JS 的**同一批钩子** |
| [[盒模型五层]] ↔ [[常规流]] | 盒子模型讲"一个盒子"，常规流讲"多个盒子怎么排" |
| [[尺寸与盒模型计算]] → [[Flexbox]] | `box-sizing: border-box` 是 Flexbox / Grid 能算得对的前提 |
| [[层叠与优先级]] ↔ [[CSS引入方式]] | 三种引入方式的强弱顺序，就是层叠的第一条规则 |
| [[继承]] ↔ [[CSS变量]] | 变量的继承**不是**普通属性继承的例外，而是同一套机制 |
| [[颜色表示法]] → [[CSS变量]] | 课件明确说过"同一个色值不要写两遍"，变量就是那个解法 |
| [[颜色表示法]] ↔ [[色彩成因]] | 同一页的四种写法，两篇分别讲**怎么写**和**为什么是这个色** |
| [[色彩成因]] → [[颜色表示法]] | 屏幕是**加色**设备，这决定了 CSS 颜色用 RGB 而不是 CMYK |
| [[对比度与可读性]] ↔ [[透明度与叠加层]] | scrim 与 caption 存在的唯一理由就是对比度 |
| [[变换transform]] ↔ [[层叠顺序与z-index]] | 两者都**不引起重排**，这是它们便宜的原因 |
| [[过渡transition]] ↔ [[关键帧动画]] | 一个要触发、一个自己跑；`steps()` 同时是帧动画的手段 |
| [[SVG矢量图形]] ↔ [[图标]] | 图标三条路里，内联 SVG 就是 Week 2 那套 path |
| [[HTML是什么]] ↔ [[DOM与开发者工具]] | DOM 是 HTML 解析后的结果，DevTools 看的就是它 |
| [[表单与输入]] ↔ [[容器与语义化]] | 表单能不能用，取决于容器语义对不对；`label` 的正确用法也依赖语义化 |
| [[三层架构]] ↔ [[后端技术栈]] | 三层是**结构**，后端栈是每一层的**实现选择** |
| [[性能与可扩展性]] ↔ [[响应式与媒体查询]] | 响应式解决"屏幕窄"，CDN 解决"离得远"，是两类问题 |

## 原始资料

`notes/raw/` 下是六份课件 PPTX 原件。笔记中的「课件原文见 …」即指向对应文件：

- [Lecture_01_Overview.pptx](<notes/raw/Lecture_01_Overview.pptx>) — Week 1 全栈概览
- [Lecture_02_HTML.pptx](<notes/raw/Lecture_02_HTML.pptx>) — Week 2 HTML
- [Lecture_03_CSS.pptx](<notes/raw/Lecture_03_CSS.pptx>) — Week 3 CSS I
- [Tutorial_01_ColorTheory.pptx](<notes/raw/Tutorial_01_ColorTheory.pptx>) — Tutorial 1 色彩理论
- [Lecture_04_CSS.pptx](<notes/raw/Lecture_04_CSS.pptx>) — Week 4 选择器 / 层叠 / 盒模型
- [Lecture_05_CSS.pptx](<notes/raw/Lecture_05_CSS.pptx>) — Week 5 布局 / 动效 / 零散属性

> 课件原件保留了原图（色卡、图示、对比演示）。**wiki 笔记里的例子是重新叙述的通用版本**，写在 [[课程场景与阅读约定#四、两个需要预设的场景（明确交代）|约定的示例站]] 上，与课件里的具体截图不一定逐字对应 —— 需要看原图时直接翻 PPTX。

## 沉淀日志

见 [[log]]。
