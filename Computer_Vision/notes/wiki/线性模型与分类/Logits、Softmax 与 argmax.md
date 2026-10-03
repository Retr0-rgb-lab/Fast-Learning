---
tags:
  - 深度学习
  - 分类
  - pytorch
created: 2026-08-31
type: 知识点
aliases:
  - logits
  - softmax
  - argmax
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# Logits、Softmax 与 argmax

分类网络从"输出 10 个数"到"给出预测类别"的三件套。

## Logits：原始分类分数

网络最后一层 `Linear(512, 10)` 直接输出的 10 个数就是 **logits**：范围是任意实数，可正可负、很大很小都行，加起来不等于 1。

它们表示模型对各类别的**相对倾向**——分数越高越倾向该类，但不能当概率读：

```text
logits = [2.0, 1.0, 0.1]
只能说：第 0 类最强、第 1 类其次、第 2 类最弱；不能说"第 0 类概率是 2"。
```

## Softmax：分数 → 概率分布

$$
\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}
$$

两步：① 对每个 logit 取指数（负数变正、大数被放大）；② 除以总和归一化，让全部加起来等于 1。

手算 `[2.0, 1.0, 0.1]`：

$$
e^{2.0}\approx 7.39,\quad e^{1.0}\approx 2.72,\quad e^{0.1}\approx 1.11,\quad \text{总和}\approx 11.22
$$

```text
概率 ≈ [0.66, 0.24, 0.10]
含义：约 66% 是第 0 类，24% 第 1 类，10% 第 2 类。
```

## 为什么训练时输出 logits，不直接输出概率？

训练用 `nn.CrossEntropyLoss`（原理见 [[交叉熵损失]]），它内部已做 `log_softmax`，模型应输出**未归一化的 logits**，`forward` 里**不要再套一层 Softmax**：

```python
logits = model(x)                        # [batch, 10] 原始分数
loss = nn.CrossEntropyLoss()(logits, y)  # 训练：直接吃 logits

probs = torch.softmax(logits, dim=1)     # 推理：才转成概率
pred = probs.argmax(dim=1)               # 或直接 logits.argmax(dim=1)
```

一句话：**神经网络原始输出是 logits（相对分数）；Softmax 只是把分数翻译成"各类概率加起来为 1"。**（二分类的对应物是 [[Sigmoid]]：一条 logit → 一个正类概率。）

## argmax：挑出预测类别

**argmax = argument of the maximum**：不返回最大值本身，而返回**最大值所在的下标**。

```python
logits = [1.2, -0.4, 3.8, 0.1, ...]   # 长度 10，下标 0~9
pred = logits.argmax()                 # 2 → 预测为第 2 类
```

一批图时形状是 `[batch, 10]`，**必须指定 `dim=1`**（每行/每张图各自找最大值的列号）：

```python
pred = logits.argmax(dim=1)   # 形状 [batch]
```

不写 `dim` 会在整个张量里只找一个全局最大值，那就错了。

### 与 Softmax 的关系

Softmax 只改数值、**不改大小顺序**（指数函数单调），所以两种写法预测类别完全一样：

```python
logits.argmax(dim=1) == torch.softmax(logits, dim=1).argmax(dim=1)
```

只想知道"是哪一类"，直接对 logits 做 argmax；想看"有多确信"才需要 Softmax。

### 训练时不用 argmax

argmax 像硬开关，几乎处处导数为 0，**不能反向传播**。训练用 `CrossEntropyLoss` 吃 logits，argmax 只用于推理和算准确率（把连续分数变成离散标签再和真实标签比较）。

## 手写 Softmax 的两个坑

自己实现 `softmax(x)` 时，**几乎一定会**遇到这两个问题，无论你多仔细。

### 坑 1：数值上溢

Softmax 公式 $\frac{e^{z_i}}{\sum_j e^{z_j}}$，如果某个 $z_i$ 很大（如 1000），`torch.exp(1000)` 直接溢出成 `inf`，最终输出 NaN。直观修复——**先减去最大值**，数学上等价（分子分母同乘 $e^{-\max}$），但所有指数项变成 $\le 0$，`exp` 永远安全：

```python
def softmax(x):
    x = x - x.max(dim=-1, keepdim=True).values   # 平移，最大变 0
    x = torch.exp(x)
    return x / x.sum(dim=-1, keepdim=True)
```

