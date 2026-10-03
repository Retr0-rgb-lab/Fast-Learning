---
tags:
  - pytorch
  - 神经网络
  - 深度学习
  - nn.Module
created: 2026-10-02
type: 知识点
aliases:
  - 块与层
  - Module 层级
  - parameters vs modules
  - 容器与叶子
---

# 块、层与参数：nn.Module 体系

[[nn.Module 与模型构建]] 讲了**怎么写一个模型**，这篇讲**术语体系本身**——`block` / `layer` / `module` / `parameter` 到底是什么、谁装谁。PyTorch 的命名体系反直觉，不理清会在自定义层、参数绑定、state_dict 存档时反复踩坑。

## 先破题:PyTorch 里没有 Block 这个类

```python
net     = nn.Sequential(...)   # 变量名叫 net
model   = nn.Sequential(...)   # 变量名叫 model
chimera = nn.Sequential(...)   # 变量名叫 chimera
block1  = nn.Sequential(...)   # 变量名叫 block1
```

**这四个是同一个类,零区别。** `Block` / `Model` / `Net` / `Sequence` 全是**别名**,不是类名。区别只在于你起的名字,以及它肚子里装了什么。

> [!warning] "Sequential" 的翻译陷阱
> `nn.Sequential` 的 "Sequential" 是「顺序容器」,**不是 NLP 里的序列模型(sequence model)**。它只表示"按顺序链式传递数据",和 RNN 毫无关系。

## 唯一的分类轴:容器 还是 叶子

```text
nn.Module
├── 容器 Module    ← 肚子里还有 Module(俗称 block / 块)
│     Sequential、自己写的 Net、残差块
│
└── 叶子 Module    ← 只做一件事,自己没有孩子(俗称 layer / 层)
      Linear、ReLU、BatchNorm、MaxPool
      └── 内部可能握着 Parameter(真正被训练的数字)
```

**"块"和"层"是同一个东西的两种叫法**,判断标准只有一条:**它有没有孩子**。

| | 例子 | 判定 |
|---|---|---|
| **层(叶子)** | `nn.Linear(784, 256)` | 没有孩子,自己做一件事 |
| **块(容器)** | `nn.Sequential(Linear, ReLU, Linear)` | 里面还有 Module |

递归嵌套:

```text
网络 ⊃ 若干块 ⊃ 若干块 ⊃ … ⊃ 若干层
```

**"层"出现在块里面,"块"出现在层外面。同一个类,看位置定称呼。**

## Parameter 不在这套体系里

```text
块 (nn.Sequential)
└── 层 (nn.Linear)          ← 是 nn.Module
    └── Parameter           ← 不是 nn.Module,是 torch.Tensor 的子类
```

**Parameter 是这条链的终点**,再往下没有东西了。

`nn.Module.__setattr__` 有个分流逻辑,决定一个属性落到哪里:

| 赋值的值类型 | 存到 | 后果 |
|---|---|---|
| `nn.Module` 实例 | `self._modules` | 被 `parameters()` / `state_dict()` / `.to(device)` 看见 |
| `nn.Parameter` | `self._parameters` | 被训练、被 `state_dict()` 收录 |
| 其他(裸张量、list、tuple) | `self.__dict__` | **PyTorch 完全看不见** |

> [!danger] 三个典型静默失效
> ```python
> self.lin = [lin]              # ❌ 塞进 list → PyTorch 看不见
> self.rand_weight = torch.rand(20, 20)   # ❌ 裸张量 → 不训练、不进 state_dict
> self.w = torch.randn(10, 784)           # ❌ 没包 nn.Parameter → 梯度不来
> ```
> 这三种**都不报错**,只是该有的行为悄悄消失了。

正确写法:

```python
self.lin = lin                                    # ✅ nn.Module 直接赋值
self.rand_weight = torch.rand(20, 20)            # 不想训练就写 requires_grad=False 的裸张量
self.w = nn.Parameter(torch.randn(10, 784))      # ✅ 要训练就包一层
```

## 一棵真实的树

