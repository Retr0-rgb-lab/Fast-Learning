---
tags: [WD, 全栈概览, HTTP, URL, 状态码]
course: COMP3421
lecture: L01
---

# HTTP与URL · The Language and the Address

> **一句话**：HTTP 的请求和响应都只有**三段**（起始行 / 头 / 体），URL 也只有**六段**，本篇是这两张表的骨架认读——**Week 1 只认得它们存在，Week 9 才拆到能自己构造**。

课件原文见 [Lecture_01_Overview.pptx](<../../raw/Lecture_01_Overview.pptx>)。本篇覆盖其中 "Backend" 一节的前两页：HTTP — The Language of the Web 与 URLs — The Address of Everything。

> [!warning] 覆盖程度声明
> 课件在两页上都标了同一件事：HTTP 在 **Week 9 goes deep**，URL 是 **Week 9: URL anatomy in depth**。
> 因此**本篇只有一页概览的深度**，没有方法、状态码全表、缓存语义、条件请求等任何细节。Week 6–13 的课件尚未进入本库 `notes/raw/`，这些内容要等 Week 9 的课件到位后回头扩写（见 [[课程场景与阅读约定]] 里的覆盖缺口表）。

## 一、请求的三段

| 段 | 是什么 | 课件给的例子 |
|---|---|---|
| **Start line**（起始行） | 动词 + 路径 + 协议版本 | `GET /index.html HTTP/1.1` |
| **Headers**（头） | 一组键值对，描述"这次请求是谁发的、要什么" | `Host`、`User-Agent`、`Accept`、`Cookie`… |
| **Body**（体） | **有时才有**——POST 的时候装表单数据或 JSON | Form data, JSON — when you POST |

把课件给的零件拼起来，一次完整请求长这样（**这是按课件列出的字段拼装的示例，不是课件的逐字原文**）：

```http
GET /index.html HTTP/1.1
Host: www.polyu.edu.hk
User-Agent: <你的浏览器标识>
Accept: <你能接受的类型>
Cookie: <你此前存下的会话标识>
```

> [!note] 客户端这一端其实只有"一个动作"
> 请求体是**有时才有**的：课件写的是 "Body (sometimes)"。GET 一般不带体，POST 才带。所以判断一次请求要花多少力气，**先看起始行的动词**。

## 二、响应的三段

| 段 | 是什么 | 课件给的例子 |
|---|---|---|
| **Status line**（状态行） | 协议版本 + 状态码 + 状态短语 | `HTTP/1.1 200 OK` — or 404, 500… |
| **Headers**（头） | 一组键值对，描述"我给你什么、怎么缓存" | `Content-Type`、`Set-Cookie`、`Cache-Control`… |
| **Body**（体） | **你要的那个东西** | The HTML, JSON, image, or file you asked for |

同样按课件的字段拼装：

```http
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: <会话标识>=<值>
Cache-Control: <缓存指令>
```

（尖括号里的具体值课件没有给出，属于未展开的部分，**不要把上面这几行当成可运行的响应**。）

> [!important] 三个头要认得出来
> 课件点名的响应头里，有三个在本课程其他周次会反复出现：
>
> | 头 | 它回答的问题 | 本库哪一篇会展开 |
> |---|---|---|
> | `Content-Type` | **这次给我的是 HTML、JSON 还是图片？** | [[后端技术栈]] 里 `res.json()` 与 `res.writeHead()` 的区别 |
> | `Set-Cookie` | **服务器要在我这边存点什么？** | 后端会话与登录（Week 11 展开） |
> | `Cache-Control` | **这个能缓存多久？** | [[性能与可扩展性]]（Week 13 展开） |
>
> 请求侧的 `Host` 也重要：它让**同一台服务器**能同时服务多个域名，这也是 [[性能与可扩展性]] 里"负载均衡器后面挂多台应用服务器"能成立的前提。

## 三、URL 的六段

课件用一个地址把六段一次列全。按它给出的顺序拆开：

| 段 | 课件里的值 | 职责（课件原话的中译） |
|---|---|---|
| **scheme**（协议） | `https://` | **怎么说话**：https（加密）、http、file… |
| **host / domain**（主机 / 域名） | `www.polyu.edu.hk` | **哪台机器** |
| **port**（端口） | `:443` | **哪扇门**：课件写作 `polyu.edu.hk:443` |
| **path**（路径） | `/comp3421/week1` | **哪个资源** |
| **query**（查询串） | `?q=web` | **额外参数**，课件举的完整形式是 `?q=web&lang=en` |
| **fragment**（片段） | `#top` | 页内定位（课件列出了它，但没有单独给它一段职责说明） |

拼起来就是：

```
https://www.polyu.edu.hk:443/comp3421/week1?q=web#top
└──┬──┘└──────┬───────┘└┬┘└──────┬──────┘└───┬───┘└──┬──┘
scheme      host      port      path       query   fragment
```

> [!tip] 记忆锚点：六段的三个问题
> **怎么说话 → 跟谁说话 → 说哪扇门 → 要哪个东西 → 附带什么条件 → 页内跳到哪。**
> 课件那句总结是 "Every piece has a job"，并且补了一句现实观察：**"and the browser hides it all in the address bar"**——六段信息全部存在，但地址栏只给你看其中一部分。
>
> 课件对 `https` 的标注是 **secure**（加密），这一点在 [[性能与可扩展性]] 的旅程起点也会再出现一次：即使是"最简个人网站"，那次访问也是走 **HTTPS** 的。

## 四、三点最容易记混

| 容易混 | 分辨 |
|---|---|
| **path vs query** | 课件用 `Which resource` 对 `Extra parameters` 来分：path 定位**哪一个资源**，query 追加**额外参数**。`?q=web` 不是另一个资源，是同一个资源的另一种调法。 |
| **host vs 站点** | `Host` 请求头 + 域名，合起来决定"连到哪台机、哪个门"。课件在 Host & port 那栏把两者合写成 `polyu.edu.hk:443`，说明它们是一对。 |
| **HTTP 不是"只有请求体"** | 响应**一定有**体（课件对请求体才特意标了 "sometimes"）。200/404/500 都可能是"有体"的——404 的体通常就是一张错误页。 |

> [!warning] 不要在这里下结论的
> 状态码课件只列了 `200 / 404 / 500` 三个作为示例，**本库不会据此推导完整状态码分类**；`Cache-Control` 的语义、`Accept` 的协商规则、HTTP/1.1 与 HTTP/2 的差异都留给 Week 9 与 Week 13（见 [[性能与可扩展性]]）。

## 关联

- 承接 → [[Web应用与客户端-服务器模型]]（本篇的 HTTP 就是那一页"双方唯一的共同语言"）
- 承接 → [[三层架构]]（第一跳 HTTP 的具体形状；第二跳 SQL 不在本篇范围）
- 后续 → [[后端技术栈]]（Week 10–11 的 Express、REST 全部建在 HTTP 之上）
- 后续 → [[性能与可扩展性]]（`Cache-Control` 头在 Week 13 才真正展开）
- 跨目录 · 前端那一面 → [[表单与输入]]（`method` 决定表单数据进不进请求体，`action` 决定 path 怎么写）
- 跨目录 · 同样两种形态 → [[链接与图像]]（`href` 的各种写法，就是 URL 六段的各种省略写法）