> 关键点：`keepdim=True` 保住维度为 `(..., 1)`，后面 `sum` 与除法能沿最后一维正确广播；否则 `(N,)` 减 `(N,)` 会触发奇怪的广播。

> 不写这层修复也能跑——只要你的 logits 都在 [-50, 50] 这种安全区间。一旦输入可能很大（语言模型最后一层、reward model 之类），漏了它就 NaN。

### 坑 2：忘了 batch 维度

> [!warning] 二维输入必须沿 `dim=-1` 求和
> 一个向量时 `.sum()` 不带参数没事；一批 `(N, C)` 的 logits，必须沿最后一维归一化，否则会跨样本求和。

```python
def softmax(x):                       # 错：只对 1 维向量成立
    total = x.sum()
    return x / total

def softmax(x, dim=-1):               # 对：批维与单维都成立
    x = x - x.max(dim=dim, keepdim=True).values
    return torch.exp(x) / torch.exp(x).sum(dim=dim, keepdim=True)
```

PyTorch 自带 `torch.softmax(x, dim=-1)` 已经做了这两件事；手写练习是为了理解不是为了替代。

## log_softmax：把分式拆成减法的稳定性技巧

> [!tip] 一句话
> `log(softmax(x)) = x − logsumexp(x)` —— **直接代数化简**,不走"概率→log 概率"那条容易下溢的路。

### 为什么这么拆

朴素写法分两步:

```python
probs = softmax(logits)              # ① 先归一化,得到 (0, 1) 的小数
loss = -torch.log(probs[range(N), y]) # ② 再 log——若真实类概率 ≈ 0,log(0) = -inf,炸
```

**关键风险**:softmax 输出有时会因为某个极端负的 logit 让 `exp` 归零,真实类概率**恰好是 0**,log 拿不到值。

**代数化简**:

$$
\log\frac{e^{z_i}}{\sum_j e^{z_j}} \;=\; \log e^{z_i} - \log\sum_j e^{z_j} \;=\; z_i - \log\sum_j e^{z_j}
$$

右式从一开始就是 `z_i` 减 `log(求和)`,**中间不出现"接近 0 的小概率"**。

### 完整稳版 log_softmax

```python
def log_softmax(X):
    X = X - X.max(dim=-1, keepdim=True).values       # 平移,exp 输入 ≤ 0
    return X - X.exp().sum(dim=-1, keepdim=True).log() # 拆成减法
```

两个稳定性补丁**一起用**:
1. **减 max**:exp 输入 ≤ 0,输出 ≤ 1,**不会上溢**
2. **代数化简**:log 直接走 logsumexp,**不会下溢**

### 几个名称的精确区分

| 量 | 公式 | 数值符号 |
|:--|:--|:--|
| `log_softmax(z_i)` | $z_i - \log\sum e^{z_j}$ | 负数(log 概率) |
| `cross_entropy / NLL(z_i)` | $-z_i + \log\sum e^{z_j}$ | 正数(loss) |
| `softmax(z_i)` | $e^{z_i}/\sum e^{z_j}$ | (0, 1) |

> [!warning] 符号差一个负号
> 自定义函数时容易写反:返回 `X - log(sum)` 才是 log_softmax;返回 `-X + log(sum)` 是 NLL / cross_entropy。看名字要和返回值的符号对得上。

### PyTorch 的对应

```python
F.log_softmax(logits, dim=-1)              # 数值稳的 log_softmax
F.cross_entropy(logits, y)                 # 内部 = -log_softmax + 挑真实类,直接吃 logits
nn.CrossEntropyLoss(reduction='mean')(logits, y)  # 默认 mean,返回标量才能 backward
```

`nn.CrossEntropyLoss(reduction='none')` 会返回 `(N,)` 的 per-sample loss,**`backward()` 会炸**——只能求 `.mean()` 或 `.sum()` 之后才能反向,见 [[交叉熵损失]]。

## argmax 何时不是最优解

`argmax(P(y=健康), P(y=癌症))` 选概率更大的那个作为预测——**只在"每类错一次代价相同"时最优**。代价不对称时不是。

### 经典反例:癌症筛查

1000 人体检,5 人真患癌(0.5%)。模型对每个人输出 `P(癌症)`:

- 真患者:P(癌症) ≈ 0.3(模型不太确定)
- 健康人:P(癌症) ≈ 0.05(模型很放心)

