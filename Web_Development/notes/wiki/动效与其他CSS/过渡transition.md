---
tags: [WD, 动效与其他CSS, transition, 过渡, 缓动]
course: COMP3421
lecture: L05
---

# 过渡transition · Transition

> **一句话**：`transition` 把一个**你自己触发的**状态变化从「啪一下跳过去」变成「慢慢变过去」—— 关键是把 `transition` 写在**基础状态**上，这样进和出两个方向都会被抹平。

课件原文见 [Lecture_05_CSS.pptx](<../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「Animation」一节的过渡部分：从「Transitions」到「Transition Recipes」。

## 一、它到底平滑了什么

课件的定义只有一句：**Smooth the change** —— 属性的一次跳变变成一次渐变。

| 要点 | 说明 |
|---|---|
| **由状态触发** | 通常是 `:hover`、`:focus` 或一个 class 的变化 |
| **性质是插值** | 旧值 → 新值之间，浏览器自己补出中间值 |
| **一个或多个属性** | `transition-property` 列出哪些属性要动 |
| **时长由你定** | `transition-duration`，秒或毫秒 |

```css
/* 两个属性，各走各的时长 */
transition: width 2s, height 4s;
```

> [!important] `transition` 需要一个触发源，`animation` 不需要
> 这条分界线是整个动效章节的分水岭：写 `transition` 的那一刻，你必须能回答「**什么时候变**」。答不上来就说明这活儿该交给 [[关键帧动画]]。两者的完整对照表在那一篇里。

## 二、写在基础状态上

这是本篇最该背下来的一条实操经验。课件 Best Practices 里的原话：**transition on the base — it plays both in and out smoothly.**

看一个反例与正例的差别（跑在示例站上，见 [[课程场景与阅读约定]]）：

```css
/* 反例：只写在 :hover 上 —— 鼠标移进去是平滑的，移出来立刻「啪」一下弹回去 */
a { color: #1E4FA8; }
a:hover {
  color: #0E3F8C;
  transition: color 0.3s ease;
}

/* 正例：写在基础状态上 —— 进去、出来都是平滑的 */
a {
  color: #1E4FA8;
  transition: color 0.3s ease;
}
a:hover { color: #0E3F8C; }
```

> [!tip] 记法
> 凡是「离开时应该也好看」的效果 —— 淡出、下滑、缩回 —— 一律把 `transition` 写在基础状态上。只写在触发态里的效果，回程一定跳。

## 三、四个长写属性

| 属性 | 管什么 | 例子 |
|---|---|---|
| `transition-property` | 哪些属性要过渡 —— `width`、`height`、`opacity`… | `width, height` |
| `transition-duration` | 过多久 —— 秒或毫秒 | `2s`、`300ms` |
| `transition-timing-function` | 曲线 | `ease`、`linear`、`ease-in`、`ease-out` |
| `transition-delay` | 开工前先等多久 | `0.1s` |

简写的**顺序固定**：`property · duration · curve · delay`。

```css
/* 长写 */
.box {
  transition-property: width, height;
  transition-duration: 2s, 4s;
  transition-timing-function: ease;
}
/* 同一件事，写成一行 */
.box { transition: width 2s, height 4s; }
```

> [!warning] 顺序写错不会报错，但会静默失效
> 简写里第一个**时间值**是 duration，第二个才是 delay（`transition: opacity 0.3s 0.1s;` = 0.3 秒过渡、延迟 0.1 秒）。写反了不会有提示，所以记死顺序比记语义省事。

## 四、计时函数：曲线决定手感

| 函数 | 曲线形态 | 用在什么感觉上 |
|---|---|---|
| `ease` | 慢起 → 快中 → 慢收 | **默认值** |
| `linear` | 从头到尾恒速 | 需要匀速的东西：进度条、旋转的 spinner |
| `ease-in` | 慢起，然后加速 | 元素「加速离开」 |
| `ease-out` | 快起，然后减速 | 元素「减速落位」—— 大多数入场动效用它 |
| `ease-in-out` | 两端慢、中间快 | 一进一出一整套动作 |

课件一句话：*「The curve decides the feel.」* 曲线决定的是**感觉**，不是效果 —— 同一个 `translateY`，用 `ease-out` 和用 `linear` 完全是两回事。做什么动作是 `transform` 的事，怎么动是 `transition` 的事，见 [[变换transform]]。

## 五、哪些东西能过渡

| 类别 | 能不能过渡 | 例子 |
|---|---|---|
| **数字（可插值）** | ✅ | 长度、颜色、`opacity`、角度 —— 任何有「中间值」的东西 |
| **关键字** | ❌ | `display: none → block` **没有中间状态**，只能跳 |
| `transform` | ✅ 首选 | 便宜又可插值 |
| `width` / `height` | ⚠️ 能，但**贵** | 会引起重排，真实 UI 里应该动 `transform` |

> [!warning] `transition: all` 是个陷阱
> 课件 Best Practices 明确点名：*「Name your transitions — avoid `transition: all`; it animates what you forgot.」* `all` 会把你**没打算动**的属性也一起过渡掉 —— 比如某个 class 顺手改了个 `border-radius`，于是边框也开始缓慢地圆起来，而你根本没写过这条意图。
>
> 正确写法是**点名**：
> ```css
> .card { transition: transform 0.3s ease, box-shadow 0.3s ease; }
> ```

### 延迟是你交错排列的帮手

```css
/* 一排卡片依次入场 */
.card:nth-child(1) { transition-delay: 0s; }
.card:nth-child(2) { transition-delay: 0.08s; }
.card:nth-child(3) { transition-delay: 0.16s; }
```

`transition-delay` 每一档差几十毫秒，一排元素就有了「波浪」的先后顺序。选择器怎么写见 [[组合选择器]]。

## 六、六个配方

课件 Transition Recipes 一页给的六个，全部是**一个状态变一个状态**：

| 配方 | 怎么做 |
|---|---|
| 悬停抬起 Hover lift | `translateY(-4px)` 配一个更大的阴影 |
| 按钮填充 Button fill | 背景色从一侧扫进来 |
| 下划线滑入 Underline slide | 链接的下划线从左往右长出来 |
| 图片放大 Image zoom | `scale(1.05)`，外层配 `overflow: hidden` |
| 按下 Press down | `:active` 上 `scale(0.97)` —— 即时反馈 |
| 焦点环 Focus ring | `:focus-visible` 上出现 `box-shadow` |

把最常用的两个抄全，跑在示例站的报名按钮上（配色取自课程调色板 Primary `#1E4FA8` 与 Gold `#FFC107`）：

```css
.btn {
  background: #1E4FA8;
  color: #fff;
  border: 0;
  border-radius: 6px;
  padding: 10px 18px;
  transition: transform 0.2s ease, box-shadow 0.2s ease,
              background-color 0.2s ease;
}
.btn:hover  { background: #3D7BD9; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18); }
.btn:active { transform: scale(0.97); }
.btn:focus-visible {
  outline: 2px solid #FFC107;
  outline-offset: 2px;
}
```

图片放大的那一款要额外一层，因为放大会溢出：

```css
.thumb { overflow: hidden; }              /* 把溢出的部分切掉 */
.thumb img { transition: transform 0.3s ease; }
.thumb:hover img { transform: scale(1.05); }
```

> [!important] 动效有代价，读者可能不要
> 课件专门有一页讲这件事：有人对运动敏感（可能引起恶心和偏头痛），系统里有对应开关。正确做法是 `@media (prefers-reduced-motion: reduce)` 里关掉动效 —— 但**别把意思一起关掉**。完整写法见 [[动效与可访问性]]。

## 关联

- 动效三件套的第一件 → [[变换transform]]（`transform` 负责「变成什么」，`transition` 负责「怎么变过去」）
- 另一种动效 → [[关键帧动画]]（要触发用 `transition`，要自己循环用 `animation`；`steps()` 是两者共用的手段）
- 触发状态怎么写 → [[伪类与伪元素]]（`:hover`、`:active`、`:focus-visible` 都是状态伪类）
- 交错排列用的选择器 → [[组合选择器]]（`nth-child()` 怎么定位第几个）
- 焦点环的声明 → [[阴影]]（也可以用 `box-shadow` 而不是 `outline` 来画焦点环）
- 缓动要照顾的读者 → [[动效与可访问性]]（`prefers-reduced-motion` 存在的原因）
