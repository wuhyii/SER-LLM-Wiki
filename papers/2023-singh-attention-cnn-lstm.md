# [論文筆記] Speech Emotion Recognition Using Attention Model

- **引用出處**：[Singh et al. (2023)](https://doi.org/10.3390/ijerph20065140)
- **完整文獻**：Singh, J., Saheer, L.B., & Faust, O. (2023). Speech Emotion Recognition Using Attention Model. *International Journal of Environmental Research and Public Health*, 20(6), 5140.
- **原始檔案**：`raw/ijerph-20-05140.pdf`
- **關聯頁面**：
  - [語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
  - [SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
  - [卷積神經網路於 SER 之應用](../architectures/cnn-for-ser.md)
  - [卷積循環神經網路架構](../architectures/crnn-architectures.md)
  - [注意力機制於語音情緒辨識](../architectures/attention-mechanisms.md)
  - 相關對比論文：[Bhanbhro et al. (2025)](2025-bhanbhro-cnn-lstm-attention.md)

---

## 1. 研究背景與動機 (Motivation)
- **心理健康監測與隱私保護**：語音情緒辨識（SER）在智慧醫療與遠距心理健康評估具有重要價值。為保護病患隱私，系統應專注於「如何表達」（聲學語音特徵）而非「所說內容」（文字語意）。
- **特徵組合迷思**：過去文獻中經常混用大量頻譜特徵與韻律節奏特徵（Rhythmic Features），本研究旨在透過消融實驗找出最具判別力且計算高效的特徵子集。
- **多數據集融合**：單一資料集規模有限，作者整合 RAVDESS、SAVEE 與 TESS 三大資料集，探討性別平衡與數據規模對模型泛化能力的影響。

---

## 2. 聲學特徵選擇實驗 (Feature Selection Experiments)
作者利用 Librosa 工具庫對多種頻譜特徵與節奏特徵進行了基準 1D-CNN 實驗（Table 1）：
- **測試特徵**：
  - 頻譜特徵：MFCC、梅爾頻譜（Mel-spectrogram）、零交叉率（ZCR）、頻譜質心（Spectral Centroid）、頻譜頻寬（Spectral Bandwidth）、頻譜滾降點（Spectral Roll-off）、均方根能量（RMS）、Chroma-STFT、Chroma-CENS、Spectral-Contrast。
  - 節奏特徵：節奏圖（Tempogram）、傅立葉節奏圖（Fourier-tempogram）。
- **關鍵實證結論**：
  - 單獨使用節奏特徵（Tempogram + F-temp）辨識率極低，僅為 **13.98%**。
  - 單獨使用 MFCC 即可達到 **85.00%** 的基準準確率。
  - 疊加額外節奏特徵不僅無法顯著提升準確率（85.70%），反而大幅增加模型參數量與計算開銷。
  - 最終選定 **MFCC** 作為後續模型的主要輸入特徵（採樣率 44.1 kHz，切分長度 2500 ms）。

---

## 3. 模型架構設計 (Model Architecture)

本架構串聯 4 個卷積區塊、LSTM、自注意力層與第二個 LSTM 層（Figure 5）：

```text
[輸入 MFCC 矩陣 (44.1kHz, 2500ms)]
              ↓
[4 個 2D 卷積區塊 (Conv2D 64, 3x3 + BatchNorm + ReLU + MaxPool2D + Dropout 0.2)]
              ↓
[LSTM 層 1 (32 單元, return_sequences=True)]
              ↓
[自注意力層 (Custom Self-Attention, tanh 活化)]
              ↓
[LSTM 層 2 (32 單元, return_sequences=False)]
              ↓
[Dense 密集層 (8 單元, SoftMax)] → 8 類情緒機率輸出
```

### 3.1 自注意力機制數學公式 (Attention Formulation)
在第一層 LSTM 生成的序列隱藏狀態中，注意力層透過雙曲正切活化動態計算特徵權重：
$$e_{i, j} = \boldsymbol{\omega}^\top \tanh(\mathbf{W} \mathbf{s}_{i-1} + \mathbf{v} \mathbf{h}_j + \mathbf{b})$$
$$\alpha_i = \text{Attend}(\mathbf{s}_{i-1}, \alpha_{i-1}, \bar{\mathbf{h}})$$
$$\mathbf{g}_i = \sum_{j=1}^L \alpha_{i, j} \mathbf{h}_j$$
此機制使模型能聚焦於承載核心情感語調的時間步，過濾語音中的無效靜音或冗餘特徵。

---

## 4. 資料集與實驗設定 (Experimental Setup)
- **組合資料集 (Customized Dataset)**：
  - **RAVDESS**：1920 筆音訊（24 位男女演員，8 種情緒）。
  - **SAVEE**：480 筆音訊（4 位男性，7 種情緒）。
  - **TESS**：2800 筆音訊（2 位女性，7 種情緒）。
  - 總計 **5160 筆音訊**，涵蓋 8 種情緒狀態（Angry, Calm, Disgust, Fear, Happy, Neutral, Sad, Surprise）。
- **訓練與驗證切分**：75% 訓練集（其中 25% 作為驗證集調優超參數），25% 為獨立測試集。
- **資料增強**：加入加性白雜訊（White Noise Augmentation）。

---

## 5. 實驗結果與核心發現 (Experimental Results)

### 5.1 增強策略與模型架構比較 (Table 2)
| 模型架構 | 是否加入雜訊增強 | 測試集準確率 (Accuracy) |
| :--- | :---: | :---: |
| CNN 2D | 否 | 80.59% |
| CNN 2D + LSTM | 否 | 81.52% |
| **CNN 2D + LSTM + Attention** | 否 | 83.05% |
| CNN 2D | 是 | 85.56% |
| CNN 2D + LSTM | 是 | 86.92% |
| **CNN 2D + LSTM + Attention (本文模型)** | **是** | **90.19%** |

### 5.2 個別資料集表現與性別差異分析 (Table 3 & Table 4)
- **個別資料集準確率**：
  - TESS（全女性）：**99.81%**
  - RAVDESS（男女平衡）：**74.44%**
  - SAVEE（全男性）：**57.50%**
  - 三者融合資料集：**90.19%**
- **性別聲學特性差異**：女性發音通常具有較高的基頻（Pitch）與較短的聲道長度（Vocal Tract Length），使共振峰與諧波特徵更為鮮明，情緒辨識率顯著高於男性語音。
- **混淆矩陣分析**：厭惡（Disgust, 94.11%）與憤怒（Angry, 89.65%）辨識度最高；悲傷最常被誤判為中立（5.24% 混淆），恐懼最常與驚訝混淆。

---

## 6. 研究限制 (Limitations)
1. **跨資料集切分協議**：採用整體隨機 75/25 切分，未實施嚴格的留一說話者（LOSO）協議，TESS 樣本數大且包含重複固定詞彙，可能存在資料集偏置。
2. **純聲學單模態**：未融合臉部表情與語意文字等多模態訊號。
