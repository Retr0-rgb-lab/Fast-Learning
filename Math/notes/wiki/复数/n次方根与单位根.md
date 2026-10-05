---
tags: [Math, 复数, n次方根, 单位根, 极形式]
aliases: [n次方根]
course: AMA2111
lecture: L01
---

# n 次方根与单位根 · nth Root and Roots of Unity

> **一句话**：$w\neq 0$ 的 $n$ 次方根**恰有 $n$ 个**，它们是 $z_k=r^{1/n}e^{i\frac{\theta+2k\pi}{n}}\ (k=0,\dots,n-1)$，均匀分布在半径 $r^{1/n}$ 的圆上、正 $n$ 边形的顶点；每个根都是第一个根乘一个 $n$ 次单位根。

课件原文见 [AMA2111-L01-ComplexNumbers.pdf](<../../raw/AMA2111-L01-ComplexNumbers.pdf>)。覆盖 §4 nth Root 全部内容（三次单位根、定理与证明、几何 remark、单位根、例 6 与例 7）。

## 定义

设 $n\geq 2$ 是整数，$w$ 是非零复数。满足

$$z^n=w$$

的复数 $z$ 称为 $w$ 的一个 **$n$ 次方根（nth root）**。

**为什么最多 $n$ 个**：$n$ 次方根就是多项式方程

$$z^n-w=0$$

的根。而**一个 $n$ 次多项式方程最多有 $n$ 个根**，所以一个复数的 $n$ 次方根个数**不超过 $n$**。（本目录不展开多项式根的定理本身；要用它时看 [[行列式的性质]]。）

**三次单位根（先看一个具体例子建立感觉）**：容易验证 $1$、$-\dfrac12+\dfrac{\sqrt3}{2}i$、$-\dfrac12-\dfrac{\sqrt3}{2}i$ 都是 $1$ 的三次方根（把后两个数的立方算出来都得 $1$）。它们互不相同，而三次方根最多三个，**所以它们就是 $1$ 的全部三次方根**。记

$$\omega=-\frac12+\frac{\sqrt3}{2}i$$

并注意 $\omega^2=-\dfrac12-\dfrac{\sqrt3}{2}i$。这三个数在单位圆上等间隔 $120^\circ$，是**正三角形顶点**。完整的单位根讨论见下文「单位根」。

## 定理（n 次方根公式）

设复数 $w$ 的模为 $r$、辐角为 $\theta$，则 $w$ 的 $n$ 次方根由

$$z_k=r^{1/n}e^{i\frac{\theta+2k\pi}{n}}=r^{1/n}\left(\cos\frac{\theta+2k\pi}{n}+i\sin\frac{\theta+2k\pi}{n}\right)$$

给出，其中

$$k=0,1,\dots,n-1$$

而 $r^{1/n}$ 表示 $r$ 的**正 $n$ 次方根**（$r>0$，所以它唯一）。

### 证明（用 [[De Moivre定理]]）

设 $w=re^{i\theta}$。若 $z=Re^{i\varphi}$ 是 $w$ 的一个 $n$ 次方根，即 $z^n=w$，则 De Moivre 公式给出

$$R^ne^{in\varphi}=re^{i\theta}$$

**比较模**：两边取模，$R^n=r$，故 $R=r^{1/n}$ 唯一确定（$R>0$）。

**比较辐角**：由 [[复指数函数]] 的周期性 $e^{i\alpha}=e^{i\beta}\iff\alpha-\beta=2k\pi$，得

$$n\varphi=\theta+2k\pi\quad\Longrightarrow\quad \varphi=\frac{\theta+2k\pi}{n}$$

**数够不够**：取 $k=0,\dots,n-1$ 给出 $n$ 个辐角，它们相差 $\frac{2\pi}{n}$（即 $360^\circ/n$），互不相同；再取 $k\geq n$ 只会绕圈重复，因为 $\varphi_{k+n}=\varphi_k+2\pi$。结合"最多 $n$ 个根"，这 $n$ 个就是**全部**根。∎

