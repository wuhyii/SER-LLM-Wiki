#!/usr/bin/env python3
"""
verify-slides.py
實際執行 Wiki 與 HTML 簡報之自動化品質驗證。
涵蓋節點 1 (Wiki 來源足夠性)、節點 3 (大綱覆蓋率)、節點 5 (12 頁結構、導覽功能、連結、手機/桌面排版與溢出保護)。
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

class SlideVerifier(HTMLParser):
    def __init__(self, root_dir: Path):
        super().__init__()
        self.root_dir = root_dir
        self.slides = {}
        self.current_slide_idx = None
        self.current_slide_cites = 0
        self.slide_cites = {}
        self.buttons = set()
        self.element_ids = set()
        self.hrefs = []
        self.in_script = False
        self.script_content = ""
        self.in_style = False
        self.style_content = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        elem_id = attr_dict.get("id")
        if elem_id:
            self.element_ids.add(elem_id)

        if tag == "button" and elem_id:
            self.buttons.add(elem_id)

        if tag == "section" and "slide" in attr_dict.get("class", "").split():
            idx = attr_dict.get("data-index")
            if idx:
                self.current_slide_idx = int(idx)
                self.slides[self.current_slide_idx] = {
                    "tag": tag,
                    "classes": attr_dict.get("class", "")
                }
                self.slide_cites[self.current_slide_idx] = 0

        if "cite-badge" in attr_dict.get("class", "") and self.current_slide_idx:
            self.slide_cites[self.current_slide_idx] += 1

        if tag == "a" and "href" in attr_dict:
            self.hrefs.append((self.current_slide_idx, attr_dict["href"]))

        if tag == "script":
            self.in_script = True

        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        if tag == "style":
            self.in_style = False
        if tag == "section":
            self.current_slide_idx = None

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data
        if self.in_style:
            self.style_content += data

def check_node_1_wiki_sufficiency(root_dir: Path):
    errors = []
    # 1. Check raw/ PDFs
    raw_pdfs = list((root_dir / "raw").glob("*.pdf"))
    if len(raw_pdfs) < 5:
        errors.append(f"raw/ 中的論文 PDF 數量不足 5 篇（目前僅 {len(raw_pdfs)} 篇）")

    # 2. Check papers/ markdown notes
    paper_notes = [p for p in (root_dir / "papers").glob("*.md") if p.name != "README.md"]
    if len(paper_notes) < 5:
        errors.append(f"papers/ 中的結構化筆記不足 5 篇（目前僅 {len(paper_notes)} 篇）")

    # 3. Check concepts & architectures
    req_concepts = ["speech-representations.md", "evaluation-metrics.md"]
    for c in req_concepts:
        if not (root_dir / "concepts" / c).exists():
            errors.append(f"缺少必要概念頁面：concepts/{c}")

    req_archs = ["cnn-for-ser.md", "crnn-architectures.md", "attention-mechanisms.md"]
    for a in req_archs:
        if not (root_dir / "architectures" / a).exists():
            errors.append(f"缺少必要架構頁面：architectures/{a}")

    return errors, len(raw_pdfs), len(paper_notes)

def check_node_3_outline_coverage(root_dir: Path):
    errors = []
    outline_path = root_dir / "reports" / "slide-outline.md"
    if not outline_path.exists():
        errors.append("未找到 reports/slide-outline.md")
        return errors

    content = outline_path.read_text(encoding="utf-8")
    for i in range(1, 13):
        pattern = rf"\*\*0?{i}\*\*"
        if not re.search(pattern, content):
            errors.append(f"大綱中未明確標註 Slide {i} 的章節定義")
    return errors

def check_node_5_slides_code_and_layout(root_dir: Path):
    errors = []
    slide_file = root_dir / "slides" / "index.html"
    if not slide_file.exists():
        errors.append("未找到 slides/index.html")
        return errors, None

    content = slide_file.read_text(encoding="utf-8")
    verifier = SlideVerifier(root_dir)
    verifier.feed(content)

    # 1. Check 12 slides structure
    slide_indices = sorted(verifier.slides.keys())
    if slide_indices != list(range(1, 13)):
        errors.append(f"簡報頁數結構不符合預期（期望 1~12，實際為 {slide_indices}）")

    # 2. Check navigation components
    required_ids = ["btn-prev", "btn-next", "btn-fullscreen", "slide-indicator", "progress-bar", "dots-container"]
    for req_id in required_ids:
        if req_id not in verifier.element_ids:
            errors.append(f"缺少導覽控制元件：id='{req_id}'")

    # 3. Check script navigation logic
    req_keys = ["ArrowRight", "ArrowLeft", "Space", "PageDown", "PageUp"]
    for k in req_keys:
        if k not in verifier.script_content:
            errors.append(f"JavaScript 鍵盤監聽事件缺少按鍵支援：'{k}'")

    # 4. Check citations on each slide
    for idx, count in verifier.slide_cites.items():
        if count == 0:
            errors.append(f"Slide {idx} 未找到任何出處標註（cite-badge）")

    # 5. Check links validity
    slides_dir = root_dir / "slides"
    for slide_idx, href in verifier.hrefs:
        if href.startswith("http://") or href.startswith("https://") or href.startswith("#"):
            continue
        elif href.startswith("file:///"):
            # Check file url
            clean_path = href.replace("file:///", "").replace("/", "\\")
            if not Path(clean_path).exists():
                errors.append(f"Slide {slide_idx} 包含無效 file:// 路徑：{href}")
        else:
            # Relative path from slides/
            target_path = (slides_dir / href).resolve()
            if not target_path.exists():
                errors.append(f"Slide {slide_idx} 包含無效相對連結：{href}（目標不存在：{target_path}）")

    # 6. Check Desktop vs Mobile responsive CSS layout and overflow protection
    style_text = verifier.style_content
    # Check media queries for responsive mobile layout
    if "@media" not in style_text or "max-width" not in style_text:
        errors.append("【排版缺陷】CSS 中未包含行動裝置媒體查詢 (@media max-width)，手機檢視可能發生嚴重排版破裂")
    else:
        # Check if mobile rules handle grid collapse (e.g. grid-template-columns: 1fr)
        if "grid-template-columns: 1fr" not in style_text and "grid-template-columns: repeat(1" not in style_text:
            errors.append("【排版缺陷】行動裝置媒體查詢中未將多欄網格 (grid-2/3/4) 折疊為單欄 (1fr)，可能導致文字嚴重擠壓")

    # Check overflow protection
    if "overflow-x: hidden" not in style_text and "overflow-x:hidden" not in style_text:
        errors.append("【排版缺陷】缺少全域水平防溢出設定 (overflow-x: hidden)，小螢幕可能出現橫向滾動溢出")

    return errors, verifier

def main():
    root_dir = Path(__file__).resolve().parent.parent
    print("=" * 65)
    print("🚦 SER LLM Wiki → 教學簡報 程式化品質驗證 (verify-slides.py)")
    print("=" * 65)

    all_passed = True

    # Node 1 Check
    print("\n[Node 1] 檢驗 Wiki 來源足夠性...")
    n1_errors, pdf_count, note_count = check_node_1_wiki_sufficiency(root_dir)
    if n1_errors:
        all_passed = False
        print("❌ [Node 1 失敗]:")
        for e in n1_errors:
            print(f"  - {e}")
    else:
        print(f"✅ [Node 1 通過]: raw/ 具備 {pdf_count} 篇 PDF，papers/ 具備 {note_count} 篇筆記，概念與架構完備。")

    # Node 3 Check
    print("\n[Node 3] 檢驗簡報大綱與覆蓋率...")
    n3_errors = check_node_3_outline_coverage(root_dir)
    if n3_errors:
        all_passed = False
        print("❌ [Node 3 失敗]:")
        for e in n3_errors:
            print(f"  - {e}")
    else:
        print("✅ [Node 3 通過]: reports/slide-outline.md 涵蓋全部 12 頁教學主題。")

    # Node 5 Check
    print("\n[Node 5] 檢驗 slides/index.html 程式碼結構、導覽與響應式排版...")
    n5_errors, verifier = check_node_5_slides_code_and_layout(root_dir)
    if n5_errors:
        all_passed = False
        print(f"❌ [Node 5 失敗]: 發現 {len(n5_errors)} 項缺陷：")
        for e in n5_errors:
            print(f"  - {e}")
    else:
        print("✅ [Node 5 通過]: 12 頁結構正常、導覽控制完整、超連結有效、具備手機/桌面自適應排版與防溢出保護。")

    print("\n" + "=" * 65)
    if all_passed:
        print("🎉 驗證全數通過！所有檢查項目均符合品質規範要求。")
        sys.exit(0)
    else:
        print("⚠️ 驗證未通過，請根據上述錯誤訊息回退至對應節點進行修正！")
        sys.exit(1)

if __name__ == "__main__":
    main()
