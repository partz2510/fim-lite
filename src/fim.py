#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
BASELINE = ".baseline.json"
REPORTS = "reports"

@dataclass(frozen=True)
class FileRec:
    path: str
    size: int
    mtime: float
    hash: str

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot(root: Path, excludes: list[str]) -> dict[str, FileRec]:
    files = {}
    for dirpath, _, fnames in os.walk(root):
        d = Path(dirpath)
        for n in fnames:
            p = d / n
            rel = p.relative_to(root).as_posix()
            if any(e in rel for e in excludes) or rel.startswith(REPORTS) or rel == BASELINE:
                continue
            s = p.stat()
            files[rel] = FileRec(rel, s.st_size, s.st_mtime, sha256(p))
    return files

def init_baseline(root: Path, excludes: list[str]):
    data = {"generated_at": datetime.now().isoformat(),
            "files": {k: asdict(v) for k, v in snapshot(root, excludes).items()}}
    with open(root / BASELINE, "w") as f: json.dump(data, f, indent=2)
    console.print(f"[green]Baseline created:[/green] {len(data['files'])} files • {BASELINE}")

def check_changes(root: Path, excludes: list[str]):
    with open(root / BASELINE) as f: old = json.load(f)["files"]
    new = snapshot(root, excludes)
    added = [k for k in new if k not in old]
    removed = [k for k in old if k not in new]
    modified = [k for k in new if k in old and new[k].hash != old[k]["hash"]]
    table = Table(title="FIM-Lite Report", box=box.SIMPLE_HEAVY)
    table.add_column("Status"); table.add_column("Path")
    for x in added: table.add_row("[green]ADDED[/green]", x)
    for x in removed: table.add_row("[red]REMOVED[/red]", x)
    for x in modified: table.add_row("[yellow]MODIFIED[/yellow]", x)
    console.print(table)
    console.print(Panel.fit(f"Unchanged: {len(new)-len(added)-len(removed)-len(modified)}", style="dim"))

def cli():
    p = argparse.ArgumentParser(description="FIM-Lite • SHA-256 file integrity checker")
    sub = p.add_subparsers(dest="cmd", required=True)
    for sp in (sub.add_parser("init"), sub.add_parser("check")):
        sp.add_argument("--root", default=".", help="Directory root")
        sp.add_argument("--exclude", action="append", default=[], help="Pattern to exclude")
    a = p.parse_args()
    root = Path(a.root)
    if a.cmd == "init": init_baseline(root, a.exclude)
    if a.cmd == "check": check_changes(root, a.exclude)

if __name__ == "__main__":
    sys.exit(cli())
