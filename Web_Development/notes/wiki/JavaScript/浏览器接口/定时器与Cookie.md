---
tags: [WD, 浏览器对象, 定时器, Cookie, setInterval]
domain: [Web 应用开发, JavaScript 浏览器接口]
course: COMP3421
lecture: L06
---

# 定时器与Cookie · Timing Events & Cookies

> **一句话**：`setTimeout` 只跑一次、`setInterval` 一直重复到被清掉，而**每一个 `setInterval` 都必须把它返回的句柄存下来**；Cookie 则是浏览器替你存的小段文本——**一个 `document.cookie` 就同时管读、写、追加**。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇对应 §7 *The DOM & the BOM* 里的 "Timing Events" 与 "Cookies" 两页。

## 一、定时器

| 成员 | 行为 |
|---|---|
| `setTimeout(fn, ms)` | **runs once** —— 在给定的毫秒数之后跑一次 |
| `setInterval(fn, ms)` | **repeats until you clear it** —— 每隔这些毫秒重复一次，直到你清掉它 |
| `clearTimeout(id)` | 停掉一个你起的 `setTimeout` |
| `clearInterval(id)` | 停掉一个你起的 `setInterval` |

### 跑一次 vs 一直重复

课件原句：**`setInterval` repeats until you clear it — always keep the handle it returns**。

```js
// 跑一次：一秒后打一行日志，就结束了
const t = setTimeout(() => {
  console.log("one second later");
}, 1000);

// 一直跑：每隔一秒执行一次 tick，直到 clearInterval
const id = setInterval(tick, 1000);

clearInterval(id);   // 这时候 id 必须还在手边
```

`setTimeout` 那个 `t` 和 `setInterval` 那个 `id` 都是**句柄（handle）**——浏览器交回来的一个凭证，之后就靠它来停这个定时器。

### 必须留句柄

> [!warning] 忘了 `setInterval` 的句柄，就停不下来
> 如果把 `setInterval(tick, 1000)` 写成一条不保存返回值的语句，之后就没法停它——`clearInterval` 需要一个句柄，而这个句柄已经丢了。课件因此把 *always keep the handle it returns* 单独写出来。
>
> 判断有没有走对，看一眼变量的名字：起的定时器有没有一个对应的 `id` 被存在某个变量里。

```js
const id = setInterval(tick, 1000);   // ✅ 句柄在手，随时能停
setInterval(tick, 1000);              // ❌ 停不下来

clearTimeout(t);     // 停掉那个 setTimeout
clearInterval(id);   // 停掉那个 setInterval
```

### 定时器不阻塞

课件第四句：**Timers do not block — The rest of the page keeps running while they wait**（定时器不阻塞：等待期间页面其余部分照跑）。

```js
const id = setInterval(() => {
  console.log("tick");
}, 1000);

console.log("这一行立刻就执行了");   // 不等一秒
```

一秒之后 `tick` 才第一次打印，而中间这一秒里页面完全正常——用户能点、能滚、能输入。**等待的是一个将来的时刻，不是卡住一段时长**。这个性质来自"回调 + 将来某个时刻再调"这个模型本身（回调写法见 [[函数表达式与自执行]]）。

## 二、Cookie

| 课件的说法 | 展开 |
|---|---|
| **Small pieces of text** | 浏览器**为你的站点**存下的小段文本，之后**再送回来** |
| **One property does it all** | `document.cookie` **读、写、追加**三件事共用一个属性 |
| **A name, a value, and options** | 名字、值、选项；`expires`、`path` 和安全标记**跟在分号后面** |
| **Every request carries them** | 每个请求都带着它们——这既是它们成为经典会话机制的原因，也是它们被规范管理的原因 |

### 读、写、追加：一个属性

```js
document.cookie = "username=John Doe";
document.cookie = "theme=dark; expires=Thu, 18 Dec 2026; path=/";
document.cookie;   // 两个键值对拼在一起的一整个字符串
```

同一个属性既写又读。第三句执行完再读 `document.cookie`，拿到的是两条记录连成的**一个字符串**（形如 `username=John Doe; theme=dark`），不是一个对象——想单独取某个值才需要在字符串里自己拆。

### 名字、值、选项

一条 cookie 的形状是 **名字 = 值**，后面跟若干**分号分隔**的选项：

```js
document.cookie = "username=John Doe";                          // 只有名字和值
document.cookie = "theme=dark; expires=Thu, 18 Dec 2026; path=/";  // 带上有效期和作用路径
```

| 部分 | 作用 |
|---|---|
| `username` / `theme` | 名字（key） |
| `John Doe` / `dark` | 值（value） |
| `expires=…` | 到期时间；不写就是一个会话级 cookie，关掉浏览器就没了 |
| `path=/` | 哪些路径的请求会带上它 |
| 安全标记 | 课件提到它们跟在分号后面，但这一页没有逐项展开 |

注意值里的空格不需要引号：写 `"username=John Doe"` 里的空格是合法值的一部分，分号才是分隔选项的符号——所以值本身不能含分号。

### 每个请求都带着它

**Every request carries them** 是这一页最重的一句。Cookie 的机制是：浏览器替你的站点存下这些小段文本，**之后对该站点的每一次请求都自动附上**。所以它成了经典做法里的**会话机制**（记一个 session id，请求自动带上，服务端就知道是谁）。

同一个性质也带来它被规范管理的原因：既然每个请求都带，cookie 能存的东西就受请求头大小的限制，累积流量也受约束；能不能写进 cookie、要不要加密、跨站要不要带，都是要管的事。

## 三、串起来

定时器和 cookie 常一起出现——延迟一段时间之后读取一个值：

```js
document.cookie = "theme=dark";        // 写一个偏好

setTimeout(() => {
  const saved = document.cookie;       // 一秒后读回来
  const box = document.querySelector("#demo");
  if (box) {
    box.textContent = saved;           // 先查 null，再改属性
  }
}, 1000);
```

那一秒的等待不阻塞任何东西（第四节那条性质），所以页面在这一秒里完全可用。`demo` 指「示例站」的 `<div id="demo"></div>`，设定见 [[课程场景与阅读约定]]，「先查 `null` 再改属性」这条本库统一写法的完整版本见 [[修改元素]]。

## 关联

- 父对象 → [[BOM与window]]（`setTimeout` / `setInterval` / `document.cookie` 都是 `window` 这一层的全局成员）
- 回调 → [[函数表达式与自执行]]（传给定时器的那个函数是回调，它"将来被调用"的写法在这里第一次出现）
- 收尾 → [[事件监听器]]（用句柄停掉一个重复任务，对照用同一函数引用摘掉一个监听器，是同一类"留好句柄"的问题）
- 等待的用途 → [[事件基础]]（`onload` 等的是页面加载完，而定时器等的是一个时间点，两者触发时机不同）
- 跨站规则 → [[链接与图像]]（cookie 的发送范围跟着站点走，而站点就是 URL 的主机部分——同一个地址的 `hostname` 决定它带哪些 cookie）