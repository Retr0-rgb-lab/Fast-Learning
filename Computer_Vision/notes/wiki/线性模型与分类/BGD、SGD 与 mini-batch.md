---
tags:
  - 深度学习
  - 优化
  - 梯度下降
  - 训练
created: 2026-09-14
type: 知识点
aliases:
  - batch gradient descent
  - stochastic gradient descent
  - mini-batch GD
  - BGD
  - SGD
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# BGD、SGD 与 mini-batch

> [!info] 定位
> 三种梯度下降的差别仅在"每步算梯度用多少样本"。这是 d2l 优化章(https://zh.d2l.ai/chapter_optimization/index.html)的核心概念,这里把命名 / 机制 / 权衡讲清。

## 一句话

三种方法的**核心公式完全一样**,只是"每次算梯度用多少样本"不同:

$$
\mathbfw \leftarrow \mathbfw - \eta \cdot \nabla L(\mathbfw; \text{某些样本})
$$

| 名字 | 每次算梯度用多少样本 | 每 epoch 步数(数据集大小 $N$) |
|:--|:--|:--|
| **BGD** (Batch) | 全部 $N$ 个 | 1 |
| **SGD**(纯,纯随机)| 1 个 | $N$ |
| **Mini-batch GD** | $B$ 个(典型 32 / 64 / 256) | $N/B$ |

## 命名约定

> [!warning] 现在说 "SGD" 通常指 mini-batch
> 严格意义的"纯 SGD"= 1 样本 1 步更新,**深度学习里几乎没人用**。
> 教科书和 PyTorch 文档里的 `optim.SGD` 默认是 **mini-batch SGD**。
> 真要"1 样本"会明确说 "pure SGD" / "online GD"。

## 直观代码

```python
# BGD:整批一次
for epoch in range(epochs):
    grad = compute_gradient(X_all, y_all)   # 慢但准
    w -= lr * grad

# 纯 SGD:逐样本
for epoch in range(epochs):
    for i in range(N):
        grad = compute_gradient(X[i], y[i]) # 极快但抖
        w -= lr * grad

# Mini-batch:折中(深度学习标配)
for epoch in range(epochs):
    for batch in dataloader:                # 每 B 个样本更新
        grad = compute_gradient(batch)
        w -= lr * grad
```

## 权衡对比

| | BGD | SGD(纯) | Mini-batch |
|:--|:--|:--|:--|
| 单步速度 | 慢(全量数据) | **极快**(1 样本) | 快($B$ 样本) |
| 单步稳定性 | **极稳**(确定性,方差 = 0) | 抖动最大 | 适中 |
| 内存 / 显存 | **极大**(要装全量) | **极小** | 适中 |
| 跳出局部极小 | 不行(收敛路径太干净) | **强**(噪声帮) | 中等 |
| 利用 GPU 并行 | 不行(顺序) | 不行 | **极强**(矩阵乘) |
| 大规模数据集 | **跑不动** | 能跑但慢 | **最佳折中** |

> ![[BGD-SGD-MiniBatch参数空间轨迹.jpg]]
>
> 三条轨迹画在同一个损失曲面上：更新公式完全相同，差别只在每次喂多少样本。

## 几点关键认识

### 1. batch 越大,梯度方差越小

$$
\text{Var}(\nabla L_{\text{batch}}) = \frac{\sigma^2}{B}
$$

- BGD:方差 = 0(每步梯度都是同一个确定值)
- mini-batch $B=1$:方差 = $\sigma^2$ 最大
- batch $B=256$:方差 = $\sigma^2 / 256$ 很小

**batch 越大,梯度越"准",收敛路径越稳**——但单步代价也高。32–256 是经验折中。

### 2. SGD 噪声的两面性

**好的方面**:噪声让梯度**不严格沿最陡下降方向**走,**能跳出浅层局部极小和鞍点**——这是 SGD 在深度网络里仍被广泛使用的重要原因。

**坏的方面**:噪声让收敛路径抖动,后期需要**衰减学习率**让收敛稳住。

### 3. linear scaling rule

实践中常用启发式:**batch size 翻 $n$ 倍,$\text{lr}$ 也按 $n$ 倍放大**(线性缩放)。前提是用 `.mean()` 归一化梯度,否则两个量同时变化互相抵消、难以调。

详见 [[SGD 与优化器#梯度归一化与学习率发散]]。

## d2l 章节对应

d2l 教材里以下两处有"梯度方差"和"对比"的相关讨论,可交叉参考:

- **d2l 优化章 *minibatch-sgd* 节**(https://zh.d2l.ai/chapter_optimization/minibatch-sgd.html):BGD 方差 = 0(最小),SGD 最大
- **d2l 优化章 *minibatch-sgd* 节(对比部分)**:SGD 噪声大,反而有助于跳出局部极小

## 一句话

**BGD** = 全量 1 步(Slow but steady);**SGD**(纯)= 1 样本 1 步(Noisy but cheap);**Mini-batch** = $B$ 样本 1 步(实际标配,折中又快又稳又能 GPU 并行)。

## 相关笔记

- **原理**:[[线性回归 解析解与最大似然]] — BGD 在的解析解场景外没法用,所以才需要迭代
- **工具**:[[SGD 与优化器]] — SGD 在 PyTorch 里的接口与 gradient scaling
- **机制**:[[梯度累加与 zero_grad]] — 为什么 `zero_grad` 必须在 `backward` 前
- **示例**:[[Softmax 回归与 MLE 推导]] — mini-batch SGD 实际训练 softmax 回归

## 参考

- d2l chapter_optimization/index.html
- Bottou, "Stochastic Gradient Descent Tricks"(2012)
- Goyal et al., "Accurate, Large Minibatch SGD"(2017) — 线性 scaling rule 的实证来源