"""Check tracked Markdown local file links and heading anchors without network requests."""
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def anchors(path):
    result, counts = set(), {}
    contents = path.read_text(encoding="utf-8")
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", contents, re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug + (f"-{number}" if number else ""))
    result.update(re.findall(r'(?:id|name)=["\']([^"\']+)["\']', contents))
    return result


def main():
    tracked = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
    errors = []
    count = 0
    for name in tracked:
        source = ROOT / name
        if source.suffix != ".md" or not source.is_file():
            continue
        contents = re.sub(r"```.*?```", "", source.read_text(encoding="utf-8"), flags=re.S)
        for raw in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", contents):
            target = raw.strip().split(' "', 1)[0].strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            path = (source.parent / unquote(url.path)).resolve() if url.path else source
            count += 1
            if not path.exists():
                errors.append(f"{name}: missing {target}")
            elif url.fragment and path.suffix == ".md" and unquote(url.fragment) not in anchors(path):
                errors.append(f"{name}: missing heading {target}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {count} local documentation links and anchors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
