---
tags:
  - 图像特征
  - 局部特征
  - SIFT
  - 描述子
  - 梯度直方图
created: 2026-10-03
type: 知识点
aliases:
  - SIFT 描述子
  - SIFT 主方向
  - 128 维描述子
  - orientation assignment
  - SIFT descriptor
domain: [计算机视觉, 特征工程]
course: COMP 4423 Easy Computer Vision
lecture: [L4]
source: "[L4-Lecture-Feature.extraction-v4.6.pdf](<../../raw/L4-Lecture-Feature.extraction-v4.6.pdf>)"
---

# SIFT-主方向与描述子

> **一句话**：先给每个关键点找一个**主方向**（它周围梯度的方向直方图里最高的那个峰），然后**把坐标系转到这个方向上**，再在转正后的邻域里统计 $4\times4$ 个格子的梯度方向直方图（每格 8 个方向）—— 得到 **$4\times4\times8=128$ 维**的描述子。**因为整个坐标系跟着主方向一起转，图像怎么旋转，描述子都不变。**

这是 SIFT 的 **Step 3: Orientation Assignment** 和 **Step 4: Description Generation**，课件 L4 p76–p82。课件原文见 [L4 Feature Extraction](<../../raw/L4-Lecture-Feature.extraction-v4.6.pdf>)。

## 完整场景：旋转不变性从哪来

到 Step 2 为止，我们已经知道每个关键点的**位置** $(x,y)$ 和**尺度** $\sigma$。还差**旋转**。

**问题**：如果图像顺时针转 30°，关键点的位置会跟着转，描述子的坐标系也必须跟着转 —— 否则同一栋房子，旋转前后的描述子会完全不同。

**SIFT 的解法不是"算出旋转角再补偿"，而是"直接换一套跟着转的坐标系"**。具体做法是：**把描述子的坐标轴对齐到该点的主方向**。这样一来，"顺时针转 30° 的图"和"没转的图"在各自的主方向坐标系里看到的是**同一个图案**。

> [!tip] 类比
> 你看一张字条来读内容。字条转了，你不会觉得内容变了 —— 因为你**跟着字条的朝向去看**。
> 主方向就是字条上那行字告诉你的朝向，跟它对齐了，图案的相对排布就不受整张图旋转的影响。

## Step 3：主方向怎么算

### 1. 算梯度的大小和方向

在关键点周围取一个小窗口（**窗口大小按该点的 $\sigma$ 缩放** —— 尺度大的点看更大的窗口），用 Sobel 算子算**图像梯度**（课件 p76）：

$$
M(x,y)=\sqrt{G_x^2+G_y^2}\quad(\text{梯度大小}),\qquad \theta(x,y)=\operatorname{atan2}(G_y,G_x)\quad(\text{梯度方向})
$$

Sobel 算子见 [[../图像表示与预处理/边缘检测(卷积核)|边缘检测（卷积核）]]。

**为什么要梯度而不是原始像素？** 梯度大小表示"这里变化多剧烈"，也就是**结构强度**。用梯度而不是灰度，就自动继承了"对整体亮度平移免疫"的性质（同 [[局部二值模式 LBP]] 的直觉）。

### 2. 投成方向直方图

把窗口内每个像素的 $\theta$ 按 360° 分成若干个 bin，累加 $M$。于是得到一张**梯度方向直方图**（课件 p76 明确写 *"the bin-counts are weighted by gradient magnitudes"*）。

直方图里的**峰**就对应"这个方向上的结构最强"。

### 3. 取峰当主方向

课件 p77 的规则：

> - **主方向 = 直方图的最高峰**
> - 若**存在多个峰**，或**任何 bin 的值超过最高峰的 0.8 倍**，就**为每个这样的方向各生成一个描述子**

关键细节（课件 p77 括号里那句）：

> *"they will all have the same **scale** and **location**"*

**同一个点、同一个尺度，可以有多个描述子。** 一个朝向强的角点常常有两个"主方向"（比如窗户的拐角有横竖两条边），这时产出两个描述子、各自描述一种朝向，比强行取一个更准。

> [!note] 这解释了课件 p78 那张图
> *"Original image / Keypoints and their orientations"* —— 关键点被标上了方向向量，方向越长的点表示其方向越显著（权重高）。

## Step 4：128 维描述子怎么来

### 步骤 1：把坐标轴转到主方向

> *"In order to achieve orientation invariance, **the coordinates of the descriptor and the gradient orientations are rotated relative to the keypoint orientation**."*（课件 p79）

**转的是两样东西**：

1. 描述子窗口的**坐标轴** → 对齐到主方向
2. 每个像素的**梯度方向 $\theta$** → 也在同一坐标系下重新度量

第 2 点常被忽略但很关键：只转坐标轴不转角度，等于只转了一半。

