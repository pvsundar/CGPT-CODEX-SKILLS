import argparse
import shutil
from datetime import date
from pathlib import Path


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem if path.suffix else path.name
    suffix = path.suffix
    parent = path.parent
    for i in range(2, 1000):
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find available backup name for {path}")


def directory_stats(path: Path) -> tuple[int, int]:
    files = [p for p in path.rglob("*") if p.is_file()]
    return len(files), sum(p.stat().st_size for p in files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a timestamped backup copy.")
    parser.add_argument("--source", required=True, help="File or directory to back up")
    parser.add_argument("--dest-dir", help="Optional parent directory for backup")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"ERROR: source does not exist: {source}")

    dest_parent = Path(args.dest_dir).resolve() if args.dest_dir else source.parent
    dest_parent.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()

    if source.is_file():
        dest = unique_path(dest_parent / f"{source.stem}_backup_{stamp}{source.suffix}")
        shutil.copy2(source, dest)
        src_size = source.stat().st_size
        dest_size = dest.stat().st_size
        if src_size != dest_size:
            raise SystemExit(f"ERROR: size mismatch: source={src_size} backup={dest_size}")
        print(f"BACKUP_OK\nsource={source}\nbackup={dest}\nbytes={dest_size}")
        return 0

    dest = unique_path(dest_parent / f"{source.name}_backup_{stamp}")
    shutil.copytree(source, dest)
    src_count, src_bytes = directory_stats(source)
    dest_count, dest_bytes = directory_stats(dest)
    if src_count != dest_count or src_bytes != dest_bytes:
        raise SystemExit(
            f"ERROR: directory mismatch: source={src_count}/{src_bytes} backup={dest_count}/{dest_bytes}"
        )
    print(f"BACKUP_OK\nsource={source}\nbackup={dest}\nfiles={dest_count}\nbytes={dest_bytes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
