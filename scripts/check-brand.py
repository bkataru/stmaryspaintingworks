# Fail on old brand strings outside an explicit whitelist.
# Allowed survivors: the owner's legal name, his fixed Gmail address,
# and the JustDial listing name/slug (JustDial requires the old substring).
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "dist", ".astro", ".agents", "justdial"}
SCAN_EXT = {".astro", ".ts", ".js", ".mjs", ".json", ".html", ".txt", ".xml", ".md", ".webmanifest", ".svg", ".css"}

ALLOWED = (
    "Anthony Jayasheelan",
    "jaypainterscontractors@gmail.com",
    "St. Mary's Jay Painters & Home Repairs",
    "St. Mary's Jay Painters &amp; Home Repairs",
    "St-Marys-Jay-Painters-Home-Repairs",
)

BANNED = ("jay painters", "jaypainters", "jay-painters", "jay_painters")

hits = []
for base, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for name in files:
        if os.path.splitext(name)[1].lower() not in SCAN_EXT:
            continue
        path = os.path.join(base, name)
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel == "docs/concepts_brief.md":
            continue
        try:
            text = open(path, encoding="utf8").read()
        except (OSError, UnicodeDecodeError):
            continue
        low = text.lower()
        for token in BANNED:
            start = 0
            while True:
                i = low.find(token, start)
                if i < 0:
                    break
                snippet = text[max(0, i - 80): i + len(token) + 80]
                if any(a.lower() in snippet.lower() for a in ALLOWED):
                    start = i + len(token)
                    continue
                hits.append((rel, token, snippet.replace("\n", " ")[:160]))
                start = i + len(token)

if hits:
    for rel, token, snippet in hits[:30]:
        print(f"OLD BRAND [{token}] in {rel}: ...{snippet}...", file=sys.stderr)
    print(f"{len(hits)} old-brand occurrence(s) found", file=sys.stderr)
    sys.exit(1)
print("brand check passed")
