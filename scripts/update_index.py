#!/usr/bin/env python3
"""ideas/ 配下の candidates*.md を走査して INDEX.md と STATS.md を再生成する。

呼び出し元:
- .github/workflows/update-index.yml (人間 / routine の push 時)
- .github/workflows/select-issue.yml / reject-issue.yml (GITHUB_TOKEN push は
  workflow を再発火しないため、commit 前に自前で実行する)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDEAS = ROOT / "ideas"
POC = ROOT / "poc"


def batch_of(fname: str) -> int:
    m = re.match(r"candidates(?:-(\d+))?\.md$", fname)
    if not m:
        return 0
    return int(m.group(1)) if m.group(1) else 1


def esc(text: str) -> str:
    """Markdown テーブルセル用エスケープ。"""
    return text.replace("|", "\\|").replace("\n", " ")


def collect() -> list[dict]:
    ideas: list[dict] = []
    for path in sorted(IDEAS.glob("*/W*/candidates*.md")):
        year = path.parent.parent.name
        week = path.parent.name  # 例: W21
        batch = batch_of(path.name)
        if batch == 0:
            continue
        text = path.read_text(encoding="utf-8")
        selected = {int(m.group(1)) for m in re.finditer(r"^> Selected:\s*#(\d+)", text, flags=re.M)}
        rejected = {int(m.group(1)) for m in re.finditer(r"^> Rejected:\s*#(\d+)", text, flags=re.M)}
        for block in re.split(r"^---\s*$", text, flags=re.M):
            m_title = re.search(r"^## (\d+)\.\s+(.+?)\s*$", block, flags=re.M)
            if not m_title:
                continue
            num = int(m_title.group(1))
            title = m_title.group(2).strip()
            cat = re.search(r"^-\s*カテゴリ:\s*(.+?)\s*$", block, flags=re.M)
            line = re.search(r"^-\s*一行で:\s*(.+?)\s*$", block, flags=re.M)
            status = "selected" if num in selected else ("rejected" if num in rejected else "")
            ideas.append(
                {
                    "id": f"{year}-{week}-{batch}#{num}",
                    "year": int(year),
                    "week": int(week.lstrip("W")),
                    "batch": batch,
                    "num": num,
                    "title": title,
                    "cat": cat.group(1).strip() if cat else "",
                    "line": line.group(1).strip() if line else "",
                    "status": status,
                }
            )
    return ideas


def selected_file_stats() -> dict:
    """selected*.md の深掘り状況を数える。"""
    picked = deep = 0
    for path in sorted(IDEAS.glob("*/W*/selected*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^> Status:\s*picked", text, flags=re.M):
            picked += 1
        elif re.search(r"^> Status:\s*idea", text, flags=re.M):
            deep += 1
    return {"picked": picked, "deep": deep}


def write_index(ideas: list[dict]) -> None:
    mark = {"selected": "✅ selected", "rejected": "🗑 rejected", "": "-"}
    rows = sorted(ideas, key=lambda i: (-i["year"], -i["week"], -i["batch"], i["num"]))
    lines = [
        "# Idea Index",
        "",
        "> 自動生成 (`scripts/update_index.py`)。手で編集しない。",
        "> 生成 routine はこのファイルを参照し、既出と同種・類似のアイデアを避けること。",
        "",
        "| ID | タイトル | カテゴリ | 一行で | 状態 |",
        "|---|---|---|---|---|",
    ]
    for i in rows:
        lines.append(
            f"| {i['id']} | {esc(i['title'])} | {esc(i['cat'])} | {esc(i['line'])} | {mark[i['status']]} |"
        )
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_stats(ideas: list[dict]) -> None:
    total = len(ideas)
    n_sel = sum(1 for i in ideas if i["status"] == "selected")
    n_rej = sum(1 for i in ideas if i["status"] == "rejected")
    sf = selected_file_stats()
    n_poc = len([p for p in POC.iterdir() if p.is_dir()]) if POC.is_dir() else 0

    weeks: dict[tuple[int, int], dict] = {}
    for i in ideas:
        key = (i["year"], i["week"])
        w = weeks.setdefault(key, {"gen": 0, "sel": 0, "rej": 0})
        w["gen"] += 1
        if i["status"] == "selected":
            w["sel"] += 1
        elif i["status"] == "rejected":
            w["rej"] += 1

    def pct(n: int, d: int) -> str:
        return f"{n * 100 // d}%" if d else "-"

    lines = [
        "# Stats",
        "",
        "> 自動生成 (`scripts/update_index.py`)。手で編集しない。",
        "",
        "## 全体",
        "",
        f"- 総生成: {total} 案",
        f"- Selected: {n_sel} ({pct(n_sel, total)}) / Rejected: {n_rej} ({pct(n_rej, total)})",
        f"- 深掘り済み (Status: idea): {sf['deep']} / スタブのまま (Status: picked): {sf['picked']}",
        f"- Bootstrap 済み (poc/): {n_poc}",
        "",
        "## 週別",
        "",
        "| 週 | 生成 | Selected | Rejected | Select 率 |",
        "|---|---|---|---|---|",
    ]
    for (year, week), w in sorted(weeks.items(), reverse=True):
        lines.append(
            f"| {year}-W{week:02d} | {w['gen']} | {w['sel']} | {w['rej']} | {pct(w['sel'], w['gen'])} |"
        )
    (ROOT / "STATS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not IDEAS.is_dir():
        print("ideas/ が見つからない", file=sys.stderr)
        return 1
    ideas = collect()
    write_index(ideas)
    write_stats(ideas)
    print(f"INDEX.md / STATS.md updated ({len(ideas)} ideas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
