from pathlib import Path


REQUIRED_FILES = [
    "pyproject.toml",
    "ASSETS.md",
    "PRD.md",
    "anima_module.yaml",
    "Dockerfile.serve",
    "docker-compose.serve.yml",
    "configs/default.toml",
    "src/anima_pyirstdmetrics/evaluator.py",
    "tests/test_evaluator_smoke.py",
]


def main() -> int:
    failures = 0
    for rel in REQUIRED_FILES:
        path = Path(rel)
        ok = path.exists()
        print(f"[{'OK' if ok else 'MISSING'}] {rel}")
        if not ok:
            failures += 1
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
