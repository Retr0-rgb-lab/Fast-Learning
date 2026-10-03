---
tags:
  - pytorch
  - 卷积神经网络
  - ResNet
  - 残差连接
  - CNN
created: 2026-09-10
type: 知识点
aliases:
  - ResNet
  - 残差块
  - Residual block
  - 残差连接
domain: [深度学习, 计算机视觉]
来源: "自学（PyTorch / 深度学习）"
---

# ResNet 与残差连接

> [!tip] ResNet 前向传播全貌
> ![[ResNet前向传播过程.png]]
>
> 图像 → 初始卷积 → **若干个残差块**（主体）→ 全局平均池化 → Linear → 类别概率。残差块是这张图的"主分支 + 捷径"叠加结构；损失函数的梯度能直接沿橙色捷径往回传。

## ResNet 解决了什么

**不是**"灾难性遗忘"（那是持续学习的问题）。ResNet 解决的是**网络变得很深时反而更难训练**的"退化问题"（degradation problem）：

> 把普通 CNN 从 20 层增加到 56 层，**训练集误差反而变高**——既然训练集也拟合得更差，那就不是过拟合，而是**优化退化**。

## 核心想法：让层只学"改变量"

普通网络让若干层直接学习完整映射 $H(x)$。ResNet 改写为：

$$
H(x) = F(x) + x
$$

其中：
- $x$ 通过**快捷连接 / identity shortcut** 直接传到输出
- 卷积层只需学习**残差**：

$$
F(x) = H(x) - x
$$

直觉：假如某几层暂时"不需要做任何事"，普通网络仍要费力学 $H(x)=x$；ResNet 只要让 $F(x)$ 接近 0，就自然得到原输入 $x$。**很深网络更容易优化**。

## 三个符号的角色

| 符号 | 含义 | 备注 |
| :-- | :-- | :-- |
| $x$ | 进入残差块的特征图 | 不一定是原始图像；可能是前面 CNN 提取的特征 |
| $H(x)$ | 这个块**最终应实现的完整变换** | 理论记号，不是独立一层 |
| $F(x)$ | 主分支（Conv/BN/ReLU 等）的输出 | 训练目标被解释为"残差" |

实际前向计算：先算主分支 $F(x)$，再 + 捷径的 $x$，得到 $H(x)$。

> [!warning] "残差"不是物理对象
> 卷积 + ReLU 等运算天然不叫残差。只有当输出被定义为"$H(x)-x$"时，才叫残差。ResNet 只是**人为选择**让卷积分支学习这个含义。

## 两种常见情形

### 情形 1：块不需要改变特征

$$
F(x) \approx 0 \;\;\Rightarrow\;\; y = F(x) + x \approx x
$$

该模块近似**恒等映射**，保留已有特征。

### 情形 2：块要做某种调整

$$
y = x + F(x) \quad \begin{cases} F(x)>0:\; \text{增强} \\ F(x)<0:\; \text{抑制} \end{cases}
$$

例：检测"猫耳朵边缘"，主分支对相关通道做正向修正 → 输出响应更强；检测到背景里的尖锐边缘，则主分支做负向修正 → 输出被抑制。

## 为什么这更容易训练

- 浅网络能做到的事，深网络**至少可以持平**（让新增模块近似"跳过"）
- 捷径给信息与反向传播的梯度都提供了**更直接的通路**
- ResNet 实验：从 20 层加到 152 层，训练误差持续下降（普通 CNN 做不到）

## 残差块结构（BasicBlock）

```text
输入 x
 ├─ 捷径：直接传递 x ──────────────────┐
 └─ 主分支：Conv → BN → ReLU → Conv → BN，得到 F(x)
                                      ↓
                              逐元素相加：F(x) + x
                                      ↓
                                    ReLU
                                      ↓
                         输出 y = ReLU(F(x) + x)
```

真实实现：主分支里夹 BN 和 ReLU，捷径分支什么都不做（形状匹配时）。

## 形状不一致时：用 1×1 卷积做投影捷径

若块改变了通道数或空间尺寸（如 stride=2 下采样），$x$ 不能直接加。改用**投影捷径**：

$$
y = F(x) + W_s x
$$

其中 $W_s$ 通常是 $1\times1$ 卷积，同时完成：

- **stride=2**：空间尺寸从 $H\times W$ 缩到一半
- **输出通道数 = 主分支输出通道数**：让两边匹配

例：输入 $64\times32\times32$，主分支输出 $128\times16\times16$，捷径用 `Conv2d(64, 128, kernel_size=1, stride=2)` 投影。

## ResNet-18/34/50/101/152

只是用不同数量的残差块堆叠出来的不同深度。越深通常能力越强，但代价是参数和计算量。

| 模型 | 残差块类型 | 深度（层数） |
| :-- | :-- | --: |
| ResNet-18 | BasicBlock（2 个 3×3 conv） | 18 |
| ResNet-34 | BasicBlock | 34 |
| ResNet-50 | Bottleneck（1×1 + 3×3 + 1×1） | 50 |
| ResNet-101 | Bottleneck | 101 |
| ResNet-152 | Bottleneck | 152 |

> "**ResNet**" 常特指由残差块组成的卷积网络；**"残差连接"** 则是通用架构组件（Transformer / GPT / BERT 也在用）。

## 相关笔记

- **手算案例**：[[ResNet 完整残差块前向]] — 残差相加、负残差 + ReLU、堆叠主分支 5 步走通
- **前向基础**：[[卷积层与滤波器]] / [[池化]]
- **维度追踪**：[[CNN 维度追踪（CIFAR-10 两层卷积）]] — 残差块的 padding=1 让 F(x) 与 x 形状一致
- **核/通道**：[[CNN 参数量与核]] — $W_s$ 1×1 卷积的参数量 = $C_\text{in}\cdot C_\text{out}$
- **批归一化**：[[CNN 训练技巧]] — BN 在残差主分支内的位置
- **反向**：[[卷积反向传播]] — 残差块的梯度同时来自 $F(x)$ 和捷径 $x$
- **输出**：[[nn.Linear 输出与 logits]] — ResNet 最后的 `nn.Linear` 输出 logits
- **训练循环**：[[优化循环与训练闭环]] — 整个 ResNet 的反向训练流程

## 参考

- [He et al. 2016: Deep Residual Learning for Image Recognition (CVPR)](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)
- [d2l: ResNet](https://d2l.ai/chapter_convolutional-modern/resnet.html)
- [PyTorch torchvision: ResNet](https://docs.pytorch.org/vision/main/models/resnet.html)