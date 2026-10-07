---
tags:
  - 深度学习
  - softmax
  - 分类
  - 极大似然估计
  - 交叉熵
created: 2026-09-12
type: 知识点
aliases:
  - softmax regression
  - softmax 回归
  - MLE for classification
  - cross-entropy derivation
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# Softmax 回归与 MLE 推导

> [!info] 定位
> 把 d2l softmax-regression 章节的核心打通:**Softmax 把 logits 变概率 → MLE 在这些概率上选最像数据的参数 → 自然落到交叉熵**。
>
> 配套底层概念见 [[似然与最大似然估计]];softmax 本身的定义见 [[Logits、Softmax 与 argmax]]。

## 一句话定位

Softmax 回归 = "线性层 + Softmax"。**损失不是另选**,而是把 Softmax 输出当作概率分布后,用 MLE(最大似然估计)推出交叉熵。

## 1. Softmax 输出:logits → 概率

线性层先给未规范化分数 $\mathbf{o}$(logits),再做:

$$
\hat{y}_j = \frac{e^{o_j}}{\sum_k e^{o_k}}
$$

于是 $\hat y_j \ge 0$,$\sum_j \hat y_j = 1$。把 $\hat y_j$ 解释为条件概率:

$$
\hat{y}_j = P(y=j\mid \mathbf{x})
$$

举例:三类预测 $(0.1, 0.8, 0.1)$ → "鸡"的概率 0.8。**预测时仍可直接 `argmax o_j`**,因为 softmax 不改变大小次序(指数函数单调),见 [[Logits、Softmax 与 argmax]]。

## 2. 单样本似然 = 真实类概率

假设标签 one-hot,真实类是 $y^*$。**这次观测的似然 = 模型给真实类的概率**:

$$
P(\mathbf{y}\mid \mathbf{x}) \;=\; \prod_{j=1}^{q} \hat y_j^{y_j} \;=\; \hat y_{y^*}
$$

第二个等号成立是因为 one-hot 里 $y_j$ 只有真实类 $y^*$ 处为 1,其余为 0——这正是 one-hot 编码的妙处:把"挑出真实类那个数"自动写成向量内积。

直觉解释:模型虽对每个类都给了概率,现实只抽中了一个类。**抽中鸡的概率,就是鸡那一格**;不是先验规定"只许看正确类"。

## 3. 多样本独立 → 连乘

$n$ 个样本独立同分布,联合似然是各样本似然之积:

$$
P(\mathbf{Y}\mid \mathbf{X}) \;=\; \prod_{i=1}^{n} \hat y^{(i)}_{y^{*(i)}}
$$

一张图错得很离谱(真实类概率接近 0),整个乘积会被拉向 0——这就是"整批数据同时被模型解释得通"的含义。

> [!tip] 为什么连乘?为什么取对数?
> 连乘表达"独立事件同时发生"的概率。取对数后:
> - 连乘 → 连加,数值稳定(避免很多小数相乘下溢)
> - 不改变最大值位置(`log` 单调递增)
> - 配套深度学习"最小化"惯例,再加负号变负对数似然(NLL)

## 4. 负对数似然 → 交叉熵(求和塌缩)

把 one-hot 代回求和形式:

$$
l(\mathbf{y}, \hat{\mathbf{y}}) \;=\; -\sum_{j=1}^{q} y_j \log \hat y_j
$$

这就是**交叉熵**。在 one-hot 分类下,大部分 $y_j=0$:

$$
\underbrace{0 \cdot \log \hat y_{\text{猫}}}_{\text{被 0 乘掉}} + \underbrace{1 \cdot \log \hat y_{\text{鸡}}}_{\text{真实类}} + \underbrace{0 \cdot \log \hat y_{\text{狗}}}_{\text{被 0 乘掉}} \;=\; -\log \hat y_{\text{鸡}}
$$

**整段求和塌缩成 $-\log \hat y_{y^*}$**——和 softmax 回归的 MLE 目标完全等价。

### 数字例子

三类 (猫、鸡、狗),真实是鸡,标签 $\mathbf{y}=(0,1,0)$。

| $\hat{\mathbf{y}}$ | 损失计算 | 数值 |
|:--|:--|:--|
| $(0.1, 0.8, 0.1)$ | $-\log 0.8$ | ≈ 0.22 |
| $(0.7, 0.1, 0.2)$ | $-\log 0.1$ | ≈ 2.30 |

