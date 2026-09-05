import glob
import os
import sys

import yaml

root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
errors = []
checked = {"base": 0, "frontmatter": 0, "json": 0, "embedded": 0}

# 1. .base files
for path in glob.glob(os.path.join(root, "**", "*.base"), recursive=True):
    rel = os.path.relpath(path, root)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        data = yaml.safe_load(text)
        checked["base"] += 1
    except yaml.YAMLError as e:
        errors.append(f"[base YAML] {rel}: {e}")
        continue
    if not isinstance(data, dict):
        errors.append(f"[base] {rel}: top level is not a mapping")
        continue
    if "views" not in data:
        errors.append(f"[base] {rel}: missing 'views'")
        continue
    for v in data["views"]:
        if "type" not in v:
            errors.append(f"[base] {rel}: a view is missing 'type'")
        if v.get("type") not in ("table", "list", "cards", "kanban", "map"):
            errors.append(f"[base] {rel}: unknown view type {v.get('type')!r}")
        for s in v.get("sort", []):
            if "property" not in s or "direction" not in s:
                errors.append(f"[base] {rel}: bad sort entry {s!r}")
            elif s["direction"] not in ("ASC", "DESC"):
                errors.append(f"[base] {rel}: bad sort direction {s['direction']!r}")

# 2. markdown frontmatter + embedded ```base blocks
for path in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
    rel = os.path.relpath(path, root)
    with open(path, encoding="utf-8") as f:
        text = f.read()

    if text.startswith("---\n"):
        end = text.find("\n---\n", 3)
        if end == -1:
            errors.append(f"[frontmatter] {rel}: unterminated frontmatter block")
        else:
            fm = text[4:end]
            # Templater placeholders are not valid YAML values on their own; they are
            # rendered before the file is ever parsed by Obsidian, so substitute them.
            probe = fm.replace("<% tp.file.title %>", "TITLE")
            for token in (
                'tp.date.now("YYYY-MM-DD dddd")',
                'tp.date.now("YYYY-MM-DD HH:mm")',
                'tp.date.now("YYYY-MM-DD")',
                'tp.date.now("gggg-[W]ww")',
                'tp.date.now("gggg 年第 ww 周")',
                'tp.date.now("YYYY-MM")',
                'tp.date.now("YYYY 年 M 月")',
            ):
                probe = probe.replace("<% " + token + " %>", "2026-01-01")
            try:
                meta = yaml.safe_load(probe)
                checked["frontmatter"] += 1
            except yaml.YAMLError as e:
                errors.append(f"[frontmatter] {rel}: {e}")
                meta = None
            if isinstance(meta, dict):
                isbn = meta.get("isbn13")
                if isbn is not None and not isinstance(isbn, str):
                    errors.append(f"[frontmatter] {rel}: isbn13 must be quoted (got {type(isbn).__name__})")
                for field in ("author", "topics"):
                    val = meta.get(field)
                    if val and not isinstance(val, list):
                        errors.append(f"[frontmatter] {rel}: {field} must be a list")

    # embedded base code blocks
    idx = 0
    while True:
        start = text.find("```base\n", idx)
        if start == -1:
            break
        end = text.find("\n```", start + 8)
        if end == -1:
            errors.append(f"[embedded base] {rel}: unterminated ```base block")
            break
        block = text[start + 8:end]
        try:
            data = yaml.safe_load(block)
            checked["embedded"] += 1
            if not isinstance(data, dict) or "views" not in data:
                errors.append(f"[embedded base] {rel}: block missing 'views'")
        except yaml.YAMLError as e:
            errors.append(f"[embedded base] {rel}: {e}")
        idx = end + 3

# 3. .obsidian json
import json

for path in glob.glob(os.path.join(root, ".obsidian", "*.json")):
    rel = os.path.relpath(path, root)
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        checked["json"] += 1
    except json.JSONDecodeError as e:
        errors.append(f"[json] {rel}: {e}")

print(f"checked: {checked}")
if errors:
    print(f"\n{len(errors)} problem(s):")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("all good")
