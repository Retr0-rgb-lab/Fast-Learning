---
tags:
  - pytorch
  - 神经网络
  - 深度学习
created: 2026-08-31
type: 知识点
aliases:
  - Build Model
  - 前向传播
---

# nn.Module 与模型构建

一个用于图片分类的**全连接神经网络**：输入一张 28×28 灰度图，输出 10 个类别各自的分数。这是 PyTorch 官方 "Build Model" 一章的标准示例。

## 完整代码

```python
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
```

## nn.Module 与 __init__

- `class NeuralNetwork(nn.Module)`：继承 PyTorch 所有神经网络层和模型的**基础类**。继承后 PyTorch 才能识别、管理模型里的层、权重、偏置和训练状态
- `super().__init__()`：初始化父类的内部机制
- `self.flatten`、`self.linear_relu_stack`：把层**注册**到模型中，这些 `Linear` 层的权重和 bias 会在训练时通过反向传播自动更新

## Flatten：压平维度

把每张 28×28 的二维图变成 784 维一维向量，**只整理形状、不改像素值，无可学习参数**：

```text
[batch, 28, 28] → [batch, 784]
```

原因：后面的 `nn.Linear(28*28, 512)` 是全连接层，期望每条输入是长度 784 的特征向量。`Flatten` 会保留 batch 维，只压每张图自己。

## Linear 与 Sequential

`Linear` 本质是 $y = xW^T + b$，W 和 b 是训练要学的参数。`nn.Sequential` 是"流水线"，数据按写入顺序逐层通过：

| 层 | 输入→输出 | 含义 |
| -- | -------- | ---- |
| `Linear(784, 512)` | 784 → 512 | 从像素组合出 512 个中间特征 |
| `ReLU()` | 512 → 512 | 负数截断为 0，引入非线性，见 [[ReLU]] |
| `Linear(512, 512)` | 512 → 512 | 继续组合、提炼特征 |
| `ReLU()` | 512 → 512 | 再引入非线性 |
| `Linear(512, 10)` | 512 → 10 | 为 10 个类别各输出一个分数 |

## forward：前向计算

`forward` 定义**前向传播**规则——输入从哪进、依次过哪些层、输出什么。PyTorch 在 `model(x)` 时自动调用它。

```text
输入 x [batch, 28, 28]
→ flatten：[batch, 784]
→ linear_relu_stack：3 个 Linear + 2 个 ReLU
→ logits：[batch, 10]
```

> [!warning] 不要直接写 `model.forward(x)`
> 写 `logits = model(x)`，让 PyTorch 同时处理 hooks、自动求导等内部机制。

## 输出是 logits，不是概率

最后 10 个数是 **logits（原始分类分数）**：可正可负、加起来不等于 1，只表示相对倾向。要变成概率需再过 Softmax——详见 [[Logits、Softmax 与 argmax]]。

**最后一层后面不加 ReLU**：负分数被截成 0 会毁掉分类分数；训练用的 [[交叉熵损失|CrossEntropyLoss]] 直接吃 logits。

## 相关笔记

- **前置**：[[Dataset 与 DataLoader]] — DataLoader 组好的 batch 就是 `model(x)` 的输入
- **下游**：[[激活函数]] — 为什么 Linear 之间必须夹激活函数（[[ReLU]]）
- **下游**：[[Logits、Softmax 与 argmax]] — 这个网络最后一层输出的 logits 怎么用
- **下游**：[[交叉熵损失]] — logits 与标签算出 loss
- **下游**：[[Autograd 自动微分]] — 算出 loss 后，参数如何沿梯度更新
- **对照**：[[Sigmoid]] — 二分类输出层的经典选择（本例是多分类，用 logits + softmax）

## 参考

- [Build the Neural Network 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
