---
tags:
  - pytorch
  - 数据预处理
  - torchvision
created: 2026-08-31
type: 知识点
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# Transforms 数据转换

**Transforms 负责把原始数据改成模型能吃的格式**；Dataset 只管"有哪些样本"，DataLoader 只管"怎么按 batch 取出来"。三者职责不同，不能互相替代。

## 三者分工

| 对象 | 职责 |
| ---- | ---- |
| Dataset | 定义数据从哪来（文件、标签），`__getitem__` 返回一条**原始**样本 |
| Transform | 在 Dataset 取出样本之后、组 batch 之前，对特征和标签做处理 |
| DataLoader | 打乱、组 batch、多进程加载 |

数据管线：

```text
磁盘原始样本 → Dataset 按索引读出（图 + 标签）→ Transform 当场处理这一条
→ DataLoader 打乱、组 batch → 训练循环喂给模型
```

## 为什么不直接写进 Dataset / DataLoader？

- Dataset 应尽量只管"读数据"，处理逻辑**可插拔**：训练做增强，验证只做 ToTensor + 归一化
- 数据增强（翻转、裁剪）需要**每次读取时随机做**，不能预先写死在磁盘上
- TorchVision 的 Dataset 已预留两个钩子：`transform`（改特征）、`target_transform`（改标签）

## 教程里的实际处理

```python
from torchvision.transforms import v2

training_data = datasets.FashionMNIST(
    root="data", train=True, download=True,
    transform=v2.Compose([
        v2.ToImage(),                        # PIL/NumPy → 图像 Tensor
        v2.ToDtype(torch.float32, scale=True),  # → float32，像素 0~255 缩到 [0,1]
    ]),
    target_transform=v2.Lambda(lambda y: F.one_hot(torch.tensor(y), num_classes=10).float()),
)
```

- `transform=` 处理**图片**；`target_transform=` 处理**标签**
- Dataset 取出一条样本时自动调用，训练循环里不用再转一遍
- 之前看到的 `[1, 28, 28]` 张量就是 transform 作用后的结果

## Compose：按顺序执行

`transform=` 参数只能传**一个**可调用对象，有多步就要用 `v2.Compose` 包成一个。它只做一件事：拿到一张图，**从上到下依次调用列表里的每一步**，把上一步输出交给下一步。

```text
原图 → ToImage（变成图像 tensor）→ ToDtype（变成 0~1 的 float32）
```

`v2` 是 torchvision 新一版 transforms API（替代老的 `ToTensor`）。

## Lambda：塞入自定义逻辑

库里有现成的转图工具，但没有现成的 one-hot，所以用 `Lambda` 包一段自己的函数：

```python
v2.Lambda(lambda y: F.one_hot(torch.tensor(y), num_classes=10).float())
```

| 片段 | 白话 |
| ---- | ---- |
| `lambda y: ...` | 匿名函数：输入标签 y，返回处理结果 |
| `torch.tensor(y)` | 整数变 tensor |
| `F.one_hot(..., num_classes=10)` | `3` → `[0,0,0,1,0,0,0,0,0,0]` |
| `.float()` | 转 float，方便算损失 |

写成普通函数完全等价，教程用 lambda 只是图省事：

```python
def to_onehot(y):
    return F.one_hot(torch.tensor(y), num_classes=10).float()
target_transform = v2.Lambda(to_onehot)
```

## v2 三步流水线的像素级追踪（CIFAR-10 风格）

以训练时常见的三步为例，把一张原始 PIL 图逐步变到网络能吃的张量。假设某像素 RGB = `(255, 128, 0)`：

### 1) `v2.ToImage()`

只做格式转换，不动像素数值：

- 调维度顺序：PIL 默认 `(H, W, C)`，PyTorch 要 `(C, H, W)`
- 转成 PyTorch tensor，dtype 固定 `uint8`，范围 `[0, 255]`

```text
PIL Image (300, 400, 3) → Tensor (3, 300, 400) dtype=uint8
```

像素值不变：`(255, 128, 0)`。

### 2) `v2.ToDtype(torch.float32, scale=True)`

两件事：

- dtype 从 `uint8` 变 `float32`（网络要浮点）
- `scale=True` 表示除以 255，归一化到 `[0, 1]`

```text
255 → 255/255 = 1.0
128 → 128/255 ≈ 0.502
0   → 0/255   = 0.0
```

> [!note] 注意
> `scale=True` 是简单除以 255，**不是** `(x - mean) / std` 那种 Z-score 标准化。这一步每个像素仍在 `[0, 1]`。

### 3) `v2.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))`

对每个通道应用：

```text
output = (input - mean) / std
```

- 第一个元组是 mean（三个通道的 R、G、B）
- 第二个元组是 std

像素追踪（以红色通道为例）：

```text
1.0   → (1.0 - 0.5)/0.5 = +1.0
0.502 → (0.502 - 0.5)/0.5 ≈ +0.004
0.0   → (0.0 - 0.5)/0.5 = -1.0
```

值域从 `[0, 1]` 变成 `[-1, 1]`，以 0 为中心。

### 为什么是 mean=0.5, std=0.5

**不是**"统计意义上的均值和标准差"，而是人为选的最简常数：当数据已是 `[0, 1]` 时，用 `mean=0.5, std=0.5` 正好把范围压成 `[-1, 1]`，让数据关于 0 对称——神经网络训练更稳定。

更严谨做法：去算整个数据集真实的像素均值和标准差。CIFAR-10 实际算出来 R/G/B 大约 `(0.49, 0.48, 0.44)` 和 `(0.25, 0.25, 0.25)`，用那组数字更精确。但 `0.5` 已经够用，是常见的简化。

### 三步总览

| 步骤 | 数据类型 | 数值范围 |
| ---- | -------- | -------- |
| 原始 PIL Image | uint8 (numpy) | `[0, 255]` |
| `ToImage()` | uint8 tensor | `[0, 255]` |
| `ToDtype(float32, scale=True)` | float32 tensor | `[0, 1]` |
| `Normalize((0.5,)*3, (0.5,)*3)` | float32 tensor | `[-1, 1]` |

最终网络看到的张量：`(3, 32, 32)`，float32，每个像素在 `[-1, 1]`。数据增强（`RandomCrop` / `RandomHorizontalFlip` 等）通常放在 `ToImage` 之前——见 [[CNN 训练技巧]]。

## 常见误解校正

| 想法 | 实际情况 |
| ---- | -------- |
| Transform 就是 Z-score 标准化 | Z-score 要用 `Normalize(mean, std)`，教程里没做，见 [[归一化与标准化]] |
| `scale=True` 就是标准化 | 它是 MinMax 式缩放，把像素缩到 [0,1] |
| Z-score 能压尾部/极端值 | 不能，离群点反而更夸张；要 clip、log、鲁棒缩放 |

教程实际做的只是**格式转换**（图→float tensor 0~1，标签→one-hot），目的是"模型能算"，不是完整特征工程。

## 相关笔记

- **前置**：[[Dataset 与 DataLoader]] — Transform 挂在 Dataset 内部，处于取样本和组 batch 之间
- **下游**：[[归一化与标准化]] — `ToDtype(scale=True)` 就是归一化到 [0,1]；Z-score 要用 `Normalize`
- **下游**：[[nn.Module 与模型构建]] — 处理后的 Tensor 才是网络能吃的输入

- **像素域那一侧**：[[../图像表示与预处理/OpenCV PyTorch 预处理流水线|OpenCV PyTorch 预处理流水线]] — 同一件事的 OpenCV 写法

## 参考

- [Transforms 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/transforms_tutorial.html)
