---
tags:
  - 系统编程
  - Unix
  - 文件描述符
  - open
  - read
  - write
  - close
created: 2026-10-07
type: 知识点
aliases:
  - open read write close
  - open
  - read
  - write
  - close
  - O_RDONLY
  - O_WRONLY
  - O_RDWR
  - lseek
  - fsync
  - ioctl
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L03]
source: "[03-Unix-File-System.pdf](<../../raw/03-Unix-File-System.pdf>)"
---

# open read write close

> **一句话**：这四个系统调用构成一次完整的文件 I/O —— **`open` 拿到 fd**（描述符）、**`read`/`write` 按 fd 读写**、**`close` 释放**。它们是**系统调用层**，直接进内核、没有缓冲；上一层的 `FILE*` 是在它们之上包装出来的。

课件对应 L03 p37–p41。课件原文见 [03-Unix-File-System](<../../raw/03-Unix-File-System.pdf>)。

## 完整场景：程序读写一个文件的三步

**不预设你写过 C。** 先把整体流程说清楚：

```
1. open()   →  告诉内核"我要打开 notes.txt，只读"
              内核做 name resolution（找到 inode）、检查权限、
              在 SFT 里建一个条目、在你进程的 fd 表里占一个号
              ★ 返回那个号（fd）

2. read()   →  告诉内核"从 fd 读 100 字节到 buf"
              内核经 SFT → inode → 数据块，取出内容拷进 buf
              ★ 返回实际读了多少字节

3. close()  →  告诉内核"这个 fd 我不用了"
              内核释放 SFT 表项、释放 fd 号
              ★ 返回 0 表示成功
```

**为什么必须 `close`**：见本篇第五节。

## 一、open：拿到 fd（p38）

### 课件给的两个原型

```c
int open(const char *pathname, int flags)
int open(const char *pathname, int flags, mode_t mode)
```

**什么时候用哪个？**

| 原型 | 什么时候需要第三个参数 `mode` |
|---|---|
| `open(path, flags)` | **只是打开**已有文件 |
| `open(path, flags, mode)` | 要**创建**新文件（此时 `flags` 里必须含 `O_CREAT`），`mode` 给出权限位 |

### 参数逐个看（p38）

**① `pathname`**

> *"pathname: **absolute or relative path** to the file"*
> 绝对路径或相对路径。相对路径从 cwd 开始 —— 见 [[../文件系统结构/当前工作目录|当前工作目录]]。

**② `flags`（打开方式 + 修改方式）**

> *"flags: must include **one of the following access modes**: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, and **bitwise-or'd**（i.e. using the `|` operator）with **zero or more of the following modifiers**…"*
> （flags **必须包含下列访问方式之一**：`O_RDONLY`、`O_WRONLY`、`O_RDWR`；并可与**零个或多个**下列修改标志**按位或**（即用 `|` 运算符）组合……）

**这三者互斥，只能选一个：**

| 宏 | 含义 |
|---|---|
| **`O_RDONLY`** | **只读** |
| **`O_WRONLY`** | **只写** |
| **`O_RDWR`** | **读写** |

**课件明确说了组合方式是 `|`（按位或）。** 这正是"一切皆文件"的又一个体现：**你可以通过 `|` 把"打开方式"和"其他行为"一次说清**：

```c
open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644)
        │        │       │        │        │
        │        │       │        │        └─ mode：新建文件的权限位（八进制）
        │        │       │        └────────── O_TRUNC：已存在就清空
        │        │       └─────────────────── O_CREAT：不存在就创建
        │        └─────────────────────────── O_WRONLY：只写
        └──────────────────────────────────── 打开方式（必需，三选一）
```

> [!tip] `mode` 的 `0644` 是什么
> **`0644` 是八进制**（C 里以 `0` 开头表示八进制），表示权限位：
> ```
> 0644  =  rw-  r--  r--
>         所有者  同组  其他人
> ```
> 这正是 [[../文件系统结构/权限位与 ls -l|权限位与 ls -l]] 里那 9 个字符对应的位。
> —— **"新建文件的默认权限"就是用那 9 位指定的。**

**③ `mode`**

只在**创建**新文件时有意义，值就是那 9 位权限。

### open 的返回值

`int` 类型，所以失败返回 **`-1`**（见 [[../Unix 总览/Unix 的特性]] 第六条）。

```c
int fd = open("someFile", O_RDONLY);
if (fd == -1) {
        perror("open");
        /* 这里 errno 记着具体原因，比如 ENOENT（文件不存在）、EACCES（权限不够） */
}
```

