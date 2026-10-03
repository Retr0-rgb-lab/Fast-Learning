---
tags:
  - opencv
  - pytorch
  - 张量排布
  - 深度学习
created: 2026-09-07
type: 知识点
aliases:
  - NCHW
  - NHWC
  - channels first
  - channels last
domain: [计算机视觉, 图像处理]
course: COMP 4423 Easy Computer Vision
来源: "自学补充（课程未覆盖，PyTorch 侧衔接）"
---

# NCHW 与 NHWC 张量排布

图像张量在内存里有两种主流排布，PyTorch 和 OpenCV/TensorFlow 用的不一样。

## 两种排布

| 排布 | 形状 | 谁默认用 |
| ---- | ---- | ---- |
| **NCHW**（channels first） | `(B, C, H, W)` | PyTorch、ONNX、Caffe |
| **NHWC**（channels last） | `(B, H, W, C)` | TensorFlow、很多 CPU/移动端推理 |

PIL、OpenCV 读图一般是 `(H, W, C)`（无 batch）。`transforms.ToTensor()` 或 `v2.ToImage()` 会改成 `(C, H, W)`，再经 DataLoader 堆成 `(B, C, H, W)`，才能直接进 `nn.Conv2d`。

## `(B, 3, 32, 32)` 是什么

四个数依次是：

| 维 | 含义 | 例 |
| :-- | :-- | :-- |
| `B` | batch，一次送进网络的样本数 | 64 |
| `3` | 通道数 C | RGB |
| `32` | 高 H | 32 像素 |
| `32` | 宽 W | 32 像素 |

→ **B 张 32×32 的彩色图**。CIFAR-10 就是这个尺寸。

`nn.Conv2d` 默认吃这种 4D 输入 `(N, C_in, H, W)`。若写成 `(B, 32, 32, 3)` 那是 NHWC（TensorFlow 常见），直接丢给 PyTorch 卷积会错。

## 写法不同，效果一样

```python
# PyTorch
x = torch.randn(B, C, H, W)

# TensorFlow
x = tf.random.normal([B, H, W, C])
```

## 为什么分两种

- **历史**：早期 NVIDIA cuDNN 在 NCHW 上更快，所以 PyTorch/ONNX 一直用 NCHW
- **新趋势**：很多 GPU 算子（尤其 TensorRT、移动端 NPU）更喜欢 NHWC 的内存布局
- **混用方式**：PyTorch 提供 `tensor.to(memory_format=torch.channels_last)`，**shape 仍写成 `(B,C,H,W)`，但内存按 NHWC 排**——给现代硬件用，但 `shape` 看到的还是 4 维

## 是不是行业规定

**不是全行业统一，是 PyTorch（以及 ONNX、Caffe）的默认约定。** TensorFlow 默认是 NHWC。换框架或导出时要注意转置，否则通道维会对错。

## 在 OpenCV ↔ PyTorch 转换里

```python
import cv2, numpy as np

img = cv2.imread("cat.jpg")           # (H, W, 3) HWC BGR
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
x = rgb.astype("float32") / 255.0    # 仍 HWC
x = np.transpose(x, (2, 0, 1))       # CHW
x_torch = torch.from_numpy(x)         # (3, H, W)
x_batch = x_torch.unsqueeze(0)         # (1, 3, H, W) = NCHW
```

## 一句话

> 写 PyTorch 模型就按 `(B, C, H, W)`；换框架或导出时注意转置，否则通道维对错。

## 相关笔记

- **下游 (PyTorch)**：[[Tensor 基础]] — 图像张量形状约定
- **使用**：[[OpenCV PyTorch 预处理流水线]] — 转 CHW 是最后一步
- **来源**：[[图像读取与通道顺序]] — 从 HWC+BGR 出发
- **维度追踪**：[[CNN 维度追踪（CIFAR-10 两层卷积）]] — CIFAR-10 输入就是 `(N, 3, 32, 32)`

## 参考

- [PyTorch memory_format 文档](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.memory_format)
