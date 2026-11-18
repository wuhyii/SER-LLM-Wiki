# [論文筆記] Qwen2-Audio Technical Report: 音訊大型語言模型在情緒理解之應用

- **引用出處**：[Chu et al. (2024)](https://arxiv.org/abs/2407.10759)
- **完整文獻**：Chu, Y., Xu, J., Yang, Q., Wei, H., Wei, X., Guo, Z., Leng, Y., Lv, Y., He, J., Lin, J., Zhou, C., & Zhou, J. (2024). Qwen2-Audio Technical Report. *arXiv preprint arXiv:2407.10759*.
- **原始檔案**：`raw/2407.10759v1.pdf`
- **關聯頁面**：
  - [語音訊號表示與頻譜特徵](../concepts/speech-representations.md)
  - [SER 評估指標與評測協議](../concepts/evaluation-metrics.md)
  - [注意力機制於語音情緒辨識](../architectures/attention-mechanisms.md)
  - 語音基底模型關聯：[HuBERT (Hsu et al., 2021)](2021-hsu-hubert.md)
  - 輕量化模型對比：[Pendyala et al. (2025) LiSER](2025-pendyala-liser-distillation.md)

---

## 1. 研究背景與核心動機 (Motivation)
- **邁向通用音訊理解 (Artificial General Intelligence)**：傳統語音情緒辨識（SER）多依賴特定任務的判別式分類器（如 CNN-LSTM），難以與使用者進行動態口語互動或綜合多輪對話語境。
- **從分層標籤轉向自然語言 Prompt**：前代 Qwen-Audio 採用複雜的階層式標籤，Qwen2-Audio 簡化預訓練流程，全面採用自然語言提示詞（Natural Language Prompts），大幅提升指令遵循（Instruction-Following）與跨任務泛化能力。
- **雙模式互動體驗**：同時支援**語音對話模式 (Voice Chat Mode)**（無文字輸入的自由端到端語音對話，能感應語氣情緒給予安撫）與**音訊分析模式 (Audio Analysis Mode)**（支援長音訊特徵分析與情緒分類）。

---

## 2. 模型架構設計 (Model Architecture)

Qwen2-Audio 參數量達 **8.2B**，由音訊編碼器與大型語言模型底座組成：

```text
[原始音訊 (16 kHz)]
        ↓
[128 通道 Mel 頻譜圖 (窗長 25ms, 步長 10ms)]
        ↓
[Whisper-large-v3 音訊編碼器 + Stride 2 池化層 (每幀表徵 40ms)]
        ↓
[Qwen-7B 語言模型 (Decoder-only Transformer, 自注意力機制)]
        ↓
[次標記自回歸預測 (Next Token Prediction) / 語音文字輸出]
```

### 2.1 音訊特徵編碼
- 採樣率 16 kHz，提取 **128 維梅爾濾波器組（128-channel Mel-spectrogram）**，窗長 25 ms，步長 10 ms。
- 接續步長為 2 的池化層（Pooling Layer），使編碼器輸出每幀特徵對應原始音訊約 40 ms。

### 2.2 三階段訓練流程
1. **多任務預訓練 (Multi-Task Pre-training)**：涵蓋語音識別（ASR）、語音翻譯（S2TT）、聲音事件檢測（VSC）與自然語言情緒提示。
2. **監督式微調 (Supervised Fine-Tuning, SFT)**：提升多輪對話共情能力與分析精準度。
3. **直接偏好優化 (Direct Preference Optimization, DPO)**：
   $$\mathcal{L}_{\text{DPO}}(P_\theta; P_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{P_\theta(y_w \mid x)}{P_{\text{ref}}(y_w \mid x)} - \beta \log \frac{P_\theta(y_l \mid x)}{P_{\text{ref}}(y_l \mid x)} \right) \right]$$
   對齊人類偏好，減少情緒對話中的幻覺與不當回應。

---

## 3. 情緒辨識與語音共情評測 (SER Evaluation)

### 3.1 MELD 對話情緒辨識表現 (Table 2)
在多方對話情緒基準資料集 **MELD**（7 類情緒）上，Qwen2-Audio 在**無特定任務微調（Zero-Shot / Prompt-based）**條件下的表現：
- **WavLM-large**（判別式微調）：準確率 **54.2%**
- **Qwen-Audio**：準確率 **55.7%**
- **Qwen2-Audio**：準確率 **55.3%**
- *分析*：生成式 LLM 在未經專門分類頭微調下，僅依賴 Prompt 即可與傳統專門模型（如 WavLM）打平，展現強大的情緒語意抽象理解力。

### 3.2 AIR-Bench 語音對話共情評估
- 由 GPT-4 進行評分（0~10 分）：Qwen2-Audio 在 Chat-Speech 維度取得 **7.18 分**，顯著超越 Gemini-1.5-pro（6.97 分）與前代 Qwen-Audio（6.47 分）。
- **實務案例**：能主動識別發話者的考試焦慮語音（Figure 4）給予放鬆建議；在包含裝修雜訊的環境中（Figure 6）依然準確捕捉說話者情緒並提出談判策略。

---

## 4. 針對 SER 發展之綜合對比與局限 (Trade-offs & Limitations)
1. **參數量極端懸殊**：
   - 傳統輕量化 SER 模型（如 [LiSER](2025-pendyala-liser-distillation.md)）僅需 **105K 參數**即可在邊緣端離線即時推斷。
   - Qwen2-Audio 達 **8.2B 參數**，推理需要高階伺服器級 GPU，難以直接內嵌於小型穿戴裝置。
2. **分類精度對比**：在封閉式演員資料集（如 RAVDESS），傳統專用模型（[Bhanbhro et al., 2025](2025-bhanbhro-cnn-lstm-attention.md)）準確率可超過 90%；但在真實開放場景與多輪對話中，Audio-LLM 展現出更高的對話自然度與多語境融合潛力。
