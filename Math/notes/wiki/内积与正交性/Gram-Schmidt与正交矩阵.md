---
tags: [Math, 内积与正交性, Gram-Schmidt, 正交矩阵, 对称矩阵对角化]
course: AMA2111
lecture: L02
---

# Gram-Schmidt与正交矩阵 · Gram-Schmidt Process and Orthogonal Matrices

> **一句话**：**Gram-Schmidt** 用投影把任意线性无关组**逐步变成标准正交集**；$Q=[q_1\,\cdots\,q_n]$ 标准正交等价于 **$Q^{-1}=Q^{T}$**，于是对称矩阵能写成 **$A=QDQ^{T}$** —— 这比一般对角化更强：$Q$ 必定存在，且是**正交**的。

课件原文见 [AMA2111LinearAlgebra Stu.pdf](<../../raw/AMA2111LinearAlgebra Stu.pdf>)。§6 的 Gram-Schmidt Process 定义页、Example 23、Example 24（标 `*`）、Orthogonal Matrix 定义页、Theorem（对称矩阵）与 Example 25。

## 投影

**定义**：设 $v,w$ 是向量且 $w\ne\mathbf 0$。$v$ 在 $w$ 上的**投影**（projection）定义为

$$\operatorname{proj}_{w}v=\frac{\langle v,w\rangle}{\|w\|^{2}}\,w .$$

**关键性质**：$v-\operatorname{proj}_{w}v$ 与 $w$ **正交**。

**证明**：

$$\Big\langle w,\ v-\operatorname{proj}_{w}v\Big\rangle
=\langle w,v\rangle-\frac{\langle w,v\rangle}{\|w\|^{2}}\langle w,w\rangle
=\langle w,v\rangle-\frac{\langle w,v\rangle}{\|w\|^{2}}\|w\|^{2}
=\langle w,v\rangle-\langle w,v\rangle=0 .\ \checkmark$$

几何意义：$v$ 拆成"沿 $w$ 方向的分量"与"垂直于 $w$ 的分量"，**投影就是前者**。分母是 $\|w\|^{2}$ 而非 $\|w\|$，是因为要归一化方向 —— 这正是单位方向上的投影长度。

## Gram-Schmidt 过程

反复应用上面的性质，就得到把**线性无关向量组变成标准正交向量组**的构造（Gram-Schmidt process）：

**输入**：线性无关的 $v_1,\dots,v_k$。

1. **不投影第一个向量**：$u_1=v_1$。
2. 对 $i=2,\dots,k$，扣掉 $v_i$ 在已建好的 $u_1,\dots,u_{i-1}$ 上的全部投影：
$$u_i=v_i-\sum_{j=1}^{i-1}\operatorname{proj}_{u_j}v_i
=v_i-\sum_{j=1}^{i-1}\frac{\langle v_i,u_j\rangle}{\|u_j\|^{2}}\,u_j .$$
3. **归一化**：$$q_i=\frac{u_i}{\|u_i\|}\qquad(i=1,\dots,k).$$

**为什么得到的是标准正交集**：由归纳，$u_i\perp u_j$（$j<i$）—— 因为 $v_i$ 减去了它在每个 $u_j$ 上的投影，而 $u_j$ 两两正交，故那 $i-1$ 个投影之和仍落在 $\operatorname{span}\{u_1,\dots,u_{i-1}\}$ 内且与每个 $u_j$ 正交。故 $\{u_i\}$ 是正交集；再除以各自的范数，**正交性保持**（$\left\langle\frac{u_i}{\|u_i\|},\frac{u_j}{\|u_j\|}\right\rangle=\frac{\langle u_i,u_j\rangle}{\|u_i\|\|u_j\|}=0$）且范数变 $1$。

> [!note] 前置条件：向量组必须线性无关
> 若 $v_1,\dots,v_k$ 线性相关，某一步的 $u_i$ 会**退化成 $\mathbf 0$**（因为 $v_i$ 完全落在前面 $u_1,\dots,u_{i-1}$ 张成的空间里），此时 $u_i/\|u_i\|$ 无意义。**"能不能做 Gram-Schmidt"本身就是线性无关的检验**；若真有零向量，先丢掉。

## 例 23：把给定向量组化为标准正交集

$$v_1=\begin{pmatrix}2\\1\\-2\end{pmatrix},\quad v_2=\begin{pmatrix}1\\-2\\0\end{pmatrix},\quad v_3=\begin{pmatrix}1\\0\\1\end{pmatrix}.$$

