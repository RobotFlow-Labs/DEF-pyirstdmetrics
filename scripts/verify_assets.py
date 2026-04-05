import importlib
import sys
from pathlib import Path


def check_path(path: Path) -> bool:
    ok = path.exists()
    print(f"[{'OK' if ok else 'MISSING'}] {path}")
    return ok


def check_import(name: str) -> bool:
    try:
        importlib.import_module(name)
    except Exception as exc:  # pragma: no cover
        print(f"[MISSING] import {name}: {exc}")
        return False
    print(f"[OK] import {name}")
    return True


def add_local_reference_repo() -> None:
    ref_repo = Path("repositories/PyIRSTDMetrics").resolve()
    if ref_repo.exists() and str(ref_repo) not in sys.path:
        sys.path.insert(0, str(ref_repo))


def main() -> int:
    add_local_reference_repo()
    checks = [
        check_path(Path("papers/2509.16888.pdf")),
        check_path(Path("repositories/PyIRSTDMetrics/readme.md")),
        check_path(Path("repositories/PyIRSTDMetrics/examples/test_data/0-pred.png")),
        check_import("py_irstd_metrics"),
    ]
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
