#!/usr/bin/env python3
"""Build the Bungo 1917 New Testament pages for jonathanmccallum-ja.

Fetches the 27 books of the 1917 大正改訳 (文語訳) New Testament from
Japanese Wikisource via the MediaWiki API and writes one Eleventy page
per book under content/bible/ plus content/bible/index.md.

Source facts (verified 2026-11-25):
- The 1917 translation is public domain (published 1917, before 1930).
- The Wikisource digitisation is CC BY-SA 4.0: every generated page
  credits Wikisource and links to its source book page.
- Book titles on Wikisource are e.g. "マタイ傳福音書(文語訳)"; 13 of
  them are redirects to the spaced form "マルコ傳福音書 (文語訳)" —
  the API is called with redirects=1 and the resolved title is used
  for the source link.
- The wikitext is plain text: chapter headings "== 第N章 ==" and
  verse headings "==== C:V ====" only. There are NO ruby/furigana
  templates in the source, so no furigana conversion was needed.
  Old kanji forms (傳, 舊, 默, etc.) are kept exactly as printed.
  Rare kanji arrive as numeric entities (e.g. &#x7006;) and are kept.
- Measured: 260 chapters, 7,951 verse headings, ~481 KB wikitext.

Do NOT use this script for the Kōgoyaku: its US copyright runs to
~2050/2051 (URAA), so only the Bungo text is hosted here. Modern
Japanese readers are linked out to the 口語訳 on YouVersion.

Usage: python3 scripts/build-bungo-nt.py   (run from the repo root)
"""
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://ja.wikisource.org/w/api.php"
UA = {"User-Agent": "jonathanmccallum-ja build script (Bungo NT pages)"}

# order, Japanese name, slug, YouVersion book code (version 81, 口語訳)
BOOKS = [
    ("マタイ傳福音書", "matthew", "MAT"),
    ("マルコ傳福音書", "mark", "MRK"),
    ("ルカ傳福音書", "luke", "LUK"),
    ("ヨハネ傳福音書", "john", "JHN"),
    ("使徒行傳", "acts", "ACT"),
    ("ロマ人への書", "romans", "ROM"),
    ("コリント人への前の書", "1-corinthians", "1CO"),
    ("コリント人への後の書", "2-corinthians", "2CO"),
    ("ガラテヤ人への書", "galatians", "GAL"),
    ("エペソ人への書", "ephesians", "EPH"),
    ("ピリピ人への書", "philippians", "PHP"),
    ("コロサイ人への書", "colossians", "COL"),
    ("テサロニケ人への前の書", "1-thessalonians", "1TH"),
    ("テサロニケ人への後の書", "2-thessalonians", "2TH"),
    ("テモテへの前の書", "1-timothy", "1TI"),
    ("テモテへの後の書", "2-timothy", "2TI"),
    ("テトスへの書", "titus", "TIT"),
    ("ピレモンへの書", "philemon", "PHM"),
    ("ヘブル人への書", "hebrews", "HEB"),
    ("ヤコブの書", "james", "JAS"),
    ("ペテロの前の書", "1-peter", "1PE"),
    ("ペテロの後の書", "2-peter", "2PE"),
    ("ヨハネの第一の書", "1-john", "1JN"),
    ("ヨハネの第二の書", "2-john", "2JN"),
    ("ヨハネの第三の書", "3-john", "3JN"),
    ("ユダの書", "jude", "JUD"),
    ("ヨハネの默示録", "revelation", "REV"),
]

YOU_VERSION = "https://www.bible.com/en-GB/versions/81-ja1955-colloquial-japanese-1955"


