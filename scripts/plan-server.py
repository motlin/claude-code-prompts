#!/usr/bin/env python3
"""HTTP server that serves all Claude plans with an auto-refreshing index."""

import html
import os
import re
import sys
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

PLANS_DIR = Path(sys.argv[1])
PORT = int(sys.argv[2])

STYLE = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }
h1 { border-bottom: 2px solid #e1e4e8; padding-bottom: 0.3em; }
h2 { border-bottom: 1px solid #e1e4e8; padding-bottom: 0.3em; margin-top: 2em; }
h3 { margin-top: 1.5em; }
code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
pre { background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; overflow-x: auto; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }
th { background: #f6f8fa; font-weight: 600; }
ul, ol { padding-left: 2em; }
li { margin: 0.3em 0; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
.back { display: inline-block; margin-bottom: 1em; font-size: 0.9em; }
"""

INDEX_STYLE = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }
h1 { border-bottom: 2px solid #e1e4e8; padding-bottom: 0.3em; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
.plan-list { list-style: none; padding: 0; }
.plan-item { padding: 12px 16px; border: 1px solid #e1e4e8; border-radius: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.plan-item:hover { background: #f6f8fa; }
.plan-title { font-size: 1.1em; font-weight: 500; }
.plan-date { color: #656d76; font-size: 0.85em; white-space: nowrap; margin-left: 16px; }
.plan-count { color: #656d76; font-size: 0.9em; margin-bottom: 1em; }
.new-marker { background: #dafbe1; color: #1a7f37; font-size: 0.75em; padding: 2px 8px; border-radius: 10px; margin-left: 8px; font-weight: 600; }
"""


def get_plans():
    """Return list of (filename, title, mtime) sorted by mtime descending."""
    plans = []
    for f in PLANS_DIR.glob("*.md"):
        title = f.stem.replace("-", " ").title()
        with open(f) as fh:
            first_line = fh.readline().strip()
            if first_line.startswith("# "):
                title = first_line[2:]
        plans.append((f.name, title, f.stat().st_mtime))
    plans.sort(key=lambda x: x[2], reverse=True)
    return plans


def render_index():
    plans = get_plans()
    now = datetime.now(timezone.utc).timestamp()

    items = []
    for filename, title, mtime in plans:
        dt = datetime.fromtimestamp(mtime, timezone.utc)
        date_str = dt.strftime("%b %d, %Y %H:%M")
        age_hours = (now - mtime) / 3600
        new_tag = '<span class="new-marker">NEW</span>' if age_hours < 1 else ""
        safe_title = html.escape(title)
        items.append(
            f'<li class="plan-item">'
            f'<span class="plan-title"><a href="/plan/{html.escape(filename)}">{safe_title}</a>{new_tag}</span>'
            f'<span class="plan-date">{date_str}</span>'
            f"</li>"
        )

    plan_list = "\n".join(items) if items else "<p>No plans found.</p>"
    count = len(plans)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Claude Plans</title>
<style>{INDEX_STYLE}</style>
<script>
let knownCount = {count};
async function checkForUpdates() {{
    try {{
        const resp = await fetch('/api/count');
        const data = await resp.json();
        if (data.count !== knownCount) {{
            window.location.reload();
        }}
    }} catch (e) {{}}
}}
setInterval(checkForUpdates, 3000);
</script>
</head>
<body>
<h1>Claude Plans</h1>
<p class="plan-count">{count} plan{"s" if count != 1 else ""}</p>
<ul class="plan-list">
{plan_list}
</ul>
</body>
</html>"""


def inline(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"`(.+?)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", text
    )
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    text = text.replace(" -- ", " &mdash; ")
    return text


def md_to_html(md):
    lines = md.split("\n")
    out = []
    in_code = False
    in_list = None
    in_table = False
    table_header_done = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(html.escape(line))
            continue

        stripped = line.strip()

        if in_list and not re.match(r"^(\d+\.|-|\*)\s", stripped) and stripped:
            out.append(f"</{in_list}>")
            in_list = None

        if in_table and not stripped.startswith("|"):
            out.append("</table>")
            in_table = False
            table_header_done = False

        if not stripped:
            continue

        m = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                table_header_done = True
                continue
            if not in_table:
                out.append("<table>")
                in_table = True
            tag = "th" if not table_header_done else "td"
            row = "".join(
                f"<{tag}>{inline(html.escape(c))}</{tag}>" for c in cells
            )
            out.append(f"<tr>{row}</tr>")
            continue

        m = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if m:
            if in_list != "ol":
                if in_list:
                    out.append(f"</{in_list}>")
                out.append("<ol>")
                in_list = "ol"
            out.append(f"<li>{inline(m.group(2))}</li>")
            continue

        m = re.match(r"^[-*]\s+(.*)", stripped)
        if m:
            if in_list != "ul":
                if in_list:
                    out.append(f"</{in_list}>")
                out.append("<ul>")
                in_list = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        out.append(f"<p>{inline(stripped)}</p>")

    if in_list:
        out.append(f"</{in_list}>")
    if in_table:
        out.append("</table>")
    if in_code:
        out.append("</code></pre>")

    return "\n".join(out)


def render_plan(filename):
    path = PLANS_DIR / filename
    if not path.exists() or not path.suffix == ".md":
        return None

    with open(path) as f:
        md = f.read()

    title_match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
    title = html.escape(title_match.group(1)) if title_match else path.stem

    mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    date_str = mtime.strftime("%b %d, %Y %H:%M UTC")

    body = md_to_html(md)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{STYLE}</style>
</head>
<body>
<a class="back" href="/">&larr; All Plans</a>
<p style="color: #656d76; font-size: 0.85em; margin-bottom: 1.5em;">Last modified: {date_str}</p>
{body}
</body>
</html>"""


class PlanHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path)

        if path == "/" or path == "/index.html":
            self.send_html(render_index())
        elif path == "/api/count":
            count = len(list(PLANS_DIR.glob("*.md")))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(f'{{"count": {count}}}'.encode())
        elif path.startswith("/plan/"):
            filename = path[6:]
            page = render_plan(filename)
            if page:
                self.send_html(page)
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def send_html(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(content.encode())

    def log_message(self, format, *args):
        pass  # suppress request logging


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), PlanHandler)
    server.serve_forever()
