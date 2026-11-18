# 卷積神經網路於 SER 之應用 (CNN for SER)

> 本頁面已整合文獻實證數據。
> 最新匯入文獻：[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)
> 回到總覽：[首頁 (index.md)](../index.md)

---

## 1. 核心動機：頻譜圖作為二維語音影像

在深度學習進入語音情緒辨識初期，研究者將[對數梅爾頻譜圖 (Log-Mel Spectrogram)](../concepts/speech-representations.md) 視為具有高度時空局部相關性的單通道影像：
- **時間軸（Time Axis）**：表徵音素轉換、語速變化與時序能量起伏。
- **頻率軸（Frequency Axis）**：表徵基頻（$F_0$）、共振峰（Formants）與能量諧波結構。

卷積神經網絡（CNN）透過**局部感知野（Local Receptive Fields）**與**權重共享（Weight Sharing）**，能夠有效捕捉頻譜圖中特定頻帶與時序範圍內的情緒線索（如激動情緒中的高頻能量激增）。

---

## 2. 數學原理與張量變換 (Mathematical Formulation)

### 2.1 2D 卷積操作 (2D Convolution)
令輸入張量為 $\mathbf{X} \in \mathbb{R}^{B \times C_{\text{in}} \times T \times F}$。第 $k$ 個卷積核權重為 $\mathbf{W}^{(k)} \in \mathbb{R}^{C_{\text{in}} \times K_t \times K_f}$，偏置為 $b^{(k)}$。

特徵圖（Feature Map）在時間位置 $t$ 與頻率位置 $f$ 的輸出為：

$$\mathbf{Y}^{(k)}[t, f] = \sigma\left( \sum_{c=1}^{C_{\text{in}}} \sum_{i=0}^{K_t - 1} \sum_{j=0}^{K_f - 1} \mathbf{W}^{(k)}[c, i, j] \cdot \mathbf{X}[c, t \cdot S_t + i, f \cdot S_f + j] + b^{(k)} \right)$$

其中：
- $K_t, K_f$ 分別為卷積核在時間維度與頻率維度的尺寸（Kernel Size）。
- $S_t, S_f$ 為卷積步長（Stride）。
- $\sigma(\cdot)$ 為非線性活化函數（如 ReLU 或 LeakyReLU）。

### 2.2 池化操作 (Pooling) 與維度折衷
最大池化（Max Pooling）在二維空間下運算：

$$\mathbf{P}^{(k)}[t, f] = \max_{0 \le i < P_t, 0 \le j < P_f} \mathbf{Y}^{(k)}[t \cdot P_t + i, f \cdot P_f + j]$$

- **時間軸池化**：降低時間長度以聚合巨觀語境，但可能抹平瞬間短暫的情緒爆發特徵。
- **頻率軸池化**：提升頻率位移不變性（Frequency Shift Invariance），但可能模糊音高（Pitch）精確位置。

---

## 3. 分類器與損失函數 (Classifier & Loss)

經過多層卷積與池化後，特徵圖經過全域平均池化（Global Average Pooling, GAP）或展平（Flatten）接全連接層，透過 Softmax 輸出情緒類別機率分佈 $\hat{\mathbf{y}} \in \mathbb{R}^C$：

$$\hat{y}_c = \frac{e^{z_c}}{\sum_{j=1}^C e^{z_j}}$$

標準交叉熵損失（Cross-Entropy Loss）計算為：

$$\mathcal{L}_{\text{CE}} = - \sum_{c=1}^C y_c \log \hat{y}_c$$

其中 $\mathbf{y}$ 為真實 One-Hot 標籤。

---

## 4. 局限性分析 (Limitations of Pure CNNs)
1. **長時序建模不足**：標準 2D CNN 依賴有限尺寸的卷積核，難以捕捉整句語音（數秒長度）的全域情感演進脈絡。
2. **時間對稱性假設**：CNN 預設輸入在空間方向具有對稱對稱性，但語音信號在時間維度上具備嚴格的單向因果性或時序語境關聯。
3. 促成後續引入循環神經網絡，形成 [CRNN 架構](crnn-architectures.md)。

---

## 5. 文獻里程碑實例與多樣態卷積設計 (Empirical Architectures)

在收錄的文獻中，卷積神經網路呈現出多種不同的演進型態：

### 5.1 1D 卷積 vs 2D 頻譜卷積
- **[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md)**：比對了 1D CNN 與 2D CNN 的效能。1D CNN 直接在一維時序特徵上卷積，難以捕捉跨頻帶的諧波相關性；升級為 4 個區塊的 2D CNN（64 通道、$3 \times 3$ 卷積核、BatchNorm、ReLU、MaxPool2D）後，在多資料集上的辨識準確率自 80.59% 躍升至 85.56%（加雜訊）。
- **[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)**：設計了 6 個時間分佈 2D CNN 區塊（Time-Distributed 2D CNN Blocks），通道數自 8 漸進式倍增至 256，並以 ELU 活化函數增強非線性表達力。

### 5.2 輕量化 3 區塊 2D CNN 特徵抽取器
- **[Pendyala et al. (2025) LiSER](../papers/2025-pendyala-liser-distillation.md)**：為適應邊緣設備，將 CNN 特徵前段極致精簡為 3 個 2D 卷積區塊（固定 64 通道，卷積核 $3 \times 3$），分別配置 $(2,2), (4,2), (4,1)$ 之非對稱最大池化，有效在壓縮頻率維度的同時保留關鍵時序長度，為整體模型僅 105K 參數立下基礎。

### 5.3 原始波形一維卷積編碼器 (Raw Waveform 1D Conv Encoder)
- **[Hsu et al. (2021) HuBERT](../papers/2021-hsu-hubert.md)**：跳過人工頻譜轉換，採用 7 層一維時序卷積直接對 16 kHz 原始波形進行特徵編碼（通道數 512，卷積核 $[10, 3, 3, 3, 3, 2, 2]$，步長 $[5, 2, 2, 2, 2, 2, 2]$），總下採樣達 320 倍，每 20 ms 產生一幀高階聲學向量，作為後續 Transformer 的輸入。

---

## 6. 關聯條目與文獻索引 (References & Cross-Links)
- 論文專頁：
  - [Bhanbhro et al. (2025) - 6 區塊時間分佈 2D CNN](../papers/2025-bhanbhro-cnn-lstm-attention.md)
  - [Singh et al. (2023) - 1D vs 2D 卷積與特徵消融](../papers/2023-singh-attention-cnn-lstm.md)
  - [Pendyala et al. (2025) - LiSER 3 區塊非對稱池化 2D CNN](../papers/2025-pendyala-liser-distillation.md)
  - [Hsu et al. (2021) - HuBERT 7 層原始波形卷積編碼器](../papers/2021-hsu-hubert.md)
- 頻譜特徵：[語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
- 延伸架構：[CRNN 架構](crnn-architectures.md)、[注意力機制](attention-mechanisms.md)
