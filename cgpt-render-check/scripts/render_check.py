import argparse
import html.parser
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


class HtmlProbe(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: set[str] = set()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag.lower())
        for key, value in attrs:
            if value is None:
                continue
            if key.lower() == "id":
                self.ids.add(value)
            elif key.lower() == "href":
                self.hrefs.append(value)
            elif key.lower() == "src":
                self.srcs.append(value)

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_parts.append(data.strip())


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


def zip_names(path: Path) -> list[str]:
    with zipfile.ZipFile(path, "r") as z:
        return z.namelist()


def check_internal_links(path: Path, probe: HtmlProbe) -> list[tuple[str, str]]:
    results = []
    missing = []
    for href in probe.hrefs:
        if href.startswith("#") and len(href) > 1 and href[1:] not in probe.ids:
            missing.append(href)
    if missing:
        results.append(("WARN", f"missing internal HTML anchors: {len(missing)}"))

    missing_assets = []
    for ref in probe.srcs:
        if re.match(r"^(?:https?:)?//|^data:|^#", ref, re.I):
            continue
        ref_path = (path.parent / ref.split("#", 1)[0].split("?", 1)[0]).resolve()
        if not ref_path.exists():
            missing_assets.append(ref)
    if missing_assets:
        results.append(("WARN", f"missing local HTML assets: {len(missing_assets)}"))
    return results


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
        names = zip_names(path)
        text = read_zip_text(path, ("word/",))
        results.append(("PASS" if "[Content_Types].xml" in names else "FAIL", "DOCX content types present"))
        results.append(("PASS" if "word/document.xml" in names else "FAIL", "DOCX main document present"))
        media = [n for n in names if n.startswith("word/media/")]
        results.append(("PASS", f"DOCX media count={len(media)}"))
    elif ext == ".pptx":
        names = zip_names(path)
        text = read_zip_text(path, ("ppt/slides/", "ppt/notesSlides/"))
        slides = [n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        rels = [n for n in names if n.startswith("ppt/slides/_rels/slide") and n.endswith(".rels")]
        media = [n for n in names if n.startswith("ppt/media/")]
        results.append(("PASS" if "[Content_Types].xml" in names else "FAIL", "PPTX content types present"))
        results.append(("PASS" if slides else "FAIL", f"PPTX slide XML count={len(slides)}"))
        results.append(("PASS", f"PPTX slide relationship files={len(rels)}"))
        results.append(("PASS", f"PPTX media count={len(media)}"))
    elif ext in {".html", ".htm", ".md", ".txt"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ext in {".html", ".htm"}:
            probe = HtmlProbe()
            probe.feed(text)
            results.append(("PASS" if "html" in probe.tags else "WARN", "HTML tag present"))
            results.append(("PASS" if "body" in probe.tags else "WARN", "body tag present"))
            results.append(("PASS" if probe.text_parts else "WARN", f"visible text chunks={len(probe.text_parts)}"))
            results.extend(check_internal_links(path, probe))
    elif ext == ".pdf":
        header = path.read_bytes()[:5]
        results.append(("PASS" if header == b"%PDF-" else "FAIL", "PDF header check"))
        tail = path.read_bytes()[-2048:] if size else b""
        results.append(("PASS" if b"%%EOF" in tail else "WARN", "PDF EOF marker check"))
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
    parser = argparse.ArgumentParser(description="Run conservative structural checks on rendered artifacts.")
    parser.add_argument("outputs", nargs="+", help="Rendered file path(s) to inspect")
    args = parser.parse_args()

    exit_code = 0
    for output in args.outputs:
        path = Path(output).resolve()
        try:
            results = check(path)
        except Exception as exc:
            results = [("FAIL", str(exc))]
        print(f"RENDER_CHECK_REPORT\nfile={path}")
        for status, message in results:
            print(f"{status}: {message}")
        if any(status == "FAIL" for status, _ in results):
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
