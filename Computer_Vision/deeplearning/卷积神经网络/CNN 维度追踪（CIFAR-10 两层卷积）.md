---
tags:
  - pytorch
  - 卷积神经网络
  - CNN
  - 维度计算
  - 计算机视觉
created: 2026-09-07
type: 知识点
aliases:
  - dimension trace
  - shape trace
  - CNN 维度
---

# CNN 维度追踪（CIFAR-10 两层卷积）

把"输入 3×32×32 的图像"经过每一层后**形状**怎么变，按一个具体的 2 层卷积网络走一遍。

## 数据形状变化总览

> [!tip] 从输入到 logits 的形状变化
> ![CNN 数据形状变化](../../图片/CNN数据形状变化.png)
>
> 输入 `3×32×32` 经过 2 层 Conv→Pool→3 层 Linear 逐步压成 `10` 维 logits。注意前 4 步**每个方向的尺寸**都写出来了，配上右边的公式（`32-5+1=28`、`28/2=14` 等）就是下文"为什么是 `(32-5)+1` = 28"一节的"成品图"。

## 完整代码（含 1 个常见 typo）

```python
class CNN_Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.conv1 = nn.Conv2d(in_channels=3,  out_channels=32, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5)
        self.pool  = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1   = nn.Linear(in_features=64 * 5 * 5, out_features=128)
        self.fc2   = nn.Linear(in_features=128, out_features=64)
        self.fc3   = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))   # 注意：原文写成 self.pooll 是 typo
        x = self.flatten(x)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x
```

> [!warning] 常见 typo：`self.pooll` → `self.pool`
> 手写网络时容易把 `self.pool` 写成 `self.pooll`（多打一个 l），运行会 `AttributeError: 'CNN_Network' object has no attribute 'pooll'`。务必改回 `self.pool`。

## 完整维度追踪（单张图，无 batch）

输入单张图 `x.shape == (3, 32, 32)`：

| 步骤 | 形状 | 公式 |
| :-- | :-- | :-- |
| 输入 | `(3, 32, 32)` | RGB 图像 |
| `conv1` (k=5, s=1, p=0) | `(32, 28, 28)` | `(32-5)/1+1 = 28` |
| `pool` (k=2, s=2) | `(32, 14, 14)` | `(28-2)/2+1 = 14` |
| `conv2` (k=5, s=1, p=0) | `(64, 10, 10)` | `(14-5)/1+1 = 10` |
| `pool` (k=2, s=2) | `(64, 5, 5)` | `(10-2)/2+1 = 5` |
| `flatten` | `(1600,)` | `64×5×5 = 1600` |
| `fc1` | `(128,)` | `1600 → 128` |
| `ReLU` | `(128,)` | |
| `fc2` | `(64,)` | `128 → 64` |
| `ReLU` | `(64,)` | |
| `fc3` | `(10,)` | `64 → 10` 类 logits |

加 batch 维：每行前面加 `N` → `(N, ...)`。`Linear` 内部对每个 batch 元素独立算，**层参数与 batch 大小无关**。

## 为什么是 `(32-5)+1` = 28

卷积把 kernel 在图上滑动，**每停一次产出 1 个数**。输出边长 = 合法停靠次数。

5×5 的核盖住 5 个像素：

- 第一次：覆盖 `[0, 4]`，起点 `0`
- 最后一次：覆盖 `[27, 31]`，起点 `27`

起点从 `0` 到 `27`，**两端都算**：

$$
(32-5)+1=28
$$

`32-5=27` 只是"最后一次能从哪开始"；没有 `+1` 会漏掉第一次——这是**篱笆桩问题**：3 根桩之间有 2 段，**桩数要再加 1**。

更小的例子：长度 5，核 3，stride 1

- 窗口：`[0,2]`、`[1,3]`、`[2,4]`
- 次数：`5-3+1=3`，不是 `5-3=2`

## 完整公式

PyTorch `Conv2d` 默认 `padding=0`、`dilation=1`：

$$
H_\text{out}=\left\lfloor\frac{H_\text{in}+2p-k}{s}\right\rfloor+1
$$

> [!tip] 写公式时**始终加括号**
> 避免写成 `14-5 除以 1+1` 或 `10-2÷2` 这种口语化表达——容易引起歧义。

## Flatten 后是 `(N, 1600)`，不是 `(1600, 64, 5, 5)`

> [!warning] 64 是通道数，不是 batch
> 第二个 pool 后形状是 `(N, 64, 5, 5)`。`nn.Flatten()` 默认从 dim=1 开始压平，**留下 batch**（dim=0）：
> - 第二层 pool 后：`(N, 64, 5, 5)`
> - Flatten：`(N, 1600)`
> - fc1：`(N, 128)`

`64 × 5 × 5 = 1600` 是**每张图**压平后的特征长度，**和 `N` 无关**。`Linear(1600, 128)` 对 batch 里每张图各算一遍；batch 是 64 还是 128，层参数都不变。

如果看到 `(64, 64, 5, 5)` 这种"4 维全压平"的写法——通常是把 dim=0 的 batch 一起压掉了，那是错的。

## 三件事别混

| | 角色 |
| :-- | :-- |
| `64`（conv2 out_channels） | 通道数，由 `Conv2d` 写死 |
| `5, 5` | 空间尺寸，由公式算出来 |
| `N`（batch） | DataLoader 决定，**不**出现在网络定义里 |

## 顺带算一下参数量

形状对上之后，**参数量也可以顺便算**（每层的 `kernel` 长什么样、`bias` 是不是矩阵，详见 [[CNN 参数量与核]]）：

| 层 | 权重 | 偏置 | 小计 |
| :-- | --: | --: | --: |
| `conv1` (3→32, k=5) | $32\times 3\times 5\times 5 = 2400$ | $32$ | 2432 |
| `conv2` (32→64, k=5) | $64\times 32\times 5\times 5 = 51200$ | $64$ | 51264 |
| `fc1` (1600→128) | $1600\times 128 = 204800$ | $128$ | 204928 |
| `fc2` (128→64) | $128\times 64 = 8192$ | $64$ | 8256 |
| `fc3` (64→10) | $64\times 10 = 640$ | $10$ | 650 |
| **合计** | | | **267530** |

可以看到：**fc1 占了 ~77% 的参数**——这也解释了为什么现代网络常用 `AdaptiveAvgPool2d(1)` + 小 FC 替代大 FC。

## 相关笔记

- **理论**：[[卷积层与滤波器]] — 输出尺寸公式更详细版
- **结构**：[[CNN 图像分类模型结构]] — 1 层 conv 的 CIFAR-10 例子
- **参数量**：[[CNN 参数量与核]] — 核怎么算、跨通道加总、bias 是什么
- **容器**：[[nn.Module 与模型构建]] — Net 类的基本结构
- **训练改进**：[[CNN 训练技巧]] — 提升准确率的常用技巧
- **进一步**：[[ResNet 与残差连接]] — 2 层 conv 加深会撞退化问题，残差块让 50/101/152 层也能训
- **相关**：[[Tensor 基础]] — Tensor 形状约定 `(C, H, W)`
- **相关**：[[Logits、Softmax 与 argmax]] — fc3 输出怎么用
- **数据预处理**：[[Transforms 数据转换]] — 训练前归一化到 `[-1, 1]`

## 参考

- [PyTorch CIFAR-10 教程](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
