---
tags: [WD, 布局与定位, flexbox, 弹性布局, 自学]
domain: [Web 应用开发, CSS 布局与定位]
course: COMP3421
lecture: L05
---

# Flexbox · Flexible Box Layout

> **一句话**：一行 `display: flex` 就把子元素变成弹性项目（flex item），**沿着一根轴排布** —— 一维的问题用 Flexbox，**同时要管行和列就换 Grid**。

课件原文见 [Lecture_05_CSS.pptx](<../../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「Flexbox」一页。

> [!warning] 这一页在课件里标注为 **SELF-STUDY（自学）**
> 课件的安排是：Flexbox 和 Grid **各占一页自学页**。课件给的指示是：*run the example, then read the W3Schools page*（先跑一遍示例，再读 W3Schools 那一页）—— 配套地址 `w3schools.com/css/css3_flexbox.asp`。
> 本篇是按那一页的内容整理的复习稿；课件本身只给属性清单和三个代码片段，细节需要在 W3Schools 上补齐。

## 一、属性清单

| 属性 | 做什么 |
|---|---|
| `display: flex` | **一行**，把这个容器的子元素变成 flex item |
| `flex-direction` | 轴朝哪个方向跑：`row`（默认）· `column` · `row-reverse` |
| `justify-content` · `align-items` | **先沿轴铺开**，**再横过来对齐** |
| `gap` · `flex-wrap` | 项目**之间的间距**；`flex-wrap` 把溢出的部分**挪到新的一行** |
| `flex: 1` | 平分**剩余空间** —— 经典的等宽列写法 |
| `flex: 1 1 220px` | 等宽**且**放不下就换行的等宽列 |

课件对 `justify-content` / `align-items` 那一条的措辞值得抄下来：**"Spread the items along the axis, then line them up across it."**（**先沿轴铺开，再横过来对齐**。）两个属性各管一根轴，别指望一个属性干两件事。

## 二、三个代码片段

```css
/* 一行，让子元素成为 flex item */
.row { display: flex; gap: 16px; }

/* 等宽列，一行满了就换行 */
.row > * { flex: 1 1 220px; }

/* 不用魔法数字就把子元素居中 */
.hero { display: flex; align-items: center; }
```

### `flex: 1 1 220px` 这个模式

`flex` 是三个数的简写：`flex-grow`（长大）、`flex-shrink`（收缩）、`flex-basis`（基准尺寸）。

| 值 | 作用 |
|---|---|
| `1`（grow） | 有剩余空间就等份长大 |
| `1`（shrink） | 空间不够就等份收缩 |
| `220px`（basis） | 起始宽度是 220px |

配套 `flex-wrap: wrap`，容器装不下时项目**换到下一行**，而每一行内部仍然是**等宽**的。这就是卡片墙的标准写法。

> [!tip] 纯 Flexbox 的等宽换行
> 课件的响应式那一页给的纯 Flexbox 版本，连媒体查询都不需要：
> ```css
> .cards { display: flex; flex-wrap: wrap; }
> .cards > * { flex: 1 1 220px; }
> ```
> **「会自己伸缩的布局是免费的」** —— 屏幕多宽就排几列，由内容宽度决定，不写断点。

## 三、`.hero`：不用魔法数字的居中

```css
.hero { display: flex; align-items: center; }
```

一行代码就让 `.hero` 里的子元素**垂直居中**。对比一下老写法：过去要算出容器高度减去子元素高度的一半，再写一个具体的 `margin-top` —— 那是个**魔法数字**，容器一改高度就失效。Flexbox 说的是「**对齐**」，不是「算位置」，所以永远跟着内容走。

这就是 Flexbox 的全部哲学：**你描述布局，别去挤盒子。**

## 四、Flexbox 还是 Grid？

课件把这条判据写在 Flexbox 的最后一行：

> **One axis only — Nav bars, card rows, centring. Rows AND columns → Grid, next page.**

| 情况 | 用哪个 |
|---|---|
| 只有**一根轴**（一排导航、一行卡片、居中） | **Flexbox** |
| **要同时管行和列**（二维对齐） | **Grid** |

`gap` 的一处区别值得留意：Flexbox 的 `gap` 管**项目之间的间距**（不含容器边缘），而 Grid 的 `gap` 一次声明**同时管行列**（是格子之间的沟槽）。

## 关联

- 二维的情况 → [[Grid]]（同一个 `gap` 家族，但一次管住行与列；两者的分工判据）
- 前提 → [[定位方式]]（`float` 那套硬凑被 Flexbox 取代；但模态浮层仍属于定位的活）
- 为什么算得对 → [[尺寸与盒模型计算]]（`box-sizing: border-box` 是 `flex: 1 1 220px` 这类宽度能落地的前提）
- 换行的行为 → [[常规流]]（`flex-wrap` 是常规流掉行行为的现代版本）
- 间距的替代方案 → [[内外边距]]（`gap` 替掉了一整排 `margin`，顺带消掉了相邻 margin 的合并问题）
- 动画的落点 → [[过渡transition]]（悬停时的位移／变色，用 `transition` 平滑化）
