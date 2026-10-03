---
tags:
  - pytorch
  - logits
  - 损失函数
  - 分类
created: 2026-09-10
type: 知识点
aliases:
  - logits
  - 线性层输出
  - Linear 输出
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# nn.Linear 输出与 logits

> [!warning] `nn.Linear` **不会自动 Softmax**
> 它只做仿射线性变换 $z = xW^T + b$，输出**任意实数**的 logits。

## `nn.Linear` 的本质

$$
z = xW^T + b
$$

- $z$ 各维可正可负
- 加起来**不必等于 1**
- 不能把 $z_i=2$ 解释成"200% 概率"

例：ResNet 最后的 `nn.Linear(512, 10)` 输出 10 个 logits：

```python
logits = [2.0, 0.3, -1.2, 0.1, 3.2, -0.5, 0.8, -0.7, 1.5, 0.4]
```

最大下标 4（值 3.2）就是模型最倾向的类别。

## 为什么叫 logit

严格定义（**二分类**）：正类概率 $p$ 的对数几率：

$$
\operatorname{logit}(p) = \log\left(\frac{p}{1-p}\right)
$$

反过来用 Sigmoid 还原：

$$
p = \sigma(z) = \frac{1}{1+e^{-z}}
$$

| logit $z$ | Sigmoid 后的 $p$ | 含义 |
| --: | --: | :-- |
| $-2$ | ≈ 0.12 | 模型较不相信正类 |
| $0$ | 0.50 | 两类同样倾向 |
| $2$ | ≈ 0.88 | 模型较相信正类 |

**深度学习里 "logits" 习惯用法**= Softmax / Sigmoid **之前**的未归一化类别分数，**不严格**要求每一维都对应某个概率的 log-odds。

## 多分类的 Softmax

$$
\operatorname{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}
$$

例：3 分类 $z = [2.0, 1.0, 0.1]$：

$$
e^{2.0} \approx 7.39,\quad e^{1.0} \approx 2.72,\quad e^{0.1} \approx 1.11,\quad \text{总和} \approx 11.22
$$

$$
\operatorname{softmax}(z) \approx [0.66,\ 0.24,\ 0.10]
$$

> 此时每项 ∈ $[0,1]$，总和 1，才是合法的概率分布。

## 训练不用 Softmax 的原因

标准写法：

```python
logits = model(images)                # 形状 [batch, num_classes]
loss = nn.CrossEntropyLoss()(logits, labels)
```

`nn.CrossEntropyLoss` 内部 = `LogSoftmax + NLLLoss` 的数值稳定融合，**期待接收 logits**。若先在模型末尾加 Softmax，会破坏数值稳定性且通常训练变差。

**不要**这么写：

```python
probs = torch.softmax(model(images), dim=1)   # 错！
loss = nn.CrossEntropyLoss()(probs, labels)
```

## 推理时：要不要 Softmax

| 目的 | 写法 |
| :-- | :-- |
| 只要预测类别 | `pred = logits.argmax(dim=1)` |
| 要看"模型有多确信" | `probs = torch.softmax(logits, dim=1)` |
| 输出概率做后处理（阈值、采样） | `probs = torch.softmax(...)` |

> Softmax 不改变大小顺序，所以只看类别时 `argmax(logits) == argmax(softmax(logits))`。
> 只为省一次计算时，直接对 logits 做 `argmax`。

## 二分类 / 多标签的区别

| 任务 | Linear 输出 | 训练损失 | 推理概率 |
| :-- | --: | :-- | :-- |
| 单标签多分类（猫/狗/鸟） | `nn.Linear(..., C)` 输出 $C$ 个 logits | `nn.CrossEntropyLoss()` | `softmax(logits, dim=1)` |
| 二分类（是猫/不是猫） | `nn.Linear(..., 1)` 输出 1 个 logit | `nn.BCEWithLogitsLoss()` | `sigmoid(logit)` |
| 多标签（一图可同时有猫、狗） | `nn.Linear(..., C)` 输出 $C$ 个 logits | `nn.BCEWithLogitsLoss()` | `sigmoid(logits)` 逐类独立 |

`BCEWithLogitsLoss` 同理是 Sigmoid + 二元交叉熵的稳定融合；**不要**先手动 `sigmoid` 再送入。

## 完整流水线图示

```text
ResNet 特征 h
   ↓
nn.Linear(512, 10)        # 仿射变换
   ↓
logits  z = Wh + b        # 任意实数
   ↓
   ├──→ 训练：nn.CrossEntropyLoss()(logits, labels)
   ├──→ 推理看概率：softmax(logits, dim=1)
   └──→ 推理看类别：logits.argmax(dim=1)
```

## 相关笔记

- **场景**：[[Logits、Softmax 与 argmax]] — 这是按 logits 分类整理的姐妹笔记
- **架构**：[[CNN 图像分类模型结构]] — `fc3(84, 10)` 输出 10 个 logits
- **架构**：[[ResNet 与残差连接]] — ResNet 最后的 `nn.Linear` 输出 logits
- **损失**：[[交叉熵损失]] — CrossEntropyLoss 内部是 LogSoftmax + NLLLoss
- **二分类**：[[Sigmoid]] — 二分类时把单 logit 转概率

## 参考

- [PyTorch `nn.Linear` 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)
- [PyTorch `nn` 文档（logits 约定）](https://docs.pytorch.org/docs/stable/nn.html)