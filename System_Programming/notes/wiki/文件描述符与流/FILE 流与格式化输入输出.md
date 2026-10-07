---
tags:
  - 系统编程
  - Unix
  - FILE 流
  - 标准输入输出
  - printf
  - scanf
  - fopen
created: 2026-10-07
type: 知识点
aliases:
  - FILE 流与格式化输入输出
  - FILE
  - 文件指针
  - file pointer
  - fopen
  - fclose
  - printf
  - scanf
  - fprintf
  - sprintf
  - 格式化输入输出
domain: [操作系统, 系统编程]
course: COMP3438 System Programming
lecture: [L03]
source: "[03-Unix-File-System.pdf](<../../raw/03-Unix-File-System.pdf>)"
---

# FILE 流与格式化输入输出

> **一句话**：`FILE*` 是 **C 标准库**提供的上层抽象 —— **`FILE` 结构里同时装着一个缓冲区和一个 fd**，所以它被称为"**句柄的句柄**"。`fopen`/`fclose` 管这个结构，`printf`/`scanf` 在上面做**格式化**。这一层比裸的 `open`/`read`/`write` 好用，代价是多了一层缓冲。

课件对应 L03 p42–p53。课件原文见 [03-Unix-File-System](<../../raw/03-Unix-File-System.pdf>)。

## 完整场景：为什么要两层

**先把两层摆在一起**，这是本篇的骨架：

```
┌────────────────────────────────────────────────┐
│ 你的代码                                        │
│   printf("sum=%d\n", a+b)                      │
│   scanf("%d", &x)                              │
│   fopen("f.txt", "r")                          │
└──────────────────┬─────────────────────────────┘
                   │  C 标准库（stdio.h）—— 用户态、带缓冲、有格式化
┌──────────────────▼─────────────────────────────┐
│ FILE 结构                                      │
│   ┌─────────────┐  ┌──────────┐                │
│   │ buffer 缓冲 │  │ fd 文件描述符│               │
│   └─────────────┘  └────┬─────┘                │
└─────────────────────────┼──────────────────────┘
                          │  系统调用（unistd.h / fcntl.h）—— 内核态、无缓冲
┌─────────────────────────▼──────────────────────┐
│ open / read / write / close                    │
└────────────────────────────────────────────────┘
```

**一句话记住差别**：`open`/`read`/`write` 是**系统调用**（无缓冲、给行家）；`fopen`/`printf` 是**C 库**（有缓冲、给日常用）。

## 一、FILE 结构：句柄的句柄（p42、p43）

课件 p42 的定义非常精确：

> *"A **file pointer** points to a **data structure FILE**, called a **file structure** in the **user area of the process**. A file structure contains a **buffer and a file descriptor**（so a file pointer is a **handle to a handle**）."*
> （**文件指针**指向一个叫 **`FILE`** 的数据结构，称为进程**用户区里的文件结构**。文件结构里包含**一个缓冲区和一个文件描述符**（所以文件指针是**句柄的句柄**）。）

### 三个关键点

| 课件用词 | 含义 |
|---|---|
| **in the user area of the process** | `FILE` 结构在**进程的用户态内存里**，不是内核 |
| **contains a buffer and a file descriptor** | 它**同时**有缓冲区和 fd |
| **handle to a handle** | fd 是"句柄"，`FILE*` 指向装着这个句柄的结构，所以是**句柄的句柄** |

> [!tip] "句柄的句柄"这个比喻值得展开
> 类比：
> - **fd** = 门牌号（如 `3`），本身没有能力，只是编号
> - **`FILE*`** = 一张写着"3 号门 + 收件缓冲区"的**卡片**
>
> 你交给 `fprintf` 的是那张卡片；`fprintf` 内部拿出卡上的 `3`，再去调 `write`。
>
> **所以 `FILE*` 能提供的额外能力，全来自那个"buffer"。**

### FILE 结构怎么连到内核（p43）

课件 p43 的图给出一条链路：

```
用户区                              内核区
┌──────────────┐              ┌──────────────────┐
│    FILE      │── fd ────▶  │ 进程 fd 表        │
│ (buffer+fd)  │              │      ↓           │
└──────────────┘              │ 系统文件表 SFT    │
                              │      ↓           │
                              │     inode        │
                              └──────────────────┘
```

**课件 p42/p43 这两张图要和 [[../文件描述符与流/文件描述符与 SFT|文件描述符与 SFT]] 那一篇的第一节对照读** —— 那篇是内核视角，这一篇是用户视角，**它们描述的是同一条链路的两端**。