> [!warning] $k$ 的范围是 $0\leq k\leq n-1$，不多不少
> - 少写了：漏根。比如三次方根只写 $k=0$ 就只给了一个根。
> - 多写了：$k=n$ 时 $\varphi_n=\varphi_0+2\pi$，**和 $k=0$ 是同一个复数**（$e^{i(\varphi+2\pi)}=e^{i\varphi}$）。所以「$k=0$ 到 $n$」会重复计一个。
> - $r^{1/n}$ 取**正**根。$(-32)^{1/5}$ 在实数里是 $-2$，但这里 $r=|-32|=32$、$r^{1/5}=2$ 恒为正，负号由辐角 $\pi$ 承担。见 [[极形式]]。

## 几何结构（考点）

1. **均匀分布**：所有 $n$ 次方根**均匀分布在以原点为圆心、半径 $R=r^{1/n}$ 的圆上**，构成**正 $n$ 边形的 $n$ 个顶点**。相邻两根的辐角差恒为 $\frac{2\pi}{n}$。
2. **定位技巧**：把根的辐角改写成

$$\frac{\theta+2k\pi}{n}=\frac{\theta}{n}+k\cdot\frac{2\pi}{n}$$

于是**第一个根的辐角是 $\frac{\theta}{n}$，第 $k$ 个根是在前一个根的辐角上加 $\frac{2\pi}{n}$ 得到的**（$1\leq k\leq n-1$）。画图时：先定第一个点，再每次转 $\frac{360^\circ}{n}$ 度。

## 例 6：求 $w=1+\sqrt3\,i$ 的全部三次方根

**第 1 步：化极形式。** $r=\sqrt{1^2+(\sqrt3)^2}=\sqrt{1+3}=2$。$\cos\theta=\frac12$、$\sin\theta=\frac{\sqrt3}{2}$，两者都正 → 第一象限，$\theta=\frac\pi3$。所以

$$w=1+\sqrt3\,i=2e^{i\pi/3}$$

**第 2 步：套公式。** $r^{1/3}=2^{1/3}\approx 1.2599$，$\frac{\theta+2k\pi}{3}=\frac{\pi/3+2k\pi}{3}=\frac\pi3\cdot\frac13+k\cdot\frac{2\pi}{3}$：

| $k$ | $\varphi_k=\frac\pi9+k\frac{2\pi}3$ | 角度 | 根 |
|---|---|---|---|
| $0$ | $\frac\pi9$ | $20^\circ$ | $2^{1/3}e^{i\pi/9}$ |
| $1$ | $\frac\pi9+\frac{2\pi}3=\frac{7\pi}9$ | $140^\circ$ | $2^{1/3}e^{i7\pi/9}$ |
| $2$ | $\frac\pi9+\frac{4\pi}3=\frac{13\pi}9$ | $260^\circ$ | $2^{1/3}e^{i13\pi/9}$ |

即全部三次方根为

$$\boxed{2^{1/3}e^{i\pi/9},\quad 2^{1/3}e^{i7\pi/9},\quad 2^{1/3}e^{i13\pi/9}}$$

**数值核对**（$2^{1/3}\approx1.25992$）：

- $k=0$：$1.25992(\cos20^\circ+i\sin20^\circ)=1.25992(0.93969+0.34202i)\approx 1.1839+0.4309i$
- $k=1$：$1.25992(\cos140^\circ+i\sin140^\circ)=1.25992(-0.76604+0.64279i)\approx-0.9652+0.8099i$
- $k=2$：$1.25992(\cos260^\circ+i\sin260^\circ)=1.25992(-0.17365-0.98481i)\approx-0.2188-1.2408i$

三个模都 $=\sqrt[3]{2}\approx1.2599$ ✓，辐角都差 $120^\circ$ ✓，代回立方都等于 $1+\sqrt3\,i$ ✓。

