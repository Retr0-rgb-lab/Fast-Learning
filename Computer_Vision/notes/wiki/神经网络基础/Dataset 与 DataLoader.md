---
tags:
  - pytorch
  - 数据加载
  - 深度学习
created: 2026-08-31
type: 知识点
domain: [深度学习]
来源: "自学（PyTorch / 深度学习）"
---

# Dataset 与 DataLoader

为了解决一个工程问题而设计：**把"数据怎么存、怎么读"与"模型怎么训练"分离**，搭起一条 `磁盘 → CPU 预处理 → mini-batch → GPU 训练` 的数据管线。

## 两者分工

| 对象 | 类比 | 职责 |
| ---- | ---- | ---- |
| `Dataset` | 数据仓库的查询接口 | 定义"第 i 条数据是什么"：返回一条样本及标签 |
| `DataLoader` | 批处理配送器 | 按 batch 取样、打乱、并行加载，持续供给训练循环 |

## 为什么不能直接读文件？

小数据集可以一次读进内存，但真实训练通常面临：

- 图像/音频/文本文件很多，全部载入内存成本高
- GPU 适合一次处理一批样本，而不是一个
- 每个 epoch 要随机打乱，避免模型记住固定顺序
- 磁盘解码、预处理可能比 GPU 计算慢，需要并行读取

## Dataset：定义单条样本

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, paths, labels):
        self.paths = paths
        self.labels = labels

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        x = load_file(self.paths[idx])  # 按索引懒加载
        y = self.labels[idx]
        return x, y
```

- `__init__`：保存路径、标签、转换规则
- `__len__`：告诉 PyTorch 总样本数
- `__getitem__(idx)`：**按索引懒加载**一条 `(feature, label)`，数据不必一次全进内存

官方例子用 `torchvision.datasets.FashionMNIST(...)` 直接得到一个现成 Dataset。

## DataLoader：组织训练供给

```python
from torch.utils.data import DataLoader

loader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=4)
```

三件高频工作：

- **分批** `batch_size=64`：64 条样本拼成一个 batch，便于并行计算
- **打乱** `shuffle=True`：每轮训练重新排列（训练集开、验证/测试集关）
- **并行加载** `num_workers`：多子进程读取，减少 GPU 等数据的时间

## 每次 iterate 返回什么？

DataLoader 本身不是"一种数据格式"，而是包在 Dataset 外面的**可迭代对象**；每迭代一次，返回一批 `(features, labels)`，**都是 `torch.Tensor`**：

| 变量 | 含义 | 类型 | FashionMNIST 形状 |
| ---- | ---- | ---- | ----------------- |
| `X` / features | 一批图片像素 | `float32` Tensor | `[64, 1, 28, 28]` |
| `y` / labels | 每张图的类别编号 | `int64` Tensor | `[64]` |

两种取法：

```python
# 快速查看一批（调试、画图）
X, y = next(iter(train_dataloader))

# 真正训练：依次取完一个 epoch 的所有 batch
for X, y in train_dataloader:
    ...
```

`iter()` 像"打开按 batch 发数据的传送带"，`next()` 从传送带拿下一箱。`X[0]` 是 batch 里第 1 张图（`[1, 28, 28]`），`y[0]` 是它的正确类别。

> **epoch vs iteration**：处理完所有 batch 一次 = 1 个 epoch；循环体每执行一次 = 1 个 iteration（一批数据）。

## labels_map：数字类别转文字

```python
labels_map = {0: "T-Shirt", 1: "Trouser", ..., 9: "Ankle Boot"}
label = train_labels[0]          # tensor(5)，0 维 Tensor
name = labels_map[label.item()]  # "Sandal"，.item() 取出 Python 整数更稳妥
```

## 在训练循环中的位置

```python
for epoch in range(epochs):
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)               # 模型同时预测 64 张图
        loss = loss_fn(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

模型只看到 Tensor batch，不关心数据来自 JPG、CSV 还是数据库。

## 相关笔记

- **前置**：[[Tensor 基础]] — batch 的形状约定 `[B, C, H, W]` 与 `.item()`
- **下游**：[[Transforms 数据转换]] — transform 挂在 Dataset 上，在取出样本后、组 batch 前执行
- **下游**：[[nn.Module 与模型构建]] — DataLoader 的 batch 就是喂给 `model(x)` 的输入
- **下游**：[[Autograd 自动微分]] — 训练循环里 `zero_grad → backward → step` 三连的细节
- **下游**：[[优化循环与训练闭环]] — epoch 外层循环 + train/test 双循环的完整结构

## 参考

- [Datasets & DataLoaders 官方教程](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