## 二、C 库里的高层函数（p44）

课件 p44 列出用 `FILE` 数据类型的高层 I/O 函数：

| 函数 | 用途 |
|---|---|
| **`fopen()`** | 打开文件，拿到 `FILE*` |
| **`printf()`** | 格式化**输出到 stdout** |
| **`scanf()`** | 格式化**从 stdin 读入** |
| **`fflush()`** | 冲刷缓冲区 |
| **`feof()`** | 问"是否已到文件尾" |
| **`fclose()`** | 关闭 |

**注意 `printf` / `scanf` 也在这个列表里** —— 它们操作的**就是** `FILE*`（默认是 stdout / stdin）。**所以"打印到屏幕"和"打印到文件"是同一套代码**，只是 `FILE*` 不同：

```c
printf("...");                  /* → stdout（fd 1）*/
fprintf(f, "...", ...);         /* → f 指向的文件 */
```

这个"换个 `FILE*` 就换个输出目的地"的能力，见下面的 `fprintf`。

## 三、fopen / fclose：打开与关闭（p45）

### fopen 原型（p45）

```c
FILE *file_stream = fopen(path, mode)
```

| 参数 | 课件说明 |
|---|---|
| **`path`** | *"char\*, **absolute or relative path**"* —— 绝对路径或相对路径 |
| **`mode`** | 一个**字符串**，见下表 |

### 六种 mode（p45 原文）

| `mode` | 课件原文含义 |
|---|---|
| **`r`** | *"open file for **reading**"* |
| **`r+`** | *"open file for **reading and writing**"* |
| **`w`** | *"**overwrite** file or **create** file for writing"* |
| **`w+`** | *"open for reading and writing; **overwrites** file"* |
| **`a`** | *"open file for **appending**（writing at **end of file**）"* |
| **`a+`** | 读 + 追加 |

**三条规律，看懂就不用背：**

| 位置 | 含义 |
|---|---|
| **第一个字母** | **读还是写**：`r` = read，`w` / `a` = write |
| **`+` 后缀** | **能不能同时读**（`r+` / `w+` / `a+`） |
| **`w` 还是 `a`** | 文件已存在时：**`w` 清空重写**，`a` **追加到末尾** |

> [!warning] `w` 的破坏性
> **`w` 会无条件清空文件** —— 不管文件原来有没有内容。
> ```c
> fopen("data.txt", "r");     /* 安全 */
> fopen("data.txt", "w");     /* ★ data.txt 的内容立刻没了 ★ */
> ```
> 而且 **文件不存在时 `fopen(…,"r")` 返回 `NULL`** —— 和 `open` 返回 `-1` 是同一个模式，见 [[../文件描述符与流/open read write close|open 的返回值约定]]。
>
> 这也是课件 p50 讨论 `scanf` 时反复提到的那个"输入缓冲里还留着 `\n`"问题的根源 —— 你用 `w` 清了屏幕，用户上次敲的换行还留在 `stdin` 的缓冲区里。

### fclose

**关掉 `FILE*`**，同时**冲刷缓冲区**并释放底层 fd。

> [!tip] `close(fd)` vs `fclose(FILE*)` 的差别
> | | `close(fd)` | `fclose(f)` |
> |---|---|---|
> | 层次 | **系统调用** | **C 库** |
> | 参数 | fd（整数） | `FILE*` |
> | 会不会冲刷缓冲 | ❌ **直接扔给内核，缓冲丢失！** | ✅ **先冲刷再关** |
>
> **所以：如果你是用 `fopen` 开的，就必须用 `fclose` 关。** 混用会导致缓冲区里的数据丢失。
>
> ⚠️ **这个区别课件 L03 没有明确讲。** 课件 p41 讲 `close`、p45 讲 `fclose`，但**没有对比两者的关系**。上面这段是根据 C 标准库的通行行为补的，**背景补充**。

## 四、printf：格式化输出（p46–p49）

### 原型（p46）

```c
printf(formatted_string, ...)
```

> *"**formatted_string**: string that **describes the output information**, variable types are **escaped with `%`**. The formatted string is followed by **as many expressions as are referenced in the formatted string**."*
> （格式化字符串：**描述要输出的信息**，变量类型**用 `%` 转义**。格式化字符串后面跟着**与格式串里引用到的数量相同的表达式**。）

**两个要点：**

