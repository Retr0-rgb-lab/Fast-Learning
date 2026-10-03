---
tags:
  - 深度学习
  - softmax
  - 大词表
  - LLM
  - 训练效率
created: 2026-09-13
type: 知识点
aliases:
  - large vocabulary softmax
  - hierarchical softmax
  - negative sampling
  - BPE
---

# 大词表 Softmax:问题与解法

> [!info] 定位
> 当 softmax 用在词表上百万的语言模型里,朴素实现直接装不下显存。记几个绕开 softmax 全分类的实用方案。

## 一句话问题

softmax 在词表大小 $V$ 上的**线性开销**——$O(V)$ 计算 + $O(d\cdot V)$ 参数——百万词表下爆显存 + 训练极慢。

## 1. 朴素实现的三大开销

### 1.1 显存(主因)

输出层权重形状 `(hidden_size, vocab_size)`。$d=512$, $V=10^5$ → 这一层 5120 万参数,约 200 MB(fp32)。训练时还要存它的**梯度 + 优化器状态**:

$$
\text{总显存} \approx 200\text{MB} \times 3 \approx 600\text{MB per layer}
$$

只这一层,几个 GB 就没了。embedding 大头往往在最后一层。

### 1.2 计算慢

每步训练:
- `H @ W`:一次大矩阵乘
- softmax 对 $V$ 项求 $\exp + \text{sum}$ 算分母
- 反向传播同样规模

**总时间** ∝ $V$,百万词表 → 每次 forward/backward 都很重。

### 1.3 概率稀疏

$V=10^5$ 类,真实 token 的概率通常 $10^{-5} \sim 10^{-3}$,其余 ≈ 0。
- 梯度信号稀疏:正样本只贡献 1,负样本 $V-1$ 个里绝大部分梯度几乎为 0
- **训练效率极低**——大部分算力浪费在"已经预测为 0 的类"上

### 1.4 长尾词学不到

训练集出现次数 < 5 的词占很大比例;softmax 对每个 token 分到的更新次数太少,学不好。

## 2. 解法对照

| 方案 | 核心思路 | 显存 | 训练速度 | 代表 |
|:--|:--|:--|:--|:--|
| **负采样** | 算 1 正样本 + $k$ 个负样本 loss,丢弃其余 | $O(d)$ 嵌入+小分类器 | 大幅加速 | word2vec / 早期 GPT |
| **层次 softmax** | 把 vocab 建成二叉树,softmax 变 log$V$ 次二分类 | $O(d \log V)$ | 加速 $\log V$ 倍 | word2vec 另一变体 |
| **BPE / 子词** | 把词拆成更小单元,词表缩小 | $O(d \cdot V')$ $V' \ll V$ | 大幅加速 | 现代 LLM 标配 |
| **类簇 softmax** | 先预测词的"类",再在类内选词 | 折中 | 中等加速 | 早期 fastText |
| **对比学习** | 不做分类,直接学"距离" | $O(d)$ | 取决于 batch | Sentence-BERT 等 |
| **自适应 softmax** | 高频词放浅层、低频词放深层,树形 | 接近层次 softmax | 接近层次 softmax | 早期 fairseq |

## 3. 几个方案详细解释

### 3.1 负采样(Negative Sampling)

**思路**:把"多分类"换成"二分类判真假"。

- **正样本**:真实下一个词
- **负样本**:从词表随机采 $k$ 个(典型 $k=5\text{–}20$)
- **loss**:对正样本要 1,对负样本要 0——二分类交叉熵的累加

$$
L = -\log\sigma(v_{w_t}^\top h) - \sum_{i=1}^k \log\sigma(-v_{w_i}^\top h)
$$

其中 $w_t$ 是真实词,$w_i$ 是负样本。

**好处**:loss 只算 $1+k$ 个词,不需遍历 $V$。**显存 $O(d \cdot k)$**,训练快。
**坏处**:采样分布影响效果;负样本数 $k$ 是个超参。

### 3.2 层次 softmax(Hierarchical Softmax)

**思路**:把 vocab 排成二叉树(常用 Huffman 树,高频词浅、低频词深)。

- 一次 softmax 多分类 = 从根到叶子的 $\log_2 V$ 次二分类
- 路径上每个内部节点一个二分类器

**好处**:**$O(\log V)$ 训练**;不用采负样本。
**坏处**:推理时要算 $\log V$ 次二分类才能定叶子,比朴素 softmax 慢。**适合训练、不适合推理**。

### 3.3 BPE / 子词

**思路**:把"词"拆成更小的子单元(byte pair encoding 或 WordPiece):

- "unhappiness" → ["un", "happiness"] 或 ["un", "happy", "ness"]
- 词表大小从 10万 降到 3万
- 罕见词由子词拼出来,**完全没词表外(OOV)问题**

**好处**:词表本身缩小,softmax 一次计算就小。
**坏处**:要把同一个词切成多个 token,序列变长。

**BPE 是当前 LLM 的标配**——GPT-4、LLaMA、Qwen 都用。

### 3.4 类簇 softmax(Adaptive Softmax)

**思路**:把词按频率分桶:

- 头部高频词:$V_1$ 个,一层 softmax
- 腰部中频词:$V_2$ 个,另一层
- 尾部低频词:$V_3$ 个,更深层

每层只在自己桶内做 softmax。**高频词路径短 → 训练快**;**低频词路径长但样本少,总开销合理**。

## 4. 实际权衡

- **训练量 vs 实现复杂度**:朴素 softmax 实现简单但慢;负采样/层次 softmax 训练快但推理慢;BPE 中庸但需要 tokenization
- **小词表 (< 1万)**:朴素 softmax 完全 OK,**别过度优化**
- **中等词表 (1万–10万)**:BPE 改造词表往往够用
- **大词表 (> 10万)**:BPE + 负采样 / 对比学习

## 5. 一个判断清单

> 训练慢、显存吃紧 → 大词表 softmax?先做:
> 1. **用 BPE 缩小词表**(改 tokenizer,不动模型)
> 2. 如果还不行,**上负采样**(改 loss)
> 3. 最后才考虑**层次 softmax**(改模型架构)
>
> 朴素 softmax 一般不要直接打大词表——先用 tokenizer 优化词表。

## 相关笔记

- **基础**:[[Logits、Softmax 与 argmax]] — softmax 公式、数值稳定性、argmax 不最优
- **推导**:[[Softmax 回归与 MLE 推导]] — softmax 配交叉熵的 MLE 原理
- **工程**:[[交叉熵损失]] — `nn.CrossEntropyLoss` 的 reduction 与数值稳定性
- **应用**:大词表 softmax 主要用在 NLP / LLM 场景;此处只记 softmax 规模化本身的工程要点,具体语言模型实践见相关 NLP 资料

## 参考

- [word2vec 原始论文 (Mikolov 2013)](https://arxiv.org/abs/1301.3781)
- [Hierarchical Softmax 解释](https://www.tensorflow.org/extras/cse_hs_explain.html)
- [BPE 算法原理 (Sennrich et al. 2016)](https://arxiv.org/abs/1508.07909)
- [Adaptive Softmax (Grave 2017)](https://arxiv.org/abs/1609.04309)