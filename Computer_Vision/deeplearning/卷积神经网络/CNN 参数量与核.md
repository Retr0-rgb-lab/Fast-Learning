---
tags:
  - pytorch
  - 卷积神经网络
  - CNN
  - 参数量
  - kernel
created: 2026-09-07
type: 知识点
aliases:
  - CNN parameters
  - kernel 计算
  - 通道加总
  - bias
---

# CNN 参数量与核

核（kernel/滤波器）、跨通道加总、bias 与参数量计算——单独成一篇，因为是 CNN 最常被卡住的几处"听起来懂、算起来错"的细节。

## 一、一个核到底长什么样

`nn.Conv2d(in_channels, out_channels, kernel_size)` 里：

- **`kernel_size`** 只定空间大小（如 `5` → $5\times5$）
- **深度** = `in_channels`，不是写死 RGB

一个核是 $C_\text{in}\times k_H\times k_W$ 的三维小盒子。`Conv2d(3, 32, 5)` 里：
- 一个核：$3\times5\times5=75$ 个数
- 32 个核：$32\times 75 = 2400$ 个权重
- 整层权重张量形状：`(out_channels, in_channels, kH, kW)` = `(32, 3, 5, 5)`

> [!note] 通道数不是默认 3
> 第二层 `Conv2d(32, 64, 5)` 每个核是 $32\times5\times5=800$，不是 75。核的深度必须等于上一层输出通道数。

## 二、跨通道怎么算（最容易混）

> [!tip] 卷积核如何扫描输入得到输出
> ![卷积核扫描输入得到输出](../../图片/卷积核扫描输入得到输出.png)
>
> 一张 $3\times32\times32$ 的输入经过 `nn.Conv2d(3, 32, 5)`：每个 5×5×3 的核在空间滑动，**三通道逐元素相乘后加总 + bias** → 输出 1 个数；32 个核各自扫完整张图 → 32 张特征图。



一个 5×5×3 的核盖住同一位置的 R、G、B 三张图：

1. R 的 25 个数 × 核的 R 切片 25 个数
2. G 的 25 个数 × 核的 G 切片 25 个数
3. B 的 25 个数 × 核的 B 切片 25 个数
4. **75 个乘积全部加总**（再加 bias）→ 输出图上 **1** 个标量

这个数**不是** `(R, G, B)`，也**不是**把颜色加回去还原像素。它是"这个局部像不像这个核在找的模式"。每个核一张**特征图**（灰度式的响应图）。

### 常见误解澄清

| 误解 | 实际 |
| :-- | :-- |
| R 通道里的 G、B 当作 0 | R 就是一张单通道图，没有"G=0、B=0" |
| 三个通道相加 = 合成 RGB 像素 | 加权求和 → 1 个**特征数** |
| 输出仍是彩色图 | 每个核 → 1 张特征图，不是 RGB |

核是 1×1 时最易看清：输出 $= w_R R + w_G G + w_B B + b$，三个颜色被**加权混合成一个标量**。

## 三、手算例子（最小三通道卷积）

输入 $3\times3\times3$（每个通道一张 $3\times3$），单个核 $2\times2\times3$，stride=1，padding=0，**无 bias**。输出应是 $2\times2$。

> [!example] 输入 X（每张是 3×3）

通道 0：
$$
\begin{bmatrix}1&2&0\\0&1&3\\2&0&1\end{bmatrix}
$$

通道 1：
$$
\begin{bmatrix}0&1&2\\1&0&1\\0&2&1\end{bmatrix}
$$

通道 2：
$$
\begin{bmatrix}2&0&1\\0&1&0\\1&0&2\end{bmatrix}
$$

> [!example] 核 K（每个通道是 2×2）

通道 0：
$\begin{bmatrix}1&0\\0&1\end{bmatrix}$

通道 1：
$\begin{bmatrix}0&1\\1&0\end{bmatrix}$

通道 2：
$\begin{bmatrix}1&1\\0&0\end{bmatrix}$

### $Y_{0,0}$（左上角）

核盖住每张图的左上 $2\times2$：

- R：$1\cdot1 + 2\cdot0 + 0\cdot0 + 1\cdot1 = 2$
- G：$0\cdot0 + 1\cdot1 + 1\cdot1 + 0\cdot0 = 2$
- B：$2\cdot1 + 0\cdot1 + 0\cdot0 + 1\cdot0 = 2$
- 总和：$2+2+2 = 6$

同理算其他三个位置，结果：

$$
Y=\begin{bmatrix}6 & 8 \\ 1 & 6\end{bmatrix}
$$

> [!warning] 这 6 不是把 RGB 加回彩色像素
> 只是这个位置的**特征响应**。一张输出图是 1 个核产生的灰度式特征图。

## 四、Bias 是什么

`Conv2d` 的 bias 是**长度 $C_\text{out}$ 的向量**，**不是矩阵**。

- 每个核（每个输出通道）**1 个数**
- 同一个核扫到的所有位置**共用这一个 $b$**
- 加在**跨通道求和之后**的标量上

