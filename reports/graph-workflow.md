# Wiki → HTML 簡報 Graph / Loop 工作流程規範 (Workflow Specification)

本文件定義了「SER LLM Wiki → 教學型 HTML 簡報」的自動化 Graph / Loop 迭代工作流程。本流程由程式化檢測腳本與獨立 AI 審查節點共同構成，具備錯誤回退（Rollback）與最多 3 輪自我修正機制。

---

## 1. 核心狀態圖與節點定義 (State Graph)

```mermaid
graph TD
    N1["[節點 1] 檢查 Wiki 資料與來源充足性"] -->|充足| N2["[節點 2] 檢索相關 Wiki 知識條目"]
    N1 -->|不充足| STOP_FAIL["終止：來源不足，嚴禁憑空捏造"]
    
    N2 --> N3["[節點 3] 檢查簡報大綱與來源覆蓋率"]
    N3 -->|大綱缺漏| N2
    N3 -->|大綱完備| N4["[節點 4] 檢查 / 修正 HTML 簡報檔案"]
    
    N4 --> N5["[節點 5] 執行程式化驗證 (verify-slides.py)"]
    N5 -->|程式驗證失敗 (結構/排版/響應式/連結)| N4
    N5 -->|程式驗證通過| N6["[節點 6] 執行獨立 AI 內容審查"]
    
    N6 -->|內容審查發現瑕疵 (數值不符/結論偏差)| DECIDE{"是否超過 3 輪修正上限？"}
    DECIDE -->|未達上限 (<= 3)| ROLLBACK["[節點 7] 退回最接近來源之節點進行局部修復"]
    ROLLBACK --> N4
    DECIDE -->|超過上限 (> 3)| STOP_WARN["終止：達到修正上限，回報未解決問題"]
    
    N6 -->|內容審查全數通過| N8["[節點 8] 全域品質簽核"]
    N8 --> SUCCESS["[節點 9] 流程圓滿結束，交付簡報"]
```

---

## 2. 節點詳細規範與檢驗標準

### [節點 1] Wiki 資料充足性檢查 (Check Wiki Sufficiency)
- **檢驗項目**：
  1. `raw/` 內至少具備 5 篇原始學術論文 PDF。
  2. `papers/` 內對應有 5 篇無虛構之結構化筆記。
  3. `concepts/` 與 `architectures/` 內已整合實證知識，無未解決之待匯入標籤。
- **失敗條件**：若論文不足 5 篇或缺少必要架構，立即停止流程，**嚴禁自行捏造內容**。

### [節點 2] 相關 Wiki 頁面檢索 (Retrieve Wiki Pages)
- **檢驗項目**：提取關於語音訊號表示（STFT、Mel）、評測協議（LOSO、WA/UA）、CNN、CRNN、Attention、HuBERT、LiSER 與 Qwen2-Audio 的核心數理公式與實驗數據。

### [節點 3] 簡報大綱與覆蓋率檢查 (Check Outline Coverage)
- **檢驗項目**：核對 `reports/slide-outline.md` 是否完整涵蓋 12 頁教學主題，且每一頁均明確標註 1~2 篇 Wiki 來源。

### [節點 4] HTML 簡報檔案檢查與修訂 (Check / Fix HTML Slides)
- **檢驗項目**：根據檢測報告與審查反饋，局部修改 `slides/index.html`。
- **修改原則**：僅修正有問題之 DOM 結構、樣式或說明文字，不更動已通過之穩定部分。

### [節點 5] 程式化自動驗證 (Automated Verification Script)
執行 `python scripts/verify-slides.py`，強制檢驗：
1. **12 頁結構**：存在 `data-index="1"` 至 `data-index="12"` 之 `section.slide`。
2. **導覽與控制元件**：存在 `btn-prev`、`btn-next`、`btn-fullscreen`、`dots-container`、`progress-bar` 及鍵盤事件監聽。
3. **超連結有效性**：所有 `href` 連結有效，無死連結。
4. **論文引用覆蓋**：每頁必須具備 `cite-badge` 標記出處。
5. **排版與響應式規則**：
   - 必須包含行動裝置媒體查詢（`@media (max-width: 768px)`）。
   - 必須針對網格配置（`grid-2`, `grid-3`, `grid-4`）進行單欄折疊自適應。
   - 必須具備視窗捲動保護與溢出防護（`overflow-y: auto`, `word-break: break-word`）。

### [節點 6] 獨立 AI 內容審查 (Independent AI Content Review)
- **執行方式**：由獨立對話上下文（或隔離之 subagent / 審查提示）審查簡報內容。
- **四大審查維度**：
  1. **事實忠實性**：簡報數據與論文原文是否一致（如 Bhanbhro 98.1%、Singh 85.00% vs 13.98%、LiSER 105K / UAR 0.595、HuBERT PNMI 0.686、Qwen2-Audio 8.2B / MELD 55.3%）。
  2. **結論一致性**：是否講反結論（如：誤將節奏特徵說成最有效、或混淆時間切分與 LOSO）。
  3. **出處對應性**：每一項核心實驗主張是否有清晰論文標註。
  4. **教學適應性**：是否符合「懂 Python/ML 但無語音背景之大學生」之理解門檻，具備直觀解釋。

### [節點 7] 錯誤回退與局部修復 (Error Rollback & Targeted Fix)
- 若程式檢驗或 AI 審查發現問題，將錯誤具體回退至對應節點（通常為節點 4 HTML 修復），進行針對性修正。

### [節點 8] 迭代迴圈控制 (Loop Iteration Control)
- **最多修正 3 輪**（Round 1 ➔ Round 2 ➔ Round 3）。
- 每輪修正後，必須重新執行節點 5 程式檢驗與節點 6 AI 審查，並將所有原始指令、輸出日誌與 diff 寫入 `reports/loop-execution-log.md`。

### [節點 9] 終止條件 (Termination Conditions)
1. **成功終止**：節點 5 程式測試 100% 通過 ＋ 節點 6 內容審查無重大缺陷 ➔ 產出交付報告。
2. **失敗終止**：達到 3 輪修正上限仍有未通過項目，或發現 Wiki 來源不足需要捏造時 ➔ 立即中止並列出阻礙清單。
