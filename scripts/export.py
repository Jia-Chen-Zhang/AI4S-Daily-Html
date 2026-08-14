#!/usr/bin/env python3
"""news-data → 静态 JSON 导出(GitHub Pages 数据源)

从主仓库的 news-data/push-*.md 解析报告,导出为本仓库 public/data/ 下的静态 JSON:
  reports.json            报告摘要列表(时间倒序)
  details/{id}.json       报告详情(板块数组)
  sections/{key}.json     栏目流(overview/insights/gaps/rss/hackernews)

安全边界:relevance(与当前工作的相关性)板块涉及内部工作方向,一律不导出。

自包含实现(仅依赖 pyyaml),解析逻辑与主仓库 src/web/reports.py 保持一致。
在主仓库根目录执行:  uv run python gitweb/scripts/export.py
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("❌ 需要 pyyaml,请在主仓库环境运行: uv run python gitweb/scripts/export.py")

GITWEB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NEWS_DATA = GITWEB_ROOT.parent / "news-data"
DEFAULT_OUT = GITWEB_ROOT / "public" / "data"

# 板块顺序与主仓库 storage._SECTION_ORDER 一致
_SECTION_ORDER = ("insights", "relevance", "gaps", "rss", "hackernews")
# 敏感板块,不导出
_EXCLUDED_KEYS = {"relevance"}
# 栏目流 key
STREAM_KEYS = ("overview", "insights", "gaps", "rss", "hackernews")

_REPORT_FILE_RE = re.compile(r"^push-(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})\.md$")
_H1_RE = re.compile(r"^#\s+(.+)$", re.M)
_H2_RE = re.compile(r"^##\s+(.+)$", re.M)

SECTION_TITLE_FALLBACK = {
    "overview": "总览",
    "insights": "今日洞察",
    "gaps": "问题发现",
    "rss": "今日Top热点",
    "hackernews": "Hacker News 热议",
}
_INSIGHTS_H2_KEYS = {"总览": "overview", "今日洞察": "insights"}


# ─── 解析(vendored,与主仓库逻辑一致) ─────────────────────────


def parse_frontmatter(text: str):
    """分离 YAML frontmatter 与正文;无 frontmatter 返回 ({}, 原文)"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    try:
        meta = yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}, text
    body = text[end + 4 :].lstrip("\n")
    return (meta if isinstance(meta, dict) else {}), body


def extract_section(push_md: str, section: str) -> str:
    """切出 <!-- SECTION:{section} BEGIN/END --> 之间的 markdown;
    无 sentinel 的老文件 section=='rss' 时返回全文"""
    pattern = re.compile(
        rf"<!--\s*SECTION:{re.escape(section)}\s*BEGIN\s*-->(.*?)<!--\s*SECTION:{re.escape(section)}\s*END\s*-->",
        re.DOTALL,
    )
    m = pattern.search(push_md)
    if m:
        return m.group(1)
    if section == "rss" and "<!-- SECTION:" not in push_md:
        return push_md
    return ""


def _strip_heading(md: str, level: str) -> str:
    return re.sub(rf"\A\s*{level}\s+[^\n]*\n*", "", md, count=1).strip()


def _split_insights(md: str):
    chunks = [c.strip() for c in re.split(r"(?m)(?=^## )", md) if c.strip()]
    if not chunks:
        return []
    if not any(_H2_RE.match(c.splitlines()[0]) for c in chunks):
        return [{"key": "insights", "title": SECTION_TITLE_FALLBACK["insights"], "markdown": md.strip()}]
    sections, preamble = [], ""
    for chunk in chunks:
        first_line = chunk.splitlines()[0]
        if not _H2_RE.match(first_line):
            preamble += chunk + "\n\n"
            continue
        body = (preamble + chunk).strip()
        preamble = ""
        title = _H2_RE.match(first_line).group(1).strip()
        sections.append({"key": _INSIGHTS_H2_KEYS.get(title, "insights"), "title": title, "markdown": body})
    if preamble.strip() and sections:
        sections[-1]["markdown"] += "\n\n" + preamble.strip()
    return sections


