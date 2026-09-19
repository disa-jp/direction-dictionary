#!/usr/bin/env python3
"""Git の履歴から、辞書の更新情報を _data/ に書き出す。

- _data/lastmod.yml : 項目番号 -> 最終更新日（YYYY-MM-DD）
- _data/updates.yml : 更新履歴（コミット単位・新しい順・最大10件）

GitHub Pages の標準ビルドではプラグインを追加できないため、
ビルド前にこのスクリプトでデータ化しておく。
"""
import subprocess, glob, re, os, datetime

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True).stdout

def yq(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

# 1) 項目ごとの最終更新日
entries = {}
for path in sorted(glob.glob("[0-9][0-9][0-9]_*.md")):
    num = os.path.basename(path)[:3]
    date = sh("git", "log", "-1", "--format=%ad", "--date=short", "--", path).strip()
    entries[num] = date or datetime.date.today().isoformat()

os.makedirs("_data", exist_ok=True)
with open("_data/lastmod.yml", "w", encoding="utf-8") as f:
    for num, date in sorted(entries.items()):
        f.write(f'"{num}": "{date}"\n')

# 2) 更新履歴（コミット単位。項目ファイルを触ったものだけ）
log = sh("git", "log", "--date=short", "--format=%x00%ad%x00%s", "--name-only",
         "--", "[0-9][0-9][0-9]_*.md")
history = []
blocks = [b for b in log.split("\x00") if b]
i = 0
while i + 1 < len(blocks):
    date = blocks[i].strip()
    rest = blocks[i + 1].split("\n")
    subject = rest[0].strip()
    files = [x for x in rest[1:] if re.match(r"^\d{3}_.*\.md$", x)]
    if files:
        nums = sorted({x[:3] for x in files})
        history.append({"date": date, "subject": subject, "count": len(nums)})
    i += 2

with open("_data/updates.yml", "w", encoding="utf-8") as f:
    for h in history[:10]:
        f.write(f'- date: "{h["date"]}"\n  summary: {yq(h["subject"])}\n  count: {h["count"]}\n')
print(f"{len(entries)} entries, {len(history)} update commits, latest {history[0]['date'] if history else '-'}")