def fetch_wikitext(title):
    q = urllib.parse.urlencode({
        "action": "query", "prop": "revisions", "rvprop": "content",
        "format": "json", "formatversion": "2", "titles": title,
        "redirects": 1,
    })
    req = urllib.request.Request(API + "?" + q, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    page = data["query"]["pages"][0]
    assert "missing" not in page, f"missing page: {title}"
    revs = page.get("revisions") or []
    assert revs, f"no content: {title}"
    return page["title"], revs[0]["content"]


def esc(text):
    """Escape HTML, but keep the &#x...; entities already in the source."""
    text = re.sub(r"&(?!#x[0-9a-fA-F]+;)", "&amp;", text)
    return text.replace("<", "&lt;").replace(">", "&gt;")


def convert(wikitext):
    """Wikitext -> HTML blocks. Returns (html, chapter_count, verse_count)."""
    lines = wikitext.split("\n")
    out = []
    chapters = 0
    verses = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"^== 第(\d+)章 ==$", line)
        if m:
            chapters += 1
            out.append(f'<h2 class="bible-chapter">第{m.group(1)}章</h2>')
            i += 1
            continue
        m = re.match(r"^==== (\d+:\d+) ====$", line)
        if m:
            verses += 1
            ref = m.group(1)
            parts = []
            i += 1
            while i < len(lines):
                t = lines[i].strip()
                if not t:
                    i += 1
                    break
                if re.match(r"^=+ ", t):
                    break
                parts.append(t)
                i += 1
            text = "".join(parts)
            out.append(
                f'<p class="bible-verse"><span class="bible-verse__num">{ref}</span> {esc(text)}</p>'
            )
            continue
        i += 1
    return "\n".join(out), chapters, verses


BODIES = {}


if __name__ == "__main__":
    # Fetch + convert first, keep bodies, then write files.
    root = Path(__file__).resolve().parent.parent
    outdir = root / "content" / "bible"
    outdir.mkdir(parents=True, exist_ok=True)
    meta = []
    total_ch = total_v = 0
    for ja, slug, code in BOOKS:
        title, wiki = fetch_wikitext(f"{ja}(文語訳)")
        body, ch, v = convert(wiki)
        assert ch > 0 and v > 0, f"empty parse: {ja}"
        total_ch += ch
        total_v += v
        BODIES[slug] = body
        meta.append({
            "ja": ja, "slug": slug, "code": code, "chapters": ch,
            "verses": v,
            "wikisource": "https://ja.wikisource.org/wiki/" + urllib.parse.quote(title),
            "youversion": f"https://www.bible.com/bible/81/{code}.1",
        })
        print(f"{ja}: {ch} chapters, {v} verses <- {title}")
    for idx, m in enumerate(meta):
        prev_m = meta[idx - 1] if idx > 0 else None
        next_m = meta[idx + 1] if idx + 1 < len(meta) else None
        fm = [
            "---",
            f'title: "{m["ja"]}"',
            f'permalink: /bible/{m["slug"]}/',
            "bibleBook: true",
            f'bookJa: "{m["ja"]}"',
            f'chapters: {m["chapters"]}',
            f'wikisourceUrl: "{m["wikisource"]}"',
            f'youversionUrl: "{m["youversion"]}"',
        ]
        if prev_m:
            fm.append(f'prevTitle: "{prev_m["ja"]}"')
            fm.append(f'prevUrl: "/bible/{prev_m["slug"]}/"')
        if next_m:
            fm.append(f'nextTitle: "{next_m["ja"]}"')
            fm.append(f'nextUrl: "/bible/{next_m["slug"]}/"')
        fm.append("---")
        fm.append(BODIES[m["slug"]])
        (outdir / f"{m['slug']}.md").write_text("\n".join(fm) + "\n", encoding="utf-8")
    rows = "\n".join(
        f'<li><a href="/bible/{m["slug"]}/">{m["ja"]}</a> <span class="meta">全{m["chapters"]}章</span></li>'
        for m in meta
    )
    index = f"""---
title: "新約聖書"
permalink: /bible/
layout: layouts/page.njk
---

<p>ここに載せている新約聖書は、1917年（大正6年）に出版された大正改訳（文語訳）です。ことばは古典的な日本語（文語）で、今の日本語とはちがいます。記事の中で引用されている口語訳の聖句とは、ことばづかいがちがいますので、ご注意ください。</p>

<p>現代の日本語で読みたい方は、<a href="{YOU_VERSION}">口語訳（YouVersion）</a>をご覧ください。口語訳の全文は、こちらのサイトには載せていません。</p>

<p>この文語訳はパブリックドメインです。本文はウィキソースのデジタル化テキスト（<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ja">CC BY-SA 4.0</a>）にもとづきます。各ページの下に、もとのページへのリンクがあります。</p>

<ul class="bible-index">
{rows}
</ul>
"""
    (outdir / "index.md").write_text(index, encoding="utf-8")
    print(f"Wrote {len(meta)} books + index: {total_ch} chapters, {total_v} verses")