**第 0 步：先确认线性无关**（否则后面会除以 $0$）。作列 $A=[v_1\,v_2\,v_3]=\begin{pmatrix}2&1&1\\1&-2&0\\-2&0&1\end{pmatrix}$：

$$|A|=2\big((-2)(1)-0\cdot0\big)-1\big((1)(1)-0\cdot(-2)\big)+1\big((1)(0)-(-2)(-2)\big)=-4-1-4=-9\ne0 .$$

故三个向量线性无关 ✓，可以放心做。

**第 1 步：$u_1=v_1$。**

$$u_1=\begin{pmatrix}2\\1\\-2\end{pmatrix},\qquad \|u_1\|^{2}=2^{2}+1^{2}+(-2)^{2}=4+1+4=9 .$$

**第 2 步：$u_2$。** 先算内积：$\langle v_2,u_1\rangle=1\cdot2+(-2)\cdot1+0\cdot(-2)=2-2+0=0$。**第一个投影恰好是零**：

$$\operatorname{proj}_{u_1}v_2=\frac{0}{9}\,u_1=\mathbf 0,\qquad
u_2=v_2-\mathbf 0=\begin{pmatrix}1\\-2\\0\end{pmatrix}.$$

$$\langle u_1,u_2\rangle=2\cdot1+1\cdot(-2)+(-2)\cdot0=2-2=0\ \checkmark,\qquad \|u_2\|^{2}=1+4+0=5 .$$

**第 3 步：$u_3$。** 算两个投影系数：

$$\langle v_3,u_1\rangle=1\cdot2+0\cdot1+1\cdot(-2)=2+0-2=0
\quad\Rightarrow\quad \operatorname{proj}_{u_1}v_3=\frac{0}{9}\,u_1=\mathbf 0,$$

$$\langle v_3,u_2\rangle=1\cdot1+0\cdot(-2)+1\cdot0=1
\quad\Rightarrow\quad \operatorname{proj}_{u_2}v_3=\frac{1}{5}\,u_2=\frac15\begin{pmatrix}1\\-2\\0\end{pmatrix}=\begin{pmatrix}\tfrac15\\-\tfrac25\\0\end{pmatrix}.$$

$$u_3=v_3-\operatorname{proj}_{u_1}v_3-\operatorname{proj}_{u_2}v_3
=\begin{pmatrix}1\\0\\1\end{pmatrix}-\begin{pmatrix}0\\0\\0\end{pmatrix}-\begin{pmatrix}\tfrac15\\-\tfrac25\\0\end{pmatrix}
=\begin{pmatrix}\tfrac45\\\tfrac25\\1\end{pmatrix}.$$

**检查**：

$$\langle u_1,u_3\rangle=2\cdot\tfrac45+1\cdot\tfrac25+(-2)\cdot1=\tfrac85+\tfrac25-2=2-2=0\ \checkmark,$$

$$\langle u_2,u_3\rangle=1\cdot\tfrac45+(-2)\cdot\tfrac25+0\cdot1=\tfrac45-\tfrac45=0\ \checkmark,$$

$$\|u_3\|^{2}=\left(\tfrac45\right)^{2}+\left(\tfrac25\right)^{2}+1^{2}
=\tfrac{16}{25}+\tfrac4{25}+1=\tfrac{20}{25}+1=\tfrac{45}{25}=\tfrac95 ,\qquad \|u_3\|=\sqrt{\tfrac95}=\frac{3}{\sqrt5}.$$

**第 4 步：归一化。**

$$q_1=\frac{u_1}{3}=\frac13\begin{pmatrix}2\\1\\-2\end{pmatrix},\qquad
q_2=\frac{u_2}{\sqrt5}=\frac1{\sqrt5}\begin{pmatrix}1\\-2\\0\end{pmatrix},$$

$$q_3=\frac{u_3}{3/\sqrt5}=\frac{\sqrt5}{3}\begin{pmatrix}\tfrac45\\\tfrac25\\1\end{pmatrix}
=\frac{1}{3\sqrt5}\begin{pmatrix}4\\2\\5\end{pmatrix}.$$

**最终标准正交集**：

$$\boxed{\left\{\frac13\begin{pmatrix}2\\1\\-2\end{pmatrix},\quad\frac1{\sqrt5}\begin{pmatrix}1\\-2\\0\end{pmatrix},\quad\frac1{3\sqrt5}\begin{pmatrix}4\\2\\5\end{pmatrix}\right\}}$$

