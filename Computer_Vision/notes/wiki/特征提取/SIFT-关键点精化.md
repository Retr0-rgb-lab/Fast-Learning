---
tags:
  - 图像特征
  - 局部特征
  - SIFT
  - 关键点精化
  - Hessian
created: 2026-10-03
type: 知识点
aliases:
  - SIFT 关键点精化
  - keypoint refinement
  - Hessian 矩阵
  - Hessian matrix
  - 亚像素定位
domain: [计算机视觉, 特征工程]
course: COMP 4423 Easy Computer Vision
lecture: [L4]
source: "[L4-Lecture-Feature.extraction-v4.6.pdf](<../../raw/L4-Lecture-Feature.extraction-v4.6.pdf>)"
---

# SIFT-关键点精化

> **一句话**：Step 1 找出的是**一堆**候选点，其中很多是**不稳定的** —— 落在平坦区的噪声点、落在边缘上的点。精化就是用两把刀剔掉它们：**泰勒展开**把点的位置修到亚像素精度并顺便剔掉低对比度的，**Hessian 特征值**剔掉那些"沿边缘方向很强、垂直方向很弱"的点。

这是 SIFT 的 **Step 2: Refinement**，课件 L4 p70–p75。课件原文见 [L4 Feature Extraction](<../../raw/L4-Lecture-Feature.extraction-v4.6.pdf>)。

## 完整场景：为什么要分两步

[[SIFT-候选定位与尺度空间]] 的 26 邻域极值检测，是一道**纯局部的判据**：只比 26 个数。代价是它**只看局部，不管全局后果**，所以必然放进两类坏点：

| 坏点类型 | 症状 | 后果 |
|---|---|---|
| **低对比度点** | 落在平坦区域里，DoG 值只是随机噪声的小起伏 | 两张图的噪声不同 → 这张图有、那张图没有 → **匹配不上** |
| **边缘上的点** | DoG 沿边缘方向响应很强，垂直方向几乎为 0 | 位置在垂直方向上**不可确定** → 差一个像素描述子就全变 |

> [!warning] 课件 p70 的一句话就是全部动机
> *"keypoint candidates at low-contrast positions or on edges are not stable enough. We have to remove them."*
> **不是"不准"，是"不稳"** —— 这是本步和下一步（描述子）之间的分界线。

## 第一刀：泰勒展开 → 亚像素定位 + 剔低对比度

### 思路（课件 p71–p72）

在候选点附近取一个小的 $3\times3\times3$ 邻域，把 DoG 函数 $D(x,y,\sigma)$ 在该点处用**二阶泰勒级数**展开。**坐标系平移到候选点为原点**，于是：

$$
D(\Delta x,\Delta y,\Delta \sigma)\approx D(0)+\frac{\partial D}{\partial x}\Delta x+\frac{\partial D}{\partial y}\Delta y+\frac{\partial D}{\partial \sigma}\Delta \sigma+\frac{1}{2}\Delta\mathbf{p}^{\top}H\Delta\mathbf{p}
$$

其中 $\Delta\mathbf{p}=(\Delta x,\Delta y,\Delta\sigma)^\top$。

记号（课件 p72 明确列出）：

| 记号 | 含义 | 矩阵大小 |
|---|---|---|
| **Offset** $\Delta\mathbf{p}$ | 相对原点的偏移 | $3\times1$ |
| **Gradient** $\nabla D$ | 一阶偏导 | $1\times3$ |
| **Hessian** $H$ | 二阶偏导矩阵 | $3\times3$ |

### 令极值为零，解出亚像素位置

极值点满足 $\nabla D(\Delta\mathbf{p})=0$，于是

$$
\Delta\mathbf{p}=-\,H^{-1}\,\nabla D
$$

$$
\text{课件的判据：}\quad \text{若}\ \lVert\Delta\mathbf{p}\rVert>0.5\ \Rightarrow\ \text{丢弃}
$$

> [!note] 0.5 这个阈值在做什么
> $\Delta\mathbf{p}$ 是**偏移量**（以像素为单位）。
> 若偏移超过半像素，说明这个点被 DoG 粗检测**推得挺远** —— 多半是噪声起伏造成的假极值。
> 纯位移（位置平移）在转动整张图时和位置一起动，不影响匹配。
> 所以这一步的产出是**一个亚像素精度的位置**，**不是**新的不变性。

