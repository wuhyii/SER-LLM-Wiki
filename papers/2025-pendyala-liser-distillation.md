# [論文筆記] Leveraging Unlabeled Audio-Visual Data in Speech Emotion Recognition using Knowledge Distillation (LiSER)

- **引用出處**：[Pendyala et al. (2025)](https://arxiv.org/abs/2507.00055)
- **完整文獻**：Pendyala, V., Morgado, P., & Sethares, W. (2025). Leveraging Unlabeled Audio-Visual Data in Speech Emotion Recognition using Knowledge Distillation. *arXiv preprint arXiv:2507.00055*.
- **原始檔案**：`raw/2507.00055v1.pdf`
- **關聯頁面**：
  - [語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
  - [SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
  - [卷積神經網路於 SER 之應用](../architectures/cnn-for-ser.md)
  - [卷積循環神經網路架構](../architectures/crnn-architectures.md)
  - 相關基底模型：[HuBERT (Hsu et al., 2021)](2021-hsu-hubert.md)
  - 相關架構對比：[Bhanbhro et al. (2025)](2025-bhanbhro-cnn-lstm-attention.md)

---

## 1. 研究背景與核心動機 (Motivation)
- **大型基底模型部署困境**：以 [HuBERT](2021-hsu-hubert.md) 為代表的自監督學習（SSL）模型在 SER 表現優異，但其參數量高達數億（95M~1B），難以部署於行動設備與邊緣低資源終端。
- **標註資料匱乏與高成本**：情緒具有高度感知模糊性，收集帶標籤的多模態影音資料極為昂貴。
- **核心創新**：提出 **LightweightSER (LiSER)** 知識蒸餾架構，利用**未標註的野生影音數據（Unlabeled In-the-Wild Audio-Visual Data）**，同時向語音教師（HuBERT）與動態人臉表情教師（S2D ViT）學習，將多模態情緒知識蒸餾至極致輕量化（僅 105K 參數）的純語音學生模型。

---

## 2. 教師與學生模型架構 (Teacher-Student Architectures)

### 2.1 語音教師 (Speech Teacher)
- 採用預訓練 `hubert-base-ls960`（95M 參數）。
- 透過低秩適應（LoRA）對自注意力權重矩陣進行微調（80% 標籤語音微調，挑選驗證集最佳 Checkpoint）。
- 輸入為原始語音波形，輸出情緒 Softmax 機率分佈。

### 2.2 影像教師 (Video Teacher)
- 採用基於 Vision Transformer (ViT) 的動態臉部表情模型 **S2D**（Chen et al., 2024）。
- 在 FERV39k 資料集上預訓練，輸入 16 幀動態人臉圖像序列（約 0.5s），輸出 7 種臉部情緒機率。

### 2.3 輕量化學生模型 (Lightweight Student Model)
- **參數量**：僅 **105K 參數**（約為 HuBERT 的千分之一）。
- **特徵輸入**：對數梅爾頻譜圖（Log-Mel Spectrogram），64 個 Mel 頻帶，窗長 128 ms，步長 32 ms，音訊切片長度 3 秒。
- **結構**（Table 1）：
  - 3 個 2D 卷積區塊（64 通道，卷積核 $3 \times 3$，搭配 BatchNorm 與 ReLU，最大池化尺度分別為 $(2,2), (4,2), (4,1)$）。
  - 1 層 LSTM 時序層（隱藏單元 64）。
  - 3 個專屬 MLP 輸出頭：
    - $g^{\text{sup}}$：監督式分類頭（1 層，節點數 $K_S$）。
    - $g^{\text{sd}}$：語音蒸餾頭（2 層，節點數 32, $K_S$）。
    - $g^{\text{vd}}$：影像跨模態蒸餾頭（2 層，節點數 32, $K_V$）。

---

## 3. 跨模態知識蒸餾與信賴度加權目標 (Training Objectives)

### 3.1 損失函數定義
在包含有標籤資料 $\mathcal{D}^L$ 與無標籤影音資料 $\mathcal{D}^U$ 的迷你批次中，定義三項損失：
1. **監督分類損失（交叉熵 CE）**：
   $$\mathcal{L}^{\text{sup}}(s_i^L, y_i^L) = \mathcal{L}_{\text{CE}}\left(g^{\text{sup}}(s_i^L, \theta), y_i^L\right)$$
2. **語音單模態蒸餾損失（平均絕對誤差 MAE）**：
   $$\mathcal{L}^{\text{sd}}(s_j^U) = \mathcal{L}_{\text{MAE}}\left(g^{\text{sd}}(s_j^U, \theta), t_s(s_j^U)\right)$$
3. **視訊跨模態蒸餾損失（MAE）**：
   $$\mathcal{L}^{\text{vd}}(s_j^U, v_j^U) = \mathcal{L}_{\text{MAE}}\left(g^{\text{vd}}(s_j^U, \theta), t_v(v_j^U)\right)$$

### 3.2 樣本級信賴度增強批次損失 (Confidence-Enhanced Loss)
針對野生影音中兩種模態情緒資訊強弱不均的問題，引入教師模型最高預測機率作為實例權重 $w_j^{\text{sd}}, w_j^{\text{vd}}$：

$$\mathcal{L}_{\text{batch\_conf}} = \frac{\sum_{i=1}^{N_l} \mathcal{L}_i^{\text{sup}} + \sum_{j=1}^{N_u} \left(\lambda^{\text{sd}} \cdot w_j^{\text{sd}} \cdot \mathcal{L}_j^{\text{sd}} + \lambda^{\text{vd}} \cdot w_j^{\text{vd}} \cdot \mathcal{L}_j^{\text{vd}}\right)}{N_l + N_u}$$

---

## 4. 實驗設定與評測基準 (Experimental Setup)
- **無標籤影音庫**：MSP-Face（自 YouTube 收集的 46.55 小時野生對話影片，涵蓋 386 位說話者，全部作為未標記資料）。
- **標註測試基準**：
  - **RAVDESS**：1440 筆錄音（24 位演員，8 種情緒）。
  - **CREMA-D**：7442 筆錄音（91 位演員，6 種情緒）。
- **評測協議**：嚴格的 **5-Fold 交叉驗證**，且**確保說話者無重疊（Speaker-Independent）**。
- **評估指標**：非加權平均召回率（UAR / Balanced Accuracy）與加權平均召回率（WAR）。

---

## 5. 核心實驗結果 (Key Results)

### 5.1 蒸餾策略在 RAVDESS 與 CREMA-D 上的效能 (Table 2)
| 配置 | RAVDESS UAR | RAVDESS WAR | CREMA-D UAR | CREMA-D WAR |
| :--- | :---: | :---: | :---: | :---: |
| **no-dstl (僅標籤監督)** | 0.517 | 0.535 | 0.551 | 0.550 |
| **vid-dstl (僅視訊教師蒸餾)** | 0.534 (+3.29%) | 0.547 | 0.576 (+4.54%) | 0.575 |
| **sp-dstl (僅語音教師蒸餾)** | 0.545 (+5.42%) | 0.556 | 0.576 (+4.54%) | 0.575 |
| **vid-sp-dstl (雙模態蒸餾)** | 0.556 (+7.54%) | 0.570 | **0.584 (+5.99%)** | **0.583** |
| **conf-vid-sp-dstl (信賴度雙模態)** | **0.595 (+15.09%)** | **0.611** | 0.578 (+4.90%) | 0.576 |

### 5.2 關鍵消融發現 (Ablations)
- **標籤效率翻倍 (Data Efficiency)**：在 CREMA-D 上，僅使用 **50% 標籤資料**配合無標籤 MSP-Face 蒸餾的學生模型，表現超越了使用 100% 標籤資料卻無蒸餾的基準模型。
- **MAE vs CE 蒸餾損失**：MAE 損失在蒸餾階段顯著優於傳統 cross-entropy（CE），歸因於 MAE 對野生數據的噪聲偽標籤具備更強韌性。
- **聯合訓練 vs 兩階段訓練**：有標籤與無標籤同步聯合優化，優於「先無標籤預訓練再微調」的傳統兩階段流程。

---

## 6. 研究限制 (Limitations)
1. 視訊教師 S2D 僅支援 0.5 秒滑動窗口，需對整段語音輸出進行平均，可能平滑化瞬態表情。
2. 跨模態蒸餾高度依賴人臉可見度，MSP-Face 中若人臉遮擋則無法提供有效視覺監督。
