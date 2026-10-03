---
tags:
  - pytorch
  - tensor
  - 深度学习
created: 2026-08-31
type: 知识点
---

# Tensor 基础

**Tensor 是 PyTorch 的核心数据结构**：类似 NumPy 的多维数组，但能跑在 GPU 等加速器上、可参与自动求导，是模型输入、输出、参数的统一载体。

## 三项元数据

```python
import torch
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
x.shape    # (2, 2) 维度和尺寸
x.dtype    # torch.float32 数据类型
x.device   # cpu / cuda:0 所在设备
```

## 创建方式

```python
torch.tensor([[1, 2], [3, 4]])  # 从 Python 数据创建
torch.zeros(2, 3)               # 全 0
torch.ones(2, 3)                # 全 1
torch.rand(2, 3)                # [0, 1) 均匀随机
torch.randn(2, 3)               # 标准正态随机
torch.ones_like(x)              # 沿用 x 的 shape/dtype/device
```

`*_like` 系列最省心：默认继承参照 Tensor 的属性，也可用 `dtype=` 覆盖。

## 索引与形状

```python
x[0]         # 第 0 行
x[:, 0]      # 第 0 列
x[..., -1]   # 最后一维的最后一个元素（... = 其余所有维度）
x[1:3, :]    # 切片

x.reshape(4, 1)     # 改形状
x.unsqueeze(0)      # 在 dim=0 增加维度
x.squeeze(0)        # 删除大小为 1 的维度
x.transpose(0, 1)   # 交换两个维度
```

索引切片风格与 NumPy 基本一致。

## 运算要分清

```python
a + b          # 逐元素加法
a * b          # 逐元素乘法（不是矩阵乘法！）
a @ b          # 矩阵乘法
a.matmul(b)    # 等价于 a @ b

torch.cat([a, b], dim=0)    # 沿已有维拼接，shape (4, 2)
torch.stack([a, b], dim=0)  # 新增一维堆叠，shape (2, 2, 2)
```

最易混淆：`*` 是逐元素乘，`@`/`matmul` 才是矩阵乘；`cat` 不加维度，`stack` 加一个新维度。

## CPU 与 GPU

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
x = x.to(device)          # 移到 GPU/CPU
x = x.to(torch.float32)   # 转数据类型
```

Tensor 默认在 CPU；CPU↔加速器频繁搬运有开销，相关计算应放在同一设备上。

## 原地操作注意

```python
x.add_(1)   # 带下划线 = 直接修改 x
```

省内存，但可能破坏自动求导依赖的计算图历史（见 [[计算图与梯度跟踪]]），训练代码中谨慎使用。

## NumPy 互操作

```python
n = np.ones(3)
x = torch.from_numpy(n)   # CPU 上共享内存
n2 = x.numpy()
```

CPU Tensor 与 NumPy 数组共享底层内存，改一个可能同步影响另一个。

## 图像张量的形状（重点）

单张图 = `[C, H, W]` = **[通道数, 高, 宽]**：

```python
gray.shape   # [1, 28, 28]  FashionMNIST 灰度图，1 个通道
rgb.shape    # [3, H, W]    R、G、B 三个通道
```

灰度图每个像素只有一个亮度值，所以是 1 通道；PyTorch 统一用 `[C, H, W]`，即使通道数为 1。

加上 batch 维后 = `[B, C, H, W]`：

```python
X.shape  # [64, 1, 28, 28]  batch_size=64 的 FashionMNIST batch
```

一句话：**单图用 `[通道, 高, 宽]`，一批图用 `[批量数, 通道, 高, 宽]`。**

## 高频排错清单

- **shape 不匹配**：先打印 `x.shape`，检查 batch 维是否在第 0 维
- **device 不一致**：参与运算的 Tensor 是否在同一 device
- **dtype 不一致**：网络输入通常 `float32`，分类标签常用 `long`
- **标量取值**：单元素 Tensor 用 `.item()` 转 Python 数值（如记录 loss）

## 相关笔记

- **下游**：[[Dataset 与 DataLoader]] — DataLoader 每个 batch 返回的就是 Tensor，形状 `[B, C, H, W]`
- **相关**：[[归一化与标准化]] — 对 Tensor 数值做缩放（除以 255、Z-score）
- **相关**：[[Logits、Softmax 与 argmax]] — 模型输出的 10 维向量也是 Tensor，用 `argmax(dim=1)` 取预测
- **下游**：[[Autograd 自动微分]] — `requires_grad=True` 的 Tensor 会积累 `.grad`

## 参考

- [PyTorch Tensors 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
