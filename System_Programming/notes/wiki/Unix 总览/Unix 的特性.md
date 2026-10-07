---
tags:
  - 系统编程
  - Unix
  - 可移植性
  - 多用户
  - 多任务
  - 健壮性
created: 2026-10-07
type: 知识点
aliases:
  - Unix 的特性
  - Unix 特性
  - 可移植性
  - 多用户
  - 多任务
  - 健壮性
  - robustness
  - perror
  - errno
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L01]
source: "[01-Overview-of-Unix.pdf](<../../raw/01-Overview-of-Unix.pdf>)"
---

# Unix 的特性

> **一句话**：课件 p14 列出 Unix 的八条特性 —— **可移植、多用户、多任务、层次化文件系统、强大的 Shell、管道、网络、健壮**。前面六条是"能用"，**最后一条"健壮"是"出错时不崩"**，它是 Unix 工程哲学里最容易被忽略、却最重要的一条。

课件对应 L01 p14–p23。课件原文见 [01-Overview-of-Unix](<../../raw/01-Overview-of-Unix.pdf>)。

## 特性清单（p14 原文）

课件 p14 的完整清单：

| # | 特性 | 英文 | 笔记 |
|---|---|---|---|
| 1 | **Portability** 可移植性 | portability | 第一节 |
| 2 | **Multiuser Operation** 多用户 | multiuser | 第二节 |
| 3 | **Multitask Processing** 多任务 | multitasking | 第三节 |
| 4 | **Hierarchical File System** 层次化文件系统 | hierarchical FS | 第四节 |
| 5 | **Powerful Shell** 强大的 Shell | powerful shell | [[Unix 哲学与工具组合]] |
| 6 | **Pipes** 管道 | pipes | [[Unix 哲学与工具组合]] |
| 7 | **Networking** 网络 | networking | 第五节 |
| 8 | **Robustness** 健壮 | robustness | 第六节（最详细） |

## 一、可移植性（p15）

> *"Unix is a relatively **hardware independent** OS. Various mechanisms (**device driver**, various C program interfaces inside of the kernel and to the user level) are designed to **encapsulate the hardware specifics**, facilitating porting between hardware platforms."*

**三个机制，各自封住一类硬件细节：**

| 机制 | 封住什么 | 笔记 |
|---|---|---|
| **设备驱动 device driver** | 硬件寄存器、中断号、设备控制器 | [[Unix 组成结构]]（设备驱动那一节） |
| **内核内的 C 程序接口** | 处理器差异 | — |
| **用户级的 C 程序接口** | 系统调用约定 | [[../文件描述符与流/open read write close\|open/read/write/close]] |

**血统上的来源**是 1973 年改写成 C（见 [[Unix 是什么与由来]]）。

> [!tip] 可移植性的判据不是"能跑在几个平台"，而是"**要加一个新平台需要改什么**"
> - 差：把汇编重写一遍
> - 好：写一个驱动，其他不动
>
> 课件 p15 点名 **device drivers** 是关键（*"One key to the portability is the device drivers"*）。

## 二、多用户（p16）

> *"Unix is a **multi-user, multi-tasking** OS. **Multiple users** may run multiple tasks concurrently. This is very different from conventional PC OSs, such as **MS-DOS or Windows**, which allows concurrent execution of multiple tasks, but **not multiple users**."*

**关键区别（课件特意点出来的）**：

| | 多任务 | 多用户 |
|---|---|---|
| 含义 | 多个**程序**同时推进 | 多个**人**同时各用各的 |
| 单机可分性 | 单人也可以有多个程序在跑 | **必须有多个独立身份** |
| 隔离单位 | 进程 | **用户 + 权限** |

**"不是多用户"的意思**：MS-DOS/早期 Windows 可以同时跑多个程序，但**所有程序都属于同一个身份** —— 没有"这个文件属于谁、谁有权限动它"的概念。

**在 Unix 里每个进程都归属某个用户**（UID），见 [[../进程管理/进程标识与查看|进程标识与查看]]；文件也归属某个用户并分派权限，见 [[../文件系统结构/权限位与 ls -l|权限位与 ls -l]]。

**多用户的直接后果**（课件把这条线贯穿到很多页）：

- **健壮性要求极高**：一个用户写错的程序不能搞垮整台机器 → 于是有了"出错就返回错误码、不 abort"的风格（第六节）
- **权限模型**：谁能读写哪个文件 → [[../文件系统结构/权限位与 ls -l|权限位与 ls -l]]
- **共享与隔离**：多个用户要能共用一套工具，又要互相不干扰

## 三、多任务（p17）

