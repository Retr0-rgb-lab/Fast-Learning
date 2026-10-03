---
tags:
  - 深度学习
  - PyTorch
  - 训练循环
  - 调参
  - 工程细节
created: 2026-09-14
type: 知识点
aliases:
  - training loop gotchas
  - PyTorch tips
  - zero_grad placement
  - Accumulator pattern
  - in-place mutation
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# PyTorch 训练循环关键细节

> [!info] 定位
> 训练循环里反复踩过的工程陷阱,一次性收齐,做训练循环时**对照检查**。
> 与 [[梯度累加与 zero_grad]]、[[SGD 与优化器]] 互为补充——这里讲"该写什么",那里讲"为什么这样写"。

## 1. `zero_grad → backward → step` 三步顺序

```python
optimizer.zero_grad()       # 先清掉上一轮残留
loss = loss_fn(y_hat, y)    # 算 loss
loss.backward()             # 反向传播算梯度
optimizer.step()            # 用梯度更新参数
```

> [!warning] 三步顺序不能换
> - `zero_grad` 必须在 `backward` **之前**,否则 `.grad` 累加 → 用了**几轮梯度之和**做更新
> - `step` 在 `backward` **之后**才有梯度可用
> - **不要**把 `zero_grad` 放到 `step` 之后(初学者常见,代码能跑但非常规)

## 2. `.grad` 默认累加

```python
w.grad.zero_() # ← 显式清零
```

PyTorch 设计上 `backward()` 把新梯度**加到**现有 `.grad` 上,不是覆盖。

**为什么**:支持**梯度累积**(显存不够时,多个小 batch 累加再 step)。但日常训练每 batch 算完要 step,所以**每步前要清**——`optimizer.zero_grad()` 就是干这个。

## 3. `loss.backward()` 只能对标量

```python
loss = nn.CrossEntropyLoss(reduction='none')   # 输出 (B,)
l = loss(y_hat, y)
l.backward()                                  # RuntimeError!
```

报错:

```
RuntimeError: grad can be implicitly created only for scalar outputs
```

> [!tip] 一句话
> `.backward()` **只能吃标量**。`reduction='none'` 返回 `(B,)` 不行——必须 `.mean()` 或 `.sum()` 收成标量才能 backward。

## 4. `len(y)` 不是 batch_size,`y.numel()` 才是

```python
for X, y in dataloader:
    batch_size = y.numel()      # ✓ 真实批大小(可能是 256,也可能是 16)
    # len(y) # 也可以,只要 y 是 1D 整数标签就行
```

> [!warning] test_loop 的经典 bug
> `len(y)` 是**最后一个 batch 的尺寸**(因为循环结束时 y 指向最后那个 batch)。**不要**用 `len(y)` 算"总样本数"——必须**累加** `y.numel()`。

见 [[交叉熵损失]]。

## 5. test_loop 的 loss 累加要加权

```python
# ✗ 错:loss_fn 返回的是 batch 平均,直接加不换算成总 loss
loss_sum += loss_fn(preds, y).item()          # 这其实是"每 batch 的均值"之和
avg_loss = loss_sum / total_samples           # 错得离谱

# ✓ 对:乘 batch_size 还原成 batch 总 loss
loss_sum += loss_fn(preds, y).item() * batch_size
avg_loss = loss_sum / total_samples           # 正确:全量平均
```

**为什么**:`loss_fn` 默认 `reduction='mean'`,返回每 batch 的**均值**。要看全量平均,必须 `Σ 均值 × batch_size / Σ batch_size`。

## 6. 不要原地改输入

```python
def cross_entropy(logits, y):
    logits -= logits.max()        # ✗ 原地改 logits,下次再用同一个 logits 进来值已变
    return ...

logits = torch.tensor([[2.0, 1.0, 0.1]])  # 3 个类的 logits
l1 = cross_entropy(logits, torch.tensor([0]))
l2 = cross_entropy(logits, torch.tensor([0]))   # l2 ≠ l1
```

```python
def cross_entropy(logits, y):
    logits = logits - logits.max()  # ✓ 重新绑定到局部变量,不动外部
    return ...
```

