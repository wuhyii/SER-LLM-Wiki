# 論文收錄與修訂歷程日誌 (Ingest Log)

本文件依據 [AGENTS.md](AGENTS.md) 規範，詳細追蹤所有學術論文的 Ingest（吸收/萃取）流程，以及對 Wiki 知識庫所進行的增修紀錄。

---

## 📌 格式範例 (Template)

每次收錄新論文時，新增一個紀錄區塊如下：

```markdown
### [YYYY-MM-DD] Ingest: <論文名稱 / 標題>
- **文獻出處**：<第一作者姓名 et al., 年份, 會議/期刊名稱, arXiv/DOI 超連結>
- **原始檔案**：`raw/<檔案名稱>.pdf`
- **論文筆記**：`papers/<年份>-<第一作者>-<簡稱>.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/<概念檔案>.md`：<更新內容摘要>
  - `architectures/<架構檔案>.md`：<更新內容摘要>
- **矛盾與爭議註記**：<若與現有觀點不同，記錄於此並對比條件>
- **更新者**：<Agent 名稱或執行者>
```

---

## 🕒 歷史紀錄 (Changelog)

### [2026-11-18] Ingest: Qwen2-Audio Technical Report
- **文獻出處**：[Chu et al. (2024)](https://arxiv.org/abs/2407.10759), *arXiv:2407.10759*.
- **原始檔案**：`raw/2407.10759v1.pdf`
- **論文筆記**：`papers/2024-chu-qwen2-audio.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/speech-representations.md`：記錄 128 維 Mel-spectrogram 前處理配置（窗長 25ms、步長 10ms、stride 2 池化對應 40ms 幀長）。
  - `concepts/evaluation-metrics.md`：補充開放式自然對話 MELD 基準（ACC 55.3%）與 AIR-Bench 語音對話共情維度（7.18 分）。
  - `architectures/attention-mechanisms.md`：擴充音訊大型語言模型（Audio-LLM）之全域自回歸 Transformer 注意力機制。
  - `index.md`：更新里程碑論文索引。
- **矛盾與爭議註記**：8.2B 參數量遠大於傳統輕量化 SER 模型（如 LiSER 的 105K），不適合端側即時離線部署，但在開放式情緒理解與多輪語音互動具備超越判別式分類器的自然度。
- **更新者**：Antigravity Agent (SER-LLM-Wiki Ingestion Loop)

### [2026-11-18] Ingest: HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units
- **文獻出處**：[Hsu et al. (2021)](https://arxiv.org/abs/2106.07447), *IEEE/ACM TASLP*, 29, 3451–3460.
- **原始檔案**：`raw/2106.07447v1 (1).pdf`
- **論文筆記**：`papers/2021-hsu-hubert.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/speech-representations.md`：記錄從連續波形經由 7 層 Conv1D（320 倍下採樣）到 K-means 離散聲學單元（PNMI 自 0.253 提升至 0.686）的自監督表徵提取。
  - `architectures/cnn-for-ser.md`：收錄原始波形一維卷積編碼器架構（7 層 Conv1D，通道 512）。
  - `architectures/attention-mechanisms.md`：擴充 Transformer 12~48 層多頭自注意力機制在語音特徵編碼的規格與作用。
  - `index.md`：更新里程碑論文索引。
- **矛盾與爭議註記**：HuBERT 依賴龐大預訓練資料庫（Libri-Light 60k 小時）與多階段離線分群，參數量 95M~1B，為當代下游 SER 頂級特徵教師，但計算昂貴。
- **更新者**：Antigravity Agent (SER-LLM-Wiki Ingestion Loop)

### [2026-11-18] Ingest: Leveraging Unlabeled Audio-Visual Data in Speech Emotion Recognition using Knowledge Distillation (LiSER)
- **文獻出處**：[Pendyala et al. (2025)](https://arxiv.org/abs/2507.00055), *arXiv:2507.00055*.
- **原始檔案**：`raw/2507.00055v1.pdf`
- **論文筆記**：`papers/2025-pendyala-liser-distillation.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/speech-representations.md`：記錄 64 Mel bands（窗長 128ms、步長 32ms）之輕量化特徵工程配置。
  - `concepts/evaluation-metrics.md`：在「爭議與觀點比較」深刻對比嚴格 5-Fold 跨說話者獨立評測下的 UAR (59.5%) 與同說話者時間分割之 Accuracy (98.1%)。
  - `architectures/cnn-for-ser.md`：收錄 3 區塊 2D CNN 非對稱池化設計（$(2,2), (4,2), (4,1)$）。
  - `architectures/crnn-architectures.md`：記錄 105K 極致輕量化 CRNN 學生模型與 3 個專屬 MLP 輸出頭設計。
  - `index.md`：更新里程碑論文索引。
- **矛盾與爭議註記**：證實 MAE 蒸餾損失在帶雜訊野生標籤下顯著優於 Cross-Entropy 損失；僅用 50% 標籤配合無標籤 MSP-Face 蒸餾超越 100% 標籤基準。
- **更新者**：Antigravity Agent (SER-LLM-Wiki Ingestion Loop)

### [2026-11-18] Ingest: Speech Emotion Recognition Using Attention Model
- **文獻出處**：[Singh et al. (2023)](https://doi.org/10.3390/ijerph20065140), *IJERPH*, 20(6), 5140.
- **原始檔案**：`raw/ijerph-20-05140.pdf`
- **論文筆記**：`papers/2023-singh-attention-cnn-lstm.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/speech-representations.md`：記錄節奏特徵（Tempogram 13.98%）對比 MFCC（85.00%）之消融實驗。
  - `concepts/evaluation-metrics.md`：分析多資料集（RAVDESS/SAVEE/TESS）融合下的性別聲學特性差異（TESS 女性 99.81% vs SAVEE 男性 57.50%）。
  - `architectures/cnn-for-ser.md`：對比 1D 卷積與 4 區塊 2D 卷積在頻譜特徵捕捉上的差距。
  - `architectures/crnn-architectures.md`：記錄雙層 LSTM 夾心自注意力架構（Conv2D -> LSTM1 -> Attention -> LSTM2 -> Dense）。
  - `architectures/attention-mechanisms.md`：補充雙曲正切自注意力層動態時間權重計算。
  - `index.md`：更新里程碑論文索引。
- **矛盾與爭議註記**：論文顯示在多資料集混合下女性辨識率顯著高於男性，突顯了語音情緒資料集性別平衡與聲道物理特徵對 SER 模型的關鍵影響。
- **更新者**：Antigravity Agent (SER-LLM-Wiki Ingestion Loop)

### [2026-11-18] Ingest: Speech Emotion Recognition: Comparative Analysis of CNN-LSTM and Attention-Enhanced CNN-LSTM Models
- **文獻出處**：[Bhanbhro et al. (2025)](https://doi.org/10.3390/signals6020022), *Signals*, 6(2), 22.
- **原始檔案**：`raw/signals-06-00022-v2.pdf`
- **論文筆記**：`papers/2025-bhanbhro-cnn-lstm-attention.md`
- **觸及/更新 Wiki 條目**：
  - `concepts/speech-representations.md`：補充標準化 16 kHz 採樣率、25 ms 窗長與 10 ms 幀移之梅爾頻譜前處理參數；補充 AWGN 與均勻雜訊增強之訊雜比動態公式與實證效果。
  - `concepts/evaluation-metrics.md`：記錄 RAVDESS 8 類情緒在時間切分協議下的評測結果；在「爭議與觀點比較」章節特別標明此高準確率（98.1%）與留一說話者（LOSO）協議不可直接混淆比較。
  - `architectures/cnn-for-ser.md`：記錄 6 層時間分佈 2D CNN 區塊設計、漸進式濾波器（8~256）與 ELU 活化函數應用。
  - `architectures/crnn-architectures.md`：記錄 2D CNN 串聯 BiLSTM 的時序特徵融合架構，以及移除 LSTM（降至 95.0%）和移除雙向機制（降至 89.0%）之消融實驗數據。
  - `architectures/attention-mechanisms.md`：記錄自注意力機制在 BiLSTM 後段對關鍵情緒顯著片段加權的數學公式與效果，特別在區分 Neutral vs Calm 等相近情緒上的提升。
  - `index.md`：更新里程碑論文索引章節與概念條目連結。
- **矛盾與爭議註記**：論文在 RAVDESS 取得 98.1% 高準確率，採用 80/10/10 時間分割（非嚴格 LOSO），故屬於說話者相依/半相依性質之性能上限驗證；跨語料（SAVEE）僅測試 7 筆，尚待更廣泛泛化驗證。
- **更新者**：Antigravity Agent (SER-LLM-Wiki Ingestion Loop)

### [2026-11-18] Wiki 知識庫骨幹架構初始化
- **操作類型**：專案初始化與結構建立
- **建立目錄**：
  - `raw/`：準備存放至少 5 篇原始 SER 核心學術論文 PDF。
  - `slides/`：準備存放未來生成的初學者繁體中文互動式 HTML 教學簡報。
  - `reports/`：準備存放自動化品質檢查報告、Agent Loop/Graph 執行紀錄與修正歷程。
  - `concepts/`：語音訊號與特徵基礎概念骨幹。
  - `architectures/`：深度學習 SER 里程碑架構骨幹。
  - `papers/`：存放論文詳細筆記之專屬目錄。
  - `scripts/`：自動化品質檢查輔助腳本。
- **建立檔案**：
  - `AGENTS.md`：規範 Agent 運作準則、反幻覺條款、命名、LaTeX 與 Ingest 流程。
  - `index.md`：知識庫總覽首頁與概念導覽地圖。
  - `concepts/speech-representations.md`（待匯入骨幹）
  - `concepts/evaluation-metrics.md`（待匯入骨幹）
  - `architectures/cnn-for-ser.md`（待匯入骨幹）
  - `architectures/crnn-architectures.md`（待匯入骨幹）
  - `architectures/attention-mechanisms.md`（待匯入骨幹）
  - `scripts/check-orphan-pages.py`：孤立頁面檢查腳本。
- **備註**：目前無論文輸入，嚴格遵守反幻覺原則，未捏造任何實驗數據或文獻結論，所有概念頁面標註為待匯入狀態。
