---
tags:
  - 系统编程
  - Unix
  - 进程管理
  - fork
  - 系统调用
created: 2026-10-07
type: 知识点
aliases:
  - fork 创建进程
  - fork
  - 创建进程
  - 父子进程
  - 进程创建
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L02]
source: "[02-Unix-Processes.pdf](<../../raw/02-Unix-Processes.pdf>)"
---

# fork 创建进程

> **一句话**：`fork()` **复制**当前进程，**一次调用返回两次** —— 父进程拿到子进程的 PID，子进程拿到 **0**。所以**你没法用返回值区分"我是爹还是儿子"，只能用 PID 是不是 0 来判断**。这是 Unix 编程里最反直觉、也最容易写错的一个系统调用。

课件对应 L02 p21–p28。课件原文见 [02-Unix-Processes](<../../raw/02-Unix-Processes.pdf>)。

## 完整场景：一次 fork 之后发生了什么

**先把"复制"这个词拆开。** 很多人以为 `fork` 之后就是"多了一个程序在跑"，实际上**两个进程执行的代码完全一样**，只是从不同的地方继续。

假设你写：

```c
printf("A\n");
int r = fork();
printf("B\n");
```

**实际输出是：**

```
A
B     ← 父进程
B     ← 子进程
```

**为什么？** `fork()` 的**下一行**开始，两个进程**各自**往下走。父进程走到 `printf("B")` 打印一次，子进程也走到 `printf("B")` 再打印一次。

> [!warning] 这里有个实际后果
> `fork` 之后的代码，**子进程会重跑一遍**。所以 `fork` 之前创建的临时变量、`已经打开的文件`、`已经分配并填充的内存`，在子进程里**都有一份副本**。
>
> 这就是为什么 `fork` 之后子进程只应该做很少的事，然后尽快 `exec` 换掉自己 —— 见 [[exec 替换进程映像]]。

## 一、fork 做了什么（p21）

课件 p21 的原话：

> *"To create a new process, typically a parent process calls the **`fork()`** system call, which **traps into the kernel** and:"*
> （要创建一个新进程，通常是父进程调用 **`fork()`** 系统调用，它**陷入内核**并且：）

**"traps into the kernel"** —— 见 [[../Unix 总览/Unix 组成结构|Unix 组成结构]]，这就是系统调用那一步的特权级切换。

课件接着列出内核做的事（原文三条）：

| # | 内核做的事 | 说明 |
|---|---|---|
| 1 | *"**Allocates a new chunk of memory** and kernel data structure."* | 分配新的内存块和内核数据结构 |
| 2 | *"**Copies the parent process's image** and kernel data structure into the new process's, with **needed modifications**（e.g. **PID, PPID**）."* | 把父进程的**映像**和内核数据结构**复制**一份，做必要修改 |
| 3 | *"Adds the ..."* | 原文在此处截断 |

第 2 步是本讲的核心：**复制**。复制完之后要改的有两个字段：

- **PID** → 换成新分配的号码
- **PPID** → 指向**父进程**

这两个字段见 [[进程标识与查看]]。

### 第 3 步补全

> [!note] 课件 p21 的第三条原文不完整
> 提取出的文本是 *"Adds the ..."*，句子被截断（PDF 排版所致）。
> 按 `fork` 的通用语义，这一步是把**子进程加入系统的进程表/调度队列**，让它可以被调度。
> **本篇不把推测写成课件内容**，仅在此标注。

## 二、返回值：一次调用，两个身份（p22–p25）

课件 p22–p25 的 demo 是同一个程序连讲四页。**核心是这段：**

```c
/* forkdemo.c */
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

void main(void){
    int ret_from_fork, mypid;

    mypid = getpid();
    printf("Before: my pid is %d\n", mypid);

    ret_from_fork = fork();
    sleep(1);
    printf("After: my pid is %d, fork() said %d\n", mypid, ret_from_fork);
    // ...
}
```

### 逐行理解返回值

**`ret_from_fork = fork();` 这一行之后，两个进程的 `ret_from_fork` 不一样：**

| 我是谁 | `getpid()`（`mypid`） | `fork()` 的返回值（`ret_from_fork`） |
|---|---|---|
| **父进程**（原来的进程） | 原来那个 PID | **子进程的 PID**（一个正整数） |
| **子进程**（新来的） | 新的 PID | **0** |

