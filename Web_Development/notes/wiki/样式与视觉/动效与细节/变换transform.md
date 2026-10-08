---
tags: [WD, 动效与其他CSS, transform, 变换, 动效]
domain: [Web 应用开发, CSS 动效与细节]
course: COMP3421
lecture: L05
---

# 变换transform · Transform

> **一句话**：`transform` 重新塑形一个盒子，**盒子原来那块地方照旧占着、旁边的元素一个都不动** —— 正因为它不引起重排（no reflow），所以它是所有动效里最便宜、最该优先用的那个。

课件原文见 [Lecture_05_CSS.pptx](<../../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「Animation」一节的变换部分：从「Three Tools for Motion」到「Transform Cheatsheet」。

## 一、三个动效工具，各管一件事

课件在进入细节之前先把三者的分工摆清楚，本篇是第一个：

| 工具 | 干什么 | 什么时候发生 |
|---|---|---|
| `transform` | 重新塑形 —— 移动、旋转、缩放、倾斜 | 立刻生效，**不做平滑** |
| `transition` | 把一个**你触发的**变化变平滑 | `:hover`、`:focus`、class 翻转时 |
| `@keyframes` + `animation` | 按时间线跑一整段序列 | 自己跑，页面加载就开始 |

课件把它们串成一句：**Reshape, smooth, then repeat** —— 先 `transform` 塑形，再 `transition` 把它抹平，最后 `@keyframes` 让它重复。

> [!important] 一个属性一件事，它们是叠着用的
> `transform` 干实际的活，`transition` 负责把这个变化**加上缓动**。写 `transition: transform 0.3s ease;` 就是在说「`transform` 怎么变都行，但请把它抹平」。

> [!tip] 为什么它便宜
> 课件原话是 "transform and opacity skip layout — the browser composites them"。动画的瓶颈通常在**重排（reflow）**和重绘；`transform` 两者都绕开了，交给合成器（compositor）处理，所以是顺滑动效的首选。

## 二、四个函数

```css
/* 一条声明里可以放任意多个函数 */
transform: translate(20px) rotate(45deg) scale(1.2);
```

| 函数 | 干什么 | 例子 |
|---|---|---|
| `translate(x, y)` | 沿 X 与 Y 轴移动 | `translate(20px, -10px)` |
| `rotate(deg)` | 绕原点自转 | `rotate(45deg)` |
| `scale(x, y)` | 放大 / 缩小 / 翻转 | `scale(1.3)` |
| `skew(x, y)` | 倾斜盒子 | `skewX(-20deg)` |

### 移动：translate

```css
.card {
  transform: translate(20px, 10px);
}
/* 向右移动自身宽度的一半 */
.card { transform: translateX(50%); }
```

> [!warning] 百分比是相对**盒子自己**的
> `translateX(50%)` 不是「父容器宽度的一半」，而是**这个盒子自身宽度的一半**。课件原文：*"`%` is relative to the box"*。想要按父容器算，就把百分比换成 `vw`、`%` 布局单位，或者干脆用 `margin: 0 auto`（见 [[尺寸与盒模型计算]]）。

`translateX()` / `translateY()` 只动一根轴，适合「只往上抬一点」这种需求。

### 旋转：rotate

```css
.box { transform: rotate(45deg); }
```

- **顺时针**为正，**负角度**逆时针：`rotate(-45deg)`。
- 单位分三种：**`px`** 是长度、**`deg`** 是角度、**`turn`** 是整圈（`turn` = 360°）。课件特别点出 "Units matter"。

### 缩放与倾斜：scale / skew

```css
/* 放大到 130% */
.box { transform: scale(1.3); }
/* 向侧边倾斜 */
.box { transform: skewX(-20deg); }
/* 水平镜像 */
.box { transform: scale(-1, 1); }
```

| 写法 | 含义 |
|---|---|
| `scale(1)` | 原样（1 是正常值） |
| `scale(0.5)` | 缩到一半 |
| `scale(1.3)` | 130% |
| `scale(n)` 一个值 | 两根轴**等比**缩放 |
| `scale(-1, 1)` | X 轴取负 = **水平镜像** |

> [!tip] `scale(0.97)` 是按钮按下去的秘诀
> 课件专门点出：*"`scale(0.97)` on `:active` gives a button a satisfying press-down feel."* 交互反馈见 [[伪类与伪元素]]，缓动见 [[过渡transition]]。

## 三、支点：transform-origin

`transform` 绕着一个点转，这个点叫**支点（pivot）**，默认是**盒子中心 `50% 50%`**。

```css
/* 绕左上角自转 */
.box {
  transform-origin: top left;
  transform: rotate(45deg);
}
/* 从右下角边缘生长出来 */
.menu { transform-origin: bottom right; }
```

| 要点 | 说明 |
|---|---|
| 默认值 | `50% 50%` —— 盒子的中心 |
| 怎么写 | 关键字、长度、百分比都行 |
| 两个值的顺序 | **先 x 后 y**，`top left` 等于 `0% 0%` |
| 换支点有什么用 | 换掉之后，「哪个角在长大 / 哪一点保持不动」就变了 |

课件一句话总结：*「The pivot decides which point stays still while everything else moves.」*（支点决定哪一点原地不动，其余全部随之运动。）

## 四、组合：函数**从右往左**作用

这是本篇最容易考错的一条。

```css
/* 先转，再向右移 40px */
.a {
  transform: translateX(40px) rotate(15deg);
}
/* 同样两个函数，顺序对调 —— 变成斜着滑出去 */
.b {
  transform: rotate(15deg) translateX(40px);
}
```

课件原话：*「Functions apply **right to left** — work backwards from the box.」* 也就是说，**列表里最后写的那个函数最先作用到盒子上**。

- 读法上把它当一句话念：`translateX(40px) rotate(15deg)` 念成「**先转 15°，再向右移 40px**」。
- 顺序一换，位移方向也跟着转，于是同一个 40px 变成了斜的 —— 这就是课件说的 "a diagonal slide"。

> [!warning] 写不出预期效果时，从盒子倒着念一遍
> 一个声明里函数的顺序一换，结果就完全不同。调试时不要怀疑参数，先怀疑顺序。

## 五、为什么它不引起重排

`transform` 是**表现层**的改动。课件的原话是 *「transform is presentational — it never changes the layout around it.」*（transform 是表现性的，它从不改变周围的布局。）

具体表现是本篇开头那句话的三件事：

| 事实 | 含义 |
|---|---|
| 盒子**保留它原来那块地方** | 视觉上移走了，布局里的槽位还在 |
| **邻居一个都不动** | 不会出现「后面的内容全被挤下去」 |
| 因此**不触发重排** | 浏览器只需合成，省下最贵的那一步 |

用 `position: relative` 也能让盒子移动，但它改变的是布局的「实际位置」；`transform` 则是**移动渲染出来的画面，原地不动**。两者的区别见 [[定位方式]]。

> [!important] 那为什么动效优先用 transform，而不是 left / top
> 因为改 `left` / `top` 会让浏览器**重新计算布局**（重排），改 `transform` 不会。课件的最佳实践第一条就是这个：`transform` + `opacity` 是便宜属性，要动的是它们，不是 `width` / `height`。缓动怎么写见 [[过渡transition]]。

## 六、速查表

课件的 Transform Cheatsheet 原样搬过来：

| 函数 | 干什么 | 例子 |
|---|---|---|
| `translate(x, y)` | 沿 X、Y 移动 | `translate(20px, -10px)` |
| `rotate(deg)` | 绕支点自转 | `rotate(45deg)` |
| `scale(x, y)` | 放大 / 缩小 / 翻转 | `scale(1.3)` |
| `skew(x, y)` | 倾斜盒子 | `skewX(-20deg)` |
| `transform-origin` | 指定支点 | `transform-origin: top left;` |

放在示例站（本库预设的假想课程主页，见 [[课程场景与阅读约定]]）上，一个悬停时轻微抬起的卡片就是这样写的：

```css
.card {
  background: #fff;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px -6px rgba(0, 0, 0, 0.25);
}
```

配色取自课程调色板的 Navy `#0E3F8C` 系，正文见 [[颜色表示法]]。`transform` 抬高配 `box-shadow` 加深，是课件 Shadow Recipes 里的 "Hover lift"，两道配方见 [[阴影]]。

## 关联

- 底下的机制 → [[层叠顺序与z-index]]（两者都绕开重排，这正是它们便宜的原因；一个管形状，一个管前后）
- 加了缓动才顺滑 → [[过渡transition]]（`transform` 负责「变成什么」，`transition` 负责「怎么变过去」）
- 按下按钮的手感 → [[伪类与伪元素]]（`scale(0.97)` 挂在 `:active` 上，状态伪类怎么写见那里）
- 什么时候用 `position` → [[定位方式]]（`relative` 改的是布局位置，`transform` 改的是渲染画面）
- 一次动好几个停靠点 → [[关键帧动画]]（关键帧里被反复动的，多半就是 `transform`）
