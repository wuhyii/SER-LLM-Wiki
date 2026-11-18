# 語音訊號表示與頻譜特徵 (Speech Representations & Features)

> 本頁面已整合文獻實證數據。
> 最新匯入文獻：[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)
> 回到總覽：[首頁 (index.md)](../index.md)

---

## 1. 一維時域波形 (Raw Waveform)

連續語音信號 $x(t)$ 經由麥克風轉換為類比電氣訊號後，透過**取樣（Sampling）**與**量化（Quantization）**轉換為離散時間數位訊號 $x[n]$：

$$x[n] = x(n T_s) = x\left(\frac{n}{f_s}\right)$$

其中：
- $f_s$ 為取樣頻率（Sampling Rate，常見如 16,000 Hz / 16 kHz）。
- $T_s = \frac{1}{f_s}$ 為取樣間隔時間（Sampling Period）。
- $n \in \mathbb{Z}$ 為離散時間索引。

一維波形富含精細時序資訊，但在情緒辨識中，語音情緒往往更直接反映在頻率分佈（如音高基頻 $F_0$、共振峰 Formants、頻譜能量分佈）的變化上。

---

## 2. 短時距傅立葉變換 (Short-Time Fourier Transform, STFT)

由於語音訊號具有**非平穩性（Non-stationary）**，但於極短時間區間內（約 20 ms 至 30 ms）可視為**準平穩訊號（Quasi-stationary）**。因此透過加窗切分計算 STFT：

$$X(m, \omega) = \sum_{n=-\infty}^{\infty} x[n] \cdot w[n - m H] \cdot e^{-j \omega n}$$

其中：
- $w[n]$ 為長度為 $N$ 的窗函數（如 Hamming 窗或 Hanning 窗），用以減少頻譜洩漏（Spectral Leakage）。
- $m \in \mathbb{Z}$ 為幀索引（Frame Index）。
- $H$ 為幀移/步長（Hop Size 或 Stride）。
- $\omega = \frac{2\pi k}{K}$ 為角頻率，其中 $k$ 為頻率箱索引（Frequency Bin），$K$ 為離散傅立葉變換（DFT）長度（通常為 512 或 1024）。

其離散形式（Discrete STFT）之複數譜矩陣為：

$$X[m, k] = \sum_{n=0}^{N-1} x[m H + n] \cdot w[n] \cdot e^{-j \frac{2\pi k n}{K}}$$

功率譜密度（Power Spectrogram）定義為其模長平方：

$$P[m, k] = |X[m, k]|^2$$

---

## 3. 梅爾頻譜 (Mel-Spectrogram) 與對數變換

### 3.1 梅爾刻度轉換 (Mel Scale Transformation)
人類聽覺系統對低頻聲音具有較高的頻率解析度，對高頻聲音的辨別力則逐漸呈對數遞減。梅爾刻度（Mel Scale）模擬人耳聽覺的臨界頻帶（Critical Bands），其物理頻率 $f$（Hz）與梅爾頻率 $m$（Mels）的嚴格轉換公式如下：

$$m = 2595 \cdot \log_{10}\left(1 + \frac{f}{700}\right) = 1127 \cdot \ln\left(1 + \frac{f}{700}\right)$$

其反轉換公式為：

$$f = 700 \cdot \left(10^{\frac{m}{2595}} - 1\right) = 700 \cdot \left(e^{\frac{m}{1127}} - 1\right)$$

### 3.2 梅爾三角濾波器組 (Mel Filterbank)
定義 $M$ 個重疊的三角帶通濾波器 $H_m[k]$（$m = 1, 2, \dots, M$），其中心頻率 $f_c(m)$ 均勻分佈於梅爾刻度上。每個濾波器的權重定義為：

$$H_m[k] = \begin{cases} 
0 & k < f[m-1] \\
\frac{k - f[m-1]}{f[m] - f[m-1]} & f[m-1] \le k \le f[m] \\
\frac{f[m+1] - k}{f[m+1] - f[m]} & f[m] \le k \le f[m+1] \\
0 & k > f[m+1]
\end{cases}$$

梅爾頻譜特徵即為功率譜通過該濾波器組的矩陣乘法求和：

$$S_{\text{Mel}}[m, i] = \sum_{k=0}^{K/2} P[m, k] \cdot H_i[k], \quad i = 1, 2, \dots, M$$

### 3.3 對數壓縮 (Log-Mel Spectrogram)
模擬人耳對聲音強度（Loudness）的對數感知特性：

$$S_{\text{Log-Mel}}[m, i] = \log\left(S_{\text{Mel}}[m, i] + \epsilon\right)$$

其中 $\epsilon > 0$（例如 $10^{-6}$）為防止計算數值溢位之微小常數。

---