**argmax 对每个人独立选 max**:
- 那 5 个人:`max(0.3, 0.7) = 0.7` → 预测**健康** ❌ 漏诊
- 995 健康人:`max(0.05, 0.95) = 0.95` → 预测健康 ✓

准确率 99.5%,**但 5 个真患者一个都没抓到**——argmax 在医疗里是灾难。

> [!warning] argmax 不"按类别总数分配"
> argmax 对**每个人**独立看自己的概率,**不知道**"全公司有 5 个癌症"。它不会把 5 个人"挑出来"——只能被动接受模型给的概率。
> 类不平衡(class imbalance)训练后,模型倾向猜多数类,argmax 就**全部猜多数类**。

### 怎么办:代价敏感决策

不改 argmax,改**判定阈值**:

```python
# 默认:argmax 等价阈值 0.5
predict = (P(cancer) > 0.5)

# 医疗:阈值压到 0.05——宁愿多查也别漏
predict = (P(cancer) > 0.05)
```

阈值 0.05 → 那 5 个人 P=0.3 会被抓出来(0.3 > 0.05),但同时多出一些假阳性(健康人被误判)。**用假阳性换不漏诊**——医疗场景这个 trade-off 是值得的。

### 何时用 argmax vs 阈值化

| 场景 | 建议 |
|:--|:--|
| 类平衡 + 错误代价对等 | argmax 默认即可 |
| 类不平衡 + 假阴性代价高(癌症、欺诈) | 阈值化 |
| 多类、各类代价不同 | 贝叶斯决策:选让**期望损失**最小的动作,不是让 P 最大的 |
| 概率未校准 | 先校准(Platt / 温度缩放),再决策 |

### 一句话

argmax 只在**等代价**假设下最优;代价不对称的场景(医疗/金融/自动驾驶)必须显式建模代价,要么调阈值,要么改用期望损失最小化。

## LogSumExp 与 cross_entropy 的稳定写法

> [!tip] 一句话
> 把"减max + logsumexp + 拿真实类 logit"三步拼成 cross_entropy,**全程不出现"接近 0 的小概率"**,PyTorch `F.cross_entropy` 内部就是这个套路。

### lse 是什么

**LogSumExp**:softmax 分母取 log——soft max 的归一化常数,只是对它做 log:

$$
\operatorname{L}(z_1, \ldots, z_n) = \log\!\left(\sum_{i=1}^{n} e^{z_i}\right)
$$

**为什么单独有个名字**——它是 NLL 推导的中间产物:

$$
\text{NLL}_i = -\log\frac{e^{z_{y_i}}}{\sum_j e^{z_j}} = -z_{y_i} + \underbrace{\log\sum_j e^{z_j}}_{\text{lse}} = \text{lse} - z_{y_i}
$$

### 完整稳版 cross_entropy

```python
import torch

def cross_entropy(logits, y):
    # ① 减 max,exp 输入 ≤ 0,输出 ≤ 1,防上溢
    logits = logits - logits.max(dim=-1, keepdim=True).values
    # ② 算 lse = log(sum(exp))
    lse = logits.exp().sum(dim=-1).log()                   # 形状 (B,)
    # ③ 拿真实类对应的 logit
    picked = logits.gather(-1, y.unsqueeze(-1)).squeeze(-1)  # 形状 (B,)
    # ④ NLL = lse - picked,均值返回标量
    return (lse - picked).mean()
```

对照 `**F.cross_entropy**`(默认 `reduction='mean'`)即可。

### `gather + unsqueeze + squeeze` 取真实类

```python
logits = torch.tensor([[2.0, 1.0, 0.1], [3.0, 2.0, 1.0]])  # (B=2, C=3)
y = torch.tensor([0, 1])                                      # (B=2,)
```

| 步骤 | 表达式 | | 形状 | 值 |
|:--|:--|:--|:--|:--|
| 1 | `y.unsqueeze(-1)` | | `(2, 1)` | `[[0], [1]]` |
| 2 | `logits.gather(-1, idx)` | | `(2, 1)` | `[[2.0], [2.0]]` |
| 3 | `.squeeze(-1)` | | `(2,)` | `[2.0, 2.0]` |