> **验证（两个条件各验一遍）**。
> **单位性**：$\|q_1\|=\frac13\cdot3=1$ ✓；$\|q_2\|=\frac1{\sqrt5}\cdot\sqrt5=1$ ✓；$\|q_3\|=\frac1{3\sqrt5}\sqrt{16+4+25}=\frac1{3\sqrt5}\cdot\sqrt{45}=\frac{3\sqrt5}{3\sqrt5}=1$ ✓。
> **正交性**：$\langle q_1,q_2\rangle=\frac13\cdot\frac15\langle u_1,u_2\rangle=0$ ✓；$\langle q_1,q_3\rangle=0$ ✓；$\langle q_2,q_3\rangle=\frac15\cdot\frac1{3\sqrt5}\langle u_2,u_3\rangle=0$ ✓。

**拼成矩阵**（列向量即标准正交集）：

$$Q=\begin{pmatrix}\tfrac23&\tfrac1{\sqrt5}&\tfrac4{3\sqrt5}\\[2pt]\tfrac13&-\tfrac2{\sqrt5}&\tfrac2{3\sqrt5}\\[2pt]-\tfrac23&0&\tfrac5{3\sqrt5}\end{pmatrix},\qquad Q^{T}Q=I .$$

> **本例的一个特点**：$v_1$ 与 $v_2$ 本来就正交，所以 $u_2=v_2$，第一次投影是零。**Gram-Schmidt 在"输入已经部分正交"时省力得多**；若输入完全乱来，每一步都要减掉 $i-1$ 个投影。

## 例 24（课件标 `*`，进阶）

课件给这一例打了 `*` 标记（`AMA2111` 的约定见 [[课程场景与阅读约定]]：星号是课件自己标的，优先级排在最末）。**方法与例 23 完全相同**，这里给全部中间量以便对照。输入：

$$v_1=\begin{pmatrix}1\\1\\1\end{pmatrix},\quad v_2=\begin{pmatrix}-1\\1\\0\end{pmatrix},\quad v_3=\begin{pmatrix}1\\2\\1\end{pmatrix}.$$

- $u_1=v_1$，$\|u_1\|^{2}=1+1+1=3$。
- $\langle v_2,u_1\rangle=(-1)(1)+1(1)+0(1)=-1+1+0=0$ ⇒ $\operatorname{proj}_{u_1}v_2=\mathbf 0$ ⇒ $u_2=\begin{pmatrix}-1\\1\\0\end{pmatrix}$，$\|u_2\|^{2}=1+1=2$。
- $\langle v_3,u_1\rangle=1+2+1=4$ ⇒ $\operatorname{proj}_{u_1}v_3=\frac43\begin{pmatrix}1\\1\\1\end{pmatrix}=\begin{pmatrix}\tfrac43\\\tfrac43\\\tfrac43\end{pmatrix}$。
- $\langle v_3,u_2\rangle=1(-1)+2(1)+1(0)=-1+2=1$ ⇒ $\operatorname{proj}_{u_2}v_3=\frac12\begin{pmatrix}-1\\1\\0\end{pmatrix}=\begin{pmatrix}-\tfrac12\\\tfrac12\\0\end{pmatrix}$。
- $$u_3=v_3-\frac43u_1-\frac12u_2=\begin{pmatrix}1-\frac43+\frac12\\2-\frac43-\frac12\\1-\frac43-0\end{pmatrix}=\begin{pmatrix}\tfrac16\\\tfrac16\\-\tfrac13\end{pmatrix}=\frac16\begin{pmatrix}1\\1\\-2\end{pmatrix},$$
$$\|u_3\|^{2}=\tfrac1{36}+\tfrac1{36}+\tfrac19=\tfrac1{36}+\tfrac1{36}+\tfrac4{36}=\tfrac6{36}=\tfrac16 .$$

**标准正交集**：

$$\boxed{\left\{\frac1{\sqrt3}\begin{pmatrix}1\\1\\1\end{pmatrix},\quad\frac1{\sqrt2}\begin{pmatrix}-1\\1\\0\end{pmatrix},\quad\frac1{\sqrt6}\begin{pmatrix}1\\1\\-2\end{pmatrix}\right\}}$$

