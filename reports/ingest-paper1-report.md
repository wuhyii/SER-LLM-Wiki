# 第 1 篇論文 Ingest 執行報告與品質檢查 (Ingestion & Quality Audit Report)

- **執行時間**：2026-11-18 16:09:15
- **匯入目標**：`raw/signals-06-00022-v2.pdf`
- **論文標題**：Speech Emotion Recognition: Comparative Analysis of CNN-LSTM and Attention-Enhanced CNN-LSTM Models
- **作者與年份**：Jamsher Bhanbhro et al. (2025)
- **發表期刊**：*Signals*, 6(2), 22 ([DOI: 10.3390/signals6020022](https://doi.org/10.3390/signals6020022))

---

## 1. 執行項目檢驗

| 檢驗項目 | 規範標準 | 執行狀態 | 驗證結果 |
| :--- | :--- | :---: | :--- |
| **真實來源核實** | 數據來自真實 PDF，嚴禁虛構數值 | ✅ 通過 | 提取自原文 Table 2, Table 3, Section 3-4 |
| **筆記建立規範** | 檔名全英文小寫 kebab-case 格式 | ✅ 通過 | `papers/2025-bhanbhro-cnn-lstm-attention.md` |
| **數學公式規範** | 保留學術級 LaTeX 推導與維度 | ✅ 通過 | STFT、Mel Scale、AWGN SNR、BiLSTM、Attention 公式齊備 |
| **概念/架構整合** | 更新 concepts/ 與 architectures/ | ✅ 通過 | 擴充 5 篇核心條目並移除待匯入標記 |
| **雙向超連結完整性** | 孤立頁面檢測 (check-orphan-pages.py) | ✅ 通過 | 6 篇文件皆由 `index.md` 雙向索引，0 孤立頁面 |
| **歷程記錄規範** | 更新 `ingest-log.md` | ✅ 通過 | 詳細記錄文獻出處、修改條目與爭議點 |

---

## 2. 論文關鍵論點與數據查驗核對表 (Fact-Checking Matrix)

| 關鍵論點 / 數據項 | 論文原文出處 | 記錄位置 | 查驗確認 |
| :--- | :--- | :--- | :---: |
| 前處理：16 kHz、25 ms 窗長、10 ms 重疊步長 | Section 3.2 | `concepts/speech-representations.md` | ✅ 核實 |
| 雜訊增強：動態 SNR 15–30 dB AWGN | Section 3.3, Eq 17-24 | `concepts/speech-representations.md` | ✅ 核實 |
| 評測協議：RAVDESS 8 類情緒，80/10/10 時間分割 | Section 3.1, 3.3 | `concepts/evaluation-metrics.md` | ✅ 核實 |
| 準確率：Model 1 (CNN-LSTM) 達到 96.5% | Table 2, Section 4 | `papers/2025-bhanbhro-cnn-lstm-attention.md` | ✅ 核實 |
| 準確率：Model 2 (BiLSTM-Attention) 達到 98.1% | Table 2, Section 4 | `papers/2025-bhanbhro-cnn-lstm-attention.md` | ✅ 核實 |
| 消融實驗：移除 LSTM 準確率降至 95.0% | Section 3.4 | `architectures/crnn-architectures.md` | ✅ 核實 |
| 消融實驗：移除 BiLSTM（僅單向）降至 89.0% | Section 3.4 | `architectures/crnn-architectures.md` | ✅ 核實 |
| 消融實驗：移除 Dropout 驗證損失增加 15% | Section 3.4 | `architectures/cnn-for-ser.md` | ✅ 核實 |
