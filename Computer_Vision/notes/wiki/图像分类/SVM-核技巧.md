---
tags:
  - 图像分类
  - SVM
  - 核技巧
  - 核函数
  - RBF
created: 2026-10-06
type: 知识点
aliases:
  - 核技巧
  - kernel trick
  - 核函数
  - kernel function
  - RBF 核
  - 高斯核
  - 多项式核
  - 非线性 SVM
domain: [计算机视觉, 机器学习]
course: COMP 4423 Easy Computer Vision
lecture: [L6]
source: "[L6-Lecture-Image.classification.fundemental-v4.6.pdf](<../../raw/L6-Lecture-Image.classification.fundemental-v4.6.pdf>)"
---

# SVM-核技巧

> **一句话**：SVM 只能画**直线**，所以遇到弯曲的类就分不开。解法是**换到高维空间去画直线** —— 但高维向量算起来很贵。**核技巧的精髓是：不必真的把点搬进高维空间，只要能算出它们在高维空间里的内积 $K(\mathbf{x}_i,\mathbf{x}_j)$ 就行。** 而 SVM 的解**只依赖内积**（见 [[SVM-软间隔与支持向量]]），所以这一步替换是完全透明的。

课件对应 L6 p49–p53。课件原文见 [L6 Image Classification](<../../raw/L6-Lecture-Image.classification.fundemental-v4.6.pdf>)。

## 完整场景：直线分不开的时候

[[SVM-软间隔与支持向量]] 的软间隔**允许违规**，但只能容忍**少数**样本违规。如果两个类本身是**弯曲交错的**（比如 A 类围成一个环、B 类在环的中间），那么：

- 硬间隔：**无解**（一条直线永远切不开环）
- 软间隔：**需要大量 $\xi_i$**，惩罚项压过间隔项，得到的边界是一条**乱穿的直线**

**根本原因：不是"允许不允许错"的问题，是"直线这个形状本身就不对"。**

## 第一步：换到高维空间（p50、p51）

### 课件的提问与回答

> **问**（p50）：`How about… **mapping data to a higher-dimensional space**?`（那……把数据映射到更高维空间呢？）
> **答**（p51）：`The original feature space **can always be mapped to some higher-dimensional feature space where the training set is separable**: $\Phi:\ \mathbf{x}\to\phi(\mathbf{x})$`

**"总是可以"是这里的关键词。** 课件给的例子很形象：一个**同心圆分布**的数据（圆环套圆环），在二维分不开，映射到三维后**用一个平面就能切开**。

### 为什么升维能解决

**核心几何事实**：

> 在 $D$ 维空间里不可分的数据，映射到足够高的维度后**总能被一个超平面分开**。

直观的道理：升维**增加了"可用的方向"**。二维只有一条线能切，升到三维就可以用一个任意倾斜的平面切，灵活度大幅提升。

| | 二维直线 | 三维平面 |
|---|---|---|
| 能分开 | 左右两堆点 | 左右两堆点、**环套环** |

### 符号：$\Phi$ 是映射，不是矩阵

课件 p51 写的 $\Phi:\ \mathbf{x}\to\phi(\mathbf{x})$ 需要读清楚：

- **$\Phi$（大写 Φ）**：**映射这个函数/操作本身**
- **$\phi(\mathbf{x})$（小写 φ）**：把**单个点** $\mathbf{x}$ 映射后的高维向量

**它们不是同一个东西。** $K$ 个样本就调用 $K$ 次 $\phi$。

> [!note] 高维空间"更宽"不等于"更好"
> 课件 p53 最后一段专门澄清了一个容易误解的点：
> *"Higher-dimensional space still has **intrinsic dimensionality $d$** (the mapping is **not onto**), but linear separators in it correspond to **non-linear separators** in original space."*
>
> 意思是：高维空间**并没有增加数据本身的信息量**（内禀维数还是 $d$，因为映射**不是满射**）。**增加的只是"可用的分隔面形状"**。
>
> **映射回原空间看：高维里的那条直直的分隔面，会变成原空间里一条弯的边界。** 这就是"非线性可分"的来源。

## 第二步：问题来了 —— 高维向量算不起（p52）

假设我们要用多项式核，映射后的向量长度是 $O(d^2)$。当 $d=1000$ 时，$\phi(\mathbf{x})$ 有 **50 万维**。每两个样本做一次内积要算 50 万次乘法：

| | $d=3$ | $d=100$ | $d=1000$ |
|---|---|---|---|
| $\phi(\mathbf{x})$ 维度 | $\sim 6$ | $\sim 5000$ | $\sim 500\,000$ |
| 一次内积 | 6 次乘法 | 5 000 次 | **50 万次** |
| $N=1000$ 个样本两两比较 | 6 000 次 | 5×10⁶ | **5×10⁸** |

**完全不可行。** 而 SVM 偏偏要算大量内积（[[SVM-软间隔与支持向量]] 里已经说明：整个对偶问题只在求 $\alpha_i$，训练点只以内积形式出现）。

## 核技巧：绕过映射（p52）

### 课件的推导

课件 p52 一步步给出答案：

**第 1 步：线性 SVM 依赖什么？**

