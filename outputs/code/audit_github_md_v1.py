"""OV4 GitHub Web Markdown & MathJax Compliance Linter (v1).

Enforces UP-010 and REPOSITORY_MANAGEMENT.md Sec. 4.3:
  1. Display math must use multi-line `$$` fences (or ```math), blank lines before/after,
     and indent < 4 spaces (0 indent preferred).
  2. Inline math containing >=2 underscores `_`, `*`, or `\\{`/`\\}` must use GitHub's
     backtick-delimited inline math `$`...`$` to prevent cmark-gfm emphasis corruption.
  3. Table cells must NEVER contain raw `|` or `\\|` inside math; use `\\vert`.
  4. Forbids `**$...$**`, inner edge spaces in `$...$`, CJK inside math, and non-portable
     macros (`\\operatorname`, `\\tag{`, `\\lvert`, `\\rvert`, `\\begin{aligned}`).
  5. Validates all relative Markdown links, `<a name="...">` anchors, and forbids `file:///`.

Run from repository root:
    python outputs/code/audit_github_md_v1.py
    python outputs/code/audit_github_md_v1.py --all
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
SKIP_ROOTS = {"参考文献-整理版", "参考文献-整理版-Markdown", "参考文献_新增", "work", ".git"}
UNSAFE_MACROS = (r"\operatorname", r"\tag{", r"\lvert", r"\rvert", r"\begin{aligned}")


def find_md_files(repo: Path):
    files = []
    for p in sorted(repo.rglob("*.md")):
        if any(part in SKIP_ROOTS for part in p.relative_to(repo).parts):
            continue
        files.append(p)
    return files


def superseded_versions(md_files):
    """Return set of Paths that are older _vN versions superseded by a higher _vM."""
    groups = {}
    for p in md_files:
        m = re.match(r"^(.+)_v(\d+)\.md$", p.name)
        if m:
            key = (p.parent, m.group(1))
            groups.setdefault(key, []).append((int(m.group(2)), p))
    older = set()
    for items in groups.values():
        if len(items) > 1:
            max_v = max(v for v, _ in items)
            for v, p in items:
                if v < max_v:
                    older.add(p)
    return older


def audit_links(md_files):
    anchors = {}
    for f in md_files:
        txt = f.read_text(encoding="utf-8")
        anchors[f.resolve()] = set(re.findall(r'<a\s+name="([^"]+)"', txt))
    errors = []
    total_links = 0
    for f in md_files:
        rel = f.relative_to(REPO).as_posix()
        txt = f.read_text(encoding="utf-8")
        clean = re.sub(r"```.*?```", "", txt, flags=re.S)
        clean_no_code = re.sub(r"(`+)(?!`)([^\n]*?)(?<!`)\1(?!`)", "", clean)
        if "file:///" in clean_no_code:
            errors.append(f"{rel}: contains absolute file:/// link outside code span")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", clean):
            href = m.group(1).strip()
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            total_links += 1
            if "#" in href:
                path_part, frag = href.split("#", 1)
            else:
                path_part, frag = href, ""
            target = (f.parent / unquote(path_part)).resolve() if path_part else f.resolve()
            if not target.exists():
                errors.append(f"{rel}: BROKEN PATH ({href}) -> {target}")
                continue
            if frag and target in anchors and frag not in anchors[target]:
                errors.append(f"{rel}: BROKEN ANCHOR ({href}) missing #{frag}")
    return total_links, errors


def check_math_expr(expr: str, is_table: bool, is_backtick: bool, is_block: bool):
    errs = []
    if not is_block and (expr.startswith(" ") or expr.endswith(" ")):
        errs.append("INLINE-EDGE-SPACE")
    if re.search(r"[\u4e00-\u9fff]", expr):
        errs.append("MATH-CONTAINS-CJK")
    for mac in UNSAFE_MACROS:
        if mac in expr:
            errs.append(f"UNSAFE-MACRO({mac})")
    if is_table and "|" in expr:
        errs.append("TABLE-PIPE-IN-MATH(use \\vert)")
    if re.search(r"\\[{}]", expr):
        errs.append("ESCAPED-BRACE(use \\lbrace/\\rbrace)")
    if not is_block and not is_backtick:
        if expr.count("_") >= 2 or "*" in expr:
            errs.append("INLINE-NEEDS-BACKTICK($`...`$)")
    return errs


def audit_github_math_and_md(path: Path):
    rel = path.relative_to(REPO).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    errs = []
    in_code_fence = False
    in_math_fence = False
    in_dollar_block = False
    fence_marker = ""

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        # Track fenced code blocks (including ```math)
        if not in_dollar_block:
            m_fence = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
            if m_fence:
                if not in_code_fence:
                    in_code_fence = True
                    fence_marker = m_fence.group(1)[0] * len(m_fence.group(1))
                    lang = m_fence.group(2).strip().lower()
                    in_math_fence = (lang == "math")
                    if in_math_fence:
                        if indent >= 4:
                            errs.append(f"{rel}:L{idx} BLOCK-INDENT(>=4 spaces)")
                        if idx > 1 and lines[idx - 2].strip() != "":
                            errs.append(f"{rel}:L{idx} BLOCK-NO-BLANK-BEFORE")
                    continue
                elif stripped.startswith(fence_marker) and stripped.strip(fence_marker[0]) == "":
                    if in_math_fence and idx < len(lines) and lines[idx].strip() != "":
                        errs.append(f"{rel}:L{idx} BLOCK-NO-BLANK-AFTER")
                    in_code_fence = False
                    in_math_fence = False
                    fence_marker = ""
                    continue

        if in_code_fence:
            if in_math_fence:
                for e in check_math_expr(line, False, True, True):
                    errs.append(f"{rel}:L{idx} {e}: {stripped[:70]}")
            continue

        # Track $$ display blocks
        if stripped == "$$":
            if not in_dollar_block:
                in_dollar_block = True
                if indent >= 4:
                    errs.append(f"{rel}:L{idx} BLOCK-INDENT(>=4 spaces)")
                if idx > 1 and lines[idx - 2].strip() != "":
                    errs.append(f"{rel}:L{idx} BLOCK-NO-BLANK-BEFORE")
            else:
                in_dollar_block = False
                if indent >= 4:
                    errs.append(f"{rel}:L{idx} BLOCK-INDENT(>=4 spaces)")
                if idx < len(lines) and lines[idx].strip() != "":
                    errs.append(f"{rel}:L{idx} BLOCK-NO-BLANK-AFTER")
            continue

        if in_dollar_block:
            for e in check_math_expr(line, False, True, True):
                errs.append(f"{rel}:L{idx} {e}: {stripped[:70]}")
            continue

        # Left-to-right tokenization: distinguish normal code spans (`...`, ``...``) from GitHub $`...`$ inline math
        is_table = stripped.startswith("|")

        def tok_repl(m):
            if m.group("bt_math") is not None:
                expr = m.group("bt_math")
                for e in check_math_expr(expr, is_table, True, False):
                    errs.append(f"{rel}:L{idx} {e}: $`{expr}`$")
                return "MATH_BT_OK"
            return "CODE_SPAN"

        token_pat = re.compile(
            r"(?P<fence>`+)(?!`)(?P<code_body>[^\n]*?)(?<!`)(?P=fence)(?!`)"
            r"|\$`(?P<bt_math>[^`\n]+?)`\$"
        )
        work = token_pat.sub(tok_repl, line)

        # Check bold wrapping math ONLY outside code spans
        if re.search(r"\*\*(?:MATH_BT_OK|\$[^$\n]+\$)\*\*", work):
            errs.append(f"{rel}:L{idx} BOLD-WRAPS-MATH: {stripped[:80]}")

        # Single-line $$ outside code spans
        if "$$" in work:
            errs.append(f"{rel}:L{idx} BLOCK-SINGLE-LINE(use multiline $$): {stripped[:85]}")
            continue

        # Standard inline $...$
        for m in re.finditer(r"(?<!\\)\$(?!\$)([^$\n]+?)(?<!\\)\$", work):
            expr = m.group(1)
            for e in check_math_expr(expr, is_table, False, False):
                errs.append(f"{rel}:L{idx} {e}: ${expr}$")

    if in_dollar_block:
        errs.append(f"{rel}: UNCLOSED $$ block")
    return errs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Also audit superseded historical _vN files")
    args = parser.parse_args()

    md_files = find_md_files(REPO)
    older = set() if args.all else superseded_versions(md_files)

    total_links, link_errors = audit_links(md_files)
    math_errors = []
    checked_math = 0
    for p in md_files:
        if p in older:
            continue
        checked_math += 1
        math_errors.extend(audit_github_math_and_md(p))

    print(f"Link audit : {len(md_files)} markdown files, {total_links} relative links -> {len(link_errors)} errors")
    print(f"GitHub MD  : {checked_math} active markdown files (skipped {len(older)} historical baselines) -> {len(math_errors)} errors")
    for e in link_errors:
        print("  [LINK]", e)
    for e in math_errors[:60]:
        print("  [MATH]", e)
    if len(math_errors) > 60:
        print(f"  ... (+{len(math_errors) - 60} more)")

    if link_errors or math_errors:
        sys.exit(1)
    print("ALL CHECKS PASSED (Errors: 0)")


if __name__ == "__main__":
    main()
