---
tags:
  - pytorch
  - optimization
  - SGD
  - 深度学习
created: 2026-09-01
type: 知识点
aliases:
  - 随机梯度下降
  - Stochastic Gradient Descent
  - optimizer
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# SGD 与优化器

**SGD = Stochastic Gradient Descent（随机梯度下降）**：用当前这批数据的梯度，按学习率把权重往"损失变小"的方向推一步：

$$
w \leftarrow w - \eta \cdot \nabla L(w)
$$

$\eta$ 是 learning rate。`optimizer.step()` 做的就是这件事。

## "随机"指什么

理论上：每次只用**一部分**数据估梯度，不是拿全集算一遍再更新。

| 方式 | 每次更新用 |
| ---- | ---------- |
| 批量梯度下降 | 整个数据集（太慢） |
| 经典 SGD | 1 条样本 |
| **mini-batch SGD** | 一个 batch（教程这种，现在口头都叫 SGD） |

「随机」来自 **DataLoader 打乱、按 batch 取样**，不是 `torch.optim.SGD` 自己在掷骰子。

```python
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
```

每个 batch `backward` 之后，`step()` 用这一批的平均损失梯度更新一次参数。

## 换优化器 = 只换 step 的规则

Adam 等是另一套更新规则（例如给每个参数自适应步长）；训练闭环 forward → loss → backward → step **不变**，只换 `step()` 怎么改权重。对照实验里 `SGD vs Adam` 就是换这一行。

## 动量 (momentum)

```python
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
```

`momentum=0.9` 在 SGD 中引入物理"惯性"：**保留 90% 之前的前进方向**，用于

- 加速收敛
- 减少震荡
- 帮助跨越 loss landscape 的小坑

直观：原本只走"梯度反方向"，加动量后还带"上一步方向"的惯性。常见于图像分类等任务的标准 CIFAR-10 模板，见 [[CNN 图像分类模型结构]]。

## 梯度归一化与学习率发散

手动实现 SGD 时最容易踩的不是公式，而是**梯度是否归一化**——直接关系到 `lr` 该取多大量级。

### 批梯度的两种口径

$$
\underbrace{\sum_{i=1}^{n}(y^{(i)}-\hat{y}^{(i)})^2}_{\text{求和（未归一化）}}
\qquad
\text{vs}
\qquad
\underbrace{\frac{1}{n}\sum_{i=1}^{n}(y^{(i)}-\hat{y}^{(i)})^2}_{\text{均值（归一化）}}
$$

两者**最优解位置相同**（常数不影响 argmin），但**梯度幅差 n 倍**——所以配的学习率也要差 n 倍：

- **loss 用 `.sum()`**：梯度量级 ~ $n$ 倍 → `lr` 要相应除以 $n$
- **loss 用 `.mean()`**：梯度与 batch 大小无关 → `lr` 与 batch size 解耦，更稳

`nn.MSELoss(reduction='mean')` / `reduction='sum'` 默认就是 `.mean()`。手写练习时一定要用 `.mean()`。

### 手动梯度 + `lr=0.01` 为何发散到 NaN

实例（`y = 2x + 1 + ε`，x ∈ [0, 10]，噪声 σ=0.5）：

| 量 | 量级 |
| :-- | :-- |
| 单样本残差 | $\lvert y-\hat{y}\rvert \le 20$ |
| 单样本梯度 `error × x` | $\le 200$ |
| 单步权重更新 `lr × grad` | $0.01 \times 200 = 2$ |

初始 `w=0` 时一步就会被甩到 `w=-2`；几轮后 `ŷ = 50x` 之类，`ŷ²` 直接溢出 → 后续所有运算 NaN。

**修复路径**（任选）：

1. 改用 `.mean()` 算梯度，量级缩到 `error·x / n ≈ 1`，`lr=0.01` 稳
2. 用向量化 **BGD**（无内层 for 循环）+ `.mean()`，单步只更新一次
3. 大残差任务里进一步降 `lr`，或加**梯度裁剪**：`grad.clamp_(-1, 1)`

> [!warning] 一句话诊断
> 训练打印 loss 一开始就 NaN，几乎一定是**梯度没归一化 + lr 没配合**；不是公式错。

### SGD 里"学习率除以 batch size"

实践中常用启发式：**batch size 翻 n 倍，`lr` 也按 n 倍放大**——线性缩放规则（linear scaling rule）。前提是用了 `.mean()` 把梯度归一化；否则两个量同时变化互相抵消，难调。

## 下山比喻的正确画法

把训练想成"下山找山谷最低点"时，容易画错坐标系：

- ❌ 以 $X$、$y$ 为平面坐标——它们是**已知条件**（这一批数据），不是要优化的变量
- ✅ 地面两轴应是**权重** $w_1, w_2$（真实网络是上亿维的"超山"），高度是 loss
- $X, y$ 决定山长什么样：换一批数据，坡度会变一点（所以叫**随机**梯度下降），但走的坐标始终是 $w$
- SGD 每步只看当前位置的坡度（梯度），沿最陡下山方向走一小步（学习率），最终到达某个梯度接近 0 的点（可能是局部最小或鞍点）

准确一句话：**神经网络每个参数都是未知数，训练在超高维参数空间里用梯度找让平均损失变小的点；$X, y$ 是用来量这座山的数据，不是平面坐标。**

## 相关笔记

- **上游**：[[优化循环与训练闭环]] — `step()` 在闭环里的位置
- **前置**：[[Autograd 自动微分]] — `step()` 用的梯度从哪来
- **相关**：[[梯度累加与 zero_grad]] — 更新前为什么要清梯度
- **相关**：[[交叉熵损失]] — 被最小化的目标

## 参考

- [torch.optim.SGD 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.optim.SGD.html)
- [Stochastic gradient descent (Wikipedia)](https://en.wikipedia.org/wiki/Stochastic_gradient_descent)
