import glob
import os
import re
import sys

root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# Build an index of every resolvable target: basename and relative path (both
# without extension for md, with extension for everything else).
names = {}
paths = set()
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, root).replace("\\", "/")
        paths.add(rel)
        stem, ext = os.path.splitext(fn)
        key = stem if ext == ".md" else fn
        names.setdefault(key, []).append(rel)
        if ext == ".md":
            paths.add(rel[:-3])

# Collect the view names declared inside every .base file so anchors can be checked.
import yaml

base_views = {}
for path in glob.glob(os.path.join(root, "**", "*.base"), recursive=True):
    rel = os.path.relpath(path, root).replace("\\", "/")
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    base_views[os.path.basename(rel)] = [v.get("name") for v in data.get("views", [])]

WIKILINK = re.compile(r"!?\[\[([^\]\|#]+)(#[^\]\|]+)?(\|[^\]]+)?\]\]")

problems = []
total = 0
for path in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
    rel = os.path.relpath(path, root).replace("\\", "/")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # strip fenced code blocks, inline code and html comments so sample or
    # placeholder links inside them are not treated as real wikilinks
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in WIKILINK.finditer(text):
        target = m.group(1).strip()
        anchor = (m.group(2) or "").lstrip("#").strip()
        if not target:
            continue  # empty placeholder [[ ]]
        total += 1
        stem, ext = os.path.splitext(target)
        key = target if ext else target
        if key not in names and target not in paths and stem not in names:
            problems.append(f"[broken link] {rel} -> [[{target}]]")
            continue
        if anchor and target.endswith(".base"):
            declared = base_views.get(os.path.basename(target), [])
            if anchor not in declared:
                problems.append(
                    f"[bad view anchor] {rel} -> [[{target}#{anchor}]] "
                    f"(available: {declared})"
                )

print(f"checked {total} wikilink(s)")
if problems:
    print(f"\n{len(problems)} problem(s):")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("all links resolve")
