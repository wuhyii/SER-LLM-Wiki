# SER 評估指標與評測協議 (Evaluation Metrics & Protocols)

> 本頁面已整合文獻實證數據。
> 最新匯入文獻：[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)
> 回到總覽：[首頁 (index.md)](../index.md)

---

## 1. 混淆矩陣與基礎定義 (Confusion Matrix)

在包含 $C$ 個情緒類別（如高興 Happy、悲傷 Sad、憤怒 Angry、中立 Neutral 等）的 SER 任務中，令混淆矩陣為 $\mathbf{M} \in \mathbb{R}^{C \times C}$：
- $M_{i, j}$：真實標籤為類別 $i$、而模型預測為類別 $j$ 的樣本總數。
- 類別 $i$ 的總樣本數：$N_i = \sum_{j=1}^{C} M_{i, j}$。
- 資料集總樣本數：$N = \sum_{i=1}^{C} N_i$。

---

## 2. 核心評估指標：WA 與 UA

語音情緒資料集普遍存在嚴重的**類別不平衡（Class Imbalance）**現象（例如中立情緒樣本數往往遠高於厭惡或恐懼）。因此，僅使用單一準確率容易產生誤導。

### 2.1 加權準確率 (Weighted Accuracy, WA)
加權準確率即為傳統的整體準確率（Overall Accuracy），其對每個樣本賦予相同權重：

$$\text{WA} = \frac{\sum_{i=1}^{C} M_{i, i}}{N} = \sum_{i=1}^{C} \left(\frac{N_i}{N}\right) \cdot \text{Acc}_i$$

其中 $\text{Acc}_i = \frac{M_{i, i}}{N_i}$ 為第 $i$ 類別的召回率（Recall）。
- **特點**：樣本數多的多數類別（Majority Class）對 WA 具有極大的主導權。

### 2.2 非加權準確率 (Unweighted Accuracy, UA)
非加權準確率亦稱為平均召回率（Macro-Average Recall / Balanced Accuracy），對所有類別賦予平等的權重，不受類別樣本數量多寡影響：

$$\text{UA} = \frac{1}{C} \sum_{i=1}^{C} \text{Acc}_i = \frac{1}{C} \sum_{i=1}^{C} \frac{M_{i, i}}{N_i}$$

- **特點**：在評估模型對少數類別（Minority Class）的辨識能力時，UA 是 SER 領域公認最具說服力與公平性的核心指標。

---

## 3. 跨說話者評測協議：LOSO vs 隨機切分

### 3.1 說話者相依 vs 獨立 (Speaker-Dependent vs Speaker-Independent)
語音訊號同時包含了說話者個體音色（Speaker Identity / Timbre）與情緒語氣（Emotion）。若模型過擬合於說話者音色，其泛化能力將大幅下降。

### 3.2 留一說話者交叉驗證 (Leave-One-Speaker-Out, LOSO)
- **協議流程**：若資料集共有 $K$ 位說話者，每次以 $K-1$ 位說話者的所有語音作為訓練集，剩餘 1 位的語音作為獨立測試集。重複進行 $K$ 次實驗並取平均。
- **優勢**：嚴格杜絕訓練集與測試集出現相同說話者，真實評估模型對未知說話者的泛化表現。

### 3.3 隨機切分（Random 5-Fold / 10-Fold）
- 若隨機切分未依據說話者分群，同一位說話者的語音會同時出現在訓練集與測試集（稱為 Speaker Leakage），這會人為虛高準確率數值，導致研究結果之間無法直接橫向比較。

---

## 4. 爭議與觀點比較 (Controversies & Trade-offs)

> [!WARNING]
> **文獻比對原則與實驗協議陷阱：為什麼不同論文準確率差距如此懸殊？**
> 
> 在收錄的 SER 論文中，不同研究在相同資料集（如 RAVDESS）上報告的準確率從 **59.5%** 到 **98.1%** 不等，若不釐清其評測協議，極易產生嚴重誤解：
> 
> 1. **時間分割 / 隨機分割 vs 嚴格說話者獨立（Speaker-Independent / LOSO）**：
>    - **[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)**：採用 80/10/10 時間分割（早段錄音訓練、晚段錄音測試），同一位演員的聲音同時存在於訓練集與測試集。模型記住了演員個人的聲學音色特質，因此達到了 **98.1% 的極高 Accuracy**。
>    - **[Pendyala et al. (2025) LiSER](../papers/2025-pendyala-liser-distillation.md)**：採用嚴格的 **5-Fold 跨說話者交叉驗證**（訓練集與測試集說話者完全不重疊）。在此嚴格條件下，105K 輕量化學生模型在 RAVDESS 上的 UAR 為 **59.5%**（WAR 為 61.1%）。
>    - **教學警示**：**絕對不可將隨機/時間切分下的整體 Accuracy 與嚴格說話者獨立協議下的 UAR 進行跨論文橫向對比**。後者考驗的是模型對未知人類語音的真實泛化能力。
> 
> 2. **單一資料集 vs 多語料庫融合與性別偏誤**：
>    - **[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md)**：合併 RAVDESS、SAVEE 與 TESS 進行實驗，發現資料集間存在劇烈偏差——全女性的 TESS 準確率高達 **99.81%**，男女平衡的 RAVDESS 為 **74.44%**，而全男性的 SAVEE 僅有 **57.50%**。這反映出女性較高基頻與短聲道使情緒聲學特徵更突出，若資料集性別失衡將嚴重扭曲評測結論。
> 
> 3. **封閉分類 vs 開放式對話對談 (MELD / AIR-Bench)**：
>    - **[Chu et al. (2024) Qwen2-Audio](../papers/2024-chu-qwen2-audio.md)**：在自然真實對話資料集 MELD 上評測零樣本 Prompt 情緒理解（ACC 55.3%），雖然帳面準確率低於實驗室表演型資料集，但在開放式人機共情互動（如 AIR-Bench 語音對話 7.18 分）具備更強實用性。

---

## 5. 關聯條目與文獻索引 (References & Cross-Links)
- 論文專頁：
  - [Bhanbhro et al. (2025) - 2D CNN-BiLSTM-Attention 評測](../papers/2025-bhanbhro-cnn-lstm-attention.md)
  - [Singh et al. (2023) - 多資料集融合與性別差異評測](../papers/2023-singh-attention-cnn-lstm.md)
  - [Pendyala et al. (2025) - LiSER 嚴格說話者獨立 5-Fold 評測](../papers/2025-pendyala-liser-distillation.md)
  - [Hsu et al. (2021) - HuBERT 語音基底評測](../papers/2021-hsu-hubert.md)
  - [Chu et al. (2024) - Qwen2-Audio MELD 與 AIR-Bench 評測](../papers/2024-chu-qwen2-audio.md)
- 基礎特徵：[語音訊號表示與頻譜特徵](speech-representations.md)
- 模型架構：[CNN for SER](../architectures/cnn-for-ser.md)、[CRNN 架構](../architectures/crnn-architectures.md)、[注意力機制](../architectures/attention-mechanisms.md)