> **验证 $u_3$ 的方向**：$\begin{pmatrix}1\\1\\-2\end{pmatrix}\cdot\begin{pmatrix}1\\1\\1\end{pmatrix}=1+1-2=0$ ✓、$\begin{pmatrix}1\\1\\-2\end{pmatrix}\cdot\begin{pmatrix}-1\\1\\0\end{pmatrix}=-1+1+0=0$ ✓。
> **几何含义**：在 $\mathbb R^3$ 中给定两个互相正交且非零的向量，**与两者都正交的方向被唯一确定到"差一个倍数"** —— 正交补是一维的。这正是标准正交集能当"直角坐标系"使的根本原因。

## 正交矩阵

**定义**：方阵 $Q$ 称为**正交矩阵**（orthogonal matrix），若

$$Q^{-1}=Q^{T},\qquad\text{即}\ QQ^{T}=Q^{T}Q=I .$$

若 $Q=[q_1\,q_2\,\cdots\,q_n]$，则 $\{q_1,\dots,q_n\}$ 是**标准正交集**，即：

1. $\langle q_i,q_j\rangle=0$ whenever $i\ne j$；
2. 所有 $q_i$ 都是单位向量（$\|q_i\|=1$）。

**为什么等价**（这一步值得记住）：$(Q^{T}Q)_{ij}=q_i^{T}q_j=\langle q_i,q_j\rangle$。所以 $Q^{T}Q$ 的**对角元是 $\|q_i\|^{2}$**、**非对角元是 $\langle q_i,q_j\rangle$**。于是 $Q^{T}Q=I$ **逐元素地**就是那两个条件（见 [[正交性]]）。

> [!important] $Q^{-1}AQ$ vs $Q^{T}AQ$ —— 同一个东西，但更好用
> - 对**一般的可对角化矩阵** $A$（见 [[对角化]]），结论是 $P^{-1}AP=D$，$P$ 的列只需**线性无关**。而且 $A$ **可能根本没有**这样的 $P$（例 19 就没有）。
> - 对**正交矩阵** $Q$，有 $Q^{-1}=Q^{T}$，所以 $P^{-1}AP=D$ 写成 $Q^{T}AQ=D$，等价地 $A=QDQ^{T}$（两侧左乘 $Q$）。
> - **两条式子是同一个式子的两种写法，不是两套理论。** 区别只在"$Q^{T}$"比"$P^{-1}$"好用：转置**不做除法**，数值上稳定得多；且列向量单位正交，各方向不互相"挤"，误差不会累积。
> - 下面的 Theorem 把这件事升级为**对称矩阵的定理**："$Q$ 存在"不再需要额外假设，而且 $Q$ 还能要求是正交的。

## Theorem：对称矩阵可正交对角化

> 设 $A$ 是 $n$ 阶**对称矩阵**（$A=A^{T}$）。则
>
> 1. $A$ 有特征向量 $q_1,\dots,q_n$ 构成**正交矩阵** $Q=[q_1\,\cdots\,q_n]$；
> 2. 存在正交矩阵 $Q$ 使 $A=QDQ^{T}$，其中 $D$ 是对角矩阵。

**这个定理比一般对角化强两点**：

| | 一般 $A$（[[对角化]] 的 Theorem） | 对称 $A$（本 Theorem） |
|---|---|---|
| 有 $n$ 个无关特征向量 | **不一定**（[[对角化]] 例 19 就失败） | **一定** |
| 变换矩阵 | 任意可逆的 $P$，$A=PDP^{-1}$ | **正交**的 $Q$，$A=QDQ^{T}$ |
| 求法 | 逐个 $\ker(A-\lambda I)$ 凑 $n$ 个 | 可先任意凑，再用 Gram-Schmidt 正交化 |

**实践含义**：数值计算里处理对称矩阵时**优先找正交 $Q$**，不要用一般 $P$。

## 例 25：找正交 $Q$ 使 $Q^{T}AQ$ 为对角阵

$$A=\begin{pmatrix}3&-2&4\\-2&6&2\\4&2&3\end{pmatrix}.$$

**第一步：确认对称。** $a_{12}=-2=a_{21}$ ✓，$a_{13}=4=a_{31}$ ✓，$a_{23}=2=a_{32}$ ✓。$A=A^{T}$，Theorem 适用。

**第二步：特征多项式。** 沿第一行展开：

