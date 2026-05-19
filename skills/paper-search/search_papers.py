"""
paper-search skill: arxiv paper search with exponential backoff.
Usage:
    python search_papers.py [--query "SLM"] [--since 2025-01-01] [--max 10]
"""
import sys
import urllib.request
import xml.etree.ElementTree as ET
import time
import argparse

# 強制 utf-8 輸出，防止 Windows cp950 亂碼
sys.stdout.reconfigure(encoding="utf-8")

NS = "http://www.w3.org/2005/Atom"

# 必須包含其中一個詞才算命中（二次過濾，防止不相關論文混入）
RELEVANCE_KEYWORDS = [
    "small language model", "slm", "on-device", "on-premise",
    "edge inference", "local llm", "tiny language", "compact language model",
    "language model deployment", "efficient language model",
]

DEFAULT_QUERIES = [
    "ti:small+language+model",
    "ti:SLM+AND+ti:language",
    "all:on-device+AND+all:language+model",
    "ti:efficient+AND+ti:language+model+AND+ti:deployment",
]


def search_arxiv(query: str, max_results: int = 20, since: str = "2025-01-01") -> list:
    url = (
        "https://export.arxiv.org/api/query"
        f"?search_query={query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate&sortOrder=descending"
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                root = ET.fromstring(resp.read())
            papers = []
            for entry in root.findall(f"{{{NS}}}entry"):
                pub = entry.find(f"{{{NS}}}published")
                if pub is None:
                    continue
                date = pub.text[:10]
                if date < since:
                    continue
                id_elem = entry.find(f"{{{NS}}}id")
                arxiv_id = id_elem.text.split("/abs/")[-1] if id_elem is not None else ""
                authors = [
                    a.find(f"{{{NS}}}name").text
                    for a in entry.findall(f"{{{NS}}}author")[:2]
                    if a.find(f"{{{NS}}}name") is not None
                ]
                summary = entry.find(f"{{{NS}}}summary")
                abstract = (summary.text.strip()[:200] + "...") if summary is not None else ""
                title_elem = entry.find(f"{{{NS}}}title")
                title = " ".join(title_elem.text.split()) if title_elem is not None else ""
                # 二次過濾：title 或 abstract 需包含相關關鍵字
                combined = (title + " " + abstract).lower()
                if not any(kw in combined for kw in RELEVANCE_KEYWORDS):
                    continue
                papers.append({
                    "date": date,
                    "title": title,
                    "authors": ", ".join(authors),
                    "id": arxiv_id,
                    "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                    "abstract": abstract,
                })
            return papers
        except Exception as e:
            wait = 15 * (2 ** attempt)
            print(f"[警告] 第 {attempt + 1} 次失敗：{e}，等待 {wait}s 後重試")
            time.sleep(wait)
    return []


def main():
    parser = argparse.ArgumentParser(description="arxiv 論文候選清單搜尋")
    parser.add_argument("--since", default="2025-01-01", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--max", type=int, default=10, help="最終輸出筆數")
    parser.add_argument("--query", default=None, help="自訂 arxiv 查詢字串（覆蓋預設）")
    args = parser.parse_args()

    queries = [args.query] if args.query else DEFAULT_QUERIES

    seen, results = set(), []
    for q in queries:
        print(f"\n[搜尋] {q}")
        for p in search_arxiv(q, max_results=20, since=args.since):
            if p["id"] not in seen:
                seen.add(p["id"])
                results.append(p)
        time.sleep(10)

    results.sort(key=lambda x: x["date"], reverse=True)
    top = results[:args.max]

    print(f"\n{'='*60}")
    print(f"找到 {len(results)} 筆 (2025+)，顯示最新 {len(top)} 筆")
    print(f"{'='*60}\n")

    for i, p in enumerate(top, 1):
        print(f"[{i}] {p['date']} — {p['title']}")
        print(f"     作者: {p['authors']}")
        print(f"     ID:   https://arxiv.org/abs/{p['id']}")
        print(f"     PDF:  {p['pdf']}")
        print(f"     摘要: {p['abstract']}")
        print()


if __name__ == "__main__":
    main()
