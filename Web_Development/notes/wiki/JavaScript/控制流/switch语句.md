---
tags: [WD, 流程控制, switch, break, 兜底分支]
domain: [Web 应用开发, JavaScript 控制流]
course: COMP3421
lecture: L06
---

# switch语句 · The switch Statement

> **一句话**：`switch` 把**一个表达式**和**一串固定的取值**逐个比对（每个 case 只比一次，按顺序比）；`break` 负责挡住"掉进下一个 case"的连锁执行，`default` 接住所有没匹配的；**判断的是固定值才用它，区间和计算继续用 `if` / `else if`**。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇覆盖 §4 Statements 中 The switch Statement 一页：表达式与 case 的比对规则、`break` 与穿透（fall-through）、`default` 的职责，以及 `switch` 与 `if` 的分工。

## 一、它是怎么工作的

`switch` 只做一件事：**拿一个表达式的值，和每个 `case` 的值比一遍**。

```
switch (表达式) {
  case 值1: ... break;
  case 值2: ... break;
  default:  ...
}
```

三个关键词的职责：

| 关键字 | 职责 | 少了会怎样 |
|---|---|---|
| `switch (表达式)` | 求出**一个**值，接下来拿它当比较对象 | —— |
| `case 值` | 和那个值比一次。**只在比较，不写条件表达式** | —— |
| `break` | **跳出整个 `switch`** | **掉进下一个 case 继续执行**（fall-through） |
| `default` | 所有 case 都没匹配时执行 | 什么都不做，且看不出来 |

关键点：**表达式只求值一次**，然后 case **从上到下逐个比**。所以 `case 5 + 5:` 里的计算只在轮到它时才算，`case time < 10:` 这类"条件"根本不该出现在 `switch` 里——`switch` 只做相等比较，不做真值判断。

## 二、`break` 挡住连锁执行

`case` 本身**不会**自动结束上一个 case。不写 `break`，执行完一个分支就会**直直地掉进下一个分支**，把它的代码也跑一遍。这叫 **fall-through**（穿透）。

> [!warning] 忘写 `break` 不报错，只是行为变了
> ```js
> let x = 1;
> switch (x) {
>   case 1:
>     text = "one";       // 执行了
>   case 2:               // 没 break，掉进来了
>     text = "two";       // 也执行了 —— 覆盖掉了上面那行
> }
> // text === "two"，而 x 只是 1
> ```
> 症状是**结果莫名其妙地变了**，而不是语法错误或运行时报错，所以特别难查。写完每个分支扫一遍：每个 case 后面要么有 `break`，要么有一句注释说明"这次故意要穿透"。

有一种情况是**故意**穿透的：几个 case 共用一段代码时，把它们叠在一起、共用一个 `break`——但这需要显式的注释标出意图，本课的写法是每段各自 `break`。

## 三、`default` 永远要写

`default` 是在**所有 `case` 都没匹配**时执行的兜底分支。课件的态度很直接：*It runs when nothing matched — always include one*。

```js
switch (value) {
  case 1:  ...; break;
  case 2:  ...; break;
  default: ...;      // ← 其他所有值
}
```

不写 `default` 的后果不是"出错"，而是**静默地什么都不发生**。页面上就是点了按钮没反应，且没有任何提示。写上 `default` 之后，"没匹配上"这件事至少**能被说出来**（哪怕只是 `console.log`）。

## 四、完整例子：星期几

```js
switch (new Date().getDay()) {
  case 6:
    text = "Today is Saturday";
    break;
  case 0:
    text = "Today is Sunday";
    break;
  default:
    text = "Looking forward to the weekend";
}
```

`new Date().getDay()` 每天返回一个 **0–6 的整数**，其中 **`0` 是星期日**、`6` 是星期六。走一遍：

| `getDay()` | 是 | 匹配 | `text` |
|---|---|---|---|
| `6` | 星期六 | `case 6` → `break` | `"Today is Saturday"` |
| `0` | 星期日 | `case 6` 不中 → `case 0` → `break` | `"Today is Sunday"` |
| `1`–`5` | 星期一至五 | 都不中 → `default` | `"Looking forward to the weekend"` |

**注意 case 的顺序不重要，但 `default` 习惯写在最后**，这样一眼能看出"上面是具体值，下面是兜底"。

## 五、什么时候用 `switch`，什么时候不用

| 需求 | 用 | 为什么 |
|---|---|---|
| 一个值对应几种固定选择（星期、菜单、状态码） | `switch` | 条件互斥、取值固定，结构一眼看完 |
| 判断一个值的范围（`0 <= age <= 18`） | `if` / `else if` | `case` 只认相等，写不出范围 |
| 拿值做计算再比较（`score * 100 > 90`） | `if` / `else if` | 同样的原因 |
| 条件之间有"更具体优先"的次序 | `if` / `else if` | 链的短路顺序要能一眼看出来 |
| 布尔判断（`isOpen`） | `if` | `switch` 对两个 `case` 没有优势 |

课件那句总结是：*Use it for fixed values. Ranges and calculations read better as if / else if.*

> [!warning] `switch` 用的是严格相等
> `switch` 内部的比较**等价于 `===`**：不做类型转换。所以 `switch (value)` 配 `case 0`，遇到字符串 `"0"` **不会匹配**。这正好是它的好处（不像 `==` 那样偷偷转换），但从 `if` 换到 `switch` 时要留意：如果 `value` 是从表单读来的字符串，条件就不是数字了（见 [[字符串与数字]]）。

## 六、写进示例站

```js
let day = new Date().getDay();
let text;

switch (day) {
  case 6:
    text = "Today is Saturday";
    break;
  case 0:
    text = "Today is Sunday";
    break;
  default:
    text = "Looking forward to the weekend";
}

const demo = document.getElementById("demo");
if (demo) {
  demo.innerHTML = "day " + day + ": " + text;
}
```

## 关联

- 平级选择 → [[条件语句]]（同一批"多选一"的需求；判断区间和计算时用 `if` 链）
- 机制依赖 → [[比较与typeof]]（`switch` 内部是严格相等，不做类型转换）
- 数据前提 → [[类型系统]]（`getDay()` 返回 `number`，所以 `case 6` 能匹配上）
- 同组邻居 → [[循环语句]]（`switch` 常写在循环里对每个元素做分派）
- 实践场景 → [[事件处理与常见事件]]（把 `event.key` 映射到不同动作，是 `switch` 的典型形状）
