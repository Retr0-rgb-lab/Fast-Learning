---
tags: [WD, 动效与其他CSS, display, 隐藏, visibility, opacity]
domain: [Web 应用开发, CSS 动效与细节]
course: COMP3421
lecture: L05
---

# display与隐藏 · display, visibility & opacity

> **一句话**：`display` 决定这个盒子**在行里怎么落座**（外部类型），`display: none` 是唯一**真正不参与布局**的隐藏方式；`visibility` 和 `opacity` 都**留着位置**，所以它们是用来做**效果**的，不是用来做布局的。

课件原文见 [Lecture_05_CSS.pptx](<../../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「Miscellaneous」一节的 display 部分：display 两页、Hiding Things 一页，以及 Miscellaneous Cheatsheet 的相关两行。

## 一、`display` 是外部盒类型

课件的原句是整篇的钥匙：**「The outside decides how it sits in the line; the inside decides how its children lay out.」**（外面决定它在行里怎么落座，里面决定它的子元素怎么排。）

| 值 | 干什么 | 在哪儿遇到它 |
|---|---|---|
| `block` | 另起一行，撑满宽度 | `<div>`、`<p>`、`<h1>`、`<li>` |
| `inline` | 在文字流里，宽度由内容决定 | `<span>`、`<a>`、`<em>` |
| `inline-block` | 在文字流里，但**是个可以给尺寸的盒子** | `<img>`、`<button>` |
| `flex` | 一个 block 盒子，它的子元素成为 flex 项目 | `display: flex;` |
| `none` | 不渲染，**不占空间** | `display: none;` |

三种常见类型在实用层面的差别：

| 类型 | 行为 |
|---|---|
| `block` | 一行一个。你设的 `width` **会被尊重** |
| `inline` | 在句子里连排。**`width` 和 `height` 都被忽略** |
| `inline-block` | 在句子里，但已经是盒子，可以给尺寸 |

```css
/* block：满宽，一行一个 */
.tag { display: block; }
/* inline：挤在句子里 */
.tag { display: inline; }
/* inline-block：在句子里，但有盒子的尺寸 */
.tag { display: inline-block; width: 120px; }
```

`flex` 是把**子元素交给布局算法**的开关，它自己的分类属于 Flexbox 那一支，见 [[Flexbox]]；两维的对应物是 [[Grid]]。

> [!warning] 经典 bug：给 inline 元素写 `width`，什么都没发生
> 这是 CSS 初学者最常撞上的一件怪事。原因不是选择器写错了，而是 **`inline` 盒子按设计就没有宽度** —— 它必须顺着文字流走，宽度就是文字有多长。要给尺寸，就得换成 `inline-block`（或 `block`）。
>
> 课件给的一句排查口诀：**「If a width is being ignored, check the display value first.」** 尺寸为什么算不对，见 [[尺寸与盒模型计算]]。

## 二、隐藏元素的三种方式

这是本篇真正要记住的对比。**三种方式看起来都是「看不见」，但后两种的副作用完全不同**：

| 属性 | 看得见吗？ | 留着位置吗？ | 还能点到吗？ |
|---|---|---|---|
| `display: none` | ❌ | ❌ | ❌ |
| `visibility: hidden` | ❌ | ✅ | ❌ |
| `opacity: 0` | ❌ | ✅ | ✅ **能** |

三列各自意味着什么，是这张表的价值所在：

| 属性 | 看不见的原因 | 还占着 | 还能交互 |
|---|---|---|---|
| `display: none` | 根本不生成盒子 | **不占**，后面的东西会补上来 | 不能 |
| `visibility: hidden` | 盒子照画，只是不可见 | **占着**，后面的东西不会补上来 | 不能 |
| `opacity: 0` | 只是不透明 | **占着** | **能** —— 鼠标照样点得到 |

```css
/* 布局层面的隐藏：菜单项收起来，后面的内容补上去 */
.nav .extra { display: none; }

/* 效果层面的隐藏：还在那儿，只是看不见 */
.tooltip { visibility: hidden; }
.tooltip:hover { visibility: visible; }
```

> [!important] `opacity: 0` 还能点，是最需要警惕的一行
> 一个 `opacity: 0` 的按钮**看不见，但仍然可以被鼠标点击**，也会继续占据焦点、仍然能被读屏软件念出来。它并没有被「隐藏」，只是被「涂成透明」。
>
> 所以：**想让用户点不到，就必须用 `display: none` 或 `visibility: hidden`，不能靠 `opacity: 0`。**

## 三、选择规则

课件在这一页给了一句判断依据：

> **display: none is for layout; visibility and opacity are for effects.**

中文就是：**要动布局用 `display`，要做效果用 `visibility` 和 `opacity`。**

| 你想干的 | 该用 | 例子 |
|---|---|---|
| 让它**从布局里消失**（后面补上来） | `display: none` | 收起的侧边栏、窄屏下隐藏广告 |
| 让它**在原地隐身**（位置不动，不能交互） | `visibility: hidden` | 提示条、暂时不用的按钮 |
| 让它**淡入淡出**（位置不动，仍可交互） | `opacity` | 弹窗、蒙层、淡入的横幅 |

> [!tip] 混用是对的
> 经常两条一起上：`display: none` 管「彻底不参与布局」，`opacity` 管「参与布局时怎么淡」—— 典型例子是抽屉式侧边栏，开合两个方向都用 `opacity` 做过渡，但收起时最终落到 `visibility: hidden` 或 `display: none` 上，这样它就不会挡住下面的点击。`transition` 怎么写见 [[过渡transition]]。

## 四、和「层叠」的关系

这三种隐藏的差别，本质上是**盒子还在不在布局里**的差别 —— 也就是它和定位、层叠是两套不同的机制：

- 盒子在（`visibility` / `opacity`）→ 它仍然按正常规则参与排列，谁盖住谁由 `z-index` 决定，见 [[层叠顺序与z-index]]。
- 盒子不在（`display: none`）→ 它连参与比较的资格都没有。

这也是为什么 `display: none` 的元素改 `z-index` 没有任何意义。

## 五、速查

课件 Miscellaneous Cheatsheet 里与之相关的两行：

| 属性 | 干什么 | 一行写法 |
|---|---|---|
| `display` | 外部盒类型 | `block \| inline \| inline-block \| none` |
| `visibility` & `opacity` | 隐藏了，但还在那儿 | `visibility: hidden` · `opacity: .5` |

> [!important] 三句话版本
> 1. `display` 决定**外部类型**，在 HTML 标签上遇到 `block` / `inline` / `inline-block` / `flex` / `none`。
> 2. 三种隐藏里，**只有 `display: none` 不占位置**。
> 3. **只有 `opacity: 0` 还能被点到** —— 想让用户点不到就别用它。
>
> 补一句排查用的口诀：**宽度设了没反应，先去查 `display`。**

## 关联

- 盒子的几何本身 → [[盒模型五层]]（`display` 决定这个盒子采不参与排列，盒模型决定它占多大）
- 给 `display` 的尺寸为什么会被忽略 → [[尺寸与盒模型计算]]（宽度算的是哪一层、什么时候被 `display` 直接废掉）
- `opacity: 0` 的完整行为 → [[透明度与叠加层]]（alpha 是怎么和背景、叠加层一起工作的）
- 消失的两种方式 → [[过渡transition]]（淡入淡出必须用 `opacity` 或 `visibility`，因为 `display` 没有中间态）
- `display: flex` 之后的事 → [[Flexbox]]（外部类型是「flex」时，内部布局由子元素的排列算法接管）
- 盒子在时的先后顺序 → [[层叠顺序与z-index]]（`display: none` 的元素不参与任何层叠比较）
