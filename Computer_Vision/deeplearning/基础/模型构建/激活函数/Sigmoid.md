---
tags:
  - 深度学习
  - 激活函数
  - 二分类
created: 2026-08-31
type: 知识点
aliases:
  - 逻辑函数
  - Logistic Function
---

# Sigmoid

Sigmoid（逻辑函数）把任意实数压缩到 $(0,1)$ 之间的 S 形函数，输出可以方便地解释为"属于正类的概率"。在逻辑回归和**二分类**输出层中尤其常见。

## 定义

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

| 输入 $x$ | 输出 $\sigma(x)$ | 含义 |
| -------: | ---------------: | :--- |
| $-5$ | ≈ 0.0067 | 非常接近 0 |
| $-1$ | ≈ 0.2689 | 倾向 0 |
| $0$ | 0.5 | 中性分界点 |
| $1$ | ≈ 0.7311 | 倾向 1 |
| $5$ | ≈ 0.9933 | 非常接近 1 |

$x \to +\infty$ 时趋近 1，$x \to -\infty$ 时趋近 0，但理论上不会真正取到 0 或 1。

## 核心性质

- **输出范围固定** $(0,1)$，适合表示概率
- **单调递增**、**平滑处处可导**，适合梯度下降和反向传播
- **中心点明确**：$\sigma(0)=0.5$
- **对称**：$\sigma(-x) = 1 - \sigma(x)$
- **导数简洁**（反向传播高效）：

$$
\sigma'(x) = \sigma(x)\bigl(1-\sigma(x)\bigr)
$$

## 为什么用于二分类

先算线性得分（这个得分就是一条 logit，见 [[Logits、Softmax 与 argmax]]）：

$$
z = w^\top x + b \quad\Rightarrow\quad p = \sigma(z) = P(y=1 \mid x)
$$

例：风控模型输出 $z=2$，则 $\sigma(2)\approx 0.881$，即模型估计正类概率约 88.1%。之后按**业务阈值**决策：常见 0.5，但欺诈检测、风险预警中会按误报/漏报成本选 0.7、0.9 等，不要机械固定 0.5。

## 优缺点

| 优点 | 缺点 |
| :-- | :-- |
| 输出在 $(0,1)$，概率含义直观 | 输入绝对值大时**饱和**，梯度接近 0 |
| 平滑、处处可导 | 深层网络易造成**梯度消失** |
| 导数形式简单 | 输出不以 0 为中心，隐藏层更新效率差 |
| 二分类输出层经典选择 | 指数计算比 ReLU 贵 |

**梯度消失**是关键问题：多层反向传播时许多小梯度连乘变得极小，前面层学不动。所以现代深度网络的隐藏层多用 [[ReLU]]、Leaky ReLU、GELU、SiLU；Sigmoid 仍是二分类输出层的经典选择——见 [[激活函数]] 的对比表。

## 实践建议

- 用在**二分类输出层**（是/否、违约/不违约、点击/不点击）
- **不要默认用在深层隐藏层**，除非特意需要门控机制
- 搭配二元交叉熵时，直接用 **`BCEWithLogitsLoss`**（logits + sigmoid + BCE 的稳定 fused 实现，原理见 [[交叉熵损失]]），避免先显式算 Sigmoid 带来的数值不稳定
- 输出形式上是概率，但**是否校准良好**要用验证集、校准曲线、Brier score 检查

## 相关笔记

- **上游**：[[激活函数]] — 与 ReLU 的定位对比
- **输入来源**：[[Logits、Softmax 与 argmax]] — Sigmoid 吃的那条线性得分 z 就是一条 logit；多分类的对应物是 Softmax
- **下游**：[[交叉熵损失]] — $\hat{y}=\sigma(z)$ 得到的概率送进 BCE 公式
- **对比**：[[ReLU]] — 正区间梯度恒 1 vs Sigmoid 两端饱和
- **场景参照**：[[nn.Module 与模型构建]] — 多分类网络的最后一层输出 logits 而不是 sigmoid/概率

## 参考

- [Google ML Crash Course: Sigmoid](https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function)
- [S 型函数 (Wikipedia)](https://zh.wikipedia.org/wiki/S型函数)
