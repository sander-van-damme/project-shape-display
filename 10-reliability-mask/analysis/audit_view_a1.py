"""DND-104 A1 audit view for the DND-108 pre-registered adversarial register.

The falsifier's `--model` loader imports this module and reads `MODEL`. The
model's own AUDIT_VIEW is the source of truth; this thin module re-exports it.

  python 07-evidence-and-decisions/falsifier_dnd104_checks.py \
      --model 10-reliability-mask/analysis/audit_view_a1.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reliability_mask import AUDIT_VIEW as MODEL  # noqa: E402,F401
