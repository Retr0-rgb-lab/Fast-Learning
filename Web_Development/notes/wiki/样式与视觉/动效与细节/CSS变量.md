---
tags: [WD, 动效与其他CSS, 自定义属性, 变量, 主题]
domain: [Web 应用开发, CSS 动效与细节]
course: COMP3421
lecture: L05
---

# CSS变量 · CSS Variables (Custom Properties)

> **一句话**：用 `--name` 把一个值**命名一次**、用 `var(--name)` 在任何地方读回来 —— 变量跟着继承流下去，所以在一处改一个值，整页（甚至整站）跟着变。

课件原文见 [Lecture_05_CSS.pptx](<../../../raw/Lecture_05_CSS.pptx>)。本篇覆盖其中「Miscellaneous」一节的变量部分：从「CSS Variables — Custom Properties」到「A Theme with Variables」。

## 一、定义与读取

| 动作 | 写法 | 备注 |
|---|---|---|
| 定义 | `--name: 值;` | **必须以两个连字符开头** |
| 读取 | `var(--name)` | |
| 读取（带兜底） | `var(--name, fallback)` | 变量没定义时用兜底值 |

```css
:root {
  --brand: #1e4fa8;
  --gap: 16px;
}
/* 用 var() 读回来 */
.btn { background: var(--brand); }
```

> [!warning] 大小写敏感
> `--brand` 和 `--Brand` 是**两个不同的变量**。自定义属性不像某些标签名那样会被浏览器归一化，写错大小写不会报错，只是静默地读不到 —— 这时候表现和「忘了写兜底值」一样。

## 二、任何值都可以命名

课件强调 *「Any value」* —— 颜色、尺寸、字体，甚至**整段字符串**：

```css
:root {
  --brand: #1E4FA8;                    /* 颜色 */
  --gap: 16px;                         /* 尺寸 */
  --font-body: "Noto Sans SC", sans-serif;   /* 字体栈 */
  --shadow-card: 0 6px 16px rgba(0,0,0,.18); /* 一整条声明的片段 */
}
.card {
  font-family: var(--font-body);
  box-shadow: var(--shadow-card);
}
```

最后一行是最能体现价值的一种用法：把**一整条声明的值部分**存起来，以后换主题只要改这一个变量，不用到处找 `0 6px 16px rgba(0,0,0,.18)`。

## 三、`:root` 是全局的家

课件的定位是 *「On `:root` — global scope, the natural home for theme values.」*

`:root` 就是 `<html>` 元素，也就是**整棵树的祖先**。定义在它上面的变量，整页都读得到。

课程调色板（见 [[课程场景与阅读约定]]，原文出自 Week 3 的 CSS I）正好是 `:root` 的标准用途：

```css
:root {
  --navy:   #0E3F8C;   /* 深色底、页脚 */
  --brand:  #1E4FA8;   /* 主色：标题、链接、强调 */
  --mid:    #3D7BD9;   /* 次级强调、hover */
  --pale:   #9DC0EE;   /* 浅底、区块背景 */
  --sky:    #B9CDEE;   /* 更浅的分隔 */
  --gold:   #FFC107;   /* 提示、高亮 */
  --alert:  #D9534F;   /* 错误、警告 */
}
```

## 四、兜底值与组合

**兜底（fallback）**在变量没被定义时顶上：

```css
.card {
  padding: var(--gap, 16px);
  background: var(--card-bg, #fff);
}
```

课件的用途说明：*「A fallback keeps a component safe when a variable isn't set.」* —— 组件在被单独拿去用、或者变量还没定义时，不会因为读不到值而塌掉。

**组合（composable）**让一个值从另一个值里长出来：

```css
margin: calc(var(--gap) * 2);   /* --gap 是 16px，这里得到 32px */
```

> [!tip] 变量 + calc = 一套有节奏的间距
> 定义 `--gap: 16px` 之后，卡片内边距用它、卡片间距用 `calc(var(--gap) * 2)`、大区块间距用 `calc(var(--gap) * 3)`。整套间距的比例关系藏在**一个数字**里。

