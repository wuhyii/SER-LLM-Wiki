# raw/ - 原始學術論文 PDF 存放區

本資料夾用於存放語音情緒辨識（SER）的原始學術論文 PDF 檔案。

## 使用指引：
1. 請在此資料夾放入至少 5 篇深度學習 SER 里程碑論文的 PDF 檔案（例如經典的 CNN、CRNN、Attention 機制應用於 SER 之代表性論文）。
2. Agent 在執行 Ingest 任務時，將直接讀取此目錄下的文獻進行結構化剖析，並將提煉後的筆記建立於 `papers/`，同時將概念整合至 `concepts/` 與 `architectures/`。