```python
class NestMLP(nn.Module):
    def __init__(self):
        self.net = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 32))
        self.linear = nn.Linear(32, 16)
    def forward(self, X):
        return self.linear(self.net(X))

chimera = nn.Sequential(NestMLP(), nn.Linear(16, 20))
```

展开后:

```text
chimera                              Sequential      ← 容器
├── 0: NestMLP                       自定义类         ← 容器
│   ├── net: Sequential(...)         Sequential      ← 容器
│   │   ├── 0.weight  Parameter (64, 20)    ← 参数,不是模块
│   │   ├── 0.bias    Parameter (64,)
│   │   ├── 2.weight  Parameter (32, 64)
│   │   └── 2.bias    Parameter (32,)
│   └── linear: Linear(32, 16)      叶子模块
│       ├── weight  Parameter (16, 32)
│       └── bias    Parameter (16,)
└── 1: Linear(16, 20)                叶子模块
    ├── weight  Parameter (20, 16)
    └── bias    Parameter (20,)
```

## 三个 API 看到的是三个不同层面

这是最容易混的地方。它们**不是"遍历模块的三种方式"**,是完全不同的东西:

| API | 遍历什么 | ReLU 会出现吗 | 备注 |
|---|---|---|---|
| `net.modules()` | 所有 Module(容器 + 叶子) | ✅ 会 | 含容器自己 |
| `net.parameters()` | Parameter | ❌ 不出现 | ReLU 没参数 |
| `net.state_dict()` | Parameter + buffer | ❌ 不出现 | 多一个 buffer |

```python
net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 1))

len(list(net.parameters()))   # 4   ← 2 个 Linear × (weight + bias)
len(list(net.modules()))      # 5   ← Sequential + Linear + ReLU + Linear + ...
len(list(net.state_dict()))   # 4
```

**跳号从哪来?**

```text
net.named_modules()    →  0, 1, 2, 3      (ReLU 占位置 1)
net.named_parameters() →  0, 2, …         (ReLU 没参数,不登记)
```

> ReLU 明明是 Module,为什么在 parameters 里消失?
> 因为它**不在 parameter 这一层** —— 它是叶子 Module,但叶子里空空如也。

## 命名规则 = 你怎么存它的

```text
nn.Sequential(...)        →  self._modules['0'] = ...   →  名字是 "0.weight"
self.lin1 = nn.Linear()   →  self._modules['lin1'] = ...  →  名字是 "lin1.weight"
```

**`state_dict` 的键是带路径的**(`'0.weight'`、`'block 1.2.bias'`),这个路径是 `load_state_dict` 做名字匹配的依据。

> [!tip] 深层网络用 OrderedDict 命名
> ```python
> net = nn.Sequential(OrderedDict([
>     ("fc1", nn.Linear(784, 256)),
>     ("act", nn.ReLU()),
>     ("fc2", nn.Linear(256, 10)),
> ]))
> # state_dict 键:'fc1.weight' 而不是 '0.weight'
> ```
> 数字索引在第 8 层就得数到 `net[11]`,命名后存档、加载、迁移都靠名字匹配。

## nn.Sequential 不是什么魔法

源码里它只做两件事(见 `torch/nn/modules/container.py`):

```python
def __init__(self, *args):
    for idx, module in enumerate(args):
        self.add_module(str(idx), module)      # ① 按位置注册

def forward(self, X):
    for block in self._modules.values():
        X = block(X)                            # ② 链式传递
    return X
```

**底层的 `_modules` 是 `dict`,不是 `list`**,key 是字符串 `"0"`。`net[0]` 走的是"按位置数第 0 个 value",不是"查 key 为 0 的项"。

自己复现一遍(`MySequential`):

```python
class MySequential(nn.Module):
    def __init__(self, *args):
        super().__init__()
        for idx, module in enumerate(args):
            self._modules[str(idx)] = module    # 内部 API
            # 推荐:self.add_module(str(idx), module)  ← 走正规接口

    def forward(self, X):
        for block in self._modules.values():
            X = block(X)
        return X
```

**对照:为什么 `self.layers = args` 不行?**

