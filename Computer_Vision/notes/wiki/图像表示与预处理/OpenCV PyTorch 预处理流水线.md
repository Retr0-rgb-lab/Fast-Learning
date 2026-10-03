---
tags:
  - opencv
  - pytorch
  - 计算机视觉
  - 数据预处理
created: 2026-09-07
type: 知识点
aliases:
  - cv2.dnn.blobFromImage
  - 预处理流水线
  - preprocessing
domain: [计算机视觉, 图像处理]
course: COMP 4423 Easy Computer Vision
来源: "自学补充（课程未覆盖，PyTorch 侧衔接）"
---

# OpenCV-PyTorch 预处理流水线

把原始照片变成 PyTorch 能吃的 batch 张量，标准流水线：

```text
原始照片 (H, W, 3) BGR
→ cv2.resize（缩放到目标尺寸）
→ cv2.cvtColor (BGR → RGB)
→ 像素归一化 (0-255 → 0-1 或 -1-1)
→ transpose (HWC → CHW)
→ 加 batch 维
→ 输入 PyTorch 模型
```

## 完整示例（手动）

```python
import cv2
import numpy as np
import torch

img = cv2.imread("cat.jpg")               # (H, W, 3) BGR uint8
resized = cv2.resize(img, (224, 224))     # (224, 224, 3)
rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
x = rgb.astype("float32") / 255.0         # 归一化到 [0,1]
x = x.transpose(2, 0, 1)                  # HWC → CHW
x = torch.from_numpy(x)                   # (3, 224, 224)
x = x.unsqueeze(0)                         # (1, 3, 224, 224) = NCHW
y = model(x)
```

## 一次性合成：`cv2.dnn.blobFromImage`

如果走 OpenCV DNN 模块，几步操作可以合成一次调用：

```python
blob = cv2.dnn.blobFromImage(
    img,
    scalefactor=1/255.0,    # 像素归一化
    size=(224, 224),         # resize 目标
    mean=(0, 0, 0),          # 减均值（可选）
    swapRB=True,             # BGR↔RGB
    crop=False               # 不裁剪
)
# 形状 (1, 3, 224, 224)
```

内部会：resize → scale → swapRB → NCHW 加 batch 维。

> [!warning] 不一定符合所有 PyTorch 模型
> `blobFromImage` 设计给 OpenCV DNN 用，mean/std 默认是 `(0,0,0)/(1,1,1)`。很多训练过的 PyTorch 模型用别的 mean/std（CIFAR-10 ≈ `(0.49, 0.48, 0.44)`，ImageNet `(0.485, 0.456, 0.406)`），需要手动 `Normalize`。

## 跟 torchvision transforms 的对比

OpenCV 手动版适合推理脚本（一次性、不需要 `Dataset`/`DataLoader`）。训练时需要可复现、随机增强、批处理——通常用 torchvision `transforms.v2.Compose` 在 `Dataset` 里做，见 [[Transforms 数据转换]]。

| | OpenCV 手动 | torchvision transforms |
| ---- | ---- | ---- |
| 适用 | 推理脚本、单张图 | 训练、`Dataset` 集成 |
| 数据增强 | 自己写 | 内置 RandomCrop / Flip / 等 |
| 颜色空间 | 默认 BGR，要 `cvtColor` | 自动转 RGB |
| 形状 | 手写 `transpose` | 自动 CHW |
| 批处理 | 自己加 batch 维 | DataLoader 自动 |

## 常见坑

1. **BGR 没转 RGB**：颜色全偏，红变蓝
2. **`cv2.resize` 的 `dsize` 是 `(W, H)`**：写反成 `(H, W)` 图像扭曲
3. **没归一化 / 用了错误的 mean/std**：模型输出完全错
4. **没 transpose**：模型报错 shape 不对
5. **letterbox 写反了 `pad` 方向**：见 [[缩放与插值]]

## 数据加载三层关系

- **DataLoader**：负责"运送数据"——按 batch 取、打乱、多进程加载
- **Dataset / Transform**：负责"加工图像"——读图、转格式、缩放、归一化、增强
- **PyTorch 模型**：负责"从加工后的数据学规律"

OpenCV 可以出现在 Dataset 的 transform 里（处理单张图）或独立预处理（推理脚本）。

## 相关笔记

- **前置**：[[OpenCV 是什么]] — 整体认识
- **基础**：[[图像读取与通道顺序]] / [[缩放与插值]] / [[旋转]]
- **格式**：[[NCHW 与 NHWC 张量排布]]
- **PyTorch 端**：[[Transforms 数据转换]] — 训练时用 `v2.Compose`
- **PyTorch 端**：[[Tensor 基础]] — Tensor 形状约定
- **维度追踪**：[[CNN 维度追踪（CIFAR-10 两层卷积）]] — `conv1` 吃 `(N, 3, 32, 32)` 的 CIFAR 图

## 参考

- [OpenCV DNN module](https://docs.opencv.org/4.x/d6/d0f/group__dnn.html)