| 要点 | 含义 |
|---|---|
| **`%` 转义** | 格式串里的 `%` 告诉 `printf`"下一个参数是什么类型" |
| **表达式个数要对应** | 格式串里有几个 `%`，后面就得有几个参数 |

### 转义符全表（p48 原文）

| 转义符 | 课件原文含义 |
|---|---|
| **`%d`, `%i`** | **decimal integer** 十进制整数 |
| **`%u`** | **unsigned decimal integer** 无符号十进制整数 |
| **`%o`** | **unsigned octal integer** 无符号八进制整数 |
| **`%x`, `%X`** | **unsigned hexadecimal integer** 无符号十六进制整数 |
| **`%c`** | **character** 字符 |
| **`%s`** | **string or character array** 字符串或字符数组 |
| **`%f`** | **float** |
| **`%e`, `%E`** | **double（scientific notation）** 科学计数法 |
| **`%g`, `%G`** | **double or float** |
| **`%%`** | *"outputs a `%` character"* — **输出一个 `%` 字符本身** |

> [!tip] `%%` 是"我要打一个百分号"
> 如果你想打印字面量 `"100% 完成"`，直接写 `printf("100% 完成")` 会在那个 `%` 处出问题。
> **必须写成 `printf("100%% 完成")`。**
> 这就是 `%%` 存在的原因 —— 它是"转义转义符自己"。

### 课件的三个例子（p49）

课件给了三条，逐条验证：

```c
printf("The sum of %d, %d, and %d is %d\n", 65, 87, 33, 65+87+33);
```
**Output**: `The sum of 65, 87, and 33 is 185`

**验证**：格式串里有 **4 个 `%d`**，后面有 **4 个参数** —— 对应。且 `65+87+33 = 185` ✓

```c
printf("Error %s occurred at line %d \n", emsg, lno);
```
**Output**: `Error invalid variable occurred at line 27`

**验证**：**1 个 `%s` + 1 个 `%d` = 2 个参数**，顺序对应 ✓

```c
printf("Hexadecimal form of %d is %x \n", 59, 59);
```
**Output**: `Hexadecimal form of 59 is 3B`

**验证**：$59 = 3\times16 + 11 = 48+11 = 59$，而 $11$ 对应十六进制的 **`B`** ✓ —— **大写 `B` 说明格式符是大写的 `%X` 还是小写的 `%x` 决定的**。

## 五、scanf：格式化输入（p50–p52）

### 原型（p50）

```c
scanf(formatted_string, ...)
```

课件对它的描述只有一句关键的话：

> *"Similar syntax as `printf`, **only the formatted string represents the data that you are reading in**."*
> （语法和 `printf` 类似，**只是格式串代表你要读进来的数据**。）

**最重要的区别在下一句**：

> *"**Must pass variables by reference.**"*
> （**必须按引用传递变量。**）

**"by reference（按引用）"是 C 里最反直觉的规则**，说明一下：

> [!warning] 为什么 `scanf` 要传地址，`printf` 不用
> ```
> int x = 5;
>
> printf("%d", x);      /* printf 只是"读" x 的值 → 直接传值 */
> scanf("%d", x);       /* ★ 错误！scanf 要"写" x ★ */
> ```
>
> **C 传参数一律按值传递。** 如果 `scanf` 直接收 `x`，它拿到的是**副本**，写副本对 `x` 毫无影响。
> **所以必须传 `x` 的地址**，让 `scanf` 知道去哪儿写：
> ```c
> scanf("%d", &x);      /* & 是"取地址" */
> ```

### 课件的例子（p50）

```c
scanf(" %d %c %s", &int_var, &char_var, string_var);
```

**注意这一行里三个参数写法不一致，这是课件故意留下的考点：**

| 参数 | 写法 | 为什么 |
|---|---|---|
| `&int_var` | **加 `&`** | `int` 是标量，需要地址才能写回去 |
| `&char_var` | **加 `&`** | `char` 是标量，同上 |
| `string_var` | **不加 `&`** | **`%s` 写进的是"字符数组"，数组名本身就是首元素地址** |

**规则一句话**：

> **`%s` 不用 `&`（数组名自带地址），其他标量都要 `&`。**

