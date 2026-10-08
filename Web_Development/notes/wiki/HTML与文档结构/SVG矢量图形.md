---
tags: [WD, HTML标记, SVG, path, viewBox, 矢量图形]
domain: [Web 应用开发, HTML]
course: COMP3421
lecture: L02
---

# SVG矢量图形 · SVG Vector Graphics

> **一句话**：SVG 用**标记而不是像素**描述图形，所以放大不糊、可以读可以改、可以交给 CSS 上色——而坐标的规则全在 `viewBox` 里，最后连动画都能**零 JavaScript** 跑起来。

课件原文见 [Lecture_02_HTML.pptx](<../../raw/Lecture_02_HTML.pptx>)。本篇覆盖课件的 "What Is SVG?"、"Basic Shapes"、"More Shapes — polyline & polygon"、"Fill, Stroke & Opacity"、"Paths & the viewBox" 和 "Animated SVG in Action" 六部分。

## 一、SVG 是什么

| 课件的说法 | 展开 |
|---|---|
| **Scalable Vector Graphics** | **用标记描述图形，而不是用像素** |
| **Crisp at any size** | 放大缩小**永远不糊** |
| **Text-based** | 一个**纯文本**格式，可以读可以改 |
| **Styleable with CSS** | 颜色和尺寸**可以从样式表改** |

```html
<circle cx="50" cy="50" r="40" fill="blue">
```

这一行就是"一个圆，用标记描述"：圆心 (50,50)、半径 40、填蓝色。**没有一张图片文件，只有三个数字和一个颜色。**

> [!note] "vector" 到底 vector 什么
> 位图（PNG / JPEG）存的是"这个像素是什么颜色"，所以放大必然要**插值**，边缘就糊了。SVG 存的是"这里有个圆，圆心在这、半径这么大"——**浏览器在显示时才把它算成像素**，所以任何尺寸下边缘都是重新算出来的，自然清晰。
>
> 代价是：复杂照片不适合用 SVG 描述（要成万上万个点），这正是 [[链接与图像]] 里 `<img>` 的地盘。

## 二、基本图形与坐标原点

| 标签 | 参数 |
|---|---|
| `<rect>` | 矩形：`x`、`y`、`width`、`height` |
| `<circle>` | 圆：`cx`、`cy`、`r` |
| `<line>` | 线：从 `x1, y1` 到 `x2, y2` |
| `<ellipse>` | 椭圆：`rx`、`ry` 两个半径 |
| （共同） | **`fill` 填充色** 与 **`stroke` 描边色** |

```html
<svg width="100" height="100">
  <rect x="0" y="0" width="100" height="100"
        fill="#1E4FA8"/>
  <circle cx="50" cy="50" r="30" fill="white"/>
</svg>
```

课件点明坐标规则：**Coordinates start at the top-left corner — (0,0) is the top-left**（坐标从左上角开始，(0,0) 是左上角）。

- `y` 向下增长——所以"往下"是 `y` 变大。
- 那个 `#1E4FA8` 是**课程调色板里的 Primary 主色**（调色板设定见 [[课程场景与阅读约定]]），白色圆叠在主色方块上。

## 三、`polyline` 与 `polygon`

| 标签 | `points` | 行为 |
|---|---|---|
| `<polyline>` | `points="x1,y1 x2,y2 …"` | **开放的**一串线段（an open chain of segments） |
| `<polygon>` | 同样的 `points` | **浏览器把形状闭合** |

**Every point is an x,y pair — vertices in order**（每个点都是一对 x,y——按顺序排的顶点）。

**Closed by default**：`polygon` 会把**最后一个点连回第一个点**。

```html
<svg width="200" height="120">
  <polyline points="10,90 40,10 70,90 100,10 130,90"
            fill="none" stroke="#1E4FA8"
            stroke-width="4"/>
  <polygon points="60,10 100,60 60,110 20,60"
            fill="#FFC107" opacity="0.8"/>
</svg>
```

上面是一条**之字形折线**（不闭合，所以 `fill="none"`，否则会尝试填充一个没封口的形状）；下面是**一个菱形**（`polygon` 自动闭合，填充课程调色板的 Gold `#FFC107`，`opacity="0.8"` 半透明）。

> [!tip] `fill="none"` 在这里为什么是必需的
> `polyline` 是一条**开放**的链，浏览器无法判断"里面"是哪一边，所以 `fill="none"` 明确表示**只描边、不填充**。这和 [[媒体元素]] 里的 `<source>` 回退是同一种思路：**把意图写清楚，交给浏览器执行**。

## 四、填充、描边与透明度

| 属性 | 课件的说法 |
|---|---|
| `fill` | 内部颜色——**`fill="none"` 让图形空心** |
| `stroke` | 轮廓颜色——**一条线需要它**（还需要 `stroke-width`） |
| `stroke-width` | 轮廓粗细——**默认 1px**，可以试 4 或 8 |
| `opacity` / `fill-opacity` | 0（不可见）到 1——**整个元素**，或**只对填充** |
| `stroke-dasharray` | 虚线——**`"4 3"` = 4 单位墨，3 单位空隙** |
| `stroke-dashoffset` | 移动虚线**从哪里开始**——**墨沿着线滑动** |
| `pathLength` | 把这条路径当作 **100 单位**——于是 `"4 3"` 就是 4% 和 3% |

### `"4 3"` 这个节奏

课件专门给了一段图解式说明：

| 概念 | 数值 |
|---|---|
| ink（墨） | **4 单位** |
| gap（空隙） | **3 单位** |
| 一个周期 | 4 + 3 = **7 单位**，然后**重复** |
| `stroke-dashoffset: 0` | 从起点开始 |
| `stroke-dashoffset: -3` | 把 `"4 3"` 这个模式**沿路径滑 3 单位** |