def split_sections(body: str):
    sections = []
    for key in _SECTION_ORDER:
        if key in _EXCLUDED_KEYS:
            continue  # 敏感板块不导出
        md = extract_section(body, key)
        if not md.strip():
            continue
        if key == "rss":
            _, md = parse_frontmatter(md)
            md = _strip_heading(md, "#")
        md = md.strip()
        if not md:
            continue
        if key == "insights":
            sections.extend(_split_insights(md))
            continue
        h2 = _H2_RE.search(md)
        sections.append(
            {
                "key": key,
                "title": h2.group(1).strip() if h2 else SECTION_TITLE_FALLBACK[key],
                "markdown": md,
            }
        )
    return sections


def normalize_str_list(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value]
    return []


def parse_report(path: Path):
    m = _REPORT_FILE_RE.fullmatch(path.name)
    if not m:
        return None
    report_id = m.group(1)
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))

    date_str, time_str = report_id[:10], f"{report_id[11:13]}:{report_id[14:16]}"
    if meta:
        title = str(meta.get("title") or "").strip()
        profile = str(meta.get("profile") or "default")
        lead = str(meta.get("lead") or "")
        highlights = normalize_str_list(meta.get("highlights"))
        source_count, total_entries = meta.get("sourceCount"), meta.get("totalEntries")
    else:
        title = ""
        profile = "morning" if "<!-- SECTION:" in body else "default"
        lead, highlights = "", []
        source_count = total_entries = None
    if not title:
        h1 = _H1_RE.search(body)
        title = h1.group(1).strip() if h1 else f"AI4S 报告 {date_str}"

    return {
        "id": report_id,
        "date": date_str,
        "time": time_str,
        "profile": profile,
        "title": title,
        "lead": lead,
        "highlights": highlights,
        "sourceCount": source_count,
        "totalEntries": total_entries,
        "sections": split_sections(body),
    }


# ─── 导出 ────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="news-data → 静态 JSON 导出")
    parser.add_argument("--news-data", default=str(DEFAULT_NEWS_DATA))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    news_data, out = Path(args.news_data), Path(args.out)
    if not news_data.is_dir():
        sys.exit(f"❌ news-data 目录不存在: {news_data}")

    reports = []
    for f in sorted(news_data.glob("push-*.md")):
        if f.stat().st_size == 0:
            continue
        try:
            r = parse_report(f)
        except Exception as e:
            print(f"⚠️ 解析失败,跳过 {f.name}: {e}")
            continue
        if r and r["sections"]:
            reports.append(r)
    reports.sort(key=lambda r: r["id"], reverse=True)
    if not reports:
        sys.exit("❌ 未解析到任何报告")

    # 全量重建输出目录
    if out.exists():
        shutil.rmtree(out)
    (out / "details").mkdir(parents=True)
    (out / "sections").mkdir(parents=True)

    def dump(rel, obj):
        (out / rel).write_text(
            json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8"
        )

    summaries = []
    streams = {k: [] for k in STREAM_KEYS}
    for r in reports:
        for sec in r["sections"]:
            if sec["key"] in streams:
                streams[sec["key"]].append(
                    {
                        "report_id": r["id"],
                        "date": r["date"],
                        "time": r["time"],
                        "profile": r["profile"],
                        "title": sec["title"],
                        "markdown": _strip_heading(sec["markdown"], "##"),
                    }
                )
        dump(f"details/{r['id']}.json", r)
        summaries.append({**r, "sections": [s["key"] for s in r["sections"]]})

    dump("reports.json", summaries)
    for key, entries in streams.items():
        dump(f"sections/{key}.json", entries)

    print(f"✅ 导出 {len(reports)} 份报告 → {out}")
    for key in STREAM_KEYS:
        print(f"   {key}: {len(streams[key])} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