> *"Even for a **single user**, **time sharing** can still support multi-tasking. Unix has some programs, such as the **system-wide accounting programs**, that **automatically run from time to time**."*
> *"Unix supports **background processing**, which allows a user to initiate a task 'in the background' and then proceed to other activities."*

**两条即使单用户也成立的路径：**

**① 时间共享（time sharing）**：即使只有你一个人在用，系统也在**多个任务之间快速切换**。课件举的例子是**系统级的记账程序**会自动定时运行 —— 你从没主动启动它，但它一直在跑。

**② 后台处理（background processing）**：启动一个任务放到后台，你**继续干别的**。课件 p17 提到这个特性，机制在 [[../进程管理/后台进程与守护进程|后台进程与守护进程]] 里展开（终端里是在命令末尾加 `&`）。

> [!warning] "多任务"在中文语境里有两个含义，别混
> - **多任务 multitasking**：一个 CPU 上多个任务轮流推进（时间片轮转）。**这里是这个意思。**
> - **多任务 multitasking（另一个含义）**：一个进程内部拆成多个可并行执行的流，即**线程**。
>
> 课件 L02 的"线程"讲的是**后者**。Unix 在 p17 讲的是**前者**。见 [[../进程与线程/进程映像与线程|进程映像与线程]]。

## 四、层次化文件系统（p18）

> *"Unix files are organized into **separate directories**. Directories are themselves organized into a **tree-like structure**. There is **one master directory**, the so-called **root directory**, from which various sub-directories branch off. The hierarchical structure offers **maximum flexibility for grouping information in a way that reflects its natural structure**."*

拆开看：

| 要素 | 内容 |
|---|---|
| **目录里装目录和文件** | 组织方式是**树**，不是平铺 |
| **唯一的根目录 root（`/`）** | 所有路径从它出发 |
| **按自然结构分组** | 课件强调的是"**反映信息的自然结构**" |

详细机制在 [[../文件系统结构/层次结构与路径名|层次结构与路径名]]，其中"为什么名字不在 inode 里"这个关键设计在 [[../inode 与链接/inode 与目录文件|inode 与目录文件]]。

**把文件系统说成"层次化"而不只是"有目录"，是因为** —— 目录**自己也是文件**、也能被放进目录，于是可以任意深度嵌套。见 [[../文件系统结构/文件类型|文件类型]] 里"目录 vs 普通文件"的对比。

## 五、网络（p21）

> *"Networking support is **built into** the Unix system. Supports **TCP/IP**, and provides a new OS abstraction, the **socket**, that allows **application-level programs** to access the Internet. The socket abstraction acts as an **interface** between application level programs and the underlying TCP/IP protocols."*

**两个要点：**

1. **TCP/IP 是内置的**，不是外挂
2. **socket 是 OS 提供的一种抽象**：把"应用程序访问网络"这件事，做成一个像文件一样的接口

**内核职责里对应的那一条**（[[Unix 组成结构]] 提到的 6 条之一）是 **network stack management（网络协议栈管理）**，但**课件 L01 没有展开** —— 这是本目录的一个已知缺口。

> [!tip] socket 的设计思想值得单独记
> 它是 Unix **"一切皆文件"** 传统的又一次体现：网络连接被包装成一个**可以 read/write 的对象**。
> 本课程的 raw 课件里没有 socket 的专题笔记，但这个思路和 [[../文件描述符与流/文件描述符与 SFT|文件描述符]] 是同一个。

## 六、健壮性（p22–p23）—— 最该记住的一条

这是八条特性里课件**用两页篇幅**展开的（p22、p23），其他七条基本一页一条。**篇幅本身就说明它是重点。**

### 核心思想（p22）

> *"When encountered an error, a Unix program **does not abort**. Instead, the program **receives a returned value indicating an error condition**, and it is **up to the program to check for the error and handle it**."*
> （遇到错误时，Unix 程序**不会中止**。相反，程序会**收到一个表示错误情况的返回值**，并且**由程序自己去检查并处理这个错误**。）

**三个关键词：**

| 关键词 | 含义 |
|---|---|
| **does not abort** | **不崩** —— 系统不会因为一个程序出错而挂掉 |
| **returns a value** | 出错用**返回值**报告，不是抛异常、不是终止进程 |
| **up to the program** | **责任在调用方** —— 内核只负责报告，不负责补救 |

### 返回什么值（p22）

> *"Typically, a returned error value is **negative if the return type is `int`**, or a **NULL** if the return type is a **pointer**."*

| 返回类型 | 成功 | 失败 |
|---|---|---|
| `int` | 非负（如 `read` 返回读了几个字节、`close` 返回 `0`） | **负值**（通常是 `-1`） |
| 指针（pointer） | 非 `NULL` | **`NULL`** |

