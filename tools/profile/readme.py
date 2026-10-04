import re
from pathlib import Path

README_FILE = Path("README.md")

def replace_zone(s: str, tag: str, new_block: str) -> str:
    pattern = re.compile(
        r"<!-- " + re.escape(tag) + r":start -->.*?<!-- " + re.escape(tag) + r":end -->",
        re.DOTALL,
    )
    new_s, n = pattern.subn(
        f"<!-- {tag}:start -->\n{new_block}\n<!-- {tag}:end -->",
        s,
    )
    if n == 0:
        raise RuntimeError(f"No match for marker {tag}:start/end")
    if n > 1:
        raise RuntimeError(f"Multiple matches for marker {tag}:start/end")
    return new_s

if __name__ == "__main__":
    readme_text = README_FILE.read_text(encoding="utf-8")
    updated = replace_zone(readme_text, "stats", "<!-- no stats yet -->")
    README_FILE.write_text(updated, encoding="utf-8")