> [!note] 课件 p38 没有列出所有 modifier
> 课件原文写的是 *"zero **or more** of the following modifiers"*，然后**列表在 PDF 里没有完整给出**。
> 上面例子里用的 `O_CREAT` / `O_TRUNC` 是 Unix 上最常用的两个，**属于背景补充**，不是课件列举的内容。

## 二、read：从 fd 读（p39）

### 课件给的原型

```c
bytes = read(fd, buffer, count)
```

### 三个参数（p39 原文）

> *"Read from file associated with `fd`; place `count` bytes into `buffer`"*

| 参数 | 课件说明 |
|---|---|
| **`fd`** | *"file descriptor to **read from**"* — 从哪个 fd 读 |
| **`buffer`** | *"**pointer to an array**"* — 指向一块数组的指针 |
| **`count`** | *"**number of bytes to read**"* — 要读几个字节 |

### 课件给的例子

```c
int fd = open("someFile", O_RDONLY);
char buffer[...];
/* ... */
```

> [!note] 课件 p39/p40 的例子在 PDF 里不完整
> 两页的代码都提取到 `char buffe...` / `char someFi...` 就断了。
> **本篇只使用课件明确写出的原型和参数说明**，不补写课件缺失的代码。

### 返回值：最容易写错的地方

> *"Returns **number of bytes read** or **–1 if an error occurred**."*
> （返回**读到的字节数**，出错返回 **–1**。）

> [!warning] `read` 的返回值有三种可能，不止两种
> | 返回值 | 含义 |
> |---|---|
> | **正数** | 实际读到的字节数 —— **可能小于 `count`！** |
> | **0** | **到达文件末尾**（end of file） |
> | **-1** | 出错 |
>
> **三个要点：**
>
> **① 读到文件尾时返回 0，不是 -1。** 混淆这两者是最常见的 bug。
> 用 0 当错误处理，会在文件末尾莫名打印"错误"。
>
> **② 返回值可能小于 `count`。** 对普通文件，一次 `read` 通常能读满；但**对终端、管道**这类字符设备，一次 `read` 会**有多少给多少**（你敲了几个字符就读几个），**它会阻塞直到有数据或读到 EOF**。
> 所以循环读文件的正确写法是：
> ```c
> ssize_t n;
> while ((n = read(fd, buf, sizeof buf)) > 0) {
>         /* 处理这 n 个字节 —— 必须用 n，不能用 sizeof buf */
> }
> if (n == -1) perror("read");
> ```
>
> **③ 字符设备的"阻塞"特性**来自 [[../文件系统结构/文件类型|文件类型]] 里讲的"字符设备按字节流传输、不可跳读"。
>
> **严格说 `read` 的返回类型是 `ssize_t` 而非 `int`** —— 这和 [[../进程管理/进程标识与查看|pid_t 可能是 int 也可能是 long]] 是同一类可移植性细节。**课件写的是 `bytes = read(...)`，未指明类型。**

## 三、write：往 fd 写（p40）

### 课件给的原型

```c
bytes = write(fd, buffer, count)
```

### 三个参数（p40 原文）

> *"Write contents of `buffer` to the file associated with `fd`; write `count` bytes into the file"*

| 参数 | 说明 |
|---|---|
| **`fd`** | *"file descriptor to **write to**"* |
| **`buffer`** | 指向要写出的数组 |
| **`count`** | 写几个字节 |

### 返回值

> *"Returns **number of bytes written** or **–1 if an error occurred**."*

**和 `read` 同构**，但有一个实际差别：

> [!warning] `write` 也可能少于 `count`
> 同样的道理：**返回的是"实际写了多少"，不是"你要求写多少"**。
>
> 典型场景：**磁盘满**。你要求写 1000 字节，实际只写了 300 就失败 —— 这时返回值是 **300**，而**磁盘满这个错误要靠 `errno` 报告**（返回值不是 -1）。
>
> 所以**严格检查 `write` 要同时看返回值和 `errno`**，这比 `read` 更容易被忽略。

## 四、close：释放 fd（p41）

### 课件给的原型

```c
return_val = close(fd)
```

> *"**Closes an open file descriptor.** Returns **0** on success, **-1** on error."*
> （**关闭一个已打开的文件描述符。** 成功返回 **0**，出错返回 **-1**。）

**这是四个调用里最简单的。** 注意 **成功返回 0**（不是 1、不是字节数）。

## 五、为什么必须 close

课件 p41 只说了 close 做什么，**没有讲"不 close 会怎样"**。但这是实践中最重要的一条规则。

