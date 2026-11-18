# AGENTS.md - Speech Emotion Recognition (SER) LLM Wiki 運作規範

本檔案定義了大型語言模型（LLM Agent）在維護、更新與擴充本「語音情緒辨識（Speech Emotion Recognition, SER）LLM Wiki」時的核心運作規範、角色分工、檔案規範與品質標準。

---

## 1. 核心願景與目標 (Mission & Scope)

- **主題領域**：專注於語音情緒辨識（SER），特別聚焦於**深度學習里程碑架構（Deep Learning SER）**（頻譜圖表示、CNN、CRNN、Attention 機制）。
- **下游目標**：作為高品質、可追溯的結構化知識庫，未來將直接提煉產出給初學者閱讀的**繁體中文互動式教材 HTML 簡報**。
- **目標讀者設定**：具備基礎 Python 與機器學習概念，但無音訊/語音處理背景的初學者。解說時需兼顧直觀物理概念與完整嚴謹的數理推導。

---

## 2. 嚴格事實性原則 (Anti-Hallucination Policy)

> [!IMPORTANT]
> **嚴禁虛構研究成果與論文數據**：
> 1. 所有收錄於 `papers/`、`concepts/`、`architectures/` 的研究結果、模型架構、實驗數據（如 WA/UA 數值）必須來自於 `raw/` 內的真實論文或確切的學術來源。
> 2. 在未提供正式原始論文或未經 Ingest 流程前，任何知識頁面僅能建立骨幹架構，並清楚標記 `<!-- 狀態：待匯入 / Pending Ingestion -->`。
> 3. 嚴禁在未見原始文獻的情況下自行捏造數值、作者宣稱或基準比較結論。

---

## 3. 語言、格式與命名規範 (Conventions)

### 3.1 語言風格 (Language)
- **主要語言**：繁體中文（台灣習慣用語，如「資訊」、「模型」、「向量」、「卷積」）。
- **專有名詞對照**：所有核心技術名詞首次出現時必須附帶英文原文對照。
  - 例：梅爾頻譜（Mel-spectrogram）、加權準確率（Weighted Accuracy, WA）、非加權準確率（Unweighted Accuracy, UA）、留一說話者交叉驗證（Leave-One-Speaker-Out, LOSO）。

### 3.2 檔名命名規範 (File Naming)
- 一律採用**全英文小寫 kebab-case**，副檔名為 `.md`。
  - 概念頁：`concepts/mel-spectrogram.md`
  - 架構頁：`architectures/crnn-architectures.md`
  - 論文頁：`papers/<年份>-<第一作者姓氏>-<核心簡稱>.md`（例如：`papers/2018-chen-crnn.md`）

### 3.3 引用與來源格式 (Citations)
- 內文引用採用**輕量化 Markdown 行內超連結**：
  - 格式範例：`[Chen et al. (2018)](https://arxiv.org/abs/xxxx.xxxxx)` 或 `[Mirzaei et al. (2022)](https://doi.org/10.xxxx/xxxx)`。
  - 確保連結有效，點擊可直達原始文獻來源。

### 3.4 數學公式規範 (Mathematics)
- 採用**標準 LaTeX 語法**（支援 KaTeX / MathJax）：
  - 行內公式：`$...$`
  - 獨立區塊公式：`$$...$$`
- 嚴格保留**學術推導級數學**，包含：
  - 短時距傅立葉變換（STFT）離散積分/求和定義
  - 梅爾濾波器組（Mel Filterbank）頻率轉換公式與三角濾波器矩陣
  - 卷積與池化特徵圖張量維度（Tensor Shapes，例如 $(B, C, T, F)$）
  - 注意力機制（Attention）Query-Key-Value 權重矩陣計算
  - 損失函數（Cross-Entropy, Focal Loss, CCC）與評測指標（WA, UA）公式

### 3.5 觀點矛盾處理機制 (Handling Contradictions)
- 遇到不同文獻結果分歧時，**嚴禁強行選邊站**。
- 必須在該條目設立「**爭議與觀點比較**」章節，記錄不同論文在不同評估設定下的成立條件：
  - 評測協議差異（LOSO 留一說話者 vs 隨機 5-Fold/10-Fold）
  - 評測指標差異（WA 加權準確率 vs UA 非加權準確率，資料集不平衡影響）
  - 特徵表示差異（Log-mel 頻譜圖維度、採樣率、窗長與步長設定）
  - 資料集特性差異（IEMOCAP、RAVDESS、MSP-Podcast 等自發情緒 vs 演出情緒）

---

## 4. 資料夾架構定義 (Directory Structure)

```text
SER-LLM-Wiki/
├── AGENTS.md                  # LLM Agent 運作規範與指引（本文件）
├── index.md                   # Wiki 核心首頁與知識地圖（所有頁面的索引入口）
├── ingest-log.md              # 論文收錄、修改與演進歷史記錄檔
├── raw/                       # 存放原始學術論文 PDF 檔案（至少 5 篇核心文獻）
├── concepts/                  # 語音與音訊基本概念條目
│   ├── speech-representations.md
│   └── evaluation-metrics.md
├── architectures/             # 深度學習 SER 模型架構條目
│   ├── cnn-for-ser.md
│   ├── crnn-architectures.md
│   └── attention-mechanisms.md
├── papers/                    # 論文詳細摘錄與精華筆記（依年-作者-簡稱命名）
├── slides/                    # 未來產出之初學者繁體中文互動式 HTML 教學簡報
├── reports/                   # 自動化品質檢查報告、Agent Loop/Graph 執行紀錄與修正紀錄
└── scripts/                   # 輔助自動化腳本（如孤立頁面檢查 check-orphan-pages.py）
```

---

## 5. Agent 角色與工作流程 (Workflows)

### 5.1 論文 Ingest 流程 (Paper Ingestion Workflow)
當使用者在 `raw/` 放入論文 PDF 或指定論文時，執行以下標準流程：
1. **讀取與解析**：提取論文標題、作者、年份、發表會議/期刊、arXiv/DOI 網址。
2. **建立論文專屬頁面**：在 `papers/` 建立 `<年份>-<第一作者>-<簡稱>.md`，記錄摘要、核心架構圖描述、數學推導、實驗設定（資料集、LOSO/10-Fold、WA/UA）。
3. **萃取與關聯**：
   - 將新架構思想更新或融入 `architectures/` 對應文件。
   - 將新特徵或概念更新至 `concepts/` 對應文件。
   - 若發現與現有文件觀點相左，更新「爭議與觀點比較」區塊。
4. **更新索引**：在 `index.md` 加入該篇論文與新條目的雙向超連結，防止孤立頁面。
5. **記錄日誌**：在 `ingest-log.md` 新增收錄時間、來源、變更頁面與更新摘要。

### 5.2 品質檢查流程 (Lint & Quality Assurance)
- **孤立頁面檢查（Orphan Pages Check）**：
  - 執行 `python scripts/check-orphan-pages.py`。
  - 確認 `concepts/`、`architectures/`、`papers/` 中的每一個 `.md` 檔案都必須至少在 `index.md` 或其他文件中被超連結引用。
- **檢查報告產出**：將檢查結果與任何修正歷程儲存於 `reports/` 目錄中。

### 5.3 簡報提煉流程 (Slide Generation Workflow)
- 以 Wiki 中的概念與架構為單一真相來源（Single Source of Truth）。
- 產出互動式教材風格單頁網頁至 `slides/` 目錄，支援章節側欄導覽、KaTeX 數學公式、架構示意圖與折疊卡片。
