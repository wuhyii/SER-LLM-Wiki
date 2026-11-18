# SER 教學簡報大綱與知識來源對照表 (Slide Outline & Source Mapping)

- **簡報主題**：「AI 如何從聲音辨識情緒？從 CNN-LSTM 到 Speech LLM」
- **目標讀者**：具備基礎 Python 與機器學習概念，但無音訊/語音處理背景的大學生
- **技術語言**：繁體中文為主，專業術語保留英文對照
- **簡報形式**：現代自包含（Standalone）HTML 互動簡報，具備鍵盤切換、進度指示與視覺圖解

---

## 📑 12 頁簡報結構與來源對照表

| 頁碼 | 簡報標題 (Slide Title) | 核心教學概念與圖解設計 | Wiki 知識庫引用來源 |
| :---: | :--- | :--- | :--- |
| **01** | **首頁：AI 如何從聲音辨識情緒？**<br/>從 CNN-LSTM 到 Speech LLM | • 課程導言與學習目標地圖<br/>• 核心技術演進軸線（手製特徵 $\to$ CRNN $\to$ Attention $\to$ SSL $\to$ Audio-LLM） | [index.md](../index.md) |
| **02** | **聲音裡的言外之意：什麼是 SER？** | • 副語言語音線索（Paralinguistics: Pitch, Volume, Intonation, Rhythm）<br/>• 任務定義：情緒分類 vs 語音識別（ASR）隱私保護對比 | [Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)<br/>[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md) |
| **03** | **聲音如何變成「影像」？梅爾頻譜圖的誕生** | • 訊號加窗與短時距傅立葉變換（STFT）直觀原理<br/>• 梅爾刻度（Mel Scale）模擬人耳非線性聽覺機制<br/>• 張量維度流：$(B, 1, T, F)$ 視覺化解析 | [concepts/speech-representations.md](../concepts/speech-representations.md) |
| **04** | **特徵大對決：MFCC vs 節奏特徵消融實證** | • 聲學特徵消融實驗數據柱狀圖（Singh et al. 2023）<br/>• 迷思破解：為什麼單獨節奏特徵（13.98%）遠輸 MFCC（85.00%）？<br/>• 雜訊資料增強（AWGN, SNR 15–30 dB）原理 | [Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md)<br/>[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md) |
| **05** | **評測協議大陷阱：為什麼同一資料集準確率從 59% 到 98%？** | • 時間分割（98.1%）vs 嚴格留一說話者 LOSO / 5-Fold（59.5% UAR）<br/>• 說話者個體音色洩漏（Speaker Leakage）警示<br/>• 資料集性別偏誤（TESS 女性 99.81% vs SAVEE 男性 57.50%） | [concepts/evaluation-metrics.md](../concepts/evaluation-metrics.md)<br/>[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)<br/>[Pendyala et al. (2025)](../papers/2025-pendyala-liser-distillation.md)<br/>[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md) |
| **06** | **視覺神經網路如何「聽音」？2D CNN 的時頻卷積** | • 頻譜圖上的空間語意（時間軸 vs 頻率軸共振峰）<br/>• 2D 卷積核局部感知野與權重共享<br/>• 經典 6 區塊時間分佈卷積架構與特徵圖縮放 | [architectures/cnn-for-ser.md](../architectures/cnn-for-ser.md)<br/>[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md) |
| **07** | **捕捉整句情感起伏：CRNN (CNN + BiLSTM)** | • CNN 局部特徵與 RNN 長程依賴的結合流程圖<br/>• 雙向 BiLSTM：正向 + 反向上下文捕捉情感脈絡<br/>• 消融實證：移除 LSTM 準確率下滑至 95%，單向退化至 89% | [architectures/crnn-architectures.md](../architectures/crnn-architectures.md)<br/>[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)<br/>[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md) |
| **08** | **聚焦情緒爆發點：Attention 注意力機制的魔力** | • 情緒顯著性（Emotional Salience）：不是每一秒都充滿情緒<br/>• 時序自注意力權重加權公式 $\alpha_t$ 與動態熱圖<br/>• 相近情緒區隔效果：解決 Neutral vs Calm 與 Sad 混淆 | [architectures/attention-mechanisms.md](../architectures/attention-mechanisms.md)<br/>[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)<br/>[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md) |
| **09** | **自監督基石：HuBERT 的遮罩聲學單元預測** | • 連續波形如何做自監督？離線 K-means 分群挖掘隱藏單元<br/>• 7 層 Conv1D（320 倍下採樣）+ Transformer 遮罩預測<br/>• 迭代精煉：PNMI 互資訊從 0.253 提升至 0.686 的震撼飛躍 | [papers/2021-hsu-hubert.md](../papers/2021-hsu-hubert.md)<br/>[concepts/speech-representations.md](../concepts/speech-representations.md) |
| **10** | **極致輕量化：LiSER 跨模態知識蒸餾 (105K 參數)** | • 邊緣終端困境：大模型（HuBERT）無法上手機怎麼辦？<br/>• 雙教師架構：HuBERT 語音教師 + S2D ViT 動態人臉教師<br/>• 利用野生無標註影音（MSP-Face）蒸餾，50% 標籤超越全數據基準 | [papers/2025-pendyala-liser-distillation.md](../papers/2025-pendyala-liser-distillation.md)<br/>[architectures/crnn-architectures.md](../architectures/crnn-architectures.md) |
| **11** | **通用共情對話：Qwen2-Audio 與 Speech LLM 時代** | • 從專用分類器走向生成式語音大模型（LALM, 8.2B 參數）<br/>• Whisper-v3（128-Mel）+ Qwen-7B 解碼器架構<br/>• MELD 對話情緒零樣本 55.3% 與 AIR-Bench 語音共情 7.18 分 | [papers/2024-chu-qwen2-audio.md](../papers/2024-chu-qwen2-audio.md)<br/>[architectures/attention-mechanisms.md](../architectures/attention-mechanisms.md) |
| **12** | **全景回顧與未來展望：SER 技術樹與挑戰** | • 技術全景對比矩陣（手製特徵 $\to$ CRNN $\to$ SSL $\to$ Audio-LLM）<br/>• 三大核心權衡：模型大小（105K vs 8.2B）、標註成本與泛化極限<br/>• 課後思考與實務專題指引 | [index.md](../index.md)<br/>[concepts/evaluation-metrics.md](../concepts/evaluation-metrics.md) |