例子：上面手算若 `bias=b`，结果是 $6+b,\ 8+b,\ 1+b,\ 6+b$——4 个位置加的是**同一个** $b$。

### 为什么是"一通道一个数"

| 共享对象 | 范围 |
| :-- | :-- |
| 核的 $C_\text{in}\cdot k_H\cdot k_W$ 个权重 | 整张图所有位置共用（权值共享） |
| bias 1 个数 | 这张特征图所有位置共用 |

和 `Linear` 一样：一个输出神经元一个 $b$。卷积只是把这个神经元在空间上滑来滑去，所以 $b$ 也跟着共用。若每个格子一个 bias，就要 $H_\text{out}\times W_\text{out}$ 个，**平移不变性也没了**。

32 个核就有 32 个不同的 $b$：第 $m$ 张输出图上每个格子都加 $b^{(m)}$。

## 五、参数量公式

### 单层 Conv2d

$$
\#\text{weight} = k_H\cdot k_W\cdot C_\text{in}\cdot C_\text{out}
$$

$$
\#\text{bias} = C_\text{out} \quad (\text{默认 } \text{bias}=\text{True})
$$

$$
\#\text{total}_\text{conv} = k_H\cdot k_W\cdot C_\text{in}\cdot C_\text{out} + C_\text{out}
$$

**和输入空间尺寸无关**——这就是权值共享的意义，Conv 层只看 $k$ 和通道数。

### 单层 Linear

$$
\#\text{total}_\text{linear} = \text{in\_features}\cdot\text{out\_features} + \text{out\_features}
$$

### Pool / ReLU / Flatten

**无参数**。

### 例：5×5×3 Conv2d(3, 32) 参数量

$$
\#\text{weight} = 5\times5\times3\times32 = 2400
$$

$$
\#\text{bias} = 32
$$

$$
\#\text{total} = 2432
$$

## 六、完整网络参数量手算（带空间尺寸推导）

> [!example] 网络结构（输入 3×32×32，padding=0，stride=1，池化 2×2 stride=2，所有层 bias=True）

```text
Conv2d(3,  16, kernel_size=3)
ReLU + MaxPool
Conv2d(16, 32, kernel_size=3)
ReLU + MaxPool
Flatten
Linear(?,   64)
ReLU
Linear(64,  32)
ReLU
Linear(32,  10)
```

### 空间尺寸推导（关键）

- $32 \xrightarrow{\text{conv }k=3} 30 \xrightarrow{\text{pool}} 15$
- $15 \xrightarrow{\text{conv }k=3} 13 \xrightarrow{\text{pool}} 6$

**6×6 只是一张特征图的高×宽**。Flatten 还要乘通道：

$$
32\times 6\times 6 = 1152
$$

所以第一层 Linear 是 `Linear(1152, 64)`，不是 `Linear(36, 64)`。

### 各层参数

| 层 | 计算 | 参数 |
| :-- | :-- | --: |
| Conv1 weight | $3\cdot3\cdot3\cdot16$ | 432 |
| Conv1 bias | $16$ | 16 |
| Conv2 weight | $3\cdot3\cdot16\cdot32$ | 4608 |
| Conv2 bias | $32$ | 32 |
| Linear1 | $1152\cdot64 + 64$ | 73792 |
| Linear2 | $64\cdot32 + 32$ | 2080 |
| Linear3 | $32\cdot10 + 10$ | 330 |
| **合计** | | **81290** |

### 易错点

- Conv bias **不是** $k\times k$ 矩阵，是每个输出通道 1 个数（Conv1 = 16，Conv2 = 32）
- Flatten 的输入是 $C\times H\times W$，**不是**只算 $H\times W$（最容易把 36 写进来当 Linear1 的 in_features）

> [!note] Conv 参数与输入是 32×32 还是 224×224 无关；Linear1 才吃 Flatten 后的 1152。

## 七、术语澄清

| 叫法 | 含义 |
| :-- | :-- |
| **核** (kernel) / **滤波器** (filter) | 一个**输出通道**对应的 $C_\text{in}\times k_H\times k_W$ 个权重 |
| **输出通道** | 一个核对应一个输出通道；`out_channels` = 核的个数 |
| **特征图** (feature map) | 一个核扫描整张输入得到的 $H_\text{out}\times W_\text{out}$ 响应图 |
| **depth** (PyTorch 中) | 输入或输出张量的通道数 |

> 一个核 ≠ 一张图。一个核产出 1 张特征图，但**一张图 = 一个核扫出来的结果**。

## 相关笔记

- **前向原理**：[[卷积层与滤波器]] — Conv2d 输出尺寸、滤波器、跨通道加总
- **维度追踪**：[[CNN 维度追踪（CIFAR-10 两层卷积）]] — 从输入到输出逐层形状
- **结构**：[[CNN 图像分类模型结构]] — 完整 CIFAR-10 Net 类
- **训练**：[[CNN 训练技巧]] — BatchNorm / Dropout / 数据增强
- **反向**：[[卷积反向传播]] — 这些权重如何更新

## 参考

- [PyTorch Conv2d 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.conv.Conv2d.html)