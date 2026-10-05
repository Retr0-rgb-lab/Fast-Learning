---
tags: [Math, 复数, DeMoivre定理, 乘方, 极形式]
aliases: ["De Moivre 定理"]
course: AMA2111
lecture: L01
---

# De Moivre 定理 · De Moivre's Theorem

> **一句话**：两个复数相乘，模相乘、辐角相加；相除则模相除、辐角相减——于是 $z^n=r^ne^{in\theta}$，乘方题变成"求 $n$ 倍角"。

课件原文见 [AMA2111-L01-ComplexNumbers.pdf](<../../raw/AMA2111-L01-ComplexNumbers.pdf>)。覆盖 §3 Polar Form 中的 De Moirve 一节（定理、推论与乘法版的证明）。

## 定理（乘与除）

设

$$z_1=r_1e^{i\theta_1}=r_1\left(\cos\theta_1+i\sin\theta_1\right),\qquad z_2=r_2e^{i\theta_2}=r_2\left(\cos\theta_2+i\sin\theta_2\right)\neq 0$$

则

$$z_1 z_2=r_1 r_2e^{i(\theta_1+\theta_2)}=r_1r_2\left[\cos(\theta_1+\theta_2)+i\sin(\theta_1+\theta_2)\right]$$

以及

$$\frac{z_1}{z_2}=\frac{r_1}{r_2}e^{i(\theta_1-\theta_2)}=\frac{r_1}{r_2}\left[\cos(\theta_1-\theta_2)+i\sin(\theta_1-\theta_2)\right]$$

一句话记忆：**模相乘除，辐角相加减。**

## 推论（De Moivre 公式，乘方）

若 $z=re^{i\theta}=r\left(\cos\theta+i\sin\theta\right)$，则对**任意整数** $n$：

$$z^n=r^ne^{in\theta}=r^n\left[\cos(n\theta)+i\sin(n\theta)\right]$$

> [!important] $n$ 可以是任意整数，不只是正整数
> $n<0$ 时由 [[复数与代数]] 的 $z^m=1/z^{-m}$ 与 $1/z=\bar z/|z|^2$ 一起得到 $z^n=r^ne^{in\theta}$（$r^n$ 与 $e^{in\theta}$ 都对负指数有意义）。所以这条公式对 $n\in\mathbb Z$ 全部成立。

## 证明要点

课件只完整示范了**乘法**，其余留作练习。用到的工具只有三个：和角公式、差角公式、勾股恒等式。

$$\sin(A\pm B)=\sin A\cos B\pm\cos A\sin B,\qquad \cos(A\pm B)=\cos A\cos B\mp\sin A\sin B,\qquad \sin^2\theta+\cos^2\theta=1$$

**乘法版（完整证明）**：把两个三角形式直接展开相乘。

$$
\begin{aligned}
z_1z_2
&=r_1r_2\left(\cos\theta_1+i\sin\theta_1\right)\left(\cos\theta_2+i\sin\theta_2\right)\\
&=r_1r_2\left[\cos\theta_1\cos\theta_2+i\cos\theta_1\sin\theta_2+i\sin\theta_1\cos\theta_2+i^2\sin\theta_1\sin\theta_2\right]\\
&=r_1r_2\left[\left(\cos\theta_1\cos\theta_2-\sin\theta_1\sin\theta_2\right)+i\left(\cos\theta_1\sin\theta_2+\sin\theta_1\cos\theta_2\right)\right]\\
&=r_1r_2\left[\cos(\theta_1+\theta_2)+i\sin(\theta_1+\theta_2)\right]\\
&=r_1r_2e^{i(\theta_1+\theta_2)}\quad ✓
\end{aligned}
$$

- **第 2 → 3 行**用 $i^2=-1$：$-i^2\sin\theta_1\sin\theta_2=+\sin\theta_1\sin\theta_2$ 挪到实部。
- **第 3 → 4 行**用和角公式：实部正是 $\cos(\theta_1+\theta_2)$，虚部正是 $\sin(\theta_1+\theta_2)$。

