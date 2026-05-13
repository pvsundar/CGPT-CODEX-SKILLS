import re
import sys
import zipfile
from pathlib import Path

PATTERNS = [
    ("unresolved cross-reference", re.compile(r"\?\?")),
    ("undefined marker", re.compile(r"undefined|UNDEFINED", re.I)),
    ("raw LaTeX command", re.compile(r"\\(?:textbf|textit|cite|ref|label|begin|end)\{")),
    ("missing figure marker", re.compile(r"\[.*?[Ff]igure.*?not found.*?\]")),
    ("template placeholder", re.compile(r"TODO|FIXME|\[PLACEHOLDER\]", re.I)),
]


def read_zip_text(path: Path, prefixes: tuple[str, ...]) -> str:
    text_parts = []
    with zipfile.ZipFile(path, "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"corrupt ZIP entry: {bad}")
        for name in z.namelist():
            if name.endswith(".xml") and name.startswith(prefixes):
                try:
                    text_parts.append(z.read(name).decode("utf-8", errors="ignore"))
                except Exception:
                    pass
    return "\n".join(text_parts)


def check(path: Path) -> list[tuple[str, str]]:
    results = []
    if not path.exists():
        return [("FAIL", f"missing file: {path}")]
    size = path.stat().st_size
    results.append(("PASS" if size > 0 else "FAIL", f"exists, bytes={size}"))
    if size < 1000:
        results.append(("WARN", "file is under 1000 bytes"))

    ext = path.suffix.lower()
    text = ""
    if ext == ".docx":
        text = read_zip_text(path, ("word/",))
        results.append(("PASS", "valid DOCX ZIP container"))
    elif ext == ".pptx":
        text = read_zip_text(path, ("ppt/slides/", "ppt/notesSlides/"))
        with zipfile.ZipFile(path, "r") as z:
            slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        results.append(("PASS" if slides else "FAIL", f"PPTX slide XML count={len(slides)}"))
    elif ext in {".html", ".htm", ".md", ".txt"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ext in {".html", ".htm"}:
            lower = text.lower()
            results.append(("PASS" if "<html" in lower else "WARN", "HTML tag present"))
            results.append(("PASS" if "<body" in lower else "WARN", "body tag present"))
    elif ext == ".pdf":
        header = path.read_bytes()[:5]
        results.append(("PASS" if header == b"%PDF-" else "FAIL", "PDF header check"))
    else:
        results.append(("WARN", f"no format-specific checks for {ext or 'no extension'}"))

    if text:
        for label, pattern in PATTERNS:
            count = len(pattern.findall(text))
            if count:
                severity = "WARN" if label == "template placeholder" else "FAIL"
                results.append((severity, f"{label}: {count}"))
        if not any(status == "FAIL" for status, _ in results):
            results.append(("PASS", "no blocking unresolved render markers detected"))
    else:
        results.append(("SKIP", "text extraction unavailable or not applicable"))
    return results


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: render_check.py <output-file>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    try:
        results = check(path)
    except Exception as exc:
        results = [("FAIL", str(exc))]
    print(f"RENDER_CHECK_REPORT\nfile={path}")
    for status, message in results:
        print(f"{status}: {message}")
    return 1 if any(status == "FAIL" for status, _ in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