## 单位根（nth roots of unity）

$\omega^n=1$ 的 $n$ 次方根称为 **$n$ 次单位根（nth roots of unity）**，记为

$$\omega_k=e^{\frac{2k\pi i}{n}}=\cos\frac{2k\pi}{n}+i\sin\frac{2k\pi}{n},\qquad 0\leq k\leq n-1$$

它们是 $w=1$（即 $r=1,\theta=0$）套公式的特例，所以**全部落在单位圆上**、等间隔、构成**正 $n$ 边形**。

**递推关系**：$\omega_0=1=e^{i\cdot 0}$，且

$$\omega_{k-1}\omega=e^{\frac{2(k-1)\pi i}{n}}e^{\frac{2\pi i}{n}}=e^{\frac{2k\pi i}{n}}=\omega_k\qquad (k=1,\dots,n-1)$$

即**每个单位根都是前一个乘同一个 $\omega$ 得到的**（相邻差一个固定的单位因子）。

**小 $n$ 的样子**（画在单位圆上）：

| $n$ | 单位根 | 几何形状 |
|---|---|---|
| $3$ | $1$，$\omega=-\frac12+\frac{\sqrt3}{2}i$，$\omega^2=-\frac12-\frac{\sqrt3}{2}i$ | 正三角形顶点，辐角 $0^\circ,120^\circ,240^\circ$ |
| $4$ | $1,\ i,\ -1,\ -i$ | 正方形顶点（辐角 $0^\circ,90^\circ,180^\circ,270^\circ$） |
| $5$ | $1$，$e^{2\pi i/5}$，$e^{4\pi i/5}$，$e^{6\pi i/5}$，$e^{8\pi i/5}$ | 正五边形顶点（辐角 $0^\circ,72^\circ,144^\circ,216^\circ,288^\circ$） |

$n=5$ 的代数写法（用到黄金比）：$2\cos\frac{2\pi}{5}=\frac{\sqrt5-1}{2}$，所以 $e^{2\pi i/5}=\frac{\sqrt5-1}{4}+i\,\frac{\sqrt{10+2\sqrt5}}{4}$。三次的情况额外成立 $1+\omega+\omega^2=0$。

## 一般根 = 单位根的旋转 + 缩放

若 $z_k$ 是 $w=re^{i\theta}$ 的某个 $n$ 次方根，则

$$z_k=r^{1/n}e^{i\frac{\theta+2k\pi}{n}}=r^{1/n}e^{i\frac{\theta}{n}}\cdot e^{\frac{2k\pi i}{n}}=z_0\,\omega_k$$

**换句话说**：$w$ 的 $n$ 次方根可以由 **$n$ 次单位根先旋转、再伸缩（dilation）** 得到——把正 $n$ 边形按 $\frac{\theta}{n}$ 转个角度，再把半径从 $1$ 拉到 $r^{1/n}$。

这解释了根为什么"均匀分布"：**均匀性完全来自单位根的均匀性**，缩放与旋转都不破坏均匀性。

## 例 7：求 $w=-32$ 的全部五次方根（经典考题）

**第 1 步：化极形式。** $-32$ 是纯负实数：$r=|-32|=32$，实部为负、虚部为 $0$ → 第二象限正 $x$ 轴端点，$\theta=\pi$。所以

$$w=-32=32e^{i\pi}$$

**第 2 步：算两个关键量。** $r^{1/5}=32^{1/5}=2$（因为 $2^5=32$ ✓）。根的辐角用定位技巧：

$$\frac{\theta+2k\pi}{5}=\frac{\pi+2k\pi}{5}=\frac{\pi}{5}+k\cdot\frac{2\pi}{5}$$

**第 3 步：$k=0,1,2,3,4$ 逐个列出。**