### 步骤 2：划格子

> *"Consider a small region around the keypoint. Divide it into $n\times n$ cells (for example, $n=4$, each cell is of size $4\times4$)."*（课件 p80）

标准 SIFT：$n=4$（$4\times4=16$ 个 cell），每个 cell 覆盖 $4\times4$ 像素。

### 步骤 3：每格建一个加权的方向直方图

> *"Build a gradient orientation histogram in each cell. Each histogram entry is weighted by the gradient magnitude and a Gaussian weighting function with $\sigma=0.5\times$ window width."*（课件 p80）

每格建一个直方图，每个 bin 的权重是**两个因子相乘**：

$$
\text{权重}=\underbrace{M}_{\text{梯度大小}}\times\underbrace{\exp\!\left(-\frac{\lVert\mathbf{r}-\mathbf{r}_0\rVert^2}{2\sigma_g^2}\right)}_{\text{高斯窗}},\qquad \sigma_g=0.5\times\text{窗口宽度}
$$

**高斯窗的作用**：让**靠近中心的像素说话更响**。理由是描述子要代表"这个点是什么"，中心附近的结构才是这个点最稳定的身份；边缘像素属于和别的点共享的部分，不该主导描述子。

### 步骤 4：展平成向量

$$
\text{维度}=n^2\times r=4\times4\times8=\mathbf{128}
$$

（课件 p81：*"Typical case used in the SIFT paper: $r=8$, $n=4$, so length of each descriptor is 128."*，其中 $r$ 是每格直方图的 bin 数。）

最后把 $16$ 个 $8$ 维直方图**首尾相连**排成一个 128 维向量。

### 步骤 5：按尺度调窗口大小

> *"To achieve scale-invariance, **the size of the window should be adjusted as per scale of the keypoint**. Larger scale = larger window."*（课件 p82）

**这一步才是尺度不变的收尾**。Step 1 找出的 $\sigma$ 在这里兑现：尺度大的关键点配大窗口，尺度小的配小窗口 —— 这样**每个点都在"适合它的观察尺度"上被描述**。

## 四个不变性各自在哪一步落地

| 不变性 | 在哪一步实现 | 机制 |
|---|---|---|
| **尺度** | Step 1 找 $\sigma$ + **Step 4 步骤 5** 按 $\sigma$ 定窗口大小 | 金字塔 + DoG 找最佳尺度，窗口跟着尺度走 |
| **旋转** | **Step 3** 找主方向 + **Step 4 步骤 1** 坐标轴对齐主方向 | 换一套跟着转的坐标系 |
| **亮度平移** | 全程隐含 | 只用梯度和相对比较，不用绝对灰度（同 LBP） |
| **稳定性** | Step 2 | 剔低对比度、剔边缘点 |

## 从描述子到能检索的向量

一个点 = 一个 128 维向量。一张图 = **数量不定**的 128 维向量（几千到几万个）。这带来两个问题：

1. **没法直接比**（[[../特征与检索/CBIR 基于内容的图像检索|CBIR]] 一次要一个向量，不是 N 个）→ [[../特征与检索/Bag of Visual Words|Bag of Visual Words]] 把 N 个描述子量化成**固定长度的词频直方图**；
2. **维度太高**（128 维）→ [[../特征与检索/降维与 PCA|降维与 PCA]]，或直接 [[../特征与检索/近似最近邻检索|ANN]] 暴力搜。

> [!tip] 和深度特征的对照
> 深度学习的对应物是 [[../卷积网络/卷积层与滤波器|卷积层与滤波器]]：在网络的某一层抽特征图，每个空间位置就是一个描述子。
> **关键区别**：SIFT 的邻域划分（格子大小、方向 bin 数、高斯窗宽度）是**人定死的超参**，从头到尾没有"学习"参与；
> 深度特征的邻域划分和权重是**训练出来的**。见 [[特征提取-知识地图]]。

## 一句话

> 主方向 + 坐标轴对齐 = 旋转不变；按尺度定窗口 = 尺度不变收尾；$4\times4$ 格 × 8 方向 = 128 维。

## 相关笔记

- **上一步**：[[SIFT-关键点精化]]
- **总览**：[[SIFT]] — 四步框架
- **第一步**：[[SIFT-候选定位与尺度空间]]
- **梯度怎么算**：[[../图像表示与预处理/边缘检测(卷积核)|边缘检测（卷积核）]] — Sobel
- **一个直方图变 128 维的同类操作**：[[局部二值模式 LBP]] — 也是统计直方图，只是格子更粗
- **N 个描述子怎么用**：[[../特征与检索/Bag of Visual Words|Bag of Visual Words]]
- **现代替代**：[[../卷积网络/CNN 图像分类模型结构|CNN 图像分类模型结构]]
