#!/usr/bin/env python3
"""
check-orphan-pages.py
檢查 Wiki 內是否存在未被 index.md 或其他頁面引用的孤立頁面 (Orphan Pages)。
"""

import os
import re
import sys
from pathlib import Path

def find_all_markdown_files(root_dir: Path):
    target_dirs = ["concepts", "architectures", "papers"]
    md_files = []
    for d in target_dirs:
        dir_path = root_dir / d
        if dir_path.exists():
            for p in dir_path.glob("**/*.md"):
                if p.name != "README.md":
                    md_files.append(p.resolve())
    return md_files

def extract_links_from_file(file_path: Path):
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return set()

    # Match standard markdown links: [label](path)
    # Ignore web URLs starting with http:// or https:// or mailto:
    pattern = r"\[.*?\]\((?!https?:\/\/|mailto:)([^\)#\s]+)(?:#[^\)]*)?\)"
    raw_links = re.findall(pattern, content)
    
    resolved_links = set()
    parent_dir = file_path.parent
    for link in raw_links:
        # Normalize and resolve link relative to the current file
        target = (parent_dir / link).resolve()
        resolved_links.add(target)
    return resolved_links

def main():
    root_dir = Path(__file__).resolve().parent.parent
    index_file = root_dir / "index.md"
    
    if not index_file.exists():
        print("❌ Error: index.md not found!")
        sys.exit(1)

    all_content_files = find_all_markdown_files(root_dir)
    
    # Collect all outgoing links across all markdown files in root, concepts, architectures, papers
    all_known_mds = list(root_dir.glob("*.md")) + [p for p in root_dir.glob("**/*.md") if ".git" not in str(p)]
    
    referenced_files = set()
    for md in all_known_mds:
        links = extract_links_from_file(md)
        referenced_files.update(links)

    # Check for orphan pages
    orphan_pages = []
    for f in all_content_files:
        if f not in referenced_files:
            orphan_pages.append(f)

    print("=" * 60)
    print("🔍 SER LLM Wiki - 孤立頁面 (Orphan Pages) 檢查報告")
    print("=" * 60)
    print(f"檢測檔案總數：{len(all_content_files)} 篇知識條目")
    
    if not orphan_pages:
        print("✅ 恭喜！未發現任何孤立頁面，所有知識文件皆已被 index.md 或相關頁面正確索引。")
        sys.exit(0)
    else:
        print(f"⚠️ 警告：發現 {len(orphan_pages)} 個孤立頁面未被任何文件引用：")
        for op in orphan_pages:
            rel_path = op.relative_to(root_dir)
            print(f"  - {rel_path}")
        print("\n請至 index.md 或對應的概念/架構頁面補上雙向超連結。")
        sys.exit(1)

if __name__ == "__main__":
    main()
