---
tags:
  - pytorch
  - autograd
  - 深度学习
created: 2026-09-01
type: 知识点
aliases:
  - 梯度累积
  - gradient accumulation
  - zero_grad
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# 梯度累加与 zero_grad

`loss.backward()` **只算梯度，不改权重**：它沿计算图用链式法则求 $\partial L/\partial w$，写进每个 `requires_grad=True` 参数的 `.grad`。本质是 `param.grad += dloss/dparam`——是**加**进去，不是覆盖。

## 三连分工

| 调用 | 干什么 |
| ---- | ------ |
| `backward()` | 算梯度，**累加**到 `.grad` |
| `step()` | 用 `.grad` 更新参数（规则见 [[SGD 与优化器]]） |
| `zero_grad()` | 清 `.grad`，避免和下一批混在一起 |

顺序必须是 `zero_grad → backward → step`。`zero_grad` 不能夹在 `backward` 和 `step` 中间，否则刚算完的梯度被清掉，`step` 等于没更新。教程写成 `backward → step → zero_grad` 也能跑，本质是"下一次 backward 之前清掉"；更常见的是循环开头先 `zero_grad()`。

## 为什么默认累加？（数值例子）

这是有意设计，不是疏忽。同一个权重 $w=2$，两笔数据都用它（$L=(wx-y)^2$，$\partial L/\partial w = 2(wx-y)x$）：

- 样本 1：$x=3, y=10$，预测 $2\times3=6$，$\text{loss}_1=(6-10)^2=16$，梯度 $= 2(6-10)\times3 = -24$
- 样本 2：$x=1, y=4$，预测 $2$，$\text{loss}_2=4$，梯度 $= 2(2-4)\times1 = -4$

- 若**覆盖**：`w.grad = -4` —— 等于只学了第 2 笔
- 若**累加**：`w.grad = -24 + (-4) = -28`

总损失 $L = L_1 + L_2$ 一次求导，梯度正好是 $-28$。**累加才是对的。**

累加真正有用的场景：

1. **RNN / 同一权重用多次**：同一个 $W$ 在多个时间步各用一次，总梯度必须是各步贡献之和
2. **梯度累积（显存不够，假装大 batch）**：256 张装不下 → 每次 64 张 `backward` 四次，中间不 `step` 也不 `zero_grad`，第五次才 `step`——数学上接近 256 的大 batch

> ![[梯度累加与计算图.jpg]]
>
> 左：两笔 loss 如何汇入同一个 `w`；右：`.grad` 两次 `backward` 如何累加。**累加之所以是对的，看左图就够了。**

## 正常训练：每批清一次

教程闭环是：一批数据 → **平均 loss** → **一次** backward → **一次** step → 下一批前 zero_grad。权重是**每个 batch 更新一次**，不是很多批攒着一起更新。

> [!warning] 别混淆两种"加"
> - **批内平均**：`CrossEntropyLoss` 默认 `reduction='mean'`，在 **loss 函数内部**把 64 张图的 loss 先算出来再**平均**成一个标量，然后只对这一个标量 `backward()` 一次。"叠加"发生在 loss 函数里，不是多次 backward 把 `.grad` 加起来
> - **跨 batch 累加**：`.grad` 的 `+=` 是 PyTorch 底层规则；正常训练每批都要 `zero_grad()`，否则等于用"上一批 + 这一批"的梯度更新——那是错的（除非你故意做梯度累积）

一句话：**加，是因为同一套参数可以对多份 loss；清，是因为下一 batch 通常不该再算上一批。**

## 梯度累积：用多次小 batch 假装大 batch

把大 batch 拆成 K 个 micro-batches，每批 forward+backward 但**不 step**，让 `.grad` 累加 K 次后再统一 step + zero_grad。数学上接近一个大 batch，但显存只需装得下一个小 batch——尤其在大模型训练里很常用。

**关键：要让更新幅度等价，必须把每个 micro-batch 的 loss 除以 K：**

```python
accum_steps = 4
for i, (x, y) in enumerate(loader):
    loss = model(x)
    loss = loss / accum_steps   # 关键：缩放
    loss.backward()             # 累加到 .grad

    if (i + 1) % accum_steps == 0:
        optimizer.step()        # 用累加后的平均梯度更新
        optimizer.zero_grad()
```

数学验证：

$$
L = \frac{1}{K}\sum_{k=1}^K L_k \;\Rightarrow\; \frac{\partial L}{\partial\theta} = \frac{1}{K}\sum_k\frac{\partial L_k}{\partial\theta}
$$

> [!warning] 不缩放直接累加 = 放大学习率
> 若不除以 K 直接累加 K 次再更新，相当于用了比大 batch 大 K 倍的梯度，**学习率实际上被放大 K 倍**，训练动态会改变（可能不稳定或发散）。

总结：

| 术语 | 含义 |
| ---- | ---- |
| **梯度累加** | PyTorch 默认行为，`.grad` 是累加器 |
| **梯度累积**（gradient accumulation） | 利用累加特性，跨多个 micro-batch 累积梯度再一次性更新 |

## `.grad` 和计算图是两套东西

|  | `.grad`（梯度） | 计算图 / 中间值 |
| :-- | :-- | :-- |
| 是什么 | 每个参数上的 $\partial L/\partial w$ | 这次 forward 记下来的运算路径 |
| 谁写 | `backward()` **往上加** | forward 时自动建 |
| 谁清 | `zero_grad()` | 一次 `backward()` 用完就自动释放 |
| `no_grad` | **不管** `.grad`，也不会清掉它 | 这段里根本不建图 |

`with torch.no_grad():` = 这段前向**不算梯度、不建图**，省显存、加快推理；里面的 `.grad` **原样保留**，不会被清。清梯度只能用 `zero_grad()`。机制详见 [[计算图与梯度跟踪]]。

## 相关笔记

- **上游**：[[Autograd 自动微分]] — 累加规则属于 autograd 的设计
- **使用处**：[[优化循环与训练闭环]] — 三连在 train_loop 里的标准位置
- **相关**：[[交叉熵损失]] — 批内 loss 是"平均"不是"累加"（`reduction='mean'`）
- **相关**：[[计算图与梯度跟踪]] — `no_grad` 与建图的关系
- **相关**：[[SGD 与优化器]] — `step()` 拿清零后的梯度做什么

## 参考

- [torch.optim.Optimizer.zero_grad 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.optim.Optimizer.zero_grad.html)
- [PyTorch 论坛：why do we need to call zero_grad](https://discuss.pytorch.org/t/why-do-we-need-to-set-the-gradients-manually-to-zero-in-pytorch/4903)