### 低对比度怎么判

**低对比度 = 响应函数在这个点附近不够"尖"**。数学上，二阶导（$H$）刻画曲率：

- $H$ 的特征值大 → 尖锐的峰或谷 → 对比度高
- $H$ 的特征值小 → 平缓的坡 → 对比度低，位置稍变响应就差不多

实践中还常用 $\det(H)$ 判据（对 2D 情形 $H$ 有三个有效自由度，$\det(H)<0$ 表示鞍点，也一并剔掉）。

> [!tip] 和图像边缘检测的类比
> 这里的"曲率判据"和 [[../图像表示与预处理/边缘检测(推导与直觉)|边缘检测（推导与直觉）]] 里的 Laplacian 判据是同一个思路：
> **二阶导 = 一阶导的变化率 = 有没有结构。** 二阶导处处为 0 的地方就是平坦区，所以 Laplacian 取 0 交叉来找边。
> SIFT 用 Hessian 做的是"这个极值够不够尖"。

## 第二刀：Hessian 特征值 → 剔掉边缘上的点

### 判据（课件 p74）

> *"At an edge candidate, the principal curvature **across** the edge is much larger than that **along** the edge."*

也就是在边缘型候选点处：

- **垂直于边缘**的方向：曲率很大（$\lambda_1$ 大）
- **沿着边缘**的方向：曲率很小（$\lambda_2$ 小）

于是出现 $\dfrac{\lambda_1}{\lambda_2}\gg 1$ 的情形。**要剔掉的正是这一类。**

常见判据（Lowe's criterion）：

$$
\text{剔除}\quad \text{若}\quad \frac{\bigl(\lambda_1+\lambda_2\bigr)^2}{\lambda_1\lambda_2}\ \ge\ \frac{(r+1)^2}{r}
$$

课件 p72 给的 $r=10$（$\lVert\Delta\mathbf{p}\rVert>0.5$）是同一步里的另一个阈值，别混。

> [!warning] 为什么"曲率比"能识别边缘
> **边缘的局部形状是"一条线"**：沿线方向近乎平坦（曲率≈0），垂直方向变化剧烈（曲率大）。
> 而**角点**在两个方向上曲率都大。
> 所以 $H$ 的两个特征值**是否接近**，正是区分"边缘"和"角点"的关键 —— 角点才是我们要的。

### 和第二步为什么必须分开做

两把刀针对的是**两种不同的病**，任何一把都去不掉另一种：

| | 低对比度（平坦区噪点） | 边缘上的点 |
|---|---|---|
| $H$ 特征值 | **两个都小** | **一大多小** |
| 需要的判据 | 绝对量级（$\det(H)$、迹） | 相对比值（$\lambda_1/\lambda_2$） |
| 课件位置 | p72–p73 | p74–p75 |

> [!note] 一句话抓住区别
> **"绝对不够尖"剔平坦区，"两个方向尖得不一样"剔边缘。** 前者看大小，后者看比例。

## 剩下什么

通过这两刀，剩下的是**稳定的关键点**：每个带 $(x,y)$（亚像素精度）、$\sigma$（尺度）。

接下来 [[SIFT-主方向与描述子]] 解决最后一个不变性 —— **旋转**。

## 一句话

> 精化 = 用二阶导信息剔掉两类不稳的点：曲率太小（对比度不足）和两个方向曲率不成比例（落在边缘上）。

## 相关笔记

- **上一步**：[[SIFT-候选定位与尺度空间]] — 26 邻域极值给出的还是候选
- **下一步**：[[SIFT-主方向与描述子]] — 解决旋转不变
- **同样的二阶导判据**：[[../图像表示与预处理/边缘检测(推导与直觉)|边缘检测（推导与直觉）]] — Laplacian 的零交叉找边
- **曲率的线性代数**：[[../特征与检索/特征值与特征向量|特征值与特征向量]] — Hessian 的特征向量就是主方向，这与 Step 3 的主方向是同一个数学对象
- **特征值 vs 奇异值**：[[../特征与检索/奇异值分解 SVD|奇异值分解 SVD]]