> *"The linear classifier relies on **inner product** between vectors $K(\mathbf{x}_i,\mathbf{x}_j)=\mathbf{x}_i^{\top}\mathbf{x}_j$"*

**第 2 步：映射之后内积变成什么？**

> *"If every datapoint is mapped into high-dimensional space via some transformation $\Phi:\ \mathbf{x}\to\phi(\mathbf{x})$, the inner product becomes: $K(\mathbf{x}_i,\mathbf{x}_j)=\phi(\mathbf{x}_i)^{\top}\phi(\mathbf{x}_j)$"*

**第 3 步：定义核函数**

> *"A **kernel function** is a **function that is equivalent to an inner product in some feature space**."*
> （核函数是一个**等价于某个特征空间中内积**的函数。）

### 关键洞察

把三步串起来看：

```
SVM 的全部求解过程  ──只用到──>  内积 K(xi, xj)
                                        │
                    ┌───────────────────┴───────────────────┐
                    ↓                                       ↓
        在原空间直接算                        在高维空间算（贵）
        K(xi,xj) = xi^T xj                   K(xi,xj) = φ(xi)^T φ(xj)
                    │                                       │
                    └─────────── 写成同一个符号 K ───────────┘
```

**核函数 $K$ 的作用：把"高维内积"这个昂贵操作，封装成一个可以直接调用的便宜函数。**

> [!tip] "技巧"体现在哪
> **我们从头到尾没有构造过 $\phi(\mathbf{x})$。** 我们只是把公式里的
> $\phi(\mathbf{x}_i)^{\top}\phi(\mathbf{x}_j)$ 换成了一个更好算的表达式 $K(\mathbf{x}_i,\mathbf{x}_j)$，
> 其余部分（SVM 的对偶问题、$\alpha_i$ 的优化、支持向量的判定）**一个字都不用改**。

**这就是"技巧"二字的含义。**

### 课件给的核函数例子（p52）

课件 p52 最后给了一个具体构造：设 $\mathbf{x}=[x_1,\ x_2]$（二维向量），令

$$
K(\mathbf{x}_i,\mathbf{x}_j)=\left(1+\mathbf{x}_i^{\top}\mathbf{x}_j\right)^2
$$

这个式子看起来平淡无奇，但它**等价于某个高维空间的内积**。

**把它展开就能看出高维空间长什么样**（设 $\mathbf{x}_i^{\top}\mathbf{x}_j=s$）：

$$
K=1+2s+s^2
$$

而

$$
\left(1+\mathbf{x}_i^{\top}\mathbf{x}_j\right)^2
=(1+x_{i1}x_{j1}+x_{i2}x_{j2})^2
$$

展开后含 9 项：$1$、$x_{i1}x_{j1}$（×2）、$x_{i2}x_{j2}$（×2）、$x_{i1}^2x_{j1}^2$（×1）、$x_{i1}x_{i2}x_{j1}x_{j2}$（×2）、$x_{i2}^2x_{j2}^2$（×1）。

**这 9 项正是"高维向量"各分量的两两内积** —— 说明对应的 $\phi(\mathbf{x})$ 是个 3 维向量。

**这个例子最有说服力的地方**：高维空间只有 3 维（比某些低维情形还小！），但它**确实实现了二次曲线分界**。**核技巧带来的不是"维数变高"，而是"边界形状变丰富"。**

## 三种核函数对照（p53）

课件 p53 列了三种，每种都配了对应的映射。

| 核 | 公式 $K(\mathbf{x}_i,\mathbf{x}_j)$ | 对应映射 $\phi(\mathbf{x})$ 的维度 | 得到的边界形状 |
|---|---|---|---|
| **线性核 Linear** | $\mathbf{x}_i^{\top}\mathbf{x}_j$ | $\phi(\mathbf{x})=\mathbf{x}$，**就是它自己** | **直线**（就是不做核变换的原始 SVM） |
| **多项式核 Polynomial**（$p$ 次） | $\left(1+\mathbf{x}_i^{\top}\mathbf{x}_j\right)^{p}$ | $\dfrac{d^2+d}{2}$（$d$ 维输入时） | **多项式曲线**（阶数由 $p$ 定） |
| **高斯核 / 径向基函数核 Gaussian (RBF)** | $\exp\!\left(-\dfrac{\lVert\mathbf{x}_i-\mathbf{x}_j\rVert^2}{2\sigma^2}\right)$ | **无限维** | **任意光滑曲线**（局部看像直线） |

### 逐条解释

**① 线性核：退化情形**

$\phi(\mathbf{x})=\mathbf{x}$，"映射"什么都没做。**它就是原始的线性 SVM**。列在表里是为了做对照。

**② 多项式核：有限的"曲线预算"**

- **$p$ 阶**对应**$p$ 次曲线**边界。
- **维度 $(d^2+d)/2$ 是有限的**，可算。
- $p$ 越大 → 边界越复杂 → 也越容易过拟合（和硬间隔 SVM 加大 $C$ 的风险类似）。

