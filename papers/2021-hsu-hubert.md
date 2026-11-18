# [論文筆記] HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units

- **引用出處**：[Hsu et al. (2021)](https://arxiv.org/abs/2106.07447)
- **完整文獻**：Hsu, W.-N., Bolte, B., Tsai, Y.-H.H., Lakhotia, K., Salakhutdinov, R., & Mohamed, A. (2021). HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, 29, 3451–3460.
- **原始檔案**：`raw/2106.07447v1 (1).pdf`
- **關聯頁面**：
  - [語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
  - [SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
  - [卷積神經網路於 SER 之應用](../architectures/cnn-for-ser.md)
  - [注意力機制於語音情緒辨識](../architectures/attention-mechanisms.md)
  - 引用本模型之 SER 研究：[Pendyala et al. (2025) LiSER](../papers/2025-pendyala-liser-distillation.md)

---

## 1. 研究背景與核心動機 (Motivation)
- **語音訊號與文字之本質差異**：
  1. 連續取值而非離散字詞：語音為連續聲學波形，無預先定義的詞彙庫（Lexicon）。
  2. 無明確單元邊界：音素長度可變，且不存在天然的詞邊界切分。
  3. 單句包含多重聲學單元：無法直接套用電腦視覺中的實例分類（Instance Classification）對比學習。
- **現存對比學習之局限 (wav2vec 2.0)**：依賴負樣本採樣策略、多樣性損失（Diversity Loss）與 Gumbel-Softmax 退火排程，訓練不穩定性較高。
- **核心主張 (Hidden Unit BERT)**：提出透過**離線無監督分群（Offline K-means Clustering）**將連續語音離散化為隱藏單元（Hidden Units），並結合類 BERT 的**遮罩預測損失（Masked Prediction Loss）**，強制模型在遮蔽區域同時學習聲學模型與語言上下文結構。

---

## 2. 模型架構與前處理 (Model Architecture)

HuBERT 包含一維卷積波形編碼器與 Transformer 編碼器（Figure 1）：

### 2.1 卷積波形編碼器 (Convolutional Waveform Encoder)
- 7 層時間卷積層（通道數皆為 512）：
  - 步長（Strides）：$[5, 2, 2, 2, 2, 2, 2]$（總下採樣率為 320 倍）。
  - 卷積核寬度（Kernel widths）：$[10, 3, 3, 3, 3, 2, 2]$。
  - 對 16 kHz 語音信號，每 20 ms 輸出一組特徵向量。

### 2.2 Transformer BERT 編碼器規格 (Table I)
| 規格配置 | BASE 模型 | LARGE 模型 | X-LARGE 模型 |
| :--- | :---: | :---: | :---: |
| **參數量 (Params)** | **95M** | **317M** | **964M (~1B)** |
| **Transformer 層數** | 12 | 24 | 48 |
| **嵌入維度 (Embedding Dim)** | 768 | 1024 | 1280 |
| **前饋層維度 (FFN Dim)** | 3072 | 4096 | 5120 |
| **注意力頭數 (Attention Heads)** | 8 | 16 | 16 |
| **投影層維度 (Projection Dim)** | 256 | 768 | 1024 |

---

## 3. 隱藏單元挖掘與迭代分群 (Acoustic Unit Discovery & Iteration)

### 3.1 迭代式標籤精煉 (Iterative Refinement)
1. **第 1 次迭代 (Iteration 1)**：在 960 小時 LibriSpeech 語音的 39 維 MFCC 特徵（13 維係數加一、二階差分）上執行 K-means 分群，生成 $C=100$ 個類別作為初始標籤。
2. **第 2 次迭代 (Iteration 2)**：利用第 1 次訓練完成的 BASE 模型第 6 層 Transformer 隱藏特徵，重新執行 K-means 分群，產生 $C=500$ 個更精細的聲學標籤。
3. **第 3 次迭代 (Iteration 3)**：利用第 2 次迭代模型的第 9 層特徵分群訓練 LARGE 與 X-LARGE 模型。

### 3.2 評估分群質量的三大指標 (Metrics of Target Quality)
- **音素純度 (Phone Purity)**：衡量每個分群內主要音素的集中度。
- **分群純度 (Cluster Purity)**：衡量相同音素落入同一分群的集中度。
- **音素正規化互資訊 (Phone-Normalized Mutual Information, PNMI)**：
  $$\frac{I(y; z)}{H(y)} = 1 - \frac{H(y|z)}{H(y)}$$
  實證顯示，從 MFCC（PNMI 0.253）到 BASE-it2（PNMI 0.686），標籤純度大幅提升，說明模型能逐步自發發現真實底層語音學單元。

---

## 4. 預訓練損失函數 (Pre-training Objectives)

令遮罩時間步集合為 $\mathcal{M} \subset [T]$（隨機選取 8% 幀作為起點，長度 $l=10$ 的 span 遮罩）。遮罩預測損失定義為：

$$\mathcal{L}_m(f; X, M, Z) = \sum_{t \in M} \log p_f(z_t \mid \tilde{X}, t)$$

其中碼本類別 $c \in [C]$ 的機率分佈由投影向量與碼本嵌入的餘弦相似度 Softmax 計算：

$$p_f(c \mid \tilde{X}, t) = \frac{\exp\left(\text{sim}(A o_t, e_c) / \tau\right)}{\sum_{c'=1}^C \exp\left(\text{sim}(A o_t, e_{c'}) / \tau\right)}$$

- **關鍵消融發現（Table V）**：僅在**被遮蔽區域計算損失（$\alpha=1.0$）**表現最佳；若在未遮蔽區域計算損失（$\alpha=0.0$），WER 劇烈惡化（自 17.86% 惡化至 96.37%），證實強制模型依賴遠程語境重構聲學單元是表徵學習的關鍵。

---

## 5. 於語音情緒辨識 (SER) 之深遠影響與應用
- **SER 領域的特徵基石**：雖然 HuBERT 原文主要在 ASR 下游任務評測，但其萃取的全局上下文特徵隨後在各大情感運算 Benchmark（如 SUPERB、IEMOCAP、RAVDESS）成為最強特徵提取器。
- **跨模態蒸餾核心教師**：在 [Pendyala et al. (2025) LiSER](2025-pendyala-liser-distillation.md) 中，研究團隊即採用預訓練 `hubert-base-ls960` 作為語音情緒教師模型，透過 LoRA 微調後將其強大的聲學情緒語意傳遞給 105K 輕量化學生模型。

---

## 6. 研究限制 (Limitations)
1. 多階段訓練負擔：需反覆執行離線 K-means 分群與特徵提取，無法單階段端到端完成。
2. 龐大參數量：BASE 模型即達 95M，X-LARGE 高達 1B 參數，需數十至數百張 GPU 預訓練，在移動與邊緣設備上極度缺乏即時推理可行性。
