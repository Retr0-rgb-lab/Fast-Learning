---
tags:
  - 系统编程
  - Unix
  - 进程管理
  - exec
  - 系统调用
created: 2026-10-07
type: 知识点
aliases:
  - exec 替换进程映像
  - exec
  - execvp
  - execlp
  - 六个 exec 变体
  - 进程替换
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L02]
source: "[02-Unix-Processes.pdf](<../../raw/02-Unix-Processes.pdf>)"
---

# exec 替换进程映像

> **一句话**：`fork` 只能造出"**跑同样代码**"的进程，`exec` 才能把进程**整个换成另一个程序**。所以 Unix 启动一个新程序的固定套路是 **`fork` 然后在子进程里 `exec`**。**最反直觉的一点：`exec` 成功就不返回了** —— 它把当前进程替换掉，没有"之后"的代码。

课件对应 L02 p33–p39。课件原文见 [02-Unix-Processes](<../../raw/02-Unix-Processes.pdf>)。

## 完整场景：fork 做不到的事

回到 [[../进程管理/fork 创建进程|fork]] 的限制：**fork 出来的子进程，跑的是和父进程完全一样的代码。**

**问题来了**：我在 shell 里敲 `ls`，我写的那个 shell 程序**从来不会包含 `ls` 的代码**。它怎么把 `ls` 跑起来？

**答案就是 `exec`。**

```
shell 想执行 ls
   │
   ├─ fork()      →  子进程（跑的仍然是 shell 的代码）
   │
   └─ 子进程里 exec("ls")
          ↓
      子进程的整个映像被换成 ls
          ↓
      从此它就是 ls 了 —— 不是"shell 变成了 ls"，是"这个进程槽位上的东西被换掉了"
```

> [!warning] 一句话记住 exec 的性质
> **`exec` 不是"调用一个函数然后回来"，而是"把调用者变成别的东西"。**
> 一旦成功，**原代码的后续行永远不会执行**。
>
> 理解这一点，p39 的 `exec has no return` 就自然懂了。

## 一、exec 做什么（p33）

课件 p33 的原话：

> *"The `fork` system call creates a **copy of the calling process**. However, **many applications require the child process to execute code different from the parent's**. The `exec` family of system calls provides a facility for **overlaying the calling process with a new executable module**."*
> （`fork` 系统调用创建调用者进程的**副本**。然而**很多应用需要子进程执行与父进程不同的代码**。`exec` 系列系统调用提供了一个**用新的可执行模块覆盖调用者进程**的功能。）

课件接着（p33 末尾）：

> *"`exec` **loads a new executable and arguments**…"*
> （`exec` **载入一个新的可执行文件及其参数**……）

**关键动词是 overlay（覆盖）**，不是"创建"。**没有任何新进程被创建** —— 进程的数量不变，只是**那个进程的"内容"被换掉了**。

> [!tip] 换个说法：进程 = 一个容器槽位
> `fork` = **再做一个一样的槽位**
> `exec` = **把槽位里的东西倒掉，换成别的**
>
> 所以 `fork` + `exec` 合起来的效果才是"启动一个新程序"，而单独的 `exec` 只是"变身"。

## 二、六个变体（p36–p38）

课件用三页讲六个变体（每页两个）。**这六个函数其实是两组独立变化的维度**：

| 维度 | 取值 | 含义 |
|---|---|---|
| **参数怎么传** | `l` 或 `v` | `l` = **l**ist（逐个列出参数）；`v` = **v**ector（传数组） |
| **路径怎么定** | 有无 `p` | 有 `p` = 从 **PATH** 环境变量里找 |
| **要不要传环境** | 有无 `e` | 有 `e` = **e**nviron，可以自定义整个环境变量表 |

### 六个原型（p36–p38 原文）

$$
\begin{aligned}
&\texttt{int execl(const char *path, const char *arg0, \dots);}\\
&\texttt{int execlp(const char *file, const char *arg0, \dots);}\\
&\texttt{int execle(const char *path, const char *arg0, \dots, char * const envp[]);}\\
&\texttt{int execv(const char *path, char * const argv[]);}\\
&\texttt{int execvp(const char *file, char * const argv[]);}\\
&\texttt{int execve(const char *path, char * const argv[], char * const envp[]);}
\end{aligned}
$$

