# 卷積循環神經網路架構 (CRNN Architectures)

> 本頁面已整合文獻實證數據。
> 最新匯入文獻：[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)
> 回到總覽：[首頁 (index.md)](../index.md)

---

## 1. 核心動機：空間表徵與時序演進的結合

純 [CNN 模型](cnn-for-ser.md) 擅長捕捉局部時頻諧波特徵，但在捕捉整句語音的情感起伏脈絡上受限於有限的感知野。CRNN（Convolutional Recurrent Neural Network）架構將 CNN 與循環神經網路（如 LSTM 或 GRU）串聯：
1. **前段 CNN 特徵提取器**：將輸入的 Log-Mel 頻譜圖壓縮並抽象化為高階聲學特徵序列。
2. **後段 RNN 時序建模器**：對 CNN 萃取出的時序向量序列進行時序因果或雙向長程依賴建模。

---

## 2. 數學原理與張量流 (Mathematical Pipeline)

### 2.1 張量維度變換 (Tensor Transformations)
令輸入頻譜圖為 $\mathbf{X} \in \mathbb{R}^{B \times 1 \times T \times F}$。
1. **經過 CNN 模組**（包含卷積、BatchNorm 與池化）：
   $$\mathbf{Y}_{\text{CNN}} \in \mathbb{R}^{B \times C_{\text{out}} \times T' \times F'}$$
2. **頻率軸展平/投影（Frequency Flatten / Projection）**：
   將通道維度與頻率維度重塑為單一時序特徵向量：
   $$\mathbf{H}_{\text{seq}} = \text{Reshape}(\mathbf{Y}_{\text{CNN}}) \in \mathbb{R}^{B \times T' \times D}, \quad D = C_{\text{out}} \times F'$$
   （或透過二維平均池化將頻率維度壓縮至 1，使 $D = C_{\text{out}}$）。

### 2.2 雙向長短期記憶網絡 (Bidirectional LSTM, BiLSTM)
在時間步 $t \in [1, T']$，前向隱藏狀態 $\overrightarrow{\mathbf{h}}_t$ 與反向隱藏狀態 $\overleftarrow{\mathbf{h}}_t$ 依序計算：

$$\begin{aligned}
\mathbf{i}_t &= \sigma(\mathbf{W}_{ii} \mathbf{x}_t + \mathbf{b}_{ii} + \mathbf{W}_{hi} \mathbf{h}_{t-1} + \mathbf{b}_{hi}) \\
\mathbf{f}_t &= \sigma(\mathbf{W}_{if} \mathbf{x}_t + \mathbf{b}_{if} + \mathbf{W}_{hf} \mathbf{h}_{t-1} + \mathbf{b}_{hf}) \\
\mathbf{g}_t &= \tanh(\mathbf{W}_{ig} \mathbf{x}_t + \mathbf{b}_{ig} + \mathbf{W}_{hg} \mathbf{h}_{t-1} + \mathbf{b}_{hg}) \\
\mathbf{o}_t &= \sigma(\mathbf{W}_{io} \mathbf{x}_t + \mathbf{b}_{io} + \mathbf{W}_{ho} \mathbf{h}_{t-1} + \mathbf{b}_{ho}) \\
\mathbf{c}_t &= \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \mathbf{g}_t \\
\mathbf{h}_t &= \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
\end{aligned}$$

雙向隱藏狀態拼接後為：

$$\mathbf{h}_t^{\text{Bi}} = [\overrightarrow{\mathbf{h}}_t \,;\, \overleftarrow{\mathbf{h}}_t] \in \mathbb{R}^{2 \cdot D_{\text{hidden}}}$$

---

## 3. 時序池化至分類 (Temporal Pooling to Classifier)
在將時序特徵送入全連接層分類器前，常見三種聚合方式：
1. **取最後時間步輸出**：$\mathbf{h}_{\text{final}} = \mathbf{h}_{T'}^{\text{Bi}}$（容易遺失語音前段情感訊息）。
2. **全域時間平均池化（Mean-Pooling）**：
   $$\mathbf{h}_{\text{mean}} = \frac{1}{T'} \sum_{t=1}^{T'} \mathbf{h}_t^{\text{Bi}}$$
3. **加權時序注意力聚合（Attention Pooling）**：促成了結合 [注意力機制的架構](attention-mechanisms.md)。

---

## 4. 文獻實證與多樣態 CRNN 設計 (Empirical Evidence & Variants)

在收錄的實證研究中，CRNN 衍生出多種結合時間序列與注意力機制的變體：

### 4.1 雙層 LSTM 夾心注意力架構 (LSTM-Attention-LSTM)
- **[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md)**：設計了獨特的雙層 LSTM 夾心結構：
  - 前段 4 個 2D 卷積區塊完成特徵抽取後，送入第一層 LSTM（32 單元，`return_sequences=True`）產出各時間步隱藏狀態；
  - 中間接入自注意力層動態計算時間顯著度；
  - 接著送入第二層 LSTM（32 單元，`return_sequences=False`）僅輸出最終狀態向量送入 Dense 分類器。
  - 實證顯示此結構比純 CNN-2D 準確率高出近 5%（自 85.56% 提升至 90.19%）。

### 4.2 輕量化 CRNN 學生模型與多頭蒸餾架構
- **[Pendyala et al. (2025) LiSER](../papers/2025-pendyala-liser-distillation.md)**：將 CRNN 參數量壓縮至極致（僅 **105K 參數**）：
  - 結構為：3 個 2D 卷積區塊（64 通道）+ 1 層 LSTM（隱藏單元 64）；
  - 輸出端配置 3 個平行的多層感知機（MLP Heads），分別對應標籤分類（$g^{\text{sup}}$）、語音教師蒸餾（$g^{\text{sd}}$）與視訊教師跨模態蒸餾（$g^{\text{vd}}$）。
  - 證實了超輕量 CRNN 透過多模態知識蒸餾，能在嚴格跨說話者評測下達到 59.5% UAR，大幅縮小與龐大基底模型的差距。

### 4.3 雙向 BiLSTM 與消融分析
- **[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)**：系統性消融實驗證實：
  - 移除 LSTM 層：測試準確率自 98.1% 大幅下滑至 **95.0%**。
  - 將雙向 BiLSTM 降級為單向 LSTM：準確率進一步退步至 **89.0%**。
  - 顯示雙向時序上下文（同時自前向與後向捕捉情感演變）對語音情緒分類具有決定性影響。

---

## 5. 關聯條目與文獻索引 (References & Cross-Links)
- 論文專頁：
  - [Bhanbhro et al. (2025) - 2D CNN-BiLSTM 消融研究](../papers/2025-bhanbhro-cnn-lstm-attention.md)
  - [Singh et al. (2023) - 雙層 LSTM 夾心注意力 CRNN](../papers/2023-singh-attention-cnn-lstm.md)
  - [Pendyala et al. (2025) - LiSER 105K 輕量化 CRNN 蒸餾](../papers/2025-pendyala-liser-distillation.md)
- 基礎特徵：[語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
- 評估指標：[SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
- 前後置架構：[CNN for SER](cnn-for-ser.md)、[注意力機制於語音情緒辨識](attention-mechanisms.md)
