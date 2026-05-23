"""Run all dream3r tests with tqdm progress.

Uses unittest discovery per file so failures are isolated and tqdm shows
per-file progress with pass/fail counts.
"""
import argparse
import importlib
import io
import sys
import time
import traceback
import unittest
from pathlib import Path

try:
    from tqdm.auto import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def discover_test_modules(tests_dir: Path):
    modules = []
    for p in sorted(tests_dir.glob("test_*.py")):
        modules.append(p.stem)
    return modules


def run_one_module(module_name: str):
    """Import + run unittest on a single test module. Return summary dict."""
    full = f"dream3r.tests.{module_name}"
    started = time.perf_counter()
    try:
        mod = importlib.import_module(full)
    except Exception as exc:
        return {
            "module": module_name,
            "status": "import_error",
            "n_tests": 0,
            "n_failures": 0,
            "n_errors": 1,
            "elapsed_s": 0.0,
            "detail": f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        }

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(mod)

    # Capture output instead of polluting tqdm display
    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=1)
    result = runner.run(suite)
    elapsed = time.perf_counter() - started

    n_tests = result.testsRun
    n_failures = len(result.failures)
    n_errors = len(result.errors)
    n_skipped = len(getattr(result, "skipped", []))

    status = "ok"
    if n_errors > 0:
        status = "error"
    elif n_failures > 0:
        status = "fail"

    detail = ""
    if status != "ok":
        for label, items in (("FAIL", result.failures), ("ERROR", result.errors)):
            for case, tb in items:
                detail += f"  [{label}] {case}\n{tb}\n"

    return {
        "module": module_name,
        "status": status,
        "n_tests": n_tests,
        "n_failures": n_failures,
        "n_errors": n_errors,
        "n_skipped": n_skipped,
        "elapsed_s": elapsed,
        "detail": detail,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tests-dir", default="dream3r/tests")
    parser.add_argument("--output", default="runs/test_report.txt")
    parser.add_argument("--only", nargs="*", default=None,
                        help="If set, only run these module names")
    args = parser.parse_args()

    tests_dir = Path(args.tests_dir).resolve()
    modules = discover_test_modules(tests_dir)
    if args.only:
        modules = [m for m in modules if m in args.only]

    iterator = modules
    if HAS_TQDM:
        iterator = tqdm(modules, desc="dream3r tests", unit="mod",
                        dynamic_ncols=True, mininterval=0.3)

    results = []
    total_tests = 0
    total_pass = 0
    total_fail = 0
    total_err = 0
    started = time.time()

    for mod_name in iterator:
        if HAS_TQDM:
            iterator.set_description(f"tests [{mod_name[:30]}]")
        result = run_one_module(mod_name)
        results.append(result)

        total_tests += result["n_tests"]
        total_fail += result["n_failures"]
        total_err += result["n_errors"]
        total_pass += result["n_tests"] - result["n_failures"] - result["n_errors"]

        if HAS_TQDM:
            iterator.set_postfix({
                "pass": total_pass,
                "fail": total_fail,
                "err": total_err,
                "last": result["status"],
            })

    elapsed = time.time() - started

    # Write a readable report
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("=" * 80)
    lines.append(f"Dream3R Test Report  (elapsed {elapsed:.1f}s)")
    lines.append("=" * 80)
    lines.append(f"Modules:  {len(modules)}")
    lines.append(f"Tests:    {total_tests}")
    lines.append(f"Pass:     {total_pass}")
    lines.append(f"Fail:     {total_fail}")
    lines.append(f"Error:    {total_err}")
    lines.append("")
    lines.append(f"{'module':<48} {'status':<10} {'tests':>5} "
                 f"{'fail':>5} {'err':>5} {'time':>7}")
    lines.append("-" * 80)
    for r in results:
        lines.append(
            f"{r['module']:<48} {r['status']:<10} {r['n_tests']:>5} "
            f"{r['n_failures']:>5} {r['n_errors']:>5} {r['elapsed_s']:>6.1f}s"
        )

    failing = [r for r in results if r["status"] != "ok"]
    if failing:
        lines.append("")
        lines.append("=" * 80)
        lines.append("FAILURE DETAILS")
        lines.append("=" * 80)
        for r in failing:
            lines.append(f"\n--- {r['module']} ({r['status']}) ---")
            lines.append(r["detail"])

    output.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("\n".join(lines[:14]))
    print(f"\nFull report: {output}")
    sys.exit(0 if (total_fail == 0 and total_err == 0) else 1)


if __name__ == "__main__":
    main()