| $k$ | $\varphi_k=\frac\pi5+k\frac{2\pi}5$ | 角度 | 根 $z_k=2e^{i\varphi_k}$ | 代数形式 |
|---|---|---|---|---|
| $0$ | $\frac\pi5$ | $36^\circ$ | $2e^{i\pi/5}$ | $\frac{1+\sqrt5}{2}+i\sqrt{\frac{5-\sqrt5}{2}}$ |
| $1$ | $\frac{3\pi}5$ | $108^\circ$ | $2e^{i3\pi/5}$ | $\frac{1-\sqrt5}{2}+i\sqrt{\frac{5+\sqrt5}{2}}$ |
| $2$ | $\pi$ | $180^\circ$ | $2e^{i\pi}$ | $-2$ |
| $3$ | $\frac{7\pi}5$ | $252^\circ$ | $2e^{i7\pi/5}$ | $\frac{1-\sqrt5}{2}-i\sqrt{\frac{5+\sqrt5}{2}}$ |
| $4$ | $\frac{9\pi}5$ | $324^\circ$ | $2e^{i9\pi/5}$ | $\frac{1+\sqrt5}{2}-i\sqrt{\frac{5-\sqrt5}{2}}$ |

数值：$2e^{i\pi/5}\approx1.6180+1.1756i$；$2e^{i3\pi/5}\approx-0.6180+1.9021i$；$2e^{i\pi}=-2$；$2e^{i7\pi/5}\approx-0.6180-1.9021i$；$2e^{i9\pi/5}\approx1.6180-1.1756i$。

（$2\cos\frac\pi5=\frac{1+\sqrt5}{2}$ 就是黄金比 $\varphi\approx1.618$；$2\sin\frac\pi5=\sqrt{\frac{5-\sqrt5}{2}}\approx1.1756$；$2\cos\frac{3\pi}5=\frac{1-\sqrt5}{2}\approx-0.618$，$2\sin\frac{3\pi}5=\sqrt{\frac{5+\sqrt5}{2}}\approx1.9021$。）

**验算**：

- $k=2$ 最容易验：$(-2)^5=-32$ ✓。
- $k=0$：模 $=\sqrt{1.6180^2+1.1756^2}=\sqrt{2.6180+1.3820}=2$ ✓，辐角 $=\arctan\frac{1.1756}{1.6180}=\arctan 0.7265=36^\circ=\frac\pi5$ ✓。
- 结构自检：五个辐角 $36^\circ,108^\circ,180^\circ,252^\circ,324^\circ$ **相邻差 $72^\circ=\frac{2\pi}5$** ✓，全在半径 $2$ 的圆上 → 半径 $2$ 的**正五边形**，一个顶点在负实轴 $-2$ 处。✓

## 流程总结

1. 把 $w$ 化成极形式 $re^{i\theta}$（[[极形式]]：求 $r$、定象限求 $\theta$）。
2. 算 $r^{1/n}$（取正根）。
3. 套公式取 $k=0,1,\dots,n-1$：**第一个辐角 $\frac{\theta}{n}$，之后每个加 $\frac{2\pi}{n}$**。
4. 化回 $a+bi$（用特殊角值），或至少给出 $re^{i\varphi}$ 形式。
5. $k\geq n$ 一定是重复的，不要写。

## 关联

- 圆上的点 → [[复平面]]（根均匀分布在以原点为圆心的圆周上）
- 模与辐角 → [[极形式]]（$r^{1/n}$ 取正根、$\theta$ 定象限）
- 周期性与旋转 → [[复指数函数]]（$e^{i(\theta+2k\pi)}=e^{i\theta}$ 是根多值的直接原因）
- 关键一步 → [[De Moivre定理]]（由 $R^ne^{in\varphi}=re^{i\theta}$ 才能比较模与辐角）
- 单位根作特征值 → [[特征值与特征向量]]（旋转矩阵的特征值就是 $n$ 次单位根，共轭成对出现）
- 旋转可对角化 → [[对角化]]（用单位根作特征值，把旋转变成缩放，这是单位根最漂亮的用途）