> [!tip] 这就是那个经典判断的由来
> ```c
> if (ret_from_fork == 0) {
>         /* 我是子进程 */
> } else {
>         /* 我是父进程，ret_from_fork 就是孩子的 PID */
> }
> ```
> **判据是"返回值是不是 0"，而不是"我是谁"。** 因为从代码上"我是谁"是无法直接问的 —— 两个进程跑的是同一份代码、同一份内存。

### 为什么 `sleep(1)` 在中间

课件在 `fork()` 和 `printf` 之间插了 `sleep(1)`。**这不是随便加的**：

> [!warning] 不加 sleep 会怎样
> 父进程和子进程是**两个独立的执行流**，它们**各自跑各自的，谁先谁后不确定**（受调度影响）。
>
> 不加 `sleep`，可能子进程先打印、父进程后打印；也可能反过来。**输出顺序不可预测。**
>
> `sleep(1)` 让父进程"先歇一会儿"，给子进程一个先跑完的机会，于是**输出顺序变得稳定**，方便课堂演示。
>
> **这是并发编程里最本质的一件事：先后顺序不由代码书写顺序决定。** 同样的道理在 [[../进程管理/wait 等待子进程|wait]] 那一讲会更明显。

## 三、标准写法：if 分支（p26）

课件 p26 给的是**更规范的版本**，用 `if` 而不是 `else`：

```c
/* forkdemo.c */
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

void main(void){
    int ret_from_fork;

    printf("Before: my pid is %d\n", getpid());

    if ((ret_from_fork = fork()) == 0){
            fprintf(stderr, "I am the child, ID = %ld\n", (long)getpid());
            // ... 子进程继续
    } else {
            fprintf(stderr, "I am the parent, ID = %ld\n", (long)getpid());
            // ... 父进程继续
    }
}
```

**为什么用 `if` 而不是 `if/else`？** 因为**失败的情况还没处理**：

> [!tip] 健壮性要求你检查失败
> 回顾 [[../Unix 总览/Unix 的特性]] 第六条"健壮"：**`int` 返回值失败时是负值**（通常是 `-1`）。
>
> 所以完整判断应该是三个分支：
> ```c
> pid_t pid = fork();
> if (pid == -1)      { perror("fork"); exit(1); }  /* 失败 */
> else if (pid == 0)  { /* 子进程 */ }
> else                { /* 父进程，pid 是孩子的 PID */ }
> ```
>
> 课件 p26/p27/p28 的课堂 demo **为了讲清楚主线没有写失败分支**。这是课件示例的简化，**实际代码必须补上**。

## 四、两种典型形态：链与扇（p27、p28）

课件给的两个练习，本质是**同一行代码的两种写法**。

### 链式：p27

```c
void main(void){
    int i, n = 4;
    pid_t childpid;

    for (i = 1; i < n; ++i)
            if (childpid = fork())
                    break;          /* parent breaks out; child continues */
    fprintf(stdout, "This is process ...", ...);
}
```

**关键那句 `if (childpid = fork()) break;` 的行为：**

| 进程 | `fork()` 返回 | `if (返回值)` | 动作 |
|---|---|---|---|
| 父进程（第一个） | 子进程 PID（**非 0**） | **真** | **`break`** — 跳出循环 |
| 子进程 | **0** | **假** | 不 break，**继续循环** → 再 fork |

**结果：一根链。**

```
原始进程
 ├── fork() → 进程 A   （A 又 fork → 进程 B）
 └── 进程 B             （B 又 fork → 进程 C）
```

总共 4 个进程（`n = 4`，循环 3 次）。

### 扇形：p28

```c
void main(void){
    int i, n = 4;
    pid_t childpid;

    for (i = 1; i < n; ++i)
            if ((childpid = fork()) <= 0)
                    break;          /* child and error break out; parent continues */
    fprintf(stdout, "This is process ...", ...);
}
```

**注意判断条件从 `if (childpid = fork())` 变成了 `if ((childpid = fork()) <= 0)`。**

| 进程 | `fork()` 返回 | `<= 0` | 动作 |
|---|---|---|---|
| **父进程** | 子进程 PID（**正数**） | **假** | 不 break，**继续循环** → 再 fork |
| **子进程** | **0** | **真** | **`break`** — 跳出循环 |

