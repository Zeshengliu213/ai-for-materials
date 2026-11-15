"""Convert Jupyter notebooks into static HTML sections at build time."""

import html
import re
from typing import Dict, List, Tuple

from . import rendering

ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


def extract_notebook_title(nb_data: dict, fallback: str) -> str:
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            for line in source.splitlines():
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    return fallback


def notebook_search_text(nb_data: dict, limit: int = 1200) -> str:
    """Plain-text digest of a notebook's prose, used by the site search index."""
    chunks: List[str] = []
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") == "markdown":
            chunks.append("".join(cell.get("source", [])))
        if sum(len(c) for c in chunks) > limit * 3:
            break
    return rendering.plain_text("\n".join(chunks), limit)


def _drop_leading_h1(source: str) -> str:
    """Remove a notebook's opening `# Title` line, which the page shows already."""
    lines = source.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.lstrip().startswith("# "):
            return "\n".join(lines[index + 1:]).lstrip("\n")
        return source
    return source


def render_outputs(outputs: list) -> str:
    if not outputs:
        return ""
    parts: List[str] = ['<div class="nb-outputs"><div class="nb-output-label">Out:</div>']
    for out in outputs:
        otype = out.get("output_type", "")
        if otype == "stream":
            text = strip_ansi("".join(out.get("text", [])))
            parts.append('<pre class="nb-output-stream">%s</pre>' % html.escape(text))
        elif otype in ("execute_result", "display_data"):
            parts.append(_render_rich_output(out.get("data", {})))
        elif otype == "error":
            ename = out.get("ename", "Error")
            evalue = out.get("evalue", "")
            traceback = strip_ansi("\n".join(out.get("traceback", [])))
            content = traceback if traceback.strip() else "%s: %s" % (ename, evalue)
            parts.append('<pre class="nb-output-error">%s</pre>' % html.escape(content))
    parts.append("</div>")
    return "\n".join(part for part in parts if part)


def _render_rich_output(data: dict) -> str:
    if "image/png" in data:
        b64 = "".join(data["image/png"]).replace("\n", "")
        return (
            '<img class="nb-output-img" loading="lazy" '
            'src="data:image/png;base64,%s" alt="Notebook 输出图像" />' % b64
        )
    if "image/jpeg" in data:
        b64 = "".join(data["image/jpeg"]).replace("\n", "")
        return (
            '<img class="nb-output-img" loading="lazy" '
            'src="data:image/jpeg;base64,%s" alt="Notebook 输出图像" />' % b64
        )
    if "image/svg+xml" in data:
        return '<div class="nb-output-html">%s</div>' % "".join(data["image/svg+xml"])
    if "text/html" in data:
        return '<div class="nb-output-html">%s</div>' % "".join(data["text/html"])
    if "text/plain" in data:
        text = strip_ansi("".join(data["text/plain"]))
        return '<pre class="nb-output-text">%s</pre>' % html.escape(text)
    return ""


def render_cells(nb_data: dict, file_prefix: str) -> Tuple[str, List[Dict[str, object]]]:
    """Render all cells to HTML and return (html, table-of-contents headings)."""
    cells_html: List[str] = []
    headings: List[Dict[str, object]] = []
    heading_ids: Dict[str, int] = {}
    code_idx = 0
    title_seen = False

    for cell in nb_data.get("cells", []):
        ctype = cell.get("cell_type")
        source = "".join(cell.get("source", []))
        if not source.strip() and not cell.get("outputs"):
            continue

        if ctype == "markdown":
            if not title_seen:
                title_seen = True
                # The page already shows this as its <h1>; a second copy here
                # would just repeat the title at the top of every notebook.
                source = _drop_leading_h1(source)
                if not source.strip():
                    continue
            rendered = rendering.render_markdown(
                source, file_prefix, heading_ids=heading_ids, headings=headings
            )
            cells_html.append(
                '<div class="nb-cell nb-cell-markdown">'
                '<div class="markdown-body">%s</div></div>' % rendered
            )
        elif ctype == "code":
            code_idx += 1
            exec_count = cell.get("execution_count")
            label = "In [%s]" % (exec_count if exec_count is not None else code_idx)
            cells_html.append(
                '<div class="nb-cell nb-cell-code">'
                '<div class="nb-code-header"><span>%s · Python</span>'
                '<button type="button" class="nb-copy-btn">复制代码</button></div>'
                "%s%s</div>"
                % (
                    label,
                    rendering.highlight_code(source, "python"),
                    render_outputs(cell.get("outputs", [])),
                )
            )

    return "\n".join(cells_html), headings
