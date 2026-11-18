# [論文筆記] Speech Emotion Recognition: Comparative Analysis of CNN-LSTM and Attention-Enhanced CNN-LSTM Models

- **引用出處**：[Bhanbhro et al. (2025)](https://doi.org/10.3390/signals6020022)
- **完整文獻**：Bhanbhro, J., Memon, A.A., Lal, B., Talpur, S., & Memon, M. (2025). Speech Emotion Recognition: Comparative Analysis of CNN-LSTM and Attention-Enhanced CNN-LSTM Models. *Signals*, 6(2), 22.
- **原始檔案**：`raw/signals-06-00022-v2.pdf`
- **關聯頁面**：
  - [語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
  - [SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
  - [卷積神經網路於 SER 之應用](../architectures/cnn-for-ser.md)
  - [卷積循環神經網路架構](../architectures/crnn-architectures.md)
  - [注意力機制於語音情緒辨識](../architectures/attention-mechanisms.md)

---

## 1. 研究背景與動機 (Motivation)
- **副語言語音線索 (Paralinguistics)**：語音除語意文字外，包含音高（Pitch）、音量（Volume）、語調（Intonation）與語速（Speech Rate）等情緒載體。
- **SER 核心挑戰**：
  - 說話者差異（個體音色、年齡、性別、口音）。
  - 背景雜訊干擾。
  - 情緒表達之主觀性與文化語境差異。
  - 高品質標註語料庫匱乏與類別不平衡。
- **研究問題**：探討 2D CNN-LSTM 與結合雙向 LSTM 及注意力機制的 Attention-Enhanced CNN-LSTM 在情緒辨識率與雜訊泛化性上的差異。

---

## 2. 音訊前處理與特徵提取 (Pre-Processing)
- **音訊格式標準化**：統一採樣率至 16 kHz，並修剪靜音片段（Trimming silent segments）。
- **短時窗分析 (Windowing)**：窗長 25 ms，重疊步長 10 ms。
- **傅立葉變換與梅爾頻譜圖**：
  - 訊號加窗：$x(n) = \sum_{m=0}^{M-1} w(m) \cdot s(n+m)$
  - 離散傅立葉轉換：$X(k) = \sum_{n=0}^{N-1} x(n) \cdot e^{-j \frac{2\pi}{N} kn}$
  - 梅爾轉換刻度：$M(f) = 2595 \log_{10}(1 + \frac{f}{700})$
  - 最終輸出二維單通道梅爾頻譜圖（Mel Spectrogram）。

---

## 3. 雜訊增強策略 (Noise Augmentation)
為解決模型過擬合（Overfitting）於實驗室乾淨語料的問題，本研究在波形端引入雜訊資料增強：
1. **正規化常數**（16 位元音訊）：
   $$\text{norm\_constant} = 2^{(\text{num\_bits}-1)}$$
   $$\text{signal\_norm} = \frac{\text{signal}}{\text{norm\_constant}}, \quad \text{noise\_norm} = \frac{\text{noise}}{\text{norm\_constant}}$$
2. **訊雜比 (SNR) 動態縮放**：
   在 15 dB 至 30 dB 範圍內隨機取樣目標 $\text{target\_snr}$：
   $$K = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}}}} \cdot 10^{-\frac{\text{target\_snr}}{10}}$$
   $$\text{noisy\_signal} = \text{signal} + K \cdot \text{noise}$$
- Model 1 採用均勻分佈雜訊（Uniform Noise），Model 2 採用加性高斯白雜訊（Additive White Gaussian Noise, AWGN）。

---

## 4. 深度學習模型架構 (Model Architectures)

### 4.1 Model 1: Time Distributed 2D CNN-LSTM
- **CNN 特徵萃取前段**：包含 6 個時間分佈 2D CNN 區塊（Time Distributed 2D CNN Blocks），濾波器數量依序倍增（8, 16, 32, 64, 128, 256）。
  - Block 1–2：$5 \times 5$ 卷積核，stride=1, padding=2，配合 Batch Normalization、ELU 活化函數與 $2 \times 2$ Max Pooling（stride 2）。
  - Block 3：$3 \times 3$ 卷積核，padding=1，配合 $2 \times 2$ Max Pooling。
  - Block 4–6：$3 \times 3$ 卷積核，padding=1，配合 $4 \times 4$ Max Pooling（stride 4）。
  - 每個 Pooling 層後接 Dropout（比率 0.2）。
