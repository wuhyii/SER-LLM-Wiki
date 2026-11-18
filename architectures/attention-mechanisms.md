# 注意力機制於語音情緒辨識 (Attention Mechanisms in SER)

> 本頁面已整合文獻實證數據。
> 最新匯入文獻：[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)
> 回到總覽：[首頁 (index.md)](../index.md)

---

## 1. 核心動機：情緒顯著性 (Emotional Salience)

在一段數秒至十餘秒的口語中，情緒訊號**並非均勻分佈**於所有時間幀上：
- 許多時間段落為靜音（Silence）、無聲輔音或平淡的中性語氣。
- 情緒的關鍵線索往往集中在少數**情緒爆發點（Emotional Salient Segments）**，例如重音加重、音高驟變（Pitch Jump）、嘆氣或破音。

傳統的平均池化（Mean-Pooling）會將關鍵情緒特徵被大量無關時間幀「稀釋」；注意力機制（Attention Mechanisms）允許模型為不同時間與頻率位置自動學習動態權重 $\alpha$，給予顯著特徵更高關注。

---

## 2. 典型注意力機制之數學推導

### 2.1 時序注意力聚合 (Temporal Attention Pooling)
給定由 [CRNN](crnn-architectures.md) 或 CNN 產生的時間特徵序列 $\mathbf{H} = [\mathbf{h}_1, \mathbf{h}_2, \dots, \mathbf{h}_T] \in \mathbb{R}^{T \times D}$。

透過可學習的投影層與注意力權重向量 $\mathbf{u} \in \mathbb{R}^{D_a}$ 計算能量評分：

$$e_t = \mathbf{u}^\top \tanh(\mathbf{W}_a \mathbf{h}_t + \mathbf{b}_a)$$

其中 $\mathbf{W}_a \in \mathbb{R}^{D_a \times D}$ 為注意力投影矩陣，$\mathbf{b}_a \in \mathbb{R}^{D_a}$ 為偏置。

利用 Softmax 函數對時間維度進行歸一化，獲得各時間步的注意力權重 $\alpha_t$：

$$\alpha_t = \frac{\exp(e_t)}{\sum_{\tau=1}^T \exp(e_\tau)}, \quad \text{滿足 } \sum_{t=1}^T \alpha_t = 1, \; \alpha_t \ge 0$$

最終聚合的整句情緒語意向量（Sentence-level Representation） $\mathbf{c} \in \mathbb{R}^D$ 為加權求和：

$$\mathbf{c} = \sum_{t=1}^T \alpha_t \mathbf{h}_t$$

---

### 2.2 縮放點積自注意力 (Scaled Dot-Product Self-Attention)
在引入 Transformer 架構的 SER 模型中，透過查詢（Query $\mathbf{Q}$）、鍵（Key $\mathbf{K}$）、值（Value $\mathbf{V}$）計算全域時間依賴：

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}}\right) \mathbf{V}$$

多頭注意力（Multi-Head Attention, MHA）使得模型能同時在不同時頻子空間關注多樣化的情緒表現模式（如音高起伏 vs 語速節奏）：

$$\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)\mathbf{W}^O$$

$$\text{head}_i = \text{Attention}(\mathbf{Q}\mathbf{W}_i^Q, \mathbf{K}\mathbf{W}_i^K, \mathbf{V}\mathbf{W}_i^V)$$

---

### 2.3 空間-時序二維注意力 (2D Spatial-Temporal Attention)
除了時間軸加權，部分 SER 架構同時對頻率軸進行加權，計算二維權重矩陣 $\mathbf{A} \in \mathbb{R}^{T \times F}$：

$$\mathbf{A}_{t, f} = \text{softmax}_{t, f}\left( f_{\text{attn}}(\mathbf{X}_{t, f}) \right)$$

使模型不僅能鎖定「何時」情緒爆發，還能鎖定「哪些頻帶」（如特定共振峰或基頻諧波）攜帶了關鍵情緒資訊。

---

## 3. 文獻實證與多層次注意力機制演進 (Empirical Evidence & Hierarchy)

在收錄的文獻中，注意力機制從簡單的「時間顯著性池化」演進至「多頭自注意力」乃至「多模態語言模型跨層注意力」：

### 3.1 時序自注意力池化 (Temporal Self-Attention Pooling)
- **[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)**：將自注意力機制置於雙向 BiLSTM 輸出端進行動態時序打分。消融實驗顯示，注意力模組顯著提升了模型對低喚醒度（Low Arousal）相近情緒（如 Neutral vs Calm、Sad vs Neutral）的區辨力，測試準確率提升至 **98.1%**。
- **[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md)**：在兩層 LSTM 之間插入雙曲正切（$\tanh$）自注意力層 $e_{i, j} = \boldsymbol{\omega}^\top \tanh(\mathbf{W} \mathbf{s}_{i-1} + \mathbf{v} \mathbf{h}_j + \mathbf{b})$，過濾多語料庫組合中的雜訊幀，使模型在 5160 筆樣本上取得 **90.19%** 的準確率。

### 3.2 Transformer 多頭自注意力 (Multi-Head Self-Attention in Foundation Models)
- **[Hsu et al. (2021) HuBERT](../papers/2021-hsu-hubert.md)**：將注意力機制規模化，在 Transformer 編碼器中堆疊 12 層（BASE，8 頭）至 48 層（X-LARGE，16 頭）的多頭自注意力（MHA）。MHA 能在不同頭部分工關注語音的語譜包絡、音高諧波與跨音素依賴，奠定了現代 SER 下游微調的特徵基礎。

### 3.3 音訊大型語言模型之全域注意力 (Global Attention in Audio-LLMs)
- **[Chu et al. (2024) Qwen2-Audio](../papers/2024-chu-qwen2-audio.md)**：透過 Whisper-large-v3 編碼器與 Qwen-7B 自回歸 Transformer，將音訊幀序列與文字 Prompt 視為一體，利用全域自注意力實現端到端的情緒對話與多模態共情推理（AIR-Bench 達 7.18 分）。

---

## 4. 關聯條目與文獻索引 (References & Cross-Links)
- 論文專頁：
  - [Bhanbhro et al. (2025) - 2D CNN-BiLSTM-Attention](../papers/2025-bhanbhro-cnn-lstm-attention.md)
  - [Singh et al. (2023) - 雙層 LSTM 夾心自注意力](../papers/2023-singh-attention-cnn-lstm.md)
  - [Hsu et al. (2021) - HuBERT Transformer 多頭自注意力](../papers/2021-hsu-hubert.md)
  - [Chu et al. (2024) - Qwen2-Audio 音訊語言自回歸注意力](../papers/2024-chu-qwen2-audio.md)
- 頻譜特徵：[語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
- 評估指標：[SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
- 前置架構：[CNN for SER](cnn-for-ser.md)、[CRNN 架構](crnn-architectures.md)