## 4. 深度學習張量維度 (Tensor Representation for Deep Learning)

在將 Log-Mel 頻譜圖送入深度神經網絡（如 CNN、CRNN）時，其通常被塑造為二維單通道「音訊影像」：

$$\mathbf{X} \in \mathbb{R}^{B \times C \times T \times F}$$

- $B$：Batch Size（批次大小）
- $C$：Channel 數（單聲道頻譜圖為 $1$，若附加一階差分 Delta 與二階差分 Delta-Delta 則為 $3$）
- $T$：時間幀長度（Time Frames，由語音長度與 Hop Size 決定）
- $F$：頻率維度（Frequency Bins，即 Mel 濾波器數量 $M$，常見為 $40, 64, 80, 128$）

---

## 5. 文獻實證配置與特徵選用對比 (Empirical Feature Comparisons)

在收錄的 5 篇核心文獻中，各研究針對語音特徵表徵提出了不同的選用策略與實證驗證：

### 5.1 頻譜特徵 vs 節奏特徵之消融實證
[Singh et al. (2023)](../papers/2023-singh-attention-cnn-lstm.md) 針對 10 餘種音訊特徵在情緒分類任務上進行了嚴謹消融比對：
- **節奏特徵（Rhythmic Features）的極限**：單獨使用節奏圖（Tempogram + Fourier-tempogram）的基準準確率僅有 **13.98%**，顯示節奏特徵無法獨立表徵情緒。
- **倒頻譜係數（MFCC）的優勢**：單獨使用 MFCC 即可達到 **85.00%** 的基準準確率。在 MFCC 基礎上額外疊加節奏特徵（85.70%）並無顯著增益，反而徒增維度與計算負擔。

### 5.2 經典 Log-Mel 頻譜圖之參數工程配置
在深度學習 SER 模型中，對數梅爾頻譜圖為最通用的二維特徵輸入，各代表論文之具體參數配置如下：
- **[Bhanbhro et al. (2025)](../papers/2025-bhanbhro-cnn-lstm-attention.md)**：採樣率 16 kHz，窗長 $N = 25 \text{ ms}$（400 採樣點），步長 $H = 10 \text{ ms}$（160 採樣點，即 15 ms 重疊），配合動態 SNR 15–30 dB 之 AWGN 雜訊增強。
- **[Pendyala et al. (2025) LiSER](../papers/2025-pendyala-liser-distillation.md)**：採樣率 16 kHz，窗長 $128 \text{ ms}$，步長 $32 \text{ ms}$，提取 **64 個 Mel 頻帶**，音訊切片長度固定為 3 秒。
- **[Chu et al. (2024) Qwen2-Audio](../papers/2024-chu-qwen2-audio.md)**：採樣率 16 kHz，窗長 $25 \text{ ms}$，步長 $10 \text{ ms}$，提取 **128 維 Mel 濾波器組**，接續 stride=2 池化層，每幀表徵 40 ms 語音信號。

### 5.3 自監督表徵學習：從連續波形到離散聲學單元
相較於人工設計的 MFCC 或 Log-Mel 特徵，[Hsu et al. (2021) HuBERT](../papers/2021-hsu-hubert.md) 證實了透過卷積波形編碼器（7 層 Conv1D，總下採樣 320 倍）與 Transformer 遮罩預測，能自發捕捉語音結構：
- 第一階段在 39 維 MFCC 上執行 K-means 分群（PNMI 為 0.253）；
- 第二階段在 Transformer 隱藏層進行分群精煉（PNMI 躍升至 0.686），大幅超越傳統手工特徵的語音語意純度。

---

## 6. 關聯條目與文獻索引 (References & Cross-Links)
- 論文專頁：
  - [Bhanbhro et al. (2025) - 2D CNN-BiLSTM 頻譜情緒辨識](../papers/2025-bhanbhro-cnn-lstm-attention.md)
  - [Singh et al. (2023) - MFCC 特徵與 Attention 模型](../papers/2023-singh-attention-cnn-lstm.md)
  - [Pendyala et al. (2025) - LiSER 輕量化 Log-Mel 蒸餾](../papers/2025-pendyala-liser-distillation.md)
  - [Hsu et al. (2021) - HuBERT 語音基底特徵學習](../papers/2021-hsu-hubert.md)
  - [Chu et al. (2024) - Qwen2-Audio 128 維 Mel 特徵與 LALM](../papers/2024-chu-qwen2-audio.md)
- 評測指標：[SER 評估指標與評測協議](evaluation-metrics.md)
- 模型架構：[卷積神經網路 (CNN for SER)](../architectures/cnn-for-ser.md)、[CRNN 架構](../architectures/crnn-architectures.md)、[注意力機制](../architectures/attention-mechanisms.md)