> [!note] 课件 p53 这个 $\frac{d^2+d}{2}$ 的出处
> 数字出现在课件 p53 的公式区（PDF 文本提取为 `p` `pd` `d` `2` `2` 分行）。
> 它是"**$d$ 维输入做完整二次展开后（去掉交叉项的冗余）**"的项数：$d$ 个平方项 + $\frac{d(d-1)}{2}$ 个交叉项 = $d+\frac{d^2-d}{2}=\frac{d^2+d}{2}$。**课件未给出推导**，这里补上以便理解。

**③ 高斯核（RBF）：无限维，但每个点代价不变**

课件 p53 对它的说明最值得读：

> *"$\phi(\mathbf{x})$ is **infinite-dimensional**: every point is mapped to a **function (a Gaussian)**; **combination of functions for support vectors is the separator**."*
> （$\phi(\mathbf{x})$ 是**无限维**的：每个点被映射成一个**函数（一个高斯函数）**；**支持向量的函数组合起来就是分隔面**。）

**这是一个视角的彻底转换。**

| | 线性/多项式核 | 高斯核 |
|---|---|---|
| 一个点 $\phi(\mathbf{x})$ 是什么 | 一个**高维向量** | 一个**高斯函数**（关于所有位置的） |
| 分隔面是什么 | 一个**超平面**（点集的线性组合） | **支持向量对应高斯函数的加权和** |
| 维度 | 有限，可数 | **无限** |
| 每个点的计算代价 | 随维度增长 | **不随"维数"增长**（因为从不枚举维数） |

**这就是 RBF 核能"用有限代价处理无限维"的原因** —— 它把 $K$ 定义成一个**闭式公式**：

$$
K(\mathbf{x}_i,\mathbf{x}_j)=\exp\!\left(-\frac{\lVert\mathbf{x}_i-\mathbf{x}_j\rVert^2}{2\sigma^2}\right)
$$

直接算就行，**不涉及任何"高维"**。

### RBF 的两个直觉

- **$\sigma$ 控制"影响半径"**：$\sigma$ 小 → 只有极近的点互相影响 → 边界**起伏多、容易过拟合**；$\sigma$ 大 → 远点的也有影响 → 边界**平滑、可能欠拟合**。
- **局部性**：单个高斯函数只在中心附近显著，所以**在远处看，每一小块都像一条直线** —— 这正是它在弯曲数据上表现好的原因。

> [!warning] $\sigma$ 是要调的参数
> 和 $C$ 一样，$\sigma$（或 RBF 核的 $\gamma$）需要靠验证集选。课件 p53 只列了公式，**未讲参数选择**。

### 实践中只用两种

| 核 | 什么时候用 |
|---|---|
| **Linear** | 特征已经很多很好了（如深度网络的倒数第二层特征）。**快**，且不会过拟合 |
| **RBF** | 特征维度不高、量级不大。**默认首选** |

多项式核实际很少单独用。**课件 p53 把三种并列，但未给选择建议。**

## 核技巧的完整链路

```
问题：SVM 只能画直线，数据弯曲时无解
  │
  ↓ 换空间
第一步：映射到高维 Φ: x → φ(x)          （p50-51）—— 直线在那里可分
  │                                        但 φ(x) 50 万维，算不起
  ↓
第二步：SVM 只依赖内积 K(xi,xj)            （p47-48）—— 这是关键前提
  │
  ↓
第三步：把「高维内积」封装成便宜函数 K      （p52）—— 从不构造 φ(x)
  │
  ↓
结果：用 2 维输入，也能画出任意光滑的边界    （p53）
      代价与维度无关
```

> [!tip] 一句话记住为什么这成立
> **SVM 的解只由内积决定。** 只要你能给出"等价于某个高维空间内积"的函数 $K$，SVM 就以为自己在高维空间里工作。
> **它从不需要知道那个高维空间长什么样。**

## 一句话

> 核技巧 = 用 $K(\mathbf{x}_i,\mathbf{x}_j)$ **冒充**高维内积，让 SVM 在高维空间画直线；因为 SVM 只依赖内积，所以这个替换天衣无缝，**且不必真的构造高维向量**。

## 相关笔记

- **上一步**：[[SVM-软间隔与支持向量]] — 训练点只以内积出现，是本讲的前提
- **回顾**：[[SVM-线性分隔与最大间隔]] — 线性 SVM
- **为什么需要非线性**：[[../特征与检索/数据可分性|数据可分性]]
- **同类"升维换表示"**：[[../特征与检索/降维与 PCA|降维与 PCA]]（**方向相反** —— PCA 降维求可分，核技巧升维求可分，但 PCA 是**线性**变换、不能产生弯曲边界）
- **核技巧的现代替代**：[[../卷积网络/卷积层与滤波器|卷积层与滤波器]] — 用神经网络学一个非线性的 $\phi$，而不是手工设计核
- **内积与特征分解**：[[../特征与检索/奇异值分解 SVD|奇异值分解 SVD]]

## 参考

- [A Short Tutorial on Kernels (NIPS 2003)](https://www.cs.nyu.edu/~mohri/nips03/handouts/h.pdf) — 经典入门
- Burges, *A Tutorial on Support Vector Machines for Pattern Recognition*, 1998