> [!warning] 注意格式串开头那个空格
> ```c
> scanf(" %d …")
>       ↑ 这个空格不是笔误
> ```
> **课件 p51 专门解释了它**：
> > *"The **leading white space** is to **ask `scanf` to ignore any white space**（including `\n`）in the input buffer."*
>
> **这个空格是用来吃掉前面残留的换行符的。**
>
> 完整的问题链：
> ```
> 用户在"请输入数字"的提示后敲了 123 并回车
>        ↓
> 缓冲区里现在是 "123\n"
>        ↓
> scanf("%d", &x) 读走 123，但 "\n" ★留在缓冲区里★
>        ↓
> 下一个 scanf("%s", buf) 不跳过空白
>        ↓
> 它读到的第一个字符是 "\n" → 字符串是空的 → 用户一脸茫然
> ```
>
> **课件 p52 还给了另一个解法**（提到 `getchar`），并说还有其它替代方式。**它没有完整列出所有替代方案**，属于已知缺口。

## 六、printf / scanf 家族（p53）

### 课件给的两个（p53）

```c
int fprintf(FILE *stream, const char *format[, argument ]…);
int sprintf(char *buffer, const char *format[, argument ]…);
```

| 函数 | 输出到 | 用途 |
|---|---|---|
| `printf` | **stdout** | 标准输出 |
| **`fprintf`** | **指定 `FILE*`** | *"Prints to a **file stream** instead of stdout"* |
| **`sprintf`** | **字符数组** | *"Prints to a **character array** instead of stdout"* |

**`fprintf` 的意义**：它让"输出到哪儿"变成一个**参数**。

```c
printf("hello\n");            /* 打到屏幕 */
fprintf(stdout, "hello\n");   /* 等价 */
fprintf(stderr, "error\n");   /* 打到 fd 2，见 [[../文件描述符与流/文件描述符与 SFT|0/1/2]] */
fprintf(f, "hello\n");        /* 打到 f 指向的文件 */
```

**这就是"一切皆文件"在输出侧的表现** —— 屏幕、终端、文件、日志，**对 `fprintf` 来说没有区别，全都是 `FILE*`**。

> [!warning] `sprintf` 的经典危险
> `sprintf(buffer, …)` **不知道 `buffer` 有多大**，格式串一长就**越界写栈**，直接踩坏内存。
> **安全做法是用 `snprintf`**，它有长度参数。
>
> ⚠️ **课件 p53 只讲了 `fprintf` 和 `sprintf`，没有提 `snprintf`，也没有提这个风险。** 属于已知缺口。

## 七、两层对照速查

| 我要做的事 | C 库层（本篇） | 系统调用层 |
|---|---|---|
| 打开文件 | `fopen(path, mode)` → `FILE*` | `open(path, flags)` → fd |
| 读 | `fscanf` / `fgets` / `fread` | `read(fd, buf, n)` |
| 写 | `printf` / `fprintf` / `fwrite` | `write(fd, buf, n)` |
| 关闭 | `fclose(f)` ← **会冲刷缓冲** | `close(fd)` ← **不会冲刷** |
| 定位 | `fseek` / `ftell` / `feof` | `lseek` |
| 头文件 | `<stdio.h>` | `<unistd.h>` `<fcntl.h>` |

## 一句话

> **`FILE*` 指向进程用户区里的 `FILE` 结构，其中同时有**缓冲区**和 **fd**，所以是"**句柄的句柄**"；`fopen`/`fclose` 管这个结构（**`w` 会清空、`r` 失败返回 `NULL`**），`printf`/`scanf` 做格式化（**转义符 %d %u %o %x %c %s %f %e %g，输出字面 `%` 要写 `%%`**；`scanf` **必须传 `&`，但 `%s` 不用**）；`fprintf` 把"输出到哪儿"变成参数，**屏幕和文件对它是同一回事**。

## 相关笔记

- **上一步**：[[../文件描述符与流/文件描述符与 SFT|文件描述符与 SFT]] — 底下的 fd 表和 SFT
- **另一层（系统调用）**：[[../文件描述符与流/open read write close|open / read / write / close]]
- **输出目的地可换**：[[../重定向与管道/I O 重定向与 dup|I/O 重定向与 dup]] — 换 fd 就能换输出目的地
- **为什么重定向能省去 `> file`**：[[../Unix 总览/Unix 哲学与工具组合|Unix 哲学与工具组合]] — Shell 帮你把 stdout 接走
- **权限位（`fopen` 的 mode 之外那层）**：[[../文件系统结构/权限位与 ls -l|权限位与 ls -l]]
- **缓冲区的坑**：[[../进程管理/fork 创建进程|fork]] 第五节 — 为什么 fork 后要 `_exit`
- **本讲总览**：[[../index|系统编程 MOC]]