- $M_{11}=\begin{vmatrix}6-\lambda&2\\2&3-\lambda\end{vmatrix}=(6-\lambda)(3-\lambda)-2\cdot2=18-6\lambda-3\lambda+\lambda^{2}-4=\lambda^{2}-9\lambda+14$，
- $M_{12}=\begin{vmatrix}-2&2\\4&3-\lambda\end{vmatrix}=(-2)(3-\lambda)-2\cdot4=-6+2\lambda-8=2\lambda-14$，
- $M_{13}=\begin{vmatrix}-2&6-\lambda\\4&2\end{vmatrix}=(-2)(2)-4(6-\lambda)=-4-24+4\lambda=4\lambda-28$。

$$f(\lambda)=(3-\lambda)(\lambda^{2}-9\lambda+14)-(-2)(2\lambda-14)+4(4\lambda-28).$$

第一项 $=3\lambda^{2}-27\lambda+42-\lambda^{3}+9\lambda^{2}-14\lambda=-\lambda^{3}+12\lambda^{2}-41\lambda+42$；第二项 $=+2(2\lambda-14)=4\lambda-28$；第三项 $=16\lambda-112$。

合计 $-\lambda^{3}+12\lambda^{2}-41\lambda+42+4\lambda-28+16\lambda-112=-\lambda^{3}+12\lambda^{2}-21\lambda-98$。

$$\boxed{f(\lambda)=-(\lambda-7)^{2}(\lambda+2)}$$

验算：$(\lambda-7)^{2}(\lambda+2)=(\lambda^{2}-14\lambda+49)(\lambda+2)=\lambda^{3}+2\lambda^{2}-14\lambda^{2}-28\lambda+49\lambda+98=\lambda^{3}-12\lambda^{2}+21\lambda+98$，取负即 $f$ ✓。

**特征值：$7$（二重）、$-2$。**

**第三步：$\lambda=7$ 的特征子空间（2 维）。**

$$A-7I=\begin{pmatrix}-4&-2&4\\-2&-1&2\\4&2&-4\end{pmatrix}.$$

三行彼此成比例（第 2 行 $=\frac12\times$ 第 1 行，第 3 行 $=-1\times$ 第 1 行），故只有**一个**独立方程 $-4v_1-2v_2+4v_3=0$，即

$$v_3=v_1+\frac12v_2 .$$

**特征子空间是二维的**（正对应二重根 $7$）。令 $v_2=0$ 取 $a=\begin{pmatrix}1\\0\\1\end{pmatrix}$；令 $v_1=0$ 取 $b=\begin{pmatrix}0\\2\\1\end{pmatrix}$。**验证两者都是 $\lambda=7$ 的特征向量**：

$$Aa=\begin{pmatrix}3\\-2+4\\4+3\end{pmatrix}=\begin{pmatrix}3\\2\\7\end{pmatrix}=7\begin{pmatrix}1\\0\\1\end{pmatrix}\ \checkmark,\qquad
Ab=\begin{pmatrix}8\\12-2\\2+3\end{pmatrix}=\begin{pmatrix}8\\10\\5\end{pmatrix}=7\begin{pmatrix}0\\2\\1\end{pmatrix}\ \checkmark$$

但它们**不正交**：$\langle a,b\rangle=1\cdot0+0\cdot2+1\cdot1=1\ne0$。**用一次投影修正**（这一步就是 Gram-Schmidt，但**只在特征子空间内部**做，所以不破坏特征向量性质）：

$$\langle b,a\rangle=1,\qquad \|a\|^{2}=1+0+1=2 .$$

$$u_1=a=\begin{pmatrix}1\\0\\1\end{pmatrix},\qquad
u_2=b-\frac{\langle b,u_1\rangle}{\|u_1\|^{2}}\,u_1
=\begin{pmatrix}0\\2\\1\end{pmatrix}-\frac12\begin{pmatrix}1\\0\\1\end{pmatrix}
=\begin{pmatrix}-\tfrac12\\2\\\tfrac12\end{pmatrix}.$$

$$\langle u_1,u_2\rangle=1\cdot\left(-\tfrac12\right)+0\cdot2+1\cdot\tfrac12=0\ \checkmark,\qquad
\|u_1\|^{2}=2,\qquad \|u_2\|^{2}=\tfrac14+4+\tfrac14=\tfrac92 .$$