**除法版**（课件留作练习，做法照搬）：$\dfrac{z_1}{z_2}=\dfrac{r_1r_2[\cos(\theta_1+\theta_2)+i\sin(\theta_1+\theta_2)]}{r_2^2[\cos2\theta_2+i\sin2\theta_2]}$，分子分母同乘分母的共轭（[[共轭]]），分母变 $r_2^2$，再用**差角公式** $\cos(\theta_1-\theta_2)=\cos\theta_1\cos\theta_2+\sin\theta_1\sin\theta_2$ 整理。

**乘方版**：把乘法版反复用 $n-1$ 次（归纳法）即得 $z^n=r^ne^{in\theta}$；$n<0$ 用 $z^{-m}=1/z^m$ 反推。

> [!warning] 差角公式的符号是反的
> 记和角：$\cos(A+B)=\cos A\cos B-\sin A\sin B$（**减**）；记差角：$\cos(A-B)=\cos A\cos B+\sin A\sin B$（**加**）；$\sin$ 的加减正好相反。$z_1/z_2$ 走差角，符号写错就会得到 $z_1z_2$ 的辐角。

## 实战套路

1. **高次幂**：先化成 $re^{i\theta}$，再算 $r^n$ 与 $n\theta$，最后用 $\cos,\sin$ 的特殊角值化回 $a+bi$。
2. **乘除形如 $\sqrt3+i$、$1-i$ 的数**：极形式下辐角一加一减就完事，不用展开。
3. **化回代数形式时用特殊角值**：$0,\frac\pi6,\frac\pi4,\frac\pi3,\frac\pi2$ 的 $\cos,\sin$ 都要能张口就来（$\cos\frac\pi3=\sin\frac\pi6=\frac12$，$\cos\frac\pi6=\sin\frac\pi3=\frac{\sqrt3}{2}$，$\cos\frac\pi4=\sin\frac\pi4=\frac{\sqrt2}{2}$）。

### 例 4：把 $\sqrt3+i$ 与 $1-i$ 的积与商写成极形式

先化极形式（见 [[极形式]] 例 3）：

$$\sqrt3+i=2e^{i\pi/6},\qquad 1-i=\sqrt2\,e^{-i\pi/4}$$

**积**：模相乘、辐角相加。

$$\left(\sqrt3+i\right)(1-i)=2\sqrt2\,e^{i(\pi/6-\pi/4)}=2\sqrt2\,e^{-i\pi/12}=2\sqrt2\,e^{23i\pi/12}$$

（$\frac\pi6-\frac\pi4=\frac{2\pi-3\pi}{12}=-\frac{\pi}{12}$；因辐角只在模 $2\pi$ 意义下确定，写成 $\frac{23\pi}{12}$ 也对，见 [[极形式]]。）

**商**：模相除、辐角相减。

$$\frac{\sqrt3+i}{1-i}=\frac{2}{\sqrt2}\,e^{i\left(\frac\pi6+\frac\pi4\right)}=\sqrt2\,e^{i5\pi/12}=\sqrt2\,e^{i75^\circ}$$

**代数形式验算**（确认模与辐角都没错）：

积：$(\sqrt3+i)(1-i)=\sqrt3-\sqrt3 i+i-i^2=(\sqrt3+1)+(1-\sqrt3)i$。模 $=\sqrt{(\sqrt3+1)^2+(1-\sqrt3)^2}=\sqrt{(4+2\sqrt3)+(4-2\sqrt3)}=\sqrt8=2\sqrt2$ ✓；实部为正、虚部为负 → 第四象限，$\tan\angle=\frac{\sqrt3-1}{\sqrt3+1}=2-\sqrt3=\tan\frac{\pi}{12}$，故 $\arg=-\frac\pi{12}$，与定理一致 ✓。

商：$\dfrac{\sqrt3+i}{1-i}=\dfrac{(\sqrt3+i)(1+i)}{2}=\dfrac{(\sqrt3-1)+(\sqrt3+1)i}{2}$。模 $=\sqrt{\dfrac{(\sqrt3-1)^2+(\sqrt3+1)^2}{4}}=\sqrt{\dfrac{8}{4}}=\sqrt2$ ✓；实部虚部都为正 → 第一象限，$\tan\angle=\dfrac{\sqrt3+1}{\sqrt3-1}=2+\sqrt3=\tan\frac{5\pi}{12}$，故 $\arg=\frac{5\pi}{12}$，与定理一致 ✓。

