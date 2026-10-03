---
tags:
  - pytorch
  - 卷积神经网络
  - 训练技巧
  - CNN
  - 深度学习
created: 2026-09-07
type: 知识点
aliases:
  - BatchNorm
  - Dropout
  - 数据增强
  - data augmentation
  - 训练改进
domain: [深度学习, 计算机视觉]
来源: "自学（PyTorch / 深度学习）"
---

# CNN 训练技巧

CIFAR-10 训练一个 2 层 CNN 跑 10 epoch 大约 60% test acc——比随机和纯全连接强，但还远没收敛。下面是常见的"性价比从高到低"改进方法。

## CIFAR-10 准确率参考

| 模型 / 训练方式 | CIFAR-10 准确率 |
| :-- | --: |
| 随机猜 | ~10% |
| 全连接网络（无卷积） | ~50% |
| 2 层 CNN + 10 epoch | ~60% |
| 同样网络训 30-50 epoch | ~65-70% |
| 经典中型 CNN | ~75% |
| ResNet | 90%+ |
| SOTA | 99%+ |

60% 是个"在学东西，但远未收敛 + 网络容量有限"的位置。下面 6 个改进方向按"改的难度 / 收益比"从高到低排。

## 1. 多训几个 epoch（最简单）

直接 `epochs=30~50`。完全不改代码结构，就能从 60% 涨到 65-70%。

判断"还没收敛"的方法：看 train loss 是否还在下降；或最后几 epoch 的 test acc 还在涨。

## 2. 加 BatchNorm

```python
self.bn1 = nn.BatchNorm2d(32)   # 32 = conv1 的 out_channels

def forward(self, x):
    x = self.pool(F.relu(self.bn1(self.conv1(x))))   # Conv → BN → ReLU → Pool
    ...
```

- 把一层输出按"均值、方差"拉到稳定尺度，训练更好走
- 加速收敛 + 提升 1-3 个点
- 详见 [[model.train 与 model.eval]]：BN 在 train/eval 下行为不同（train 用当前 batch 统计并更新 running；eval 用 running），测试循环要 `model.eval()`

## 3. 加 Dropout

```python
self.dropout = nn.Dropout(0.5)   # 全连接层后
```

- 训练时随机置 0 一部分神经元，逼网络别死记某几条连接
- 防止过拟合
- 测完若继续训练必须 `model.train()`，否则 Dropout 一直停在"全开"模式

## 4. 数据增强（收益最大的之一）

```python
train_transform = v2.Compose([
    v2.RandomCrop(32, padding=4),
    v2.RandomHorizontalFlip(),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize((0.5,)*3, (0.5,)*3),
])
```

- 训练时给图加 random crop + horizontal flip = **免费增加数据量**
- 提升 3-5 个点
- 只在训练集开；验证/测试集**不要**开增强（否则评估不公平）

详见 [[Transforms 数据转换]] 的 Compose / 数据增强相关小节。

## 5. 换 Adam 优化器

```python
optimizer = optim.Adam(model.parameters(), lr=1e-3)
```

- 通常比 SGD 收敛更快，特别是前 10 epoch
- 见 [[SGD 与优化器]] 中 SGD vs Adam 的对比
- 简单任务用 Adam 起步是稳妥选择；如果后面要做 SOTA 论文，SGD+momentum 仍是常见配置

## 6. 网络加深

加 1-2 层 conv，注意 `fc1` 的 `in_features` 要随之改（看 flatten 后的通道×高×宽）：

```python
self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)   # 加 padding 控尺寸
```

可以用 [[CNN 维度追踪（CIFAR-10 两层卷积）]] 的公式自己算每层输出。

> [!tip] 整张 CNN 的形状流
> ![[CNN数据形状变化.png]]
>
> 输入 `3×32×32` → 两层 conv+pool → flatten → 三层 linear → 10 维 logits。注意每步旁边的尺寸公式（`32-5+1=28`、`28/2=14` 等）就是 [[CNN 维度追踪（CIFAR-10 两层卷积）]] 里"篱笆桩 +1"那条直觉的成品图。

## 7. 进一步：换 ResNet

当 2 层 conv + 3 层 fc 加深到 5+ 层就难训练了——这正是 [[ResNet 与残差连接]] 解决的"退化问题"。残差块把"学习完整映射"改成"学习在已有特征上的增量"，让 50/101/152 层也能训。配合 [[CNN 训练技巧]] 的 BatchNorm + 数据增强，ImageNet 准确率能从 75% 跳到 90%+。

## 推荐起步组合

> [!tip] 入门最快收益
> **多训 epoch + 加 BatchNorm**——代码改动小，收益最明显。建议先做这两步再考虑其他。

如果过拟合明显（train acc 高、test acc 低）→ 加 Dropout + 数据增强。
如果前 10 epoch 收敛太慢 → 换 Adam。

## 相关笔记

- **使用**：[[CNN 图像分类模型结构]] / [[CNN 维度追踪（CIFAR-10 两层卷积）]] — 这些技巧都堆在 CNN 骨架上
- **数据预处理**：[[Transforms 数据转换]] — 数据增强在 transform 里实现
- **核心层**：[[卷积层与滤波器]] / [[池化]]
- **模式**：[[model.train 与 model.eval]] — BN/Dropout 在 eval 下要切换
- **优化器**：[[SGD 与优化器]] — SGD vs Adam 选择

## 参考

- [PyTorch CIFAR-10 教程](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- d2l: BatchNorm / Dropout / 数据增强
