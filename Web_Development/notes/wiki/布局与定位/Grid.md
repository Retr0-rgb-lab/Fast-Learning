---
tags: [WD, 布局与定位, grid, 网格布局, 自学]
course: COMP3421
lecture: L05
---

# Grid · CSS Grid Layout

> **一句话**：`display: grid` 让子元素**同时进入行和列**，而 `fr` 单位是**一份均分剩余空间**的份额 —— `repeat(auto-fit, minmax(220px, 1fr))` 这一行就让你**不用写任何断点**就得到自适应列数。

课件原文见 [Lecture_05_CSS.pptx](<../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「CSS Grid」一页。

> [!warning] 这一页在课件里标注为 **SELF-STUDY（自学）**
> 课件的安排是：Grid **一页自学页**。课件给的指示是：*run the example, then read the W3Schools page*（先跑一遍示例，再读 W3Schools 那一页）—— 配套地址 `w3schools.com/css/css_grid.asp`。
> 本篇按那一页的内容整理；课件这一页给的是属性清单和两个代码片段，完整语法需要在 W3Schools 上补齐。

## 一、属性清单

| 属性 | 做什么 |
|---|---|
| `display: grid` | 一个**子元素同时进入行和列**的容器 |
| `grid-template-columns` | **几列、每列多宽**：`repeat(3, 1fr)`、`1fr 3fr` |
| `fr` | **一份均分剩余空间的份额** —— 列**跟着容器走** |
| `minmax()` + `auto-fit` | `repeat(auto-fit, minmax(220px, 1fr))` —— **能放几列就放几列** |
| `gap` | **行和列之间的沟槽**，**一条声明**同时管住两者 |

## 二、两个代码片段

```css
/* 三等分列，跟着容器走 */
.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* 页面骨架：一窄一宽 */
.page {
  display: grid;
  grid-template-columns: 1fr 3fr;
}
```

### `1fr 3fr` —— 页面骨架的形状

`1fr 3fr` 的意思是：**左边一份、右边三份**。这是典型的**页面外壳（page shell）**比例：左边窄（侧栏），右边宽（正文）。它比「左栏 240px、右栏剩下的」更稳 —— 因为**两栏的比例在任何宽度下都保持**，而不是左栏固定、右栏被动伸缩。

> [!tip] 页脚要跨满怎么办
> `1fr 3fr` 只定义了两列。要让某一项横跨整行，用 `grid-column: 1 / -1`（`-1` 指最后一条线）。这属于 `grid` 模板的完整语法，课件这一页没展开，W3Schools 上有。

## 三、`fr` 到底是什么

> **fr = the space that is left 的**一份**。**

| 说法 | 含义 |
|---|---|
| 一份等分份额 | 容器内**剩余**空间按 `fr` 的个数等分 |
| 列跟着容器 | 容器变宽，**列自动变宽**；**不需要重算 px** |

所以 `repeat(3, 1fr)` 的字面意思是「**三列，各占三分之一**」，而**分母是当前容器的宽度**。这就是它比 `width: 33%` 更稳的原因：`33%` 算的是容器宽度但**不管 gap**（三个 33% 加上两段 gap 一定溢出），`1fr` 是**在扣掉 gap 之后**再分。

## 四、`minmax()` + `auto-fit`：不用断点的自适应列

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
```

拆开看三个词：

| 词 | 作用 |
|---|---|
| `repeat(auto-fit, …)` | **重复多少次由浏览器算** —— 它算出当前宽度能塞下几份 |
| `minmax(220px, 1fr)` | 每列**最少 220px**，最多**占满一份剩余空间** |
| `1fr` | 上限不是固定值，所以列会**填满容器** |

**净效果：能放几列就放几列，放不下的自动换到下一行。** 窄屏 1 列、平板 2 列、桌面 3 列，**一条声明，不写断点**。

> [!important] 这是「断点来自内容」的最干净实现
> 课件的响应式原则是 **"Breakpoints from the content — not from device sizes"**（断点来自内容，不是设备尺寸）。`minmax(220px, 1fr)` 把这个原则**直接编码进声明**：220px 是**内容要求的最小宽度**，不是某台设备的尺寸。见 [[响应式与媒体查询]]。
>
> 若你更想要「撑满就撑满、别留空」的严格自适应，Grid 里还有 `auto-fill` 与 `auto-fit` 的差别（后者会把空出来的轨道折叠掉），课件这一页只用到 `auto-fit`。

## 五、`gap` 一次管住行和列

```css
.cards { display: grid; gap: 16px; }
```

一条 `gap` 同时设成**行间距**与**列间距**。这是 Grid 相对 Flexbox 的一处省心之处 —— Flexbox 的 `gap` 只管项目**之间**，不含容器外缘，Grid 的 `gap` 是**格子之间的沟槽**。

## 六、Grid 还是 Flexbox

课件把判据放在这一页的最后一行：

> **Two dimensions → Grid. A single line of items → Flexbox.**

| 情况 | 用哪个 |
|---|---|
| **同时要管行和列**（二维对齐、页面外壳、卡片矩阵） | **Grid** |
| **只有一根轴**（一排导航、一行按钮、居中） | **Flexbox** |

- 「有一个复杂表格／页面骨架要二维对齐」→ Grid
- 「一排等宽的东西要居中或两端对齐」→ Flexbox
- 「卡片墙要自动换行」→ 两者都能，Grid 的 `auto-fit` 更简洁

> [!important] 两页都自称「一轴 / 二维」，但别把它当互斥
> 课件的分法是**按你心里那个问题**来选：我想排**一条**东西 → Flexbox；我想排**一片**东西 → Grid。实际项目里两者经常共存 —— 一个 Grid 管页面的大骨架（`1fr 3fr`），每个格子里再放一个 Flex 做一行控件。

## 关联

- 一维的兄弟方案 → [[Flexbox]]（同一节里并排的另一个自学页；两者的分工判据）
- 尺寸算法 → [[尺寸与盒模型计算]]（`fr` 算的是**扣掉 gap 之后**的剩余空间，前提是 `box-sizing` 已统一）
- 沟槽的来源 → [[内外边距]]（`gap` 替掉了靠 margin 撑开间距的老办法，也避免了 margin 合并）
- 断点从哪来 → [[响应式与媒体查询]]（`minmax()` 实现的「断点来自内容」原则）
- 行高与栅格的间接影响 → [[文本与字体]]（栅格里的换行与 `line-height` 一起决定每格的高度）
- 减少像素值的动机 → [[长度与单位]]（`fr` 是「比 px 更好的另一种单位」的例子）