- **時序與全連接分類器**：Flatten 後輸入 Dense 層降維，接標準 Softmax 輸出 8 種情緒類別機率。

### 4.2 Model 2: Stacked Time Distributed 2D CNN–BiLSTM with Attention
- **雙向 LSTM (BiLSTM)**：同時自正向與反向處理時序特徵序列：
  $$\overrightarrow{\mathbf{h}}_t = \text{LSTM}(\mathbf{x}_t, \overrightarrow{\mathbf{h}}_{t-1}), \quad \overleftarrow{\mathbf{h}}_t = \text{LSTM}(\mathbf{x}_t, \overleftarrow{\mathbf{h}}_{t+1})$$
  $$\mathbf{h}_t = [\overrightarrow{\mathbf{h}}_t \,;\, \overleftarrow{\mathbf{h}}_t]$$
- **自注意力機制 (Self-Attention)**：對 BiLSTM 隱藏狀態動態打分，聚合最具情緒顯著性的片段：
  $$e_t = \tanh(\mathbf{W}_a \mathbf{h}_t + \mathbf{b}_a)$$
  $$\alpha_t = \frac{\exp(e_t)}{\sum_{i=1}^T \exp(e_i)}$$
  $$\mathbf{c} = \sum_{t=1}^T \alpha_t \mathbf{h}_t$$
- **輸出層**：$\mathbf{y} = \text{softmax}(\mathbf{W}_c \mathbf{c} + \mathbf{b}_c)$。

---

## 5. 資料集與實驗設定 (Experimental Setup)
- **核心資料集**：RAVDESS（Ryerson Audio-Visual Database of Emotional Speech and Song）
  - 1440 筆音訊檔，24 位專業演員（12 男 12 女），8 種情緒（Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprise）。
- **資料切分協議**：
  - 80% 訓練集、10% 驗證集、10% 測試集。
  - 採用時間分割（Temporal separation：早期錄音作為訓練，晚期作為測試）以降低過擬合。
- **硬體與訓練超參數**：
  - GPU：NVIDIA RTX 3080，Batch Size 32，訓練 200 Epochs。
  - 優化器：Adam，損失函數：Categorical Cross-Entropy。

---

## 6. 實驗結果與消融實驗 (Results & Ablation)

### 6.1 整體準確率比較
| 模型配置 | 增強策略 | 測試集準確率 (Accuracy) | 訓練時間 (200 Epochs) |
| :--- | :--- | :--- | :--- |
| **Model 1: 2D CNN-LSTM** | 無雜訊增強 | 80.0% | - |
| **Model 1: 2D CNN-LSTM** | 均勻雜訊 (Uniform Noise) | **96.5%** | 71 分鐘 |
| **Model 2: 2D CNN-BiLSTM + Attention** | 無雜訊增強 | 85.0% | - |
| **Model 2: 2D CNN-BiLSTM + Attention** | AWGN 高斯白雜訊 | **98.1%** | 103 分鐘 |

### 6.2 消融實驗結論 (Ablation Analysis)
- **LSTM 模組影響**：在 Model 2 中若移除 LSTM，準確率自 98.1% 顯著下滑至 95.0%，證實長程時序依賴建模的必要性。
- **雙向機制影響**：若將雙向 BiLSTM 改為單向 LSTM，準確率降至 89.0%，顯示雙向語境對捕捉完整情緒起伏的重要性。
- **Dropout 影響**：若省略 Dropout，驗證損失（Validation Loss）上升 15%，出現明顯過擬合現象。
- **注意力機制價值**：Attention 模組使模型在相近情緒（如 Calm vs Neutral、Sad vs Neutral）的分辨率大幅提升。

---

## 7. 論文局限性與批判性思考 (Limitations)
1. **資料集限制**：實驗主要集中於 RAVDESS（北美口音、演員表演型情緒），尚未在大規模多語言或真實日常對話語料（如自然自發情緒）中進行廣泛檢驗。
2. **跨語料庫泛化驗證初步**：作者僅在 SAVEE 資料集抽取 7 筆樣本進行初步零樣本推斷（正確辨識 5 筆），跨語料庫泛化（Cross-corpus Generalization）仍待全面評測。
3. **單模態限制**：雖然 RAVDESS 原生包含影像，本篇僅使用純語音，未融合人臉表情多模態資訊。
4. **計算成本權衡**：Model 2 引入雙向結構與注意力後，訓練時間自 71 分鐘增至 103 分鐘（增加約 45%）。