## 五、作用域与继承

这一节是变量最容易被低估的地方，也是它和普通属性联系最紧的地方。

| 规则 | 说明 |
|---|---|
| `:root` 是全局的 | 定义在那里的变量整页可见 |
| **选择器可以限定作用域** | 在组件里定义，就把它**本地化**了 |
| **子元素自动继承** | 子元素能直接读到父元素的 `--name`，**不需要重新声明** |
| **在子元素上重定义即覆盖** | 重新声明一次，就改掉了继承来的值 |

```css
:root     { --brand: #1e4fa8; }
.card     { --brand: #3d7bd9; }   /* 这一棵树内部都变成 mid 色 */
```

> [!important] 这就是普通的继承，不是例外
> 自定义属性**不是**普通属性继承的特例，它用的就是同一套继承机制：父元素上有的，子元素读得到；子元素上重新写的，就地覆盖。普通属性「文本属性会流下去、盒属性留在原地」那条规律，同样适用于变量 —— 详见 [[继承]]。
>
> 换句话说：**变量的继承不是「CSS 变量自己的设计」，是继承这件事本身。** 理解了 [[继承]]，这一节就免费了。

## 六、主题：改几个变量，整页跟着变

把颜色和尺寸集中在 `:root`，再用一个类**只覆盖变量本身**：

```css
:root {
  --bg:   #f0f5fc;
  --text: #1a2230;
}
body.dark {
  --bg:   #1a2230;
  --text: #f0f5fc;
}
```

课件点名了这套办法的四个好处：

| 好处 | 说明 |
|---|---|
| **一个地方** | 颜色和尺寸住在 `:root` |
| **深色模式只改变量** | 一个 `.dark` 类就够了 |
| **组件不用重写** | 组件仍然写 `var(--brand)`，**自动更新** |
| **切换开关** | 从 JavaScript 翻这个类即可 |

```js
// 一个类，就是整套主题的开关
document.body.classList.toggle('dark');
```

> [!important] 这是「同一个色值不要写两遍」的解法
> Tutorial 1（色彩理论）的 Rules Worth Remembering 一页把这条单独立了出来：*「Do not write colour twice — the same hex pasted into twenty rules drifts apart the moment you rebrand. Define it once as a CSS variable, then use the variable.」*
>
> 同一个十六进制值粘进二十条规则里，改版那天它们就会各走各的。定义一次、用变量引用，是唯一的防漂移手段。四种颜色写法见 [[颜色表示法]]。

## 七、易错点小结

- [ ] 忘记两个连字符：`--brand`，不是 `-brand` 或 `$brand`。
- [ ] 大小写写错：`--Brand` 和 `--brand` 是两个变量，**静默失效**。
- [ ] 用了没定义的变量且没写兜底：那条声明直接作废，元素退回默认样式。
- [ ] 把变量定义在某个组件上，却指望它影响组件**外面** —— 作用域是向下的，不是双向的。
- [ ] 以为变量必须定义在使用之前 —— 不需要，`:root` 里的定义整页都读得到。

## 关联

- 这就是继承本身 → [[继承]]（变量的作用域与覆盖，走的是和普通属性完全相同的继承机制）
- 课件点名的那个动机 → [[颜色表示法]]（「同一个色值不要写两遍」，变量是它的解法）
- 变量的典型载荷 → [[配色方案]]（一套配比方案落成代码，就是几个命名好的色值）
- 定义在 `:root` 之后还要切换时 → [[响应式与媒体查询]]（`prefers-color-scheme` 可以不写一行 JavaScript 就跟着系统走）
- 颜色值怎么写 → [[透明度与叠加层]]（变量里存 `rgba()` 时，alpha 是另一条独立的轴）
- 收录本主题全部属性 → [[index]]（本目录共 8 篇，这一篇属于其中的「Miscellaneous」一组）