### 对照表

| 函数 | 路径 | 参数 | 环境 | 用起来 |
|---|---|---|---|---|
| `execl` | **给全路径** | 逐个列 | 用当前环境 | 知道确切路径时 |
| `execlp` | 从 **PATH** 找 | 逐个列 | 用当前环境 | **最常用**（敲 `ls` 就行） |
| `execle` | 给全路径 | 逐个列 | **自定义** | 极少用 |
| `execv` | 给全路径 | 传数组 | 用当前环境 | 参数是动态拼出来的 |
| `execvp` | 从 **PATH** 找 | 传数组 | 用当前环境 | **最常用**（参数动态时） |
| `execve` | 给全路径 | 传数组 | **自定义** | 最底层，其他都是它的包装 |

> [!tip] 选哪个的决策树
> ```
> 需要自定义环境变量吗？
>   是 → 给全路径？ 是→execle  否→execve
>   否 ↓
> 从 PATH 找还是给全路径？
>   给全路径 → 参数是逐个列还是数组？ 逐个→execl  数组→execv
>   从 PATH 找 → 逐个→execlp  数组→execvp   ← 绝大多数情况是这两个
> ```

> [!warning] `arg0` 和 `argv[0]` 不是同一个东西
> 看原型：`execl(path, arg0, ...)` 里，**`path` 是"去哪里找文件"，`arg0` 是"把程序名报成什么"**。
>
> 惯例是 **`arg0` = 你在命令行上敲的名字**。所以你敲 `ls`，`arg0` 就是 `"ls"`；你敲 `/bin/ls`，`arg0` 就应该是 `"/bin/ls"`。
>
> **这会影响程序里 `argv[0]` 的值，进而影响它的报错信息长什么样。**

## 三、标准例子：跑 `ls -l`（p34、p35）

课件 p34/p35 的 demo 是**完整的 fork + exec**：

```c
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
    int status;
    pid_t childpid;

    if ((childpid = fork()) == -1){
            perror("Error in the fork");
            exit(1);
    } else if (childpid == 0){
            /* child code */
            if (execvp("ls", argv) < 0){
                    perror("Exec of ls failed");
                    exit(1);
            }
    } else {
            /* parent code */
            if (childpid != wait(&status)) {
                    /* 错误处理 */
            }
    }
}
```

### 三个分支各自在做什么

| 分支 | 判据 | 角色 | 做的事 |
|---|---|---|---|
| `== -1` | **失败** | — | `perror` 报错，退出 |
| `== 0` | **子进程** | 干活 | `execvp("ls", argv)` |
| `else` | **父进程** | 收尸 | `wait(&status)` |

**子进程那一支只做两件事**：exec，失败才报错。**没有别的。** 这就是上一节说的"fork 之后子进程要尽快 exec"。

> [!note] `argv` 从哪来
> 课件代码里 `execvp("ls", argv)` 的 `argv` 就是 **`main` 的第二个参数**，也就是**用户在命令行上敲的原始参数**。
>
> 也就是说：**shell 把自己收到的 `argv` 原样交给了 exec**。你敲 `ls -l`，`argv` 就是 `["./shell名字", "ls", "-l"]`，取从下标 1 开始的 `[1:]` 传给 `ls`。

## 四、exec 没有返回（p39）

课件 p39 的标题就是答案：**`exec has no return`**。

### 课件的 demo

```c
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
    printf("Old image: pid=%d\n", getpid());
    execlp("./newimage", "newimage", NULL);
    printf("Old image: hello\n");     /* 这行永远不执行 */
    return 0;
}
```

课件配套了两个文件：`oldimage.c`（上面这段）和 `newimage.c`（被 exec 载入的新程序）。

**输出只有：**

```
Old image: pid=12345
```

**第二句 `Old image: hello` 永远不会出现。**

### 为什么

```
execlp(...) 这行执行
      │
      ├─ 失败（找不到 ./newimage、没权限、格式不对…）
      │      → 返回 -1，设置 errno → 继续往下走，打印 "Old image: hello"
      │
      └─ 成功
             → 载入 newimage 的代码，替换整个进程映像
             → ★ 原来的代码（包括下面那行 printf）已经不存在了 ★
             → 从来不会"回来"
```

