---
tags:
  - pytorch
  - autograd
  - 深度学习
created: 2026-08-31
type: 知识点
aliases:
  - 自动微分
  - automatic differentiation
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# Autograd 自动微分

> [!info] 定位
> 对应 PyTorch 官方教程 *Learn the Basics* 的 *Autograd* 章(https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)。回答一个问题：**模型参数的梯度是怎么来的？**

## 自动微分 ≠ 优化算法

容易混淆的两步（"令导数=0 找最小值"的理解不对）：

- **自动微分（autograd）**：自动、精确地计算"损失函数对每个权重的导数/梯度"
- **优化算法（梯度下降、Adam）**：用这些梯度去更新权重，让损失逐步变小

autograd 不负责找"导数等于 0"的权重，也不保证全局最小。它只告诉优化器：**当前每个参数往哪个方向微调，损失下降最快**。

一句话分清：**反向传播 = 利用自动微分和链式法则算梯度的过程；梯度下降/Adam = 使用梯度更新权重。**

## 训练流程

设模型参数为 $w$、损失为 $L(w)$：

1. **前向传播**：由输入和当前权重算出预测值和损失 $L(w)$
2. **反向传播 / 自动微分**：计算梯度 $\frac{\partial L}{\partial w}$
3. **优化器更新**（以梯度下降为例）：

$$
w \leftarrow w - \eta \frac{\partial L}{\partial w}
$$

其中 $\eta$ 是学习率。

4. 重复以上过程，直到损失足够低或达到训练轮数。

## 为什么不是"直接令导数为零"？

一元简单凸函数的极小点满足 $L'(w)=0$，可以直接解方程。但神经网络有百万~数十亿参数、损失高度非线性非凸，解 $\nabla L(w)=0$ 不可行。实际做法：每步算**当前位置的局部斜率**，向下走一小步，最终到达某个梯度接近 0 的点（可能是局部最小或鞍点），而非解析地解出最优权重。

## 极简例子

$L(w)=(w-3)^2$，$\frac{dL}{dw}=2(w-3)$：

- **自动微分**：当前 $w=1$ 时，算出梯度为 $-4$
- **优化器**：学习率 $\eta=0.1$，更新为 $w \leftarrow 1-0.1\times(-4)=1.4$
- 重复多次后 $w$ 逐渐接近 3；此时梯度接近 0，损失接近最小

## PyTorch 对应 API

```python
loss.backward()        # 自动微分：计算各参数梯度，存入 .grad
optimizer.step()       # 优化器：按梯度更新参数
optimizer.zero_grad()  # 清除旧梯度，避免累积
```

> [!warning] 梯度默认累积
> 梯度会累加（`+=`）在参数的 `.grad` 中，训练循环每步前要 `zero_grad()`——为什么累加、什么时候反而要利用累加，见 [[梯度累加与 zero_grad]]。

## 相关笔记

- **下游**：[[计算图与梯度跟踪]] — backward 是怎么沿计算图把梯度算出来的
- **下游**：[[梯度累加与 zero_grad]] — `.grad` 累加的数值例子、正确顺序与梯度累积技巧
- **前置**：[[交叉熵损失]] — loss 从哪来，它是 `backward()` 的起点
- **使用处**：[[Dataset 与 DataLoader]] — 训练循环里的 `zero_grad → backward → step` 三连
- **使用处**：[[nn.Module 与模型构建]] — 被更新的是模型里注册的参数
- **下游**：[[优化循环与训练闭环]] — 把三连放进完整 epoch 循环
- **下游**：[[反向传播机制]] — autograd 实现的算法：链式法则 + 计算图

## 参考

- [Autograd 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
