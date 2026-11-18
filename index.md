# 語音情緒辨識（Speech Emotion Recognition, SER）LLM Wiki

歡迎來到 **SER LLM Wiki**！本知識庫專注於整理與探索**語音情緒辨識（Speech Emotion Recognition, SER）**領域的核心知識，特別以**深度學習里程碑架構（Deep Learning SER）**為核心探討主軸。

本 Wiki 是後續生成「繁體中文初學者教學互動 HTML 簡報」的單一知識來源（Single Source of Truth）。

---

## 🗺️ 知識庫地圖與目錄 (Knowledge Map)

### 1. 核心概念 (Core Concepts)
深入理解語音訊號如何從一維時域波形轉化為機器學習可理解的特徵表示，以及標準評測準則。

- **[語音訊號表示與頻譜特徵 (Speech Representations & Features)](concepts/speech-representations.md)**
  - 一維時域波形（Raw Waveform）與取樣頻率
  - 短時距傅立葉變換（Short-Time Fourier Transform, STFT）數學定義
  - 語音頻譜圖（Spectrogram）與梅爾濾波器組（Mel Filterbank）矩陣推導
  - 對數梅爾頻譜（Log-Mel Spectrogram）的感知意義
- **[SER 評估指標與評測協議 (Evaluation Metrics & Protocols)](concepts/evaluation-metrics.md)**
  - 加權準確率（Weighted Accuracy, WA）與非加權準確率（Unweighted Accuracy, UA）
  - 類別不平衡（Class Imbalance）對評測的影響
  - 留一說話者交叉驗證（Leave-One-Speaker-Out, LOSO）vs 隨機切分（Random Split）

---

### 2. 深度學習里程碑架構 (Milestone Deep Learning Architectures)
探討從經典卷積神經網路到融合時間序列與注意力機制的架構演進歷程。

- **[卷積神經網路於 SER 之應用 (CNN for SER)](architectures/cnn-for-ser.md)**
  - 頻譜圖作為「二維單通道影像」的空間與時序特性
  - 二維卷積（2D CNN）與張量維度變化（Tensor Shapes）
  - 池化操作（Max/Average Pooling）對時間解析度的折衷
- **[卷積循環神經網路架構 (CRNN Architectures)](architectures/crnn-architectures.md)**
  - 空間特徵萃取（CNN）與時間序列建模（RNN / LSTM / GRU）的結合
  - 雙向循環神經網路（Bi-directional RNNs）對語音語境的捕捉
  - 瓶頸層與特徵對齊
- **[注意力機制於語音情緒辨識 (Attention Mechanisms in SER)](architectures/attention-mechanisms.md)**
  - 時序注意力（Temporal Attention）：聚焦情緒爆發點與語音顯著段落
  - 自注意力（Self-Attention）與多頭注意力（Multi-Head Attention）
  - 空間-時序二維注意力（Spatial-Temporal Attention）

---

### 3. 里程碑論文精華筆記 (Milestone Papers)
收錄於 `raw/` 5 篇核心學術文獻之詳細結構化筆記與深度分析：

1. **[Bhanbhro et al. (2025) - CNN-LSTM 與 Attention-Enhanced CNN-LSTM 模型比較分析](papers/2025-bhanbhro-cnn-lstm-attention.md)**
   - 出處：*Signals* 2025 ([DOI: 10.3390/signals6020022](https://doi.org/10.3390/signals6020022))
   - 核心貢獻：對比 2D CNN-LSTM 與 2D CNN-BiLSTM-Attention 架構在 RAVDESS 資料集上的情緒分類表現，驗證 AWGN 雜訊增強與注意力機制帶來的泛化能力（準確率達 98.1%）。
2. **[Singh et al. (2023) - 基於自注意力機制之語音情緒辨識模型](papers/2023-singh-attention-cnn-lstm.md)**
   - 出處：*IJERPH* 2023 ([DOI: 10.3390/ijerph20065140](https://doi.org/10.3390/ijerph20065140))
   - 核心貢獻：消融驗證 MFCC 為最佳聲學單特徵（85% 基準），提出 4 區塊 2D CNN + 雙層 LSTM 夾心自注意力結構，在 RAVDESS + SAVEE + TESS 混合資料集上取得 90.19% 準確率。
3. **[Pendyala et al. (2025) - LiSER：利用未標註多模態影音資料進行知識蒸餾](papers/2025-pendyala-liser-distillation.md)**
   - 出處：*arXiv:2507.00055* (2025)
   - 核心貢獻：以 HuBERT 為語音教師、S2D ViT 為視訊教師，將情緒知識透過 MAE 損失蒸餾至僅 105K 參數的輕量化 2D CNN-LSTM 學生模型，在 RAVDESS 與 CREMA-D 達到顯著 UAR 提升（最高提升 15.09%）。
4. **[Hsu et al. (2021) - HuBERT：基於隱藏單元遮罩預測之自監督語音表徵學習](papers/2021-hsu-hubert.md)**
   - 出處：*IEEE/ACM TASLP* 2021 ([arXiv:2106.07447](https://arxiv.org/abs/2106.07447))
   - 核心貢獻：奠定當代語音自監督表徵之基石，結合 7 層波形卷積編碼器與 Transformer 遮罩預測，透過 K-means 迭代挖掘聲學單元（PNMI 自 0.253 提升至 0.686），廣泛作為下游 SER 頂尖教師特徵。
5. **[Chu et al. (2024) - Qwen2-Audio 技術報告：音訊大型語言模型之情緒理解](papers/2024-chu-qwen2-audio.md)**
   - 出處：*arXiv:2407.10759* (2024)
   - 核心貢獻：8.2B 參數多模態音訊大型語言模型，結合 Whisper-large-v3 編碼器（128-Mel）與 Qwen-7B 解碼器，在無微調下以自然語言 Prompt 在 MELD 對話情緒辨識取得 55.3% 準確率，並在 AIR-Bench 展現出色的口語共情互動能力。

詳情請參閱 [論文收錄日誌 (ingest-log.md)](ingest-log.md)。

---

### 4. 系統與維護管理 (Maintenance & Infrastructure)
- **[Agent 運作指引與規範 (AGENTS.md)](AGENTS.md)**：定義 Agent 角色、引用格式、反幻覺原則與品質標準。
- **[收錄與修訂歷程日誌 (ingest-log.md)](ingest-log.md)**：記錄所有文獻 Ingest 軌跡與 Wiki 演進紀錄。
- **品質檢查與執行報告**：查看 [reports/](reports/) 目錄中的自動化檢查與迴圈紀錄。
- **教學簡報與產出物**：查看 [slides/index.html](slides/index.html)（初學者教學互動 HTML 簡報：從 CNN-LSTM 到 Speech LLM）。
