#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a clean optimize_tests skeleton inside a factor directory."
    )
    parser.add_argument("factor_dir", type=Path)
    parser.add_argument("--factor-name", default=None)
    parser.add_argument("--engine", default="infer from existing factor artifacts")
    parser.add_argument("--data", default="infer from existing factor artifacts")
    parser.add_argument("--metrics", default="user-specified or infer from context")
    parser.add_argument("--overwrite-manifest", action="store_true")
    args = parser.parse_args()

    factor_dir = args.factor_dir.expanduser().resolve()
    if not factor_dir.exists() or not factor_dir.is_dir():
        raise SystemExit(f"factor_dir does not exist or is not a directory: {factor_dir}")

    root = factor_dir / "optimize_tests"
    for rel in ("period_sweep", "ablation", "refinement"):
        (root / rel).mkdir(parents=True, exist_ok=True)

    manifest_path = root / "00_manifest.json"
    if args.overwrite_manifest or not manifest_path.exists():
        manifest = {
            "factor_dir": str(factor_dir),
            "factor_name": args.factor_name or factor_dir.name,
            "engine": args.engine,
            "data": args.data,
            "metrics": args.metrics,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "initialized",
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    placeholders = {
        root / "period_sweep" / "period_sweep_summary.md": "# Period Sweep 总结\n\n",
        root / "ablation" / "ablation_summary.md": "# Ablation 总结\n\n",
        root / "refinement" / "refinement_summary.md": "# Refinement 总结\n\n",
        root / "optimize_report.md": "# 因子优化报告\n\n",
    }
    for path, text in placeholders.items():
        if not path.exists():
            path.write_text(text)

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