> [!warning] fd 是"进程 fd 表里的一个号"，而这个号是**有限的**
> [[../文件描述符与流/文件描述符与 SFT|文件描述符与 SFT]] 说 fd 是"**最低可用号**"。
>
> 意思是：**关掉一个 fd 之后，那个号会被下一个 `open` 重新使用。**
> 所以：
>
> | 做法 | 后果 |
> |---|---|
> | 不 close，循环里反复 open | **fd 号很快耗尽**，`open` 开始返回 -1（`EMFILE`） |
> | 忘了 close 就 `fork` | **子进程会继承这些 fd** —— 管道的一端可能永远不关闭，父进程一直等 EOF，见 [[../重定向与管道/管道与进程间通信\|管道与进程间通信]] |
> | 不 close 就 `exec` | 同上，被 exec 替换掉的进程带走了 fd |
>
> **规则：谁 open，谁 close。** 而且要**紧挨着**（中间不要有 return/break/goto 跳过它）。
>
> > ⚠️ **这个后果课件 L03 没有讲** —— p41 只有一句"关闭一个已打开的 fd"。
> > 上面这段是根据"fd 是有限的下标"这一模型推出来的，**背景补充**。

**实际代码里的常见做法**：把 fd 存起来，出错路径也要关：

```c
int fd = open("f", O_RDONLY);
if (fd == -1) { perror("open"); return -1; }

char buf[4096];
ssize_t n = read(fd, buf, sizeof buf);   /* 这行如果出错 */

close(fd);                                /* 无论 read 成功与否都要走到这里 */
if (n == -1) { perror("read"); return -1; }
/* … 用 buf … */
```

## 六、四个调用的对照速查

| 调用 | 做什么 | 成功返回 | 失败 |
|---|---|---|---|
| **`open`** | 拿到 fd | **非负的 fd**（0/1/2 已被占用，所以通常 ≥ 3） | **`-1`** |
| **`read`** | 从 fd 读 | **读到的字节数**（**可能小于请求**，**0 表示到文件尾**） | **`-1`** |
| **`write`** | 往 fd 写 | **写出的字节数**（**可能小于请求**） | **`-1`** |
| **`close`** | 释放 fd | **`0`** | **`-1`** |

**三个 fd 相关的对照要点：**

| | |
|---|---|
| **只有 open 返回 fd** | 所以 fd 的唯一来源是 `open`（以及预置的 0/1/2） |
| **read/write 靠 fd 定位文件** | 它们不知道文件名，只知道整数 |
| **close 之后 fd 号可被复用** | 所以必须及时关，见第五节 |

### 课件 p35 还列了三个相关调用

> *"The Unix file system calls use file descriptors（via **`open`, `read`, `write`, `close`, `fsync`, `lseek`, and `ioctl`**）."*

| 调用 | 课件是否展开 | 用途（按命名与通行语义） |
|---|---|---|
| **`lseek`** | ❌ 未展开 | **改变读写偏移** —— 在文件里跳着读写 |
| **`fsync`** | ❌ 未展开 | 把**缓冲区内容强制刷到磁盘** |
| **`ioctl`** | ❌ 未展开 | **设备专用控制** —— 查终端大小、设置网卡参数 |

> ⚠️ **`ioctl` 是"一切皆文件"的边界所在**：读磁盘文件用 `read` 就够了，但**控制设备需要 `ioctl`**（因为设备的控制命令千差万别，没法统一）。
> **课件 L03 只列了名字，没有给原型和例子** —— 属于已知缺口。

## 一句话

> **`open` 拿到 fd**（flags 用 `|` 组合 `O_RDONLY`/`O_WRONLY`/`O_RDWR` 与修改标志，创建时再加 `mode` 权限位）、**`read`/`write` 按 fd 读写并返回实际字节数**（**可能小于请求；`read` 返回 0 表示到文件尾，不是错误**）、**`close` 返回 0**；失败一律 **`-1`**，且 **fd 号有限、必须及时 close**。

## 相关笔记

- **上一步**：[[../文件描述符与流/文件描述符与 SFT|文件描述符与 SFT]] — fd 是什么、fd 表和 SFT 两层
- **C 库那一层**：[[../文件描述符与流/FILE 流与格式化输入输出|FILE 流与格式化输入输出]] — `FILE*` 是在这四个之上包装的
- **重定向改的就是 fd 表项**：[[../重定向与管道/I O 重定向与 dup|I/O 重定向与 dup]]
- **管道的两端也是 fd**：[[../重定向与管道/管道与进程间通信|管道与进程间通信]]
- **名字怎么变成 inode**：[[../inode 与链接/名称解析与文件大小上限|名称解析与文件大小上限]] — `open` 的第一步
- **权限检查在哪一步**：[[../文件系统结构/权限位与 ls -l|权限位与 ls -l]] — `open` 会检查权限，`mode` 就是权限
- **健壮风格**：[[../Unix 总览/Unix 的特性]] 第六条（失败返回 -1）
- **本讲总览**：[[../index|系统编程 MOC]]