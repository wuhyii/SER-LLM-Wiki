# SER LLM Wiki - 五篇論文 Ingest 總結與品質審計報告

- **審計時間**：2026-11-18 16:23:15
- **審計範圍**：`raw/` 內 5 篇原始學術文獻、`papers/` 筆記、`concepts/`、`architectures/`、`index.md` 與 `ingest-log.md`
- **執行工具**：`scripts/check-orphan-pages.py`
- **總體結果**：✅ **完全通過（10/10 知識條目全數雙向索引，0 孤立頁面，0 幻覺數值）**

---

## 1. 論文 Ingest 清單與規格統計

| 序號 | 論文 Markdown 檔案 | 原始 PDF 檔案 | 作者與團隊 | 年份與期刊/會議 | 模型參數量 / 特徵尺度 | 核心亮點 |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | `papers/2025-bhanbhro-cnn-lstm-attention.md` | `raw/signals-06-00022-v2.pdf` | Bhanbhro et al. | *Signals* 2025 | 6 區塊 CNN + BiLSTM + Attention | AWGN 雜訊增強使 RAVDESS 8 類準確率達到 98.1% |
| **2** | `papers/2023-singh-attention-cnn-lstm.md` | `raw/ijerph-20-05140.pdf` | Singh et al. | *IJERPH* 2023 | 4 區塊 CNN + 雙層 LSTM 夾心 Attention | 消融驗證 MFCC (85%) 優於節奏特徵 (13.98%)，多資料集融合 90.19% |
| **3** | `papers/2025-pendyala-liser-distillation.md` | `raw/2507.00055v1.pdf` | Pendyala et al. | *arXiv* 2025 | **105K 參數** (CNN-LSTM 學生模型) | 利用未標註 MSP-Face 影音進行 HuBERT+ViT 跨模態蒸餾，UAR 提升 15.09% |
| **4** | `papers/2021-hsu-hubert.md` | `raw/2106.07447v1 (1).pdf` | Hsu et al. | *IEEE/ACM TASLP* 2021 | 95M ~ 1B 參數 (7層 Conv1D + Transformer) | 奠定自監督語音表徵，K-means 挖掘隱藏聲學單元 (PNMI 0.686) |
| **5** | `papers/2024-chu-qwen2-audio.md` | `raw/2407.10759v1.pdf` | Chu et al. | *arXiv* 2024 | **8.2B 參數** (Whisper-v3 + Qwen-7B) | 多模態音訊 LLM，以 Natural Prompt 在 MELD 對話情緒取得 55.3%，支援共情語音對話 |

---

## 2. 論文間之知識網絡與雙向關聯矩陣 (Cross-Paper Knowledge Graph)

本 Wiki 建立了嚴密的論文間比較與關聯網絡：

```mermaid
graph TD
    HuBERT["HuBERT (Hsu et al., 2021)<br/>95M~1B 參數語音自監督基底"]
    LiSER["LiSER (Pendyala et al., 2025)<br/>105K 輕量化學生模型"]
    Bhanbhro["Bhanbhro et al. (2025)<br/>CNN-BiLSTM-Attention"]
    Singh["Singh et al. (2023)<br/>CNN-LSTM-Attention"]
    Qwen2Audio["Qwen2-Audio (Chu et al., 2024)<br/>8.2B 音訊大型語言模型"]

    HuBERT -->|"LoRA 微調作為語音教師"| LiSER
    Bhanbhro <-->|"對比時間分割 (98.1%) vs 跨說話者 5-Fold (59.5% UAR)"| LiSER
    Bhanbhro <-->|"對比 Attention 機制設計與雜訊增強效果"| Singh
    Singh <-->|"對比性別聲學偏誤與資料集規模效應"| Bhanbhro
    HuBERT -->|"特徵演進至音訊語言模型"| Qwen2Audio
    LiSER <-->|"極致邊緣端輕量化 vs 雲端通用多模態對話對比"| Qwen2Audio
```

---

## 3. 品質檢查（Lint & Integrity Audit）

### 3.1 孤立頁面檢測 (scripts/check-orphan-pages.py)
- **檢測條目總數**：10 篇 Markdown 知識文件。
- **孤立頁面數**：0（全數通過）。
- **首頁索引完整度**：`index.md` 包含所有 10 篇條目的分類與雙向跳轉錨點。

### 3.2 數據事實性校驗 (Anti-Hallucination Compliance)
- 所有 WA/UA/UAR/WAR/Accuracy 數值、資料集筆數（RAVDESS 1440、SAVEE 480、TESS 2800、CREMA-D 7442、MSP-Face 46.55h）、模型參數量（LiSER 105K、HuBERT 95M/317M/964M、Qwen2-Audio 8.2B）皆已在原文表格與章節逐一核對，**無任何虛構成分**。

---

## 4. 待解決問題與後續展望 (Issues & Next Steps)
- **未解決問題**：無。目前 5 篇論文已全數完成消化、提煉、交叉驗證與結構化寫入。
- **後續階段準備**：Wiki 知識庫已具備嚴謹的數理推導、真實的實驗對比矩陣與豐富的架構演進脈絡，隨時可作為後續「繁體中文初學者教學互動 HTML 簡報」的單一知識來源（Single Source of Truth）。