**报错细节**：调用 **`perror()`** 可以把错误信息打印出来。

### 完整例子（p23）

课件给的例子是 `open`，我把每行都解释一遍：

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int fd;
if ((fd = open("my.file", O_RDONLY)) == -1)
        perror("Unsuccessful open of my.file");
```

**逐行读：**

| 行 | 含义 |
|---|---|
| `#include <fcntl.h>` | `open` 和 `O_RDONLY` 在这个头文件里 |
| `int fd;` | 声明一个整型变量 `fd` 存放**文件描述符**（见 [[../文件描述符与流/文件描述符与 SFT\|文件描述符]]） |
| `open("my.file", O_RDONLY)` | 打开 `my.file`，`O_RDONLY` 表示**只读** |
| `== -1` | **失败判定**：`int` 返回值类型下，失败返回负值 |
| `perror("...")` | 打印你给的前缀 + 系统记录的错误原因 |

**课件给出的实际输出**（如果 `my.file` 不存在）：

```
Unsuccessful open of my.file: No such file or directory
```

**注意格式**：`perror` 先打印你传入的那句自定义消息，**冒号后面接系统给的错误原因**（这里是 `ENOENT` 的可读形式）。

### 为什么这条比前七条更重要

这是**多用户系统的必然要求**（见第二节）。把因果串起来：

```
多个用户共用一台机器（多用户，p16）
        ↓ 因此
一个用户的程序出错，绝不能拖垮整机（p22）
        ↓ 因此
每个可能出错的调用都必须「返回错误码」而不是「中止」
        ↓ 因此
调用方的代码里到处都要检查返回值
        ↓ 于是
坑特别多 —— 这就是所有 Unix 程序都长这样的原因
```

> [!warning] 这条特性是"特性"也是"代价"
> "每个调用都要检查返回值"意味着：
> ```c
> fd = open(a, O_RDONLY);
> if (fd == -1) { perror("open a"); return -1; }
> n = read(fd, buf, sizeof buf);
> if (n == -1) { perror("read"); return -1; }
> ```
> 代码量比"直接崩掉"多了一大截。
>
> 但换来的是：**一个失败的操作不会悄悄毁掉别的数据**。在多用户、要长期运行、要能被别人依赖的系统里，这个交换是划算的。
>
> 后续笔记里会反复看到这个模式：[[../进程管理/wait 等待子进程|`wait` 的 `ECHILD` / `EINTR`]]、[[../文件描述符与流/open read write close|open/read/write/close 的返回值]]、[[../文件系统结构/当前工作目录|`getcwd` 的 `ERANGE`]]。

## 八条特性速查

| # | 特性 | 一句话 | 落地在哪篇笔记 |
|---|---|---|---|
| 1 | 可移植 | **驱动 + C 接口**把硬件细节封起来 | [[Unix 组成结构]] |
| 2 | 多用户 | 每人一个**独立身份**，互不干扰 | [[../进程管理/进程标识与查看]]、[[../文件系统结构/权限位与 ls -l]] |
| 3 | 多任务 | 单人也多任务：**时间共享 + 后台处理** | [[../进程管理/后台进程与守护进程]] |
| 4 | 层次 FS | 目录自己也是文件，构成**唯一的根之树** | [[../文件系统结构/层次结构与路径名]] |
| 5 | 强大的 Shell | 重定向 + 脚本 + 参数 | [[Unix 哲学与工具组合]] |
| 6 | 管道 | 输出直接接输入，**中间不落盘** | [[Unix 哲学与工具组合]]、[[../重定向与管道/管道与进程间通信]] |
| 7 | 网络 | TCP/IP 内置，**socket** 做抽象 | 本讲第五节（机制未展开） |
| 8 | 健壮 | **不 abort**，返回错误码，`perror` 报告 | 本讲第六节 |

## 一句话

> 八条特性里前七条是"Unix 能干什么"，**第八条"健壮"是"Unix 出错时怎么办"** —— 它是多用户系统的必然要求，也是读懂所有 Unix C 代码的钥匙。

## 相关笔记

- **上一节**：[[Unix 组成结构]] — 这些特性由哪几层实现
- **特性的思想来源**：[[Unix 哲学与工具组合]]
- **血统**：[[Unix 是什么与由来]]
- **多任务落到 L02**：[[../进程与线程/进程是什么]]、[[../进程管理/后台进程与守护进程]]
- **层次 FS 落到 L03**：[[../文件系统结构/层次结构与路径名]]
- **健壮的代码实例**：[[../文件描述符与流/open read write close|open/read/write/close]]
- **本讲总览**：[[../index|系统编程 MOC]]