### 例 5：计算 $(1+i)^{10}$（经典考题）

**第 1 步：把底数化极形式。** $1+i$：$r=\sqrt{1^2+1^2}=\sqrt2$；$\cos\theta=\frac{1}{\sqrt2}$、$\sin\theta=\frac{1}{\sqrt2}$，都正 → 第一象限，$\theta=\frac{\pi}{4}$。所以

$$1+i=\sqrt2\,e^{i\pi/4}$$

**第 2 步：用 De Moivre 推论，模取 10 次幂、辐角乘 10。**

$$(1+i)^{10}=\left(\sqrt2\right)^{10}e^{i\cdot 10\pi/4}=2^5e^{i5\pi/2}=32e^{i5\pi/2}$$

**第 3 步：把辐角化到 $[0,2\pi)$ 并求特殊角值。** $\frac{5\pi}{2}=2\pi+\frac{\pi}{2}$，而 $e^{i5\pi/2}=e^{i(2\pi+\pi/2)}=e^{i2\pi}e^{i\pi/2}=1\cdot i=i$（周期性，见 [[复指数函数]]）。于是

$$(1+i)^{10}=32\left(\cos\frac{5\pi}{2}+i\sin\frac{5\pi}{2}\right)=32\left(\cos\frac\pi2+i\sin\frac\pi2\right)=32(0+i)=32i$$

$$\boxed{(1+i)^{10}=32i}$$

**验算（用连乘法，完全独立的一条路）**：

$$
\begin{aligned}
(1+i)^2&=(1+i)(1+i)=1+2i+i^2=1-1+2i=2i\\
(1+i)^4&=(2i)^2=4i^2=-4\\
(1+i)^8&=(-4)^2=16\\
(1+i)^{10}&=(1+i)^8\cdot(1+i)^2=16\cdot 2i=32i\quad ✓
\end{aligned}
$$

两条路答案一致。

> [!warning] 第 3 步是最容易丢分的地方
> 1. **$32e^{i5\pi/2}$ 别直接当最终答案**——题面通常要 $a+bi$ 形式。用 $e^{i2\pi}=1$ 或 $\cos\frac{5\pi}{2}=\cos\frac\pi2$ 化简。
> 2. **辐角乘 $n$ 后可以超出一圈**：$\frac{10\pi}{4}=\frac{5\pi}{2}$ 已经超过 $2\pi$，这不是错误，只需化简。
> 3. **$r^n$ 是 $r$ 的 $n$ 次幂，不是辐角也变 $n$ 倍**。$(\sqrt2)^{10}=2^5=32$（因为 $(\sqrt2)^{2}=2$）。

## 逆向问题

已知 $z^n=w$ 求 $z$，就是这条推论反过来用：$r^n=|w|$、$n\theta=\arg w$。但辐角有 $2k\pi$ 的多值性，所以解**不止一个**——见 [[n次方根与单位根]]。

## 关联

- 三角形式前提 → [[极形式]]（$z=r(\cos\theta+i\sin\theta)$）
- 指数律前提 → [[复指数函数]]（$e^{i\theta_1}e^{i\theta_2}=e^{i(\theta_1+\theta_2)}$ 就是"辐角相加"）
- 逆向应用 → [[n次方根与单位根]]（$z^n=w$ 的全部解，关键一步是比较辐角）
- 辐角取负 → [[共轭]]（$\bar z=re^{-i\theta}$，共轭在极形式下是"辐角取负"）
- 复幂进入线性代数 → [[对角化的应用]]（$A^m=PD^mP^{-1}$ 中复特征值 $\lambda=re^{i\theta}$ 的 $\lambda^m$ 就是 De Moivre 公式）
- 复根给出实解 → [[二阶常系数齐次方程]]（辅助方程的共轭根对应 $e^{\alpha x}\cos\beta x,\ e^{\alpha x}\sin\beta x$）