> [!tip] 这带来一条编码规则
> **`exec` 后面紧跟的那几行，只可能处理"失败"。**
>
> 所以标准的写法是：
> ```c
> execlp("./newimage", "newimage", NULL);
> /* 只有 exec 失败才会走到这里 */
> perror("execlp");
> exit(1);
> ```
>
> **凡是 exec 之后的代码，都要假定"我是失败的那条路"。**

## 五、fork + exec 为什么要配对用

把两篇笔记的机制合起来看，就明白了这个固定套路的必然性：

| 你想做的事 | 单靠 fork | 单靠 exec |
|---|---|---|
| **启动一个新程序** | ❌ 造出来的还是自己 | ❌ 把**自己**变成新程序，自己就没了 |

所以必须两步：

```
① fork()          → 造出一个"替身"（真正的自己留下来继续当 shell）
② 子进程 exec()    → 把替身换成目标程序
```

**这就是为什么 Unix 没有一个 `spawn("ls", args)` 这样的"一条龙"系统调用。**

> [!note] 其他系统确实有
> POSIX 后来补了 **`posix_spawn()`** —— 它把 fork+exec 封装成一个调用，内部该 fork 还是 fork。
>
> **课件 L02 没有提到 `posix_spawn`**，只讲了 fork+exec 这个两步套路。属于已知缺口。

## 六、一个典型的反面例子

看完上面的机制，可以推出 Unix 编程里一条著名的不成文规则：

> **`fork` 之后、子进程 `exec` 之前，除了必要的清理和 `close`，几乎什么都不该做。**

**为什么？** 因为从 fork 到 exec 之间，子进程**跑的仍然是父进程的代码**。父进程在 fork 之前做过的每一件事，子进程都会**再来一遍**。

| 父进程 fork 前做过 | 子进程会 |
|---|---|
| 分配并填充了一块内存 | 那块内存**也有一份副本**（浪费） |
| 打开了几个文件描述符 | **这些 fd 也被复制了**（泄漏） |
| 改了全局数据结构 | **又改一次**（可能触发不一致） |
| 已经在缓冲区里攒了输出没冲刷 | `exit` 时会**再冲刷一遍** → 输出重复 |

**每一行"多余的代码"在 fork 之后都是双倍代价。**

> 这条规则的完整推导（尤其"为什么子进程退出要用 `_exit`"）见 [[../进程管理/wait 等待子进程|wait 等待子进程]] 第五节的完整示例，那里逐行标了每处的原因。

## 本课六个问题里的第 4 问

[[进程是什么]] 列的 *"How is a process created? **In how many ways?**"* ——

**"怎么创建"** 由 `fork` + `exec` 完成（本篇 + [[../进程管理/fork 创建进程|fork]]）。
**"有几种方式"** 课件 L02 **没有展开**（其他机制如 `vfork`、`posix_spawn` 未讲）。

## 一句话

> `fork` 只能造出"跑同样代码"的副本，`exec` 把进程**整个覆盖**成新程序；两者配对才是 Unix 启动程序的固定套路。**六个变体是"路径怎么定 × 参数怎么传 × 环境要不要换"三组选择**；**`exec` 成功则不返回**，后面的代码只处理失败。

## 相关笔记

- **上一步**：[[../进程管理/fork 创建进程|fork 创建进程]] — 没有它就没地方 exec
- **下一步**：[[wait 等待子进程|wait 等待子进程]] — 父进程这一支；或 [[进程终止]]
- **为什么子进程要尽快 exec**：[[../进程管理/wait 等待子进程]] 第五节 — `_exit` vs `exit`
- **映像被换掉之后是什么**：[[../进程与线程/进程映像与线程|进程映像与线程]]
- **完整的一条命令执行**：[[../Unix 总览/Unix 组成结构|Unix 组成结构]]
- **PATH 环境变量是什么**：[[../文件系统结构/文件类型|文件类型]]（环境变量属于进程的公共数据）
- **本讲总览**：[[../index|系统编程 MOC]]