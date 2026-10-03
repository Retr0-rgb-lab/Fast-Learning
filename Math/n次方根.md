# n 次方根

归属 [[AMA2111 Lecture 01 复数]]。[[De Moivre 定理]] 的逆问题：$z^n = w$ 的全部解。

## 定理

设 $w = re^{i\theta} \neq 0$，则 $w$ 的 n 次方根恰有 **n 个**：

$$z_k = r^{1/n} e^{i\frac{\theta+2k\pi}{n}} = r^{1/n}\Big(\cos\tfrac{\theta+2k\pi}{n} + i\sin\tfrac{\theta+2k\pi}{n}\Big),\qquad k = 0,1,\dots,n-1$$

（$r^{1/n}$ 取正实根。）

**证明思路**：设 $z = Re^{i\varphi}$，$z^n = R^n e^{in\varphi} = re^{i\theta}$ ⟹ $R^n=r$（唯一）且 $n\varphi = \theta+2k\pi$；由 $\sin,\cos$ 的周期性，$k=0,\dots,n-1$ 恰给 n 个互异解。

## 几何结构（考点）

- n 个根**均匀分布在**半径 $r^{1/n}$ 的圆上，是**正 n 边形的顶点**
- 定位技巧：$\dfrac{\theta+2k\pi}{n} = \dfrac{\theta}{n} + k\cdot\dfrac{2\pi}{n}$ —— 第一个根在辐角 $\theta/n$，之后每个加 $2\pi/n$

## 单位根

$w=1$ 的 n 次方根记 $\omega_k = e^{2k\pi i/n}$，$0\le k\le n-1$：

- 全部在单位圆上，构成正 n 边形（$n=3,4,5$ 图见讲义 p26）
- $\omega_0=1$，$\omega_{k-1}\cdot\omega = \omega_k$（相邻差常数倍）
- 三次单位根特例：$\omega = -\frac12+\frac{\sqrt3}{2}i$，$\omega^2 = -\frac12-\frac{\sqrt3}{2}i$，$1+\omega+\omega^2=0$

## 一般根 = 单位根的旋转 + 缩放

$$z_k = r^{1/n}e^{i\theta/n}\cdot\omega_k = z_0\,\omega_k$$

即：任一根 × 单位根 = 其余各根（先旋转后缩放）。这解释了根的"均匀分布"从何而来。

**流程**：化 $w$ 为 [[极形式]] → 套公式取 $k=0,\dots,n-1$ → 验算 $k\ge n$ 会重复。