**结果：一把扇子。** 原始进程连续 fork 出 3 个子进程，它们都不再 fork。

```
原始进程
 ├── 子进程 1
 ├── 子进程 2
 └── 子进程 3
```

### 两者的对照（这是本页最值得记的）

| | 链式 p27 | 扇形 p28 |
|---|---|---|
| 判断 | `if (childpid = fork())` | `if ((childpid = fork()) <= 0)` |
| 谁 break | **父进程** | **子进程** |
| 形状 | 一根**链**（每个子进程继续生） | 一把**扇**（只有原点继续生） |
| 进程总数 | $n$ | $n$ |
| 常用场景 | 构建**流水线/管道链** | **并行处理一批任务** |

> [!tip] 一句话记住差别
> **看 `fork()` 的返回值落在判断的哪一侧**：非 0（父）break 就是链；`<= 0`（子）break 就是扇。
>
> 这两行代码长得极像，**含义完全相反** —— 是这一讲最容易看错的地方。

> [!warning] 两段代码都有的隐患
> 课件这两段用的是 `void main(void)`，且**都没有检查 `fork()` 失败**。
> 循环里 `fork` 失败（比如进程数超上限）时：
> - 链式：父进程会**把失败当成功**，因为 `-1` 也是非 0 → `break`
> - 扇形：子进程会**把失败当子进程**，因为 `-1` 也 `<= 0` → `break`
>
> **实际代码必须先判 `-1`，再判 `0`。** 课件为了突出"链 vs 扇"这个主线没有写。

## 五、fork 之后的常见模式

**课件 p34/p35 展示了最标准的组合**（那部分见 [[exec 替换进程映像]]）：

```
fork()
  │
  ├─ 子进程：只做极少的事 → exec(新程序) → 彻底变成另一个程序
  │                          ↑
  │                     为什么要 exec？因为 fork 出来的子进程
  │                     只能"跑一样的代码"，没法变成别的程序
  │
  └─ 父进程：wait() 收尸 → 继续自己的事
```

**这就是 Unix Shell 执行一条命令的全部过程**：

1. Shell（父进程）`fork()`
2. 子进程 `exec()` 换成 `ls` 的映像
3. 父进程 `wait()` 等它跑完

三步分别对应本目录的三篇笔记：

| Shell 的动作 | 笔记 |
|---|---|
| `fork()` | **本篇** |
| `exec()` | [[exec 替换进程映像]] |
| `wait()` | [[wait 等待子进程]] |

> [!tip] 为什么子进程必须尽快 exec
> 回顾本篇开头那个"A/B"输出例子：`fork` 之后子进程会**把后面的代码重跑一遍**。
>
> 如果子进程不 exec 就继续跑父进程的逻辑，它会**重复执行父进程已经做过的事**—— 比如再 fork 一次、再写一次文件。
>
> **所以 fork 的标准用法是"子进程只做必要的清理，然后立刻 exec"。**

## 六、本课六个问题里的第 3、4 问

[[进程是什么]] 列的课件问题中：

- **"When is a process created? By whom?"** → **本篇第一、二节**：由**父进程**通过 `fork()` 创建
- **"How is a process created? In how many ways?"** → 课件 L02 只讲了 **`fork()` 这一种**。括号里那半问"有几种方式"**课件没有展开**（其他 Unix 创建机制如 `vfork`、`posix_spawn` 未讲）

## 一句话

> `fork()` **复制**父进程，一次调用**返回两次**：父进程拿到孩子 PID（正数）、子进程拿到 **0**；**判断身份靠返回值是否为 0**，链式和扇形两段代码的差别**全在这句 `if` 怎么写**。

## 相关笔记

- **上一步**：[[进程标识与查看]] — 新进程的 PID / PPID 是谁填的
- **下一步**：[[exec 替换进程映像]] — fork 只能"跑一样的代码"，要变成别的程序必须 exec
- **再下一步**：[[wait 等待子进程]] — 父进程怎么知道孩子干完了
- **fork 的底层机制**：[[../进程与线程/进程映像与线程]] — Linux 上是 copy-on-write
- **一个专门的例子**：[[../Unix 总览/Unix 组成结构|Unix 组成结构]] — shell 执行 `ls` 走的就是 fork→exec→wait
- **本讲总览**：[[../index|系统编程 MOC]]