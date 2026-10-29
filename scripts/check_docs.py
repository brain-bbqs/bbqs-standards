"""Check that the documents in content/ follow the conventions in README.md.

The BBQS website builds directly from this repository, so a document that breaks these
conventions would show up broken (or not at all) on the site.

Usage: python scripts/check_docs.py   (requires PyYAML)
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

CONTENT = Path(__file__).resolve().parent.parent / "content"

REQUIRED_FIELDS = {"title": str, "short_title": str, "description": str, "order": int}

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# The website parses front matter as flat `key: value` lines, not full YAML.
FLAT_FIELD = re.compile(r"^[A-Za-z_][\w-]*: (?![|>\[{&*!]).+$")
# Inline links and images: [text](target) / ![alt](target)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")


def check_document(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(CONTENT.parent)

    match = FRONT_MATTER.match(text)
    if not match:
        return [f"{rel}: missing YAML front matter"]
    for lineno, line in enumerate(match.group(1).split("\n"), start=2):
        if line.strip() and not line.lstrip().startswith("#") and not FLAT_FIELD.match(line):
            errors.append(f"{rel}:{lineno}: front matter must be single-line 'key: value' fields")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"{rel}: invalid YAML front matter: {exc}"]
    for field, kind in REQUIRED_FIELDS.items():
        if field not in meta:
            errors.append(f"{rel}: front matter is missing '{field}'")
        elif not isinstance(meta[field], kind) or isinstance(meta[field], bool):
            errors.append(f"{rel}: front matter '{field}' must be a {kind.__name__}")

    body = text[match.end():]
    in_fence = False
    for lineno, line in enumerate(body.split("\n"), start=text[: match.end()].count("\n") + 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("# "):
            errors.append(f"{rel}:{lineno}: '# ' heading; the title comes from front matter, start sections at '##'")
        prose = INLINE_CODE.sub("", line)
        for tag in HTML_TAG.findall(LINK.sub("", prose)):
            errors.append(f"{rel}:{lineno}: raw HTML {tag!r}; wrap placeholders in backticks")
        for target in LINK.findall(prose):
            url = urlparse(target)
            if url.scheme or target.startswith(("#", "/")):
                continue
            if not (path.parent / unquote(url.path)).exists():
                errors.append(f"{rel}:{lineno}: broken relative link '{target}'")
    return errors


def main():
    docs = sorted(CONTENT.glob("*/index.md"))
    errors = []
    if not docs:
        errors.append("no documents found (expected content/<name>/index.md)")
    for entry in sorted(CONTENT.iterdir()):
        if entry.is_dir() and not (entry / "index.md").exists():
            errors.append(f"{entry.relative_to(CONTENT.parent)}: folder has no index.md")
    for doc in docs:
        errors.extend(check_document(doc))
    for error in errors:
        print(error)
    print(f"Checked {len(docs)} document(s): {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
