---
tags:
  - 系统编程
  - Unix
  - 历史
  - POSIX
created: 2026-10-07
type: 知识点
aliases:
  - Unix 是什么
  - Unix 由来
  - Unix 家族树
  - POSIX
  - 可移植操作系统接口
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L01]
source: "[01-Overview-of-Unix.pdf](<../../raw/01-Overview-of-Unix.pdf>)"
---

# Unix 是什么与由来

> **一句话**：Unix 是一族**多任务、多用户**的操作系统，起源于 1970 年代贝尔实验室。它之所以能存在至今、并且几乎所有现代系统都在模仿它，靠的是一件事：**1973 年被 Ken Thompson 和 Dennis Ritchie 用 C 语言重写了一遍**，从此它可以被移植到任何有 C 编译器的机器上。

课件对应 L01 p3–p4。课件原文见 [01-Overview-of-Unix](<../../raw/01-Overview-of-Unix.pdf>)。

## 完整场景

**这一节不预设你了解这段历史。** 时间线从头梳理。

### 起点：1969 年的贝尔实验室

课件 p3 引用 Wikipedia 的定义：

> *"Unix is a family of **multitasking, multiuser** computer operating systems that derive from the original AT&T Unix, development starting in the **1970s** at the **Bell Labs** research center by **Ken Thompson, Dennis Ritchie**, and others."*

拆开这句话里的四个要点：

| 词 | 含义 |
|---|---|
| **family（家族）** | Unix 不是**一个**操作系统，而是**一族**共享同一套设计思想的系统 |
| **multitasking（多任务）** | 一台机器上可以同时推进多个"正在运行的程序" |
| **multiuser（多用户）** | 多个**真实的人**可以同时各用各的 |
| **AT&T Unix / Bell Labs** | 起源是美国电话电报公司（AT&T）贝尔实验室的 UNIX 研究组 |

### 分水岭：1973 年改写成 C（p4）

课件 p4 列出三件关键事实：

1. **originally written in assembly**（最初用**汇编语言**写成）
2. **In 1973, v4 was mostly rewritten in C**（1973 年，第四版基本上用 **C** 重写）
3. **making it portable**（这才使它**可移植**）

> [!warning] "可移植"这一步为什么这么关键
> 汇编语言是**跟硬件绑死**的。同一个 `ls` 程序，用 x86 汇编写的就只能在 x86 上跑。
>
> 改写成 C 之后，源代码不变、换一个平台**重新编译**就能用。
> **"一份源码 + 任意平台的编译器" = 可移植。** 这是 Unix 家族能扩张到几乎所有平台的唯一原因。
>
> 这个逻辑在 [[Unix 的特性]] 里"可移植性"那一条会再次出现，从工程机制的角度展开。

### 后来：POSIX 标准（p4）

**POSIX = Portable Operating System Interface**（可移植操作系统接口），课件把它标在家族树图上，旁边写着一句话：

> *"POSIX to **unify Unix APIs**"*

**Unix 家族越来越大，分支各有各的系统调用**，应用程序想在不同 Unix 上跑就很麻烦。POSIX 就是**把各家 API 统一起来**的标准。

> [!tip] 有了 POSIX，"Unix"这个词就分成了两个意思
> - **历史意义**：指 AT&T / 贝尔实验室那一条血统（真正的 Unix）
> - **工程意义**：指"**符合 POSIX 标准的任何系统**"
>
> 第二节会看到 Linux 正好卡在这个区分上——它**血统上不是 Unix**，但**标准上是**。见 [[Unix 家族与变体]]。

## 本讲后续内容的入口

知道"Unix 是一族可移植的、多用户多任务的系统"之后，真正的问题才刚开始：

| 问题 | 由哪篇笔记回答 |
|---|---|
| 它由哪几部分组成？谁管谁？ | [[Unix 组成结构]] |
| 为什么设计成这样？ | [[Unix 哲学与工具组合]] |
| 多用户 / 多任务 / 可移植具体指什么？ | [[Unix 的特性]] |
| Linux、macOS 算不算 Unix？ | [[Unix 家族与变体]] |

## 一句话

> Unix 始于 1970 年代的贝尔实验室；**1973 年改写成 C** 这一步让它从"只能在贝尔实验室的机器上跑"变成"能在任何机器上跑"，这才有了后来的 Unix 家族。

## 相关笔记

- **下一步**：[[Unix 组成结构]] — 这个系统到底由哪几块组成
- **设计动机**：[[Unix 哲学与工具组合]]
- **可移植性怎么实现**：[[Unix 的特性]]、[[Unix 组成结构]]（设备驱动那一层）
- **血统与标准**：[[Unix 家族与变体]]
- **本讲总览**：[[../index|系统编程 MOC]]