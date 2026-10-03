---
tags:
  - pytorch
  - 训练技巧
  - 深度学习
created: 2026-09-01
type: 知识点
aliases:
  - model.train()
  - model.eval()
  - 训练模式与评估模式
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# model.train 与 model.eval

`model.train()` / `model.eval()` **只是切换模式**：不会训练、不会算梯度、**不改任何权重**。它们是在告诉 Dropout、BatchNorm 这类层：现在是在学，还是在正式考试。

## 两者差别

|  | `model.train()` | `model.eval()` |
| :-- | :-- | :-- |
| 干什么 | 设成训练模式 | 设成评估/推理模式 |
| Dropout | 随机丢神经元 | 全部打开，不随机丢 |
| BatchNorm | 用**当前 batch** 的均值/方差，并更新 running stats | 用训练时攒下的 running stats，不再更新 |
| 权重 | **不改** | **不改** |

两者都不调用 `forward`，也不 `backward`。

## Dropout 是什么

训练时随机把一部分神经元输出改成 0，逼网络别死记某几条连接：

- **训练**：这次可能关掉 30% 的神经元，下次关的又不同
- **测试**：全部打开——结果要稳定，不能同一张图每次预测都不一样

所以测试必须 `eval()`，否则同一张图多跑几次答案会抖。

## BatchNorm（BN）是什么

把一层的输出按"均值、方差"拉到比较稳定的尺度，训练更好走：

- **训练**：用当前这一批的均值/方差，并慢慢记下全局统计（running stats）
- **测试**：用训练时记下的统计，不能再依赖"这一批里别人长什么样"

测试若还停在 `train()`，一批只有 1 张图时 BN 会乱掉。

## 与 torch.no_grad() 不是一回事

- `eval()`：换**层的行为**（测试时结果要稳定）
- `no_grad()`：**不算梯度、不建图**（省显存）——机制见 [[计算图与梯度跟踪]]

测试循环通常**两个都要**：

```python
model.eval()
with torch.no_grad():
    for X, y in test_dataloader:
        pred = model(X)
        ...
```

测完若还要继续训练，必须再 `model.train()`，否则 Dropout/BN 会一直停在评估行为上。

> [!note] 小网络也要养成习惯
> FashionMNIST 教程网络只有 Linear + ReLU，没有 Dropout/BN，切不切换数值几乎一样；但习惯上训练前 `train()`、测试前 `eval()`。真正改权重的始终是 `backward` + `step`。

## 相关笔记

- **上游**：[[优化循环与训练闭环]] — test_loop 里的标准写法
- **相关**：[[计算图与梯度跟踪]] — `no_grad` 的机制
- **相关**：[[nn.Module 与模型构建]] — 层的行为由 Module 的模式状态决定

## 参考

- [What does model.train() do? (Stack Overflow)](https://stackoverflow.com/questions/51433378/what-does-model-train-do-in-pytorch)
- [d2l: Dropout](http://d2l.ai/chapter_multilayer-perceptrons/dropout.html) / [Batch Normalization](https://d2l.ai/chapter_convolutional-modern/batch-norm.html)