第二行:把 0.7 分给猫再高,对这个样本也没用——因为标签在鸡上是 1、猫上是 0。**训练只逼模型把真实类概率抬高**。

## 5. 干净的梯度

把 softmax 代回损失:

$$
l \;=\; \log\sum_k e^{o_k} \;-\; \sum_j y_j o_j
$$

对 logit $o_j$ 求导:

$$
\frac{\partial l}{\partial o_j} \;=\; \underbrace{\frac{e^{o_j}}{\sum_k e^{o_k}}}_{\hat y_j} \;-\; \underbrace{y_j}_{\text{真实 one-hot}} \;=\; \hat y_j - y_j
$$

**梯度就是"预测概率 - 真实 one-hot"**——非常干净的形式
- 预测完全对($\hat y = y$):梯度为 0,不再更新
- 预测错了某个类:梯度非零,推它去修正

这也是为什么 PyTorch 的 `nn.CrossEntropyLoss` 直接吃 logits,内部做 log-softmax + NLL——它直接告诉你"`F.linear(z, weight) - y_one_hot`"这条最短路径(数值更稳),见 [[交叉熵损失]]。

## 6. 与 MSE 的视角对照

| | 回归(MSE) | 分类(交叉熵) |
|:--|:--|:--|
| 模型输出 | 任意实数 $\hat y$ | 概率 $\hat y_j \ge 0$,$\sum=1$ |
| 噪声假设 | 高斯 $\mathcal{N}(0, \sigma^2)$ | 类别标签(隐含多项分布) |
| 损失 | $\sum(y-\hat y)^2$ | $-\sum y_j \log \hat y_j$ |
| 梯度 | $2(\hat y - y)$ | $\hat y - y$ |
| 同源 | 都是 MLE | 都是 MLE |

**两套损失本质同源——都是 MLE**,只是噪声假设不同:
- 高斯 → MSE(平方误差,见 [[似然与最大似然估计]])
- 多项 / 伯努利 → 交叉熵(对数似然)

## 7. 为什么这么设计"对数"和"负号"

数字例子最直观:正确类概率 $0.99 \to -\log 0.99 \approx 0.01$(几乎没错,小惩罚);$0.01 \to -\log 0.01 \approx 4.6$(大惩罚)。
- **取对数**:把 $(0, 1]$ 的概率压到 $[0, \infty)$,给极端错误(概率 → 0)一个**发散**的损失——模型不太敢把真实类的概率降到 0
- **加负号**:让训练变成"最小化"——配合梯度下降的标准方向

两个操作合起来,等价于"惩罚**信息量**:你让真实类概率变成 $\hat y$,传达一个真实事件所需的信息量是 $-\log \hat y$"(信息论视角,见 [[交叉熵与信息熵]])。

## 8. 训练/精度分开算

**训练**:用交叉熵(可微)算 loss,反向传播更新参数。
**评估**:用 accuracy / precision / recall,把预测和真实标签做硬比对。

两者**不能混**——argmax 几乎处处导数为 0,不能反向传播(见 [[Logits、Softmax 与 argmax#训练时不用 argmax]])。

## 相关笔记

- **理论**:[[似然与最大似然估计]] — 概率/似然/MLE 的完整推导;伯努利分布那条线直接接本页
- **定义**:[[Logits、Softmax 与 argmax]] — softmax 怎么把 logits 变概率,numerical stability,为什么训练输出 logits
- **工具**:[[交叉熵损失]] — `nn.CrossEntropyLoss` 内部 = `LogSoftmax + NLLLoss`,直接吃 logits
- **对照**:[[交叉熵与信息熵]] — 同一公式的信息论解读(香农熵、KL 散度)
- **类比**:[[线性回归 解析解与最大似然]] — 回归侧的 MLE → MSE 同源故事

- **本篇的概率视角**：[[../图像分类/贝叶斯分类器|贝叶斯分类器]] — 同一个后验 $P(y\mid\mathbf{x})$，贝叶斯用**训练集频次比**估，本篇用**可学习权重**

## 参考

- [d2l softmax-regression](https://zh.d2l.ai/chapter_linear-networks/softmax-regression.html)
- [PyTorch nn.CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [MLE for classification (Blog)](https://jramkiss.github.io/2022/01/03/softmax-regression/)