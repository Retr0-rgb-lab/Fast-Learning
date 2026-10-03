---
tags:
  - 深度学习
  - 激活函数
  - 神经网络
created: 2026-08-31
type: 知识点
aliases:
  - Rectified Linear Unit
  - 整流线性单元
---

# ReLU

ReLU（Rectified Linear Unit）是最常用的隐藏层激活函数：**正数原样通过，负数变成 0**。作用是引入非线性——见 [[激活函数]]。

## 公式

$$
\operatorname{ReLU}(x) = \max(0, x) =
\begin{cases}
x & x > 0 \\
0 & x \le 0
\end{cases}
$$

例子：`[-2.0, 0.5, 3.1]` → `[0.0, 0.5, 3.1]`。

没有可学习参数，逐元素处理，形状不变：`[batch, 512]` 进，`[batch, 512]` 出。

## 为什么正半轴是直线，它却算非线性？

观察对了一半：$x>0$ 段确实是 $y=x$。但真正的线性要求对**所有**输入满足：

$$
f(ax+by) = a f(x) + b f(y)
$$

反例：$\operatorname{ReLU}(-5+1)=\operatorname{ReLU}(-4)=0$，而 $\operatorname{ReLU}(-5)+\operatorname{ReLU}(1)=0+1=1$，两边不等。整条函数在 $x=0$ 有折角，术语叫**分段线性**，整体是非线性的。

## 为什么要"掐掉"负数？

不是为了扔掉信息，而是故意在 0 处折断，换来两件事：

1. **制造折点才有非线性**：若负数也原样保留，ReLU 就退化成 $y=x$，两层 Linear 又能合成一层。
2. **稀疏激活**：512 维里很多通道表示"有没有某类特征"，分数为负 ≈ 特征没出现，置 0 等于这次不算它——像开关："靴子"通道亮着、"包"通道关掉，只传有用的正激活。

负方向信息并不丢：下一层权重可正可负，需要"负方向"时把正激活乘上负权重即可。

## 反向传播时的表现

导数极简：

- $x > 0$：梯度为 1，原样往回传
- $x \le 0$：梯度为 0，这条路暂时关掉

正区间梯度不衰减，比 [[Sigmoid]]/Tanh 更不容易**梯度消失**，训练更快（只需比较和置零）。

## 副作用：死 ReLU

若某个神经元对**所有**样本输入都是负的，梯度恒为 0，就"死掉"学不动了。这是副作用不是设计目标，可用 **Leaky ReLU**（负数乘一个很小的斜率）缓解；小网络里普通 ReLU 通常够用。

## 使用位置

```text
Linear(784→512) → ReLU → Linear(512→512) → ReLU → Linear(512→10)
```

只在隐藏层用；**最后一层输出 logits 不加 ReLU**，让类别分数能正能负。

## 相关笔记

- **上游**：[[激活函数]] — 为什么需要它、放在哪
- **使用处**：[[nn.Module 与模型构建]] — `linear_relu_stack` 中的两个 `nn.ReLU()`
- **对比**：[[Sigmoid]] — 正区间梯度为 1，缓解了 Sigmoid 的梯度消失问题
- **相关**：[[Logits、Softmax 与 argmax]] — 为什么输出层不加 ReLU（logits 要能正能负）

## 参考

- [Rectified Linear Unit (Wikipedia)](https://en.wikipedia.org/wiki/Rectified_linear_unit)
- [Build the Neural Network 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