**$u_2$ 仍是 $\lambda=7$ 的特征向量**（投影只在 $\ker(A-7I)$ 这个平面内移动，平面内的任何向量都还是特征向量）：$Au_2=\begin{pmatrix}3(-1/2)-2(2)+4(1/2)\\-2(-1/2)+6(2)+2(1/2)\\4(-1/2)+2(2)+3(1/2)\end{pmatrix}=\begin{pmatrix}-7\\14\\7\end{pmatrix}=7\begin{pmatrix}-1/2\\2\\1/2\end{pmatrix}=7u_2\ \checkmark$

$$\lambda=7\ \text{的单位特征向量：}\quad
q_1=\frac{u_1}{\sqrt2}=\frac1{\sqrt2}\begin{pmatrix}1\\0\\1\end{pmatrix},\qquad
q_2=\frac{u_2}{3/\sqrt2}=\frac{\sqrt2}{3}\begin{pmatrix}-\tfrac12\\2\\\tfrac12\end{pmatrix}=\frac1{3\sqrt2}\begin{pmatrix}-1\\4\\1\end{pmatrix}.$$

**第四步：$\lambda=-2$ 的特征向量。**

$$A+2I=\begin{pmatrix}5&-2&4\\-2&8&2\\4&2&5\end{pmatrix}.$$

第 2 式除以 $2$：$-v_1+4v_2+v_3=0\Rightarrow v_1=4v_2+v_3$。代回第 1 式：$5(4v_2+v_3)-2v_2+4v_3=18v_2+9v_3=0$，即 $2v_2+v_3=0\Rightarrow v_3=-2v_2$，故 $v_1=4v_2-2v_2=2v_2$。取 $v_2=1$：

$$v_3=\begin{pmatrix}2\\1\\-2\end{pmatrix},\qquad \|v_3\|^{2}=4+1+4=9 .$$

**验证**：

$$Av_3=\begin{pmatrix}3\cdot2-2\cdot1+4(-2)\\-2\cdot2+6\cdot1+2(-2)\\4\cdot2+2\cdot1+3(-2)\end{pmatrix}=\begin{pmatrix}6-2-8\\-4+6-4\\8+2-6\end{pmatrix}=\begin{pmatrix}-4\\-2\\4\end{pmatrix}=-2\begin{pmatrix}2\\1\\-2\end{pmatrix}\ \checkmark$$

$$q_3=\frac{v_3}{3}=\frac13\begin{pmatrix}2\\1\\-2\end{pmatrix}.$$

**第五步：验证三个 $q$ 两两正交**（这一步必查，见下方 warning）：

$$\langle q_1,q_3\rangle\propto\langle u_1,v_3\rangle=1\cdot2+0\cdot1+1\cdot(-2)=2-2=0\ \checkmark,$$
$$\langle q_2,q_3\rangle\propto\langle u_2,v_3\rangle=\left(-\tfrac12\right)\cdot2+2\cdot1+\left(\tfrac12\right)(-2)=-1+2-1=0\ \checkmark,$$
$$\langle u_1,u_2\rangle=0\ \checkmark\ (\text{第三步已验}).$$

三个范数：$\|q_1\|=\frac{\sqrt2}{\sqrt2}=1$ ✓、$\|q_2\|=\frac1{3\sqrt2}\sqrt{1+16+1}=\frac{\sqrt{18}}{3\sqrt2}=\frac{3\sqrt2}{3\sqrt2}=1$ ✓、$\|q_3\|=\frac13\cdot3=1$ ✓。

**第六步：写出 $Q$ 与 $D$。**

$$Q=\begin{pmatrix}
\tfrac1{\sqrt2}&-\tfrac1{3\sqrt2}&\tfrac23\\[2pt]
0&\tfrac4{3\sqrt2}&\tfrac13\\[2pt]
\tfrac1{\sqrt2}&\tfrac1{3\sqrt2}&-\tfrac23
\end{pmatrix}=\begin{bmatrix}q_1&q_2&q_3\end{bmatrix},\qquad D=\begin{pmatrix}7&0&0\\0&7&0\\0&0&-2\end{pmatrix}.$$

**验证 $Q^{T}AQ=D$**（不必手算 $9$ 个元素，两行就够）：对角元 $q_j^{T}Aq_j=\lambda_jq_j^{T}q_j=\lambda_j\cdot1=\lambda_j$（因为 $Aq_j=\lambda_jq_j$、$q_j^{T}q_j=1$）；非对角元 $q_i^{T}Aq_j=\lambda_j\,q_i^{T}q_j=0$（因为 $q_i\perp q_j$）。所以