```python
self.layers = args    # ❌ args 是 tuple,普通 Python 对象
```

PyTorch 看不见它 → `parameters()` 空、`state_dict()` 空、`.to(device)` 无效。**必须逐个注册成子模块,而不是塞进一个普通容器。**

## Sequential 支持索引,nn.Module 子类不支持

| 操作 | `nn.Sequential` | 自定义 `nn.Module` |
|---|---|---|
| `net[0]` | ✅ | ❌ `TypeError: not subscriptable` |
| `len(net)` | ✅ | ❌ |
| `for m in net` | ✅ | ❌ |
| `net[0:2]` 切片 | ✅ 返回新 Sequential | ❌ |
| `net[-1]` 负索引 | ✅ | ❌ |
| `net + Sequential(...)` | ✅ | ❌ |
| `m.lin1` 属性 | ❌(key 是数字) | ✅ **唯一访问方式** |

**机制**:`nn.Sequential` 定义了 `__getitem__` / `__len__` / `__iter__`,因为它**保证顺序**(源码 docstring 明确说 ModuleList 只是"一个装 Module 的 list",而 Sequential 的层是**级联连接**的)。普通 `nn.Module` 只有 `__getattr__`(按属性名查),因为它的子模块名是用户自定义字符串,没有顺序约束。

> [!warning] 混用必炸
> ```python
> net[2].weight    # nn.Sequential  ✅
> net.lin1         # nn.Module 子类 ✅
> net[2]           # 你的 Net 类   ❌ TypeError
> ```

## Linear 的维度口诀

```python
nn.Linear(in_features, out_features)
```

| 问题 | 答案 |
|---|---|
| 神经元个数? | **out_features**(输出有多长) |
| 每个神经元几个权重? | **in_features**(每个样本喂进多少维) |
| `weight` 形状? | `(out_features, in_features)` |
| `bias` 形状? | `(out_features,)` |
| 本层参数总数? | `out × (in + 1)` |

**`nn.Linear(784, 256)` = 256 个神经元,每个手握 784 个权重 + 1 个偏置 = 785 个参数。**
本层共 `256 × 785 = 200,960` 个参数。

> [!tip] 一句话锚点
> `state_dict` 里 `weight` 的 shape = `(out_features, in_features)`,**第一维是输出维**。
> 神经元个数 = 输出维度。这条规则同时解释了:为什么 `named_parameters()` 会跳号(ReLU 占了位置)、为什么 `net[2].weight` 是 `(1, 8)` 而不是 `(8, 1)`。

## 速查表

| 术语 | 在 PyTorch 里 | 判定标准 |
|---|---|---|
| **model / net** | 顶层 nn.Module | 随便起的名字 |
| **block(块)** | **容器** Module | 肚子里还有 Module |
| **layer(层)** | **叶子** Module | 只做一件事 |
| **parameter** | `nn.Parameter` | **不是 Module**,是 Tensor |
| **buffer** | 普通 Tensor,挂在 Module 上 | 不训练但要存(如 BN 的 running_mean) |
| **Sequential** | 顺序容器 | 只表示链式执行,≠ 序列模型 |

## 相关笔记

- **前置**:[[nn.Module 与模型构建]] — 用这个术语体系写出的第一个完整模型
- **配套**:[[model.train 与 model.eval]] — `self.training` 标记只存在于 Module 上,Parameter 没有
- **下游**:[[梯度累加与 zero_grad]] — 遍历 `parameters()` 做梯度清零
- **下游**:[[SGD 与优化器]] — `optimizer = SGD(net.parameters())` 为什么收 generator
- **对照**:[[激活函数]] — ReLU 是叶子 Module 但没有 Parameter 的典型例子

## 参考

- [PyTorch 官方:nn.Module 文档](https://docs.pytorch.org/docs/stable/nn.html)
- [D2L 5.1 层和块](https://zh.d2l.ai/chapter_deep-learning-computation/model-construction.html)
- [D2L 5.2 参数管理](https://zh.d2l.ai/chapter_deep-learning-computation/parameters.html)
