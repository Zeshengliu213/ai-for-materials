"""Jinja2 environment and the shared context every page template needs."""

from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from . import config

TEMPLATE_DIR = config.ROOT_DIR / "templates"

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%2316324f'/%3E"
    "%3Ctext x='16' y='21' font-size='13' font-family='Georgia,serif' "
    "font-weight='bold' fill='%23f5c86b' text-anchor='middle'%3EAI%3C/text%3E%3C/svg%3E"
)

_ENV = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def site_context() -> Dict[str, Any]:
    """Values shared by every template, derived from builder/config.py."""
    return {
        "title": config.SITE_TITLE,
        "subtitle": config.SITE_SUBTITLE,
        "description": config.SITE_DESCRIPTION,
        "base_url": config.SITE_BASE_URL,
        "github_repo": config.GITHUB_REPO,
    }


def render(template_name: str, **context: Any) -> str:
    """Render a template with the shared defaults filled in."""
    defaults: Dict[str, Any] = {
        "site": site_context(),
        "favicon": FAVICON,
        "description": config.SITE_DESCRIPTION,
        "active": "syllabus",
        "with_toc": False,
        "headings": [],
        "current_nb": None,
        "canonical": "",
        "nb_solution": None,
        "current_slug": "",
        "modules": [],
        "previous": None,
        "following": None,
        "p": "",
    }
    defaults.update(context)
    return _ENV.get_template(template_name).render(**defaults)