$$Q^{T}AQ=\begin{pmatrix}7&0&0\\0&7&0\\0&0&-2\end{pmatrix}=D .$$

**等价地 $A=QDQ^{T}$**。抽查 $(1,1)$ 元（外积逐项：$(q_jq_j^{T})_{11}=(q_{j,1})^{2}$）：

$$\big(QDQ^{T}\big)_{11}=7(q_{1,1})^{2}+7(q_{2,1})^{2}-2(q_{3,1})^{2}
=7\cdot\tfrac12+7\cdot\tfrac1{18}-2\cdot\tfrac49
=\tfrac{63}{18}+\tfrac7{18}-\tfrac{16}{18}
=\tfrac{54}{18}=3=a_{11}\ \checkmark$$

（**这里容易漏掉平方**：$q_3$ 的第一分量是 $\frac23$，其平方是 $\frac49$，再乘系数 $-2$ 得 $-\frac{16}{18}$ 而不是 $-\frac8{18}$。算成 $\frac{62}{18}$ 就会误判"$Q$ 不对"。外积 $q_jq_j^{T}$ 的元素是**对应分量相乘**，不是逐元素相乘。）

**答案**：

$$\boxed{Q=\begin{pmatrix}\tfrac1{\sqrt2}&-\tfrac1{3\sqrt2}&\tfrac23\\[2pt]0&\tfrac4{3\sqrt2}&\tfrac13\\[2pt]\tfrac1{\sqrt2}&\tfrac1{3\sqrt2}&-\tfrac23\end{pmatrix},\qquad Q^{T}AQ=\begin{pmatrix}7&0&0\\0&7&0\\0&0&-2\end{pmatrix}}$$

> [!warning] 本例最容易出错的地方：二重根的子空间里**必须再正交化**
> $\lambda=7$ 是二重根，$\ker(A-7I)$ 是**二维平面**。随手取的两个基（如上面先取的 $\begin{pmatrix}1\\0\\2\end{pmatrix}$ 和 $\begin{pmatrix}0\\1\\1\end{pmatrix}$）**常常既不满足 $Av=7v$、也不互相正交**。正确流程是：
> 1. 回到方程 $-4v_1-2v_2+4v_3=0$ **解出整个平面**（别凭感觉取向量）；
> 2. 在平面内做一次 Gram-Schmidt 投影，**投影后仍是特征向量**（因为没离开该平面）；
> 3. **再检查特征值不同的那个特征向量是否恰好落在该平面的正交补里**（对称矩阵保证了这一点，见 Theorem 第 1 条）。
>
> 另一点：**$Q$ 不唯一**。$q_1,q_2$ 同属 $\lambda=7$，可以互换、可以同时反号；$q_3$ 也能整体反号。**唯一的是 $D$ 里的特征值多重集 $7,7,-2$。**

## 这一节的位置

§6 到此结束。**§5、§6 是本课的新内容**（课件无 `(AMA1120)` 标记），本节的 Theorem 是整讲的**收束**：它把 §5 的"可对角化"（只对部分矩阵成立）升级为"对称矩阵**一定**可以，且变换矩阵是正交的"。而 [[对角化的应用]] 的 $A^{m}=PD^{m}P^{-1}$ 在 $P=Q$ 时同样约掉，只是多了一个转置。

## 关联

- 前提 → [[内积与范数]]（投影里的 $\langle v,w\rangle$、$\|w\|^{2}$、以及 $\|u_i\|=0$ 时"不能归一化"都出自这四条性质）
- 输入的多半不是正交 → [[正交性]]（例 22 里已正交时只需除以范数；否则要走本节的投影）
- 与对角化的关系 → [[对角化]]（$P^{-1}AP$ 的 $P$ 只要求列无关；对称时才能换成 $Q^{T}AQ$）、[[对角化的应用]]（$A^{m}=QD^{m}Q^{T}$）
- 底层运算 → [[转置]]（$Q^{-1}=Q^{T}$；$Q^{T}Q$ 的对角元是 $\|q_i\|^{2}$、非对角元是 $\langle q_i,q_j\rangle$）、[[矩阵运算]]（$QQ^{T}=I$ 里的矩阵乘按 $c_{ij}=\sum_s q_{is}q_{sj}$ 展开正是内积）
- 前提条件的出处 → [[线性相关与无关]]（Gram-Schmidt 要求输入**线性无关**）、[[高斯消去法]]（无关性靠消元判定）
