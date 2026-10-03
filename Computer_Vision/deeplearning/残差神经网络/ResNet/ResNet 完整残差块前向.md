---
tags:
  - pytorch
  - 卷积神经网络
  - ResNet
  - 残差块
  - 手算
created: 2026-09-10
type: 知识点
aliases:
  - 残差块手算
  - 残差相加
---

# ResNet 完整残差块前向（手算）

[[ResNet 与残差连接]] 给出了概念。本笔记做几道手算题，从最简单的"逐元素相加"到"真实简化 BasicBlock 前向"，把每个步骤都过一遍。

> 所有题都暂时忽略 BatchNorm，只算 $y = F(x) + x$（或带 ReLU）。

## 最小残差块：identity 卷积核

输入 $3\times3$ 单通道：

$$
x = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 1 & 0 \\ 2 & 1 & 2 \end{bmatrix}
$$

主分支是 1 次 $3\times3$ 卷积，padding=1，bias=0，卷积核：

$$
K = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}
$$

### 主分支输出

这个卷积核只取窗口中心：$F(x) = x$（padding 在边缘处补 0，但窗口中心位置不变，所以输出值仍等于输入对应位置）。

### 残差相加 + ReLU

$$
y = F(x) + x = x + x = 2x
$$

$$
y = \begin{bmatrix} 2 & 4 & 2 \\ 0 & 2 & 0 \\ 4 & 2 & 4 \end{bmatrix}
$$

所有元素都 ≥ 0，ReLU 不改变结果。

> [!tip] 形状相同才能直接相加
> 这里 padding=1 让 F(x) 与 x 形状一致；不补零的话 F(x) 是 $1\times1$，加不进 $3\times3$ 的 $x$。ResNet 用 padding=1（k=3）或 $1\times1$ 卷积保持形状。

## 矩阵残差相加

### 情形 A：正负混合

$$
x = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},\qquad F(x) = \begin{bmatrix} 0 & 1 \\ 2 & -1 \end{bmatrix}
$$

逐元素相加：

$$
y = F(x) + x = \begin{bmatrix} 0+1 & 1+2 \\ 2+3 & -1+4 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 5 & 3 \end{bmatrix}
$$

### 情形 B：负残差 + ReLU

$$
x = \begin{bmatrix} 2 & 4 \\ 1 & 3 \end{bmatrix},\qquad F(x) = \begin{bmatrix} -1 & -2 \\ 0 & -4 \end{bmatrix}
$$

逐元素相加：

$$
z = F(x) + x = \begin{bmatrix} 1 & 2 \\ 1 & -1 \end{bmatrix}
$$

过 ReLU（把负数压成 0）：

$$
y = \operatorname{ReLU}(z) = \begin{bmatrix} 1 & 2 \\ 1 & 0 \end{bmatrix}
$$

> [!warning] 残差加法是 feature map 逐元素相加
> 不是把所有元素求总和，也不是把每行/列分别求和。是同位置元素一对一相加。

## 边缘检测卷积核 + 残差

输入：

$$
x = \begin{bmatrix} 1 & 2 & 1 \\ 1 & 2 & 1 \\ 1 & 2 & 1 \end{bmatrix}
$$

主分支卷积核（垂直边缘检测，左负右正）：

$$
K = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}
$$

padding=1，stride=1，bias=0。

### 主分支输出

对中心位置 $F(x)_{2,2}$（padding 后覆盖 $3\times3$ 全部 9 个数，核只保留左右 3 列）：

$$
F(x)_{2,2} = (-1)\cdot1 + 0\cdot2 + 1\cdot1 + (-1)\cdot1 + 0\cdot2 + 1\cdot1 + (-1)\cdot1 + 0\cdot2 + 1\cdot1 = 0
$$

对所有 $3\times3$ 位置同理算（输入每行都是 $[1,2,1]$），得：

$$
F(x) = \begin{bmatrix} 4 & 0 & -4 \\ 6 & 0 & -6 \\ 4 & 0 & -4 \end{bmatrix}
$$

### 残差相加 + ReLU

$$
z = F(x) + x = \begin{bmatrix} 5 & 2 & -3 \\ 7 & 2 & -5 \\ 5 & 2 & -3 \end{bmatrix}
$$

$$
y = \operatorname{ReLU}(z) = \begin{bmatrix} 5 & 2 & 0 \\ 7 & 2 & 0 \\ 5 & 2 & 0 \end{bmatrix}
$$

**结果解读**：

- **左列** $F(x)=+4/+6/+4$：残差为正，输入特征被**增强**（$1\to5$、$1\to7$、$1\to5$）
- **中列** $F(x)=0$：主分支不改动，**保留捷径传来的原特征**（$2\to2$）
- **右列** $F(x)=-4/-6/-4$：残差为负，加回 x 后变负，ReLU 截断为 $0$——**强烈抑制**

> 卷积核本身是垂直边缘检测器：在原图上从左到右的"亮 → 暗"变化处产生负响应，"暗 → 亮"产生正响应，相等则不响应。

## 真实简化 BasicBlock 前向

更接近真正的 ResNet 块结构：两层 1×1 卷积 + ReLU 堆叠。

输入：

$$
x = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}
$$

第一层 $1\times1$ 卷积，$K_1 = 2,\ b_1 = -1$；第二层 $1\times1$ 卷积，$K_2 = 1,\ b_2 = -1$。前向流程：

$$
a = F_1(x) = 2x - 1
$$

$$
r = \operatorname{ReLU}(a)
$$

$$
F(x) = F_2(r) = r - 1
$$

$$
z = F(x) + x
$$

$$
y = \operatorname{ReLU}(z)
$$

### 逐步算

$$
a = 2\begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix} - \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} = \begin{bmatrix} 1 & -1 \\ 3 & 1 \end{bmatrix}
$$

过 ReLU（负数置 0）：

$$
r = \begin{bmatrix} 1 & 0 \\ 3 & 1 \end{bmatrix}
$$

$$
F(x) = r - \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix}
$$

$$
z = F(x) + x = \begin{bmatrix} 1 & -1 \\ 4 & 1 \end{bmatrix}
$$

$$
y = \operatorname{ReLU}(z) = \begin{bmatrix} 1 & 0 \\ 4 & 1 \end{bmatrix}
$$

## 常见错点速查

| 易错点 | 正确做法 |
| :-- | :-- |
| 残差加法求成总和 | 必须是**逐元素相加**，形状相同 |
| 残差加法写成 $2K$ | $K$ 是卷积核，$F(x)$ 才是特征图；相加是 $F(x)+x$ |
| ReLU 后还期望看到负数 | ReLU 把负数变 0；如果全 0，说明 $F(x)$ 严重抑制 $x$ |
| 形状不同直接相加 | 用 $1\times1$ 卷积投影捷径匹配通道和空间尺寸 |

## 相关笔记

- **概念**：[[ResNet 与残差连接]] — $H(x)=F(x)+x$、退化问题、投影捷径
- **前向基础**：[[卷积层与滤波器]] / [[池化]]
- **训练**：[[CNN 训练技巧]] — 残差块内 BN/ReLU 位置
- **反向**：[[卷积反向传播]] — 残差块梯度的两条通路

## 参考

- [d2l: ResNet 实战](https://d2l.ai/chapter_convolutional-modern/resnet.html)