**`unsqueeze(-1)`**:1D → 2D,让 `y` 能跟 logits 配合做 `gather`
**`gather(-1, idx)`**:沿最后一维(类维)按 `idx` 取值,**等价 `logits[range(N), y]`**,但形状保证 `(B, 1)` 稳定
**`squeeze(-1)`**:去掉 size-1 维,让 `picked` 形状 `(B,)` 跟 `lse` 对齐做减法

### `.values` 具名元组陷阱

`tensor.max(dim=...)` 返回**具名元组 `(values, indices)`**,不是张量:

```python
X = torch.randn(3, 4)
X.max(dim=1, keepdim=True)
# torch.return_types.max(values=tensor([...]), indices=tensor([...]))

X - X.max(dim=1, keepdim=True)              # ✗ TypeError
X - X.max(dim=1, keepdim=True).values       # ✓
```

类似的:`min` / `sort` / `topk` / `mode` 都返回 `(values, indices)` 元组。`argmax` 只返回 `indices`。

### 形状日记

```
logits                (B, C)    [2.0, 1.0, 0.1]
max(dim=-1, keepdim)  (B, 1)    max
logits - max          (B, C)    平移,exp 输入 ≤ 0
.exp()                (B, C)    e^{z-c} ≤ 1
.sum(dim=-1)          (B,)      sum
.log()                (B,)      lse
y.unsqueeze(-1)       (B, 1)    [[0], [1]]
logits.gather(...)    (B, 1)    [[z_y], [z_y]]
.squeeze(-1)          (B,)      [z_y, z_y]
lse - picked          (B,)      NLL
.mean()               ()        标量
```

## 易错点对照表(踩过的坑)

> [!warning] 易混对照表(踩过的坑)
>
> | 错误说法 | 正确认识 |
> |:--|:--|
> | "MSE 对 softmax 输出梯度是 $\hat y - y$" | 错——是 $2(\hat y - y)$,2 的系数在 |
> | "MSE 数值小 → 梯度消失" | 错——是 **softmax 饱和**使 $\hat y(1-\hat y) \to 0$ 把梯度压平 |
> | "σ² 必须先估出才能训练" | 错——MLE 里 σ² 是常数缩放,**直接消掉**,根本不影响 argmin |
> | "正规方程在 $n \gg d$ 时失效" | 错——这恰恰是闭式解**最理想**的场景;失效是**特征线性相关**导致 $\mathbf{X}^\top\mathbf{X}$ 不可逆 |
> | "全 0 初始化 → loss 高" | 错——是"**对称破缺不了**":所有权重梯度相同,网络永远学不出差别 |
> | "nn.CrossEntropyLoss(reduction='none').backward()" | 错——`backward` 要求标量,`(N,)` 输入会 RuntimeError |
> | "`tensor.max(dim=...)` 是张量" | 错——是**具名元组 `(values, indices)`**,要 `.values` 或解包 |
> | "logits -= logits.max() 安全" | 错——**原地改输入**,下次再用同一个 logits 进来值已偏 |
> | "test_loop 用 `len(y)` 算总样本" | 错——`len(y)` 是**最后 batch 的大小**,要用 `y.numel()` 累加 |
> | "test_loop 直接累加 loss 值" | 错——loss 默认是 batch 均值,得乘 `batch_size` 再求和 |

## 相关笔记

- **上游**：[[nn.Module 与模型构建]] — 网络最后一层输出的 logits 从哪来
- **相关**：[[激活函数]] — 为什么输出层不加激活、直接输出 logits
- **对照**：[[Sigmoid]] — 二分类时"一条 logit → 一个概率"，是多分类 Softmax 的特例
- **工具**：[[Tensor 基础]] — `dim` 参数与 `.item()` 的用法
- **下游**：[[交叉熵损失]] — logits + 标签 → loss，训练的起点
- **推导**：[[Softmax 回归与 MLE 推导]] — "为什么 softmax 配交叉熵"——从 MLE 视角的完整推导
- **变体**：[[大词表 Softmax 问题与解法]] — vocab 太大时 softmax 怎么改造
- **优化**：[[BGD、SGD 与 mini-batch]] — 三种梯度下降的差别
- **工程**：[[PyTorch 训练循环关键细节]] — 训练循环容易踩的工程细节

## 参考

- [torch.argmax 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.argmax.html)
- [PyTorch 论坛：分类损失与 softmax 的关系](https://discuss.pytorch.org/t/multi-class-cross-entropy-loss-and-softmax-in-pytorch/24920)
