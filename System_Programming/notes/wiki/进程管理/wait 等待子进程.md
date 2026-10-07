---
tags:
  - 系统编程
  - Unix
  - 进程管理
  - wait
  - 孤儿进程
  - errno
created: 2026-10-07
type: 知识点
aliases:
  - wait 等待子进程
  - wait
  - waitpid
  - 孤儿进程
  - orphan process
  - ECHILD
  - EINTR
  - errno
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L02]
source: "[02-Unix-Processes.pdf](<../../raw/02-Unix-Processes.pdf>)"
---

# wait 等待子进程

> **一句话**：父进程要等孩子干完，就调 `wait()`。它返回**那个刚结束的孩子的 PID**（正数），失败返回 **`-1`** 并设 `errno`。**最要紧的一条**：父进程要是先死了没等，孩子就成了**孤儿进程（orphan process）**，而创建孤儿"几乎总是糟糕的编程实践"。

课件对应 L02 p29–p32。课件原文见 [02-Unix-Processes](<../../raw/02-Unix-Processes.pdf>)。

## 完整场景

[[../进程管理/fork 创建进程|fork]] 之后，父进程手里有两个东西要处理：

1. **孩子还在跑** —— 要不要等它？
2. **孩子跑完了** —— 它干得怎么样？退出码是多少？

**`wait()` 就是处理第 2 件事的阻塞式接口**：调它，进程**挂起**直到有孩子结束，然后拿到那个孩子的 PID 和退出状态。

## 一、wait 的原型与语义（p29）

课件 p29 给出原型：

$$
\texttt{pid\_t wait(int *stat);}
$$

> *"In general, the `wait` system call causes the caller process to **pause until a child terminates or stops**, or until the caller **receives a signal**."*
> （一般来说，`wait` 系统调用使调用者进程**暂停，直到某个子进程终止或停止，或者调用者收到一个信号**。）

**两个要点：**

| 要点 | 含义 |
|---|---|
| **pause（阻塞）** | 这是一个**阻塞**调用，父进程会**停在这儿**不干活 |
| **直到…或者…** | 结束的是 **terminated（终止）** 或 **stops（停止）**，**或者**有**信号**打断它 |

### `stat` 这个出参

> *"The `stat` is a **pointer to an integer variable** that **stores the exit status of the child**."*
> （`stat` 是一个**指向整型变量的指针**，用来**存放子进程的退出状态**。）

所以典型用法是：

```c
int status;
pid_t pid = wait(&status);
/* pid  = 哪个孩子结束了
   status = 那个孩子怎么结束的   */
```

## 二、返回值与错误码（p31）

课件 p31 的两条规则：

> *"If `wait` returns because a **child terminated**, the return value is **positive** and is the **PID of that child**."*
> （如果 `wait` 是因为某个**子进程终止**而返回，返回值是**正数**，即**那个子进程的 PID**。）

> *"Otherwise, `wait` returns **–1** and **sets `errno`**."*
> （否则，`wait` 返回 **–1** 并**设置 `errno`**。）

### 两种 errno

课件明确点名两个：

| `errno` 值 | 含义（课件原文） |
|---|---|
| **`ECHILD`** | *"there were **no unwaited-for child processes**"* — **没有还没被等待的子进程** |
| **`EINTR`** | *"the call was **interrupted by a signal**"* — **调用被信号中断** |

> [!tip] 两个错误码的区别，正是 p29 那句"until … or …"的两端
> ```
> wait() 正常返回        → 有孩子终止了         → 返回正数（那个孩子的 PID）
> wait() 返回 -1 + ECHILD → 没有孩子可等         → 你不是任何进程的爹，或孩子都已被回收
> wait() 返回 -1 + EINTR   → 等的过程中被信号打断 → 没等到，需要重试
> ```
>
> `EINTR` 属于 Unix"健壮"风格下**必须处理的正常情况**（见 [[../Unix 总览/Unix 的特性|Unix 的特性]] 第六条）—— 信号随时可能来，所以 `wait` 的标准写法是一个循环：

```c
while ((pid = wait(&status)) == -1) {
        if (errno == EINTR) continue;   /* 被信号打断，重试 */
        perror("wait");
        return -1;
}
```

> 课件 p31 **没有给这个循环写法**，但 `EINTR` 的存在本身就要求调用方这样处理。

## 三、孤儿进程（p30）

这是本篇**最重要的一条工程规则**。

课件 p30 的原话：

> *"If a **parent process terminates first without waiting for its children**, the children processes become **orphan processes**."*
> （如果父进程**先终止、没有等待它的子进程**，这些子进程就成了**孤儿进程**。）

> *"It is **almost always poor programming practice** to create orphaned processes, because there may be **no indication**（of the failure）…"*
> （**几乎总是糟糕的编程实践**去制造孤儿进程，因为**可能没有任何迹象**表明出错了……）

### 为什么孤儿是坏消息

把这句话展开成三个具体后果：

| 后果 | 说明 |
|---|---|
| **退出码没人取** | 孩子怎么结束的，只有 `wait` 能取到。没人 `wait` ⇒ **退出状态丢失** |
| **失败无迹象** | 课件说的 *"no indication"* —— 孩子失败了，**父进程已经不在，没人报告** |
| **可能变成僵尸** | 内核还得留着那个进程的**退出状态表项**直到有人收走 |

