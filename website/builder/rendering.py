"""Build-time Markdown, math and syntax-highlighting rendering.

Everything is rendered to final HTML while building, so the published pages
contain real text (good for search engines and for readers with JavaScript
disabled) and never flash unstyled Markdown. Only KaTeX runs in the browser,
from a locally vendored copy.
"""

import html
import re
from typing import Dict, List, Tuple

from markdown_it import MarkdownIt
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

PYGMENTS_STYLE = "friendly"
PYGMENTS_STYLE_DARK = "stata-dark"
_FORMATTER = HtmlFormatter(style=PYGMENTS_STYLE, cssclass="highlight", nowrap=False)
_FORMATTER_DARK = HtmlFormatter(style=PYGMENTS_STYLE_DARK, cssclass="highlight", nowrap=False)

_CODE_TOKEN_RE = re.compile(r"```[\s\S]*?```|`[^`\n]+`")
# Math delimiters: $$...$$, \[...\], $...$ and \(...\)
_DISPLAY_DOLLAR_RE = re.compile(r"\$\$([\s\S]+?)\$\$")
_DISPLAY_BRACKET_RE = re.compile(r"\\\[([\s\S]+?)\\\]")
_INLINE_DOLLAR_RE = re.compile(r"(?<!\\)\$(?!\s)([^\n$]+?)(?<!\s)\$")
_INLINE_PAREN_RE = re.compile(r"\\\((.+?)\\\)")
_HEADING_RE = re.compile(r"<h([23])>(.*?)</h\1>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def pygments_css() -> str:
    """Stylesheet for build-time highlighted code blocks, light and dark."""
    return "%s\n\n/* Dark theme */\n%s\n" % (
        _FORMATTER.get_style_defs(".highlight"),
        _FORMATTER_DARK.get_style_defs('[data-theme="dark"] .highlight'),
    )


def highlight_code(source: str, lang: str = "python") -> str:
    """Highlight a block of code, falling back to escaped plain text."""
    try:
        lexer = get_lexer_by_name(lang, stripnl=False)
    except ClassNotFound:
        return '<div class="highlight"><pre>%s</pre></div>' % html.escape(source)
    return pygments_highlight(source, lexer, _FORMATTER)


def _md_highlight(source: str, lang: str, attrs: str) -> str:
    return highlight_code(source, lang or "text")


_MD = MarkdownIt("gfm-like", {"highlight": _md_highlight, "html": True, "linkify": False})
_MD.disable("linkify")


def _is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "data:", "#", "/", "mailto:"))


def rewrite_relative_paths(md_text: str, file_prefix: str) -> str:
    """Point local relative image links at the copied dist/files/<slug>/ assets.

    Handles both Markdown `![alt](img/x.png)` and raw HTML `<img src="img/x.png">`,
    which notebook authors mix freely inside Markdown cells.
    """

    def repl_md_img(match: "re.Match") -> str:
        alt, url = match.group(1), match.group(2).strip()
        if _is_external(url):
            return match.group(0)
        return "![%s](%s%s)" % (alt, file_prefix, url.lstrip("./"))

    def repl_html_src(match: "re.Match") -> str:
        attr, quote, url = match.group(1), match.group(2), match.group(3).strip()
        if _is_external(url):
            return match.group(0)
        return "%s=%s%s%s%s" % (attr, quote, file_prefix, url.lstrip("./"), quote)

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_md_img, md_text)
    return re.sub(r"\b(src|poster)=(\"|')([^\"']+)\2", repl_html_src, text)


def _stash_math(text: str) -> Tuple[str, List[Dict[str, object]]]:
    """Replace math segments with opaque tokens so Markdown never touches them."""
    tokens: List[Dict[str, object]] = []

    def stash(tex: str, display: bool) -> str:
        token = "@@MATHTOKEN%d@@" % len(tokens)
        tokens.append({"token": token, "tex": tex.strip(), "display": display})
        return token

    # Code first: a `$` inside code is not math.
    code_tokens: List[Tuple[str, str]] = []

    def stash_code(match: "re.Match") -> str:
        token = "@@CODETOKEN%d@@" % len(code_tokens)
        code_tokens.append((token, match.group(0)))
        return token

    text = _CODE_TOKEN_RE.sub(stash_code, text)

    text = _DISPLAY_DOLLAR_RE.sub(lambda m: stash(m.group(1), True), text)
    text = _DISPLAY_BRACKET_RE.sub(lambda m: stash(m.group(1), True), text)
    text = _INLINE_DOLLAR_RE.sub(lambda m: stash(m.group(1), False), text)
    text = _INLINE_PAREN_RE.sub(lambda m: stash(m.group(1), False), text)

    for token, original in code_tokens:
        text = text.replace(token, original)
    return text, tokens


def _restore_math(rendered: str, tokens: List[Dict[str, object]]) -> str:
    for item in tokens:
        token = item["token"]
        tex = html.escape(str(item["tex"]))
        if item["display"]:
            node = r'<div class="math-block" data-tex="%s">\[%s\]</div>' % (tex, tex)
            rendered = rendered.replace("<p>%s</p>" % token, node)
        else:
            node = r'<span class="math-inline" data-tex="%s">\(%s\)</span>' % (tex, tex)
        rendered = rendered.replace(token, node)
    return rendered


def slugify_heading(text: str, used: Dict[str, int]) -> str:
    base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip().lower()).strip("-")
    base = base or "section"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else "%s-%d" % (base, count + 1)


def add_heading_anchors(
    rendered: str, used: Dict[str, int], headings: List[Dict[str, object]]
) -> str:
    """Give every h2/h3 a stable id and record it for the table of contents."""

    def repl(match: "re.Match") -> str:
        level, inner = int(match.group(1)), match.group(2)
        text = html.unescape(_TAG_RE.sub("", inner)).strip()
        if not text:
            return match.group(0)
        anchor = slugify_heading(text, used)
        headings.append({"level": level, "text": text, "id": anchor})
        return '<h%d id="%s">%s</h%d>' % (level, anchor, inner, level)

    return _HEADING_RE.sub(repl, rendered)


def render_markdown(
    md_text: str,
    file_prefix: str = "",
    heading_ids: Dict[str, int] = None,
    headings: List[Dict[str, object]] = None,
) -> str:
    """Render Markdown (with LaTeX math) to final HTML at build time."""
    if not md_text.strip():
        return ""
    text = rewrite_relative_paths(md_text, file_prefix) if file_prefix else md_text
    text, math_tokens = _stash_math(text)
    rendered = _MD.render(text)
    rendered = _restore_math(rendered, math_tokens)
    if headings is not None:
        rendered = add_heading_anchors(rendered, heading_ids if heading_ids is not None else {}, headings)
    return rendered


def plain_text(md_text: str, limit: int = 600) -> str:
    """Strip Markdown/LaTeX down to searchable plain text."""
    text = re.sub(r"```[\s\S]*?```", " ", md_text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\$\$[\s\S]*?\$\$", " ", text)
    text = re.sub(r"\$[^\n$]*\$", " ", text)
    text = re.sub(r"[#>*_|\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]
