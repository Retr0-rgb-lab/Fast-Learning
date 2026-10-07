---
tags:
  - 系统编程
  - Unix
  - Linux
  - POSIX
  - 家族树
created: 2026-10-07
type: 知识点
aliases:
  - Unix 家族与变体
  - Unix 变体
  - Unix 家族树
  - Unix-like
  - Linux
  - Android
  - Mac OS X
  - macOS
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L01]
source: "[01-Overview-of-Unix.pdf](<../../raw/01-Overview-of-Unix.pdf>)"
---

# Unix 家族与变体

> **一句话**：**Linux 不是 Unix**（它没继承 Unix 的代码），但**按 POSIX 标准算，Linux 可以被看作一种 Unix**。课件 p25 把这件事说得很直接：**Unix 这个词有两层意思 —— 历史血统 vs 标准符合度。**

课件对应 L01 p24–p28。课件原文见 [01-Overview-of-Unix](<../../raw/01-Overview-of-Unix.pdf>)。

## 完整场景：为什么"Linux 是不是 Unix"这个问题会有两种答案

**要回答这个问题，得先把"算不算"这件事拆成两个判据：**

| 判据 | 问题 | Linux 的答案 |
|---|---|---|
| **血统（血统）** | 代码是不是从原始 Unix 传下来的？ | **不是** —— 从零重写 |
| **标准（标准）** | 符不符合 POSIX？ | **是** —— 符合 |

**这两个判据可以给出不同答案，于是"Linux 是不是 Unix"这句话本身就问糊了。**

## Linux：血统不是，标准是（p25）

课件 p25 的三层表述，逐条看：

> *"Strictly speaking, Linux source code is **not inherited from the Unix family tree**. Linux is a **Unix-like OS**."*
> （严格说来，Linux 源码**不是从 Unix 家族树继承来的**。Linux 是一个 **Unix-like（类 Unix）** 系统。）

> *"**But if you consider the Portable Operating System Interface (POSIX) standards**, then Linux **can be regarded as a kind of Unix**."*
> （**但如果按 POSIX 标准来看**，Linux **可以被当作某种 Unix**。）

> *"Linux is a Unix clone written from scratch by Linus Torvalds with assistance from hackers across the Net"* —— Linux 内核 README 的官方说法
> （Linux 是 Linus Torvalds 在 Net 上的黑客们协助下**从零写出来的 Unix 克隆**。）

### 三个词要分清

| 词 | 含义 | Linux |
|---|---|---|
| **Unix** | 原始 AT&T Unix 的**血统** | ❌ 不是 |
| **Unix-like / 类 Unix** | "长得像 Unix"（接口、命令、行为兼容） | ✅ 是 |
| **POSIX** | 把 Unix API 统一的**标准**（见 [[Unix 是什么与由来]]） | ✅ 符合 |

> [!warning] "写了 20 年、别人也叫它 Unix"的现实
> Linux 内核官方 README 自己用的词是 **"Unix clone"**（Unix 克隆），**不是** "Unix"。
>
> 但在实际工程语境里，人们日常会把 Linux 和各种 Unix 系统统称为"Unix 系统"，甚至说"Linux 就是 Unix"。**这在做课程作业、读文档时要小心**：课件强调的是**严格意义上的区分**。

## Android：建在 Linux 上（p26）

课件 p26 只给了两张图和一句话：

> *"Android architecture"（quoted from Wiki）*

**关键词是（based on Linux）** —— Android 架构建立在 Linux 内核之上。

> [!note] 课件没有展开
> p26 是一张 Android 架构图 + 一个链接，**没有文字说明**。本页只登记"Android 基于 Linux"这个事实，不推测其细节。

## Mac OS X（p27）

课件 p27 同样只给了：

> *"Mac OS X architecture"（quoted from Wiki）*

一张架构图。**本目录没有对应笔记。**

> [!note] 课件 p27–p28 的实际内容是"链接页"
> p27 是 Mac OS X 架构图，p28 是三个外部链接（UNIX-systems.org、bell-labs.com/history/unix）。**这三页是"课后看看"的清单，不是要讲的知识点。**

## 家族树在课件里的画法（p4）

课件 p4 把家族树画成一张图，上面标注了三件事：

```
原始 Unix（AT&T / Bell Labs, 1970s）
   │
   ├── 写汇编
   ├── 1973: v4 改写成 C  ← 可移植性的起点
   │
   ▼
  各家分支 ──────→ POSIX（把 API 统一起来）
```

**图上的两个标注，正好对应本篇的两个判据：**

- 左侧的血统线（各厂商从原始 Unix 分支）
- 右侧的 POSIX 汇聚（不同分支被同一标准统一）

> [!tip] 家族树与标准的关系，一句话
> **血统决定"代码从哪来"，标准决定"接口长什么样"。**
> 代码血统可以完全不同（Linux），但接口可以一模一样（都符合 POSIX）—— 这正是 POSIX 存在的意义，见 [[Unix 是什么与由来]]。

## 为什么本课程要学"Unix-like"系统

这不是课程明说的推断，而是从 [[Unix 组成结构]] 的可移植性机制反推出来的：

| 层次 | 接口是否统一 | 统一了吗 |
|---|---|---|
| **系统调用（API）** | 由 **POSIX** 统一 | ✅ 是 |
| **文件描述符模型** | 文件描述符模型 | ✅ 是 |
| **文件系统语义** | inode / 路径名 | ✅ 基本是 |
| **内核内部结构** | 不统一 | ❌ 各家不同 |
| **设备驱动** | 硬件相关 | ❌ 各家不同 |

**所以"可编程接口"在 POSIX 这一层被统一了，而"内核怎么实现"没有。** 这意味着：

- 本课程讲的 `fork` / `exec` / `wait` / `open` / `read` / `pipe` 这些，**在 Linux、macOS、各家 Unix 上都能用**（因为它们是 POSIX 接口）
- 但它们的**内部实现、调度算法、内核数据结构**可能差别很大（因为那没统一）

> [!note] 这个区分在本目录后续的意义
> [[../进程管理/fork 创建进程|`fork`]]、[[../文件描述符与流/open read write close|`open`]] 这些笔记讲的是 **POSIX 层的接口契约**。
> 遇到"这个系统上 `fork` 有什么特殊行为"这类问题时，要意识到**那已经是 POSIX 之外的事**了。

## 一句话

> **Linux 与 Unix 的关系是：代码血统无关，但接口标准一致（POSIX）** —— 课件 p25 用两句话讲清了这件事，其余变体（Android、macOS）课件只给架构图，未展开。

## 相关笔记

- **上一节**：[[Unix 的特性]] — 可移植性是怎么做到的
- **POSIX 是什么**：[[Unix 是什么与由来]]
- **统一标准的具体内容长什么样**：[[../文件描述符与流/open read write close|open/read/write/close]]（POSIX 接口实例）
- **内核实现为何不统一**：[[Unix 组成结构]] — 设备驱动那一层是硬件相关的
- **本讲总览**：[[../index|系统编程 MOC]]