> [!note] 僵尸进程（zombie / defunct process）
> 孩子已经死了，但它的**退出状态还留在内核的进程表里**，等父进程来 `wait` 取走。**这个残留的表项叫僵尸。**
>
> **僵尸不是"还活着的进程"** —— 它已经死了，只是**记录还没被领走**。
>
> 课件 L02 **没有出现 "zombie" 这个词**，也没有画这张图。上面这段是根据"退出状态存放 + 需 wait 取走"的机制补的，属于**背景补充，不是课件原文**。

### 孤儿会怎样（课件留白的部分）

> [!warning] 课件 p30 说到孤儿就停了，"后来怎么办"没讲
> 实际 Unix 的处理是：**孤儿进程会被"过继"（re-parent）给系统里某个进程，通常是 PID 1**。
>
> 于是 PID 1 会负责收走它们的退出状态。**这也是为什么 PID 1 必须存在、且不能随便退出。**
>
> **课件 L01–L03 没有讲 PID 1 和过继机制**，属于已知缺口。本篇不做进一步推测。

## 四、只有直接孩子才算（p32）

课件 p32 的 demo 标题里就点明了：

> *"Only one forked process is a **child of the original process**."*
> （只有一个被 fork 出来的进程是**原始进程的子进程**。）

**这句话解决的是一个具体困惑。** 课件 p32 的例子（结合 p27 的链式 fork）产生了这样一棵树：

```
原始进程
 ├── A      ← A 是原始进程的孩子
 │   └── B  ← B 是 A 的孩子
 │       └── C  ← C 是 B 的孩子
```

| 进程 | `wait()` 能等到它吗 |
|---|---|
| A | ✅ 能 —— 原始进程的**直接**孩子 |
| B | ❌ **不能** —— 它的爹是 A，原始进程不是它爹 |
| C | ❌ **不能** |

**只有一条规则**：`wait()` **只等待调用者自己的直接子进程**。孙子和曾孙不算。

> [!warning] 那 B 和 C 由谁收尸
> 规则是：**A 等 B，B 等 C**。这就把责任一层层传下去了。
>
> **如果 A 也不等 B 就退出**，那 B 就成了孤儿，被过继给别人。
>
> 这条链式的责任传递就是"**每个父进程都必须 wait 自己的孩子**"这条规则的由来 —— 见上面"孤儿是坏消息"那一节。

## 五、标准的 fork + wait 模式

把三篇笔记的机制合起来，就是 Unix Shell 执行一条命令的完整骨架：

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>

int main(void){
    pid_t pid = fork();

    if (pid == -1) {
            perror("fork");
            return 1;
    } else if (pid == 0) {
            /* 子进程：只做极少的事，然后 exec 换掉自己 */
            execlp("ls", "ls", "-l", (char *)NULL);
            perror("execlp");        /* exec 失败才会走到这 */
            _exit(1);                /* 注意用 _exit，不是 exit */
    } else {
            /* 父进程：等孩子 */
            int status;
            while (waitpid(pid, &status, 0) == -1) {
                    if (errno == EINTR) continue;
                    perror("waitpid");
                    return 1;
            }
            if (WIFEXITED(status))
                    printf("子进程正常退出，退出码 %d\n", WEXITSTATUS(status));
    }
    return 0;
}
```

**四个要点，每个都对应前面某一节：**

| 代码 | 对应 | 原因 |
|---|---|---|
| `fork()` 返回 `-1` 要判 | [[../进程管理/fork 创建进程\|fork]] | Unix 健壮风格 |
| `while (waitpid(...) == -1)` + `EINTR` | 本篇第二节 | 信号随时可能打断 |
| `execlp` 失败后用 **`_exit`** | [[进程终止]] | `exit` 会跑 atexit 处理器、冲刷 `fork` 前就打开的缓冲区 |
| 父进程一定 `wait` | 本篇第三节 | 否则造孤儿 |

> [!note] `_exit` vs `exit` 这个细节
> **课件 L02 提到了 `exit` 与 `_exit` 的区别**（见 [[进程终止]]），但**没有把"`fork` 之后子进程必须用 `_exit`"这个规则讲出来**。
>
> 原因：`fork` 复制了父进程的**所有内存**，包括 `stdio` 已经写入但**还没冲刷**的缓冲区。如果子进程调 `exit()`，它会把**父进程那份**缓冲内容**再冲刷一遍**，于是父进程的输出会**莫名其妙地出现两遍**。
> `fork` 之后子进程唯一的正确出口是 `_exit()`。

## 本课六个问题里的第 5 问

[[进程是什么]] 列的 *"When does a process stop? **Can we wait for a process to die?**"* —— **"能不能等"就是本篇**。

问题的另一半（*"When does a process stop?"*）见 [[进程终止]]。

## 一句话

> `wait()` **阻塞**父进程直到有孩子终止，返回**那个孩子的 PID**（正数），失败返回 **`-1`** 并设 `errno`（`ECHILD` = 没有孩子可等，`EINTR` = 被信号打断需重试）；**父进程不等就退出会造出孤儿进程，课件说这是"几乎总是糟糕的编程实践"**。

## 相关笔记

- **上一步**：[[../进程管理/fork 创建进程|fork 创建进程]] — 孩子是怎么来的
- **下一步**：[[exec 替换进程映像]] — `wait` 之后的流程（shell 版）；或 [[进程终止]] — 终止本身
- **等的是谁**：[[../进程与线程/进程是什么]] — 父子关系是创建关系
- **元信息**：[[进程标识与查看]]
- **完整示例**：[[../Unix 总览/Unix 组成结构|Unix 组成结构]] — shell 执行 `ls` = fork + exec + wait
- **健壮风格来源**：[[../Unix 总览/Unix 的特性]] — 为什么处处要查返回值
- **本讲总览**：[[../index|系统编程 MOC]]