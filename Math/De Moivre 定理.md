# De Moivre 定理

归属 [[AMA2111 Lecture 01 复数]]。[[极形式]] + [[复指数函数]] 的直接产物。

## 定理（乘除）

$z_1 = r_1e^{i\theta_1},\ z_2 = r_2e^{i\theta_2}\neq0$：

$$z_1 z_2 = r_1 r_2 e^{i(\theta_1+\theta_2)}, \qquad \frac{z_1}{z_2} = \frac{r_1}{r_2}e^{i(\theta_1-\theta_2)}$$

即：**模相乘除，辐角相加减**。

## 推论（乘方）

$$z^n = r^n e^{in\theta} = r^n(\cos n\theta + i\sin n\theta), \quad n\in\mathbb Z$$

## 证明要点（讲义留给练习的部分）

乘法版：把 $r(\cos\theta+i\sin\theta)$ 直接展开相乘，实部出现 $\cos\theta_1\cos\theta_2-\sin\theta_1\sin\theta_2 = \cos(\theta_1+\theta_2)$，虚部出现 $\sin(\theta_1+\theta_2)$（和角公式 + $\sin^2+\cos^2=1$）。除法版与乘方版用归纳/指数律。

## 实战套路

1. $(1+i)^{10}$ 这类：先化 $r e^{i\theta}$，再 $r^{10}e^{i10\theta}$，最后化回代数形式
2. 乘/除 $\sqrt3+i$、$1-i$ 这类：极形式下辐角一加一减，秒杀
3. 高次幂结果化回 $a+bi$ 时用 $\cos,\sin$ 的特殊角值

逆问题（$z^n=w$ 已知 $w$ 求 $z$）→ [[n次方根]]。
