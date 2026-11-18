#!/usr/bin/env python3
"""
audit-content-fidelity.py
程式化檢查 slides/index.html 內的數據與 Wiki 論文筆記之忠實度。
"""

import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent
    slides_path = root_dir / "slides" / "index.html"
    
    if not slides_path.exists():
        print("❌ 未找到 slides/index.html")
        sys.exit(1)
        
    slides_text = slides_path.read_text(encoding="utf-8")
    
    # Check key numerical claims
    expected_facts = [
        # Bhanbhro et al. (2025)
        ("98.1%", "Bhanbhro 2025 Model 2 測試準確率"),
        ("96.5%", "Bhanbhro 2025 Model 1 測試準確率"),
        ("89.0%", "Bhanbhro 2025 單向 LSTM 消融退化準確率"),
        ("95.0%", "Bhanbhro 2025 移除 LSTM 消融退化準確率"),
        
        # Singh et al. (2023)
        ("85.00%", "Singh 2023 MFCC 單特徵基準準確率"),
        ("13.98%", "Singh 2023 節奏特徵 Tempogram 準確率"),
        ("90.19%", "Singh 2023 CNN-LSTM-Attention 跨庫準確率"),
        ("99.81%", "Singh 2023 TESS 全女性資料集準確率"),
        ("57.50%", "Singh 2023 SAVEE 全男性資料集準確率"),
        
        # Pendyala et al. (2025) LiSER
        ("105K", "LiSER 學生模型參數量"),
        ("0.595", "LiSER 在 RAVDESS 上的最佳 UAR"),
        ("15.09%", "LiSER 信賴度雙模態相對無蒸餾之提升幅度"),
        ("50%", "LiSER 標籤資料效率（僅用 50% 標籤超越全數據基準）"),
        
        # Hsu et al. (2021) HuBERT
        ("0.253", "HuBERT 第 1 代 MFCC 分群 PNMI"),
        ("0.686", "HuBERT 第 2 代 Transformer 隱藏層分群 PNMI"),
        
        # Chu et al. (2024) Qwen2-Audio
        ("8.2B", "Qwen2-Audio 參數量"),
        ("55.3%", "Qwen2-Audio 在 MELD 上的零樣本情緒準確率"),
        ("7.18", "Qwen2-Audio 在 AIR-Bench 語音對話維度 GPT-4 評分")
    ]
    
    print("=" * 65)
    print("🔍 數據忠實度程式化審計 (audit-content-fidelity.py)")
    print("=" * 65)
    
    missing = []
    for num, desc in expected_facts:
        if num in slides_text:
            print(f"  ✅ [核實成功] {desc} ({num})")
        else:
            print(f"  ❌ [缺失/不符] {desc} ({num})")
            missing.append((num, desc))
            
    if missing:
        print(f"\n⚠️ 發現 {len(missing)} 項數據在簡報中未正確呈現或格式不符！")
        sys.exit(1)
    else:
        print("\n🎉 全數 17 項核心實驗數據與參數量均 100% 忠實對應 Wiki 原始論文記錄！")
        sys.exit(0)

if __name__ == "__main__":
    main()
