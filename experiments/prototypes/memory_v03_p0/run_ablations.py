"""CLI wrapper for the Memory v0.3 P0 local prototype."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_v03_p0.run_ablations import main


if __name__ == "__main__":
    raise SystemExit(main())