课件那句解释是：**The tick is the path's start; offset -3 slides the "4 3" pattern 3 units along it**（刻度是路径的起点；`offset: -3` 把 `"4 3"` 模式沿它滑 3 单位）。

一条真正的虚线：

```html
<line x1="10" y1="60" x2="190" y2="60" stroke-dasharray="4 3" />
```

还有一条简写规则，课件单独列出：**A lone number is shorthand — "4" means "4 4"**（单个数字是简写——`"4"` 意味着 `"4 4"`，即 4 单位的划和 4 单位的空隙）。

> [!important] `pathLength` 的价值
> 虚线节奏的**绝对数字很烦人**——4 单位在 100 长的线上和在 1000 长的线上观感完全不同。`pathLength` 的作用是**声明"把这条路径看作 100 单位"**，这样 `"4 3"` 立刻变成 4% 和 3%，**和路径实际多长无关**。虚线动画能只靠 CSS 做出来，靠的就是这一条。

## 五、`path` 与 `viewBox`

| 课件的说法 | 展开 |
|---|---|
| **`<path>`** | **最强大的图形**——任意曲线 |
| `d="…"` | 一条命令串：**M**（移动）、**L**（直线）、**C**（曲线）、**Z**（闭合） |
| **Case matters** | **M 是绝对坐标，m 是相对于当前点** |
| **Control handles** | C 带**两个**控制柄；曲线被**拉向**它们，**不经过**它们 |
| **`viewBox`** | **这张图的坐标系** |
| **Shapes everywhere** | **图标和图表通常都是 path** |

```html
<path d="M16 29 C8 20 2 14 2 9 C2 4 6 2 9 2 … Z" />
```

课件给的心形例子：**A heart — seven curves, one attribute**（一颗心——七条曲线，一个属性）。

### 控制柄那条最反直觉

**The curve is pulled toward them, not through them**（曲线被**拉向**控制柄，而**不是穿过**它们）。

所以看到 `C` 后面四个数字时，别把它们当成"曲线上的点"——那两点在曲线**外面**，是"磁铁"。想调整弧度就是移动这两点。这条一旦搞错，后面所有 path 调形都会偏。

### `viewBox` 管的是"缩放不糊"这件事

前面说 SVG 放大不糊，**靠的就是 `viewBox`**：它声明"我画图时用的坐标系是这么大"。显示尺寸由 `width` / `height` 决定，**画图坐标由 `viewBox` 决定**，两者分开，缩放时才不会失真。

> [!important] 这和 [[图像映射]] 的坐标系是两回事
> 图像映射的坐标**死死钉在图片文件的像素上**——用 CSS 改大小就会错位（课件明确禁止）。SVG 的坐标绑在 `viewBox` 上，**缩放是它设计好的行为**。同样是"用坐标画图"，一个怕缩放，一个靠缩放吃饭。[[图标]] 那一篇讲的正是 SVG 图标这条路。

## 六、动画：零 JavaScript

课件给了一个场景里的四种手法，并强调 **Zero JavaScript — markup, CSS and SMIL, nothing else**：

| 手法 | 课件的说法 |
|---|---|
| **Pulse rings**（脉冲环） | **一个圆的三份拷贝**：**一条 `@keyframes`，三个 delay** |
| **Orbit**（环绕） | **`animateMotion`** 载着两个"旅行者"绕椭圆转 |
| **Waveform**（波形） | **16 单位的虚线节奏**沿着一条固定路径滑动 |
| **Halo**（光晕） | 一个**模糊的渐变**用透明度"呼吸" |

> [!tip] 脉冲环的配方值得记住
> "**三个相同的圆 + 一条 `@keyframes` + 三个不同的 `animation-delay`**"——这是纯 CSS 实现扩散涟漪的标准做法：不需要复制三段动画代码，只要错开开始时间就行。`@keyframes` 本身在 [[关键帧动画]] 里展开。
>
> 环绕用的 `animateMotion` 属于 **SMIL**（SVG 自己的动画声明），其余三种课件明确说是 markup + CSS。

## 七、一个合起来的例子

```html
<svg viewBox="0 0 100 100" width="100" height="100">
  <rect x="0" y="0" width="100" height="100" fill="#1E4FA8"/>
  <circle cx="50" cy="50" r="30" fill="none"
          stroke="white" stroke-width="4" stroke-dasharray="4 3"/>
  <polygon points="60,10 100,60 60,110 20,60"
           fill="#FFC107" opacity="0.8"/>
</svg>
```

- `viewBox="0 0 100 100"` 声明坐标系；`width` / `height` 声明显示尺寸。
- 背景方块是课程主色 `#1E4FA8`。
- 白色的空心圆用虚线 `"4 3"`（墨 4、空 3）。
- 半透明的金色菱形是 `polygon`，自动闭合。

## 关联

- → [[链接与图像]]（`<img>` 是位图路线，SVG 是矢量路线；同一个图形需求的两条不同答案）
- → [[图像映射]]（同目录 — 另一套"用坐标画图"的坐标系，对比它怕缩放的教训）
- → [[图标]]（跨目录 — 课件说"图标和图表通常都是 path"，内联 SVG 图标就是这一篇的 `<path>`）
- → [[关键帧动画]]（跨目录 — 脉冲环那条"一条 `@keyframes` 三个 delay"的配方）
- → [[颜色表示法]]（跨目录 — `fill="#1E4FA8"` 就是课程调色板的 Primary 主色，调色板设定见 [[课程场景与阅读约定]]）