**PyTorch 习惯**:函数对参数的修改应是**纯函数**(输入定输出定,不副作用)。

## 7. `tensor.max(dim=...)` 返回具名元组

```python
X = torch.randn(3, 4)
m = X.max(dim=1, keepdim=True)
print(m)  # torch.return_types.max(values=tensor([...]), indices=tensor([...]))
```

要拿到最大值,必须 `.values`:

```python
X = X - X.max(dim=-1, keepdim=True).values     # ✓
X = X - X.max(dim=-1, keepdim=True)            # ✗ TypeError
```

或者解包:

```python
vals, idxs = X.max(dim=-1, keepdim=True)
```

**常见陷阱**:`max`、`min`、`sort`、`topk`、`mode` 都返回 `(values, indices)` 具名元组;`argmax` 只返回 `indices`。

## 8. `argmax(dim=...)` 的形状

```python
preds = torch.randn(32, 10)
preds.argmax(dim=1)     # 形状 (32,),值是 0–9 的整数
preds.argmax(dim=0)     # 形状 (10,),值是 0–31 的整数
```

- `argmax(dim=k)`:**沿第 k 维**求 argmax,**那一维被消掉**(默认),其他维保留
- 与 `max(dim=k)` 区别:`max` 还返回 values,`argmax` 只返回 indices
- 与 `softmax(dim=k)` 区别:softmax 保留全部维,argmax 沿求轴消维

## 9. `.item()` 把 0 维张量转成 Python 数

```python
loss = torch.tensor(0.5)        # 0-dim tensor
n = loss.item()                 # Python float 0.5
loss_np = loss.numpy()          # NumPy 0-dim array
```

**什么时候用 `.item()`**:
- 打印日志时(否则会显示显示 `tensor(0.5)`)
- 累加到普通 Python 变量(避免 autograd 引用)
- 写文件 / 调非 PyTorch 函数时

**陷阱**:`loss.item()` **会阻断梯度图**——只能用于**已经 detach 的** loss 用于日志,不能用于还在传播的 loss。

## 10. `with torch.no_grad():` 在不需要梯度的地方

```python
metric.add(l.sum().item(), ...)   # 累加纯数字,不建图
with torch.no_grad():
    preds = net(X)               # 评估时不需要梯度
```

不写也能跑——只是浪费内存、可能让图变长。**判断准则**:这段代码的结果**不参与 `.backward()`**,就 `no_grad`。

## 11. `reduction='mean'` vs `'sum'` vs `'none'`

| | 输出形状 | 梯度"尺度" | 何时用 |
|:--|:--|:--|:--|
| `'mean'` | `()` | 每样本平均 | **默认,标准训练** |
| `'sum'` | `()` | 整 batch 总和 | `lr` 配合调整 |
| `'none'` | `(B,)` | per-sample | 高级用法:per-sample 加权、累加梯度 |

**默认 `mean`** 是 PyTorch 的约定——loss 量级、lr 调节都基于此。

## 一句话总结:训练循环 checklist

- [ ] `zero_grad` 在 `backward` 前
- [ ] `loss.backward()` 只能对标量
- [ ] `loss_fn` 默认 `reduction='mean'`,输出标量
- [ ] test_loop 用 `y.numel()` 累加样本数,不用 `len(y)`
- [ ] test_loop 累加 `loss.item() * batch_size`,不是直接 `loss.item()`
- [ ] 函数不要原地改输入
- [ ] `tensor.max(dim=...)` 后面要 `.values` 或解包
- [ ] 累加/打印用 `.item()`
- [ ] 评估用 `with torch.no_grad():`
- [ ] 不写 `.backward()` 在 `(N,)` 形状的 loss 上

## 相关笔记

- **机制**:[[梯度累加与 zero_grad]]、[[计算图与梯度跟踪]]
- **工具**:[[SGD 与优化器]]、[[优化循环与训练闭环]]
- **公式**:[[线性回归 解析解与最大似然]]、[[Softmax 回归与 MLE 推导]]
- **同伴**:[[BGD、SGD 与 mini-batch]]