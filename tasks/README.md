# Tasks — DEF-pyirstdmetrics
# PyIRSTDMetrics: Standardized IRSTD Performance Analysis
# NOTE: This is an EVALUATION TOOLKIT — no training, no model inference
# Total PRDs: 8 | Estimated Hours: 32
# Critical Path: PRD-001 → PRD-002 → PRD-003 → PRD-004 → PRD-005

---

## PRD-001: Installation + Verification (2h)
**Priority**: P0 — BLOCKER for everything
**Dependencies**: None

### Objective
Install PyIRSTDMetrics and verify all metrics produce correct reference values.

### Steps
```bash
# 1. Clone repo for development
cd /mnt/forge-data/shared_infra/repos/
git clone https://github.com/lartpang/PyIRSTDMetrics.git
cd PyIRSTDMetrics

# 2. Create uv environment
uv venv .venv --python 3.10
source .venv/bin/activate

# 3. Install dependencies
uv pip install numpy scikit-image scipy opencv-python matplotlib

# 4. Install package in editable mode
uv pip install -e .

# 5. Run unit tests
cd examples/
python test_metrics.py -v
# Expected: All tests pass, matching reference values in default_results dict

# 6. Verify metric recorder example
python metric_recorder.py
# Should produce: per-sample metrics + averaged metrics + plots

# 7. Quick API verification
python -c "
import py_irstd_metrics
import numpy as np

# Create synthetic data
pred = np.random.rand(128, 128).astype(np.float64)
mask = np.zeros((128, 128), dtype=bool)
mask[50:55, 60:65] = True  # small target

# Test pixel-level
cm = py_irstd_metrics.CMMetrics(
    num_bins=10, threshold=0.5,
    metric_handlers={
        'iou': py_irstd_metrics.IoUHandler(with_dynamic=False, with_binary=True, sample_based=False),
        'f1': py_irstd_metrics.FmeasureHandler(with_dynamic=False, with_binary=True, sample_based=False, beta=1),
    }
)
cm.update(pred, mask)
print('Pixel metrics:', cm.get())

# Test target-level
pd_fa = py_irstd_metrics.ProbabilityDetectionAndFalseAlarmRate(num_bins=1, distance_threshold=3)
pd_fa.update(pred, mask)
print('PD/FA:', pd_fa.get())

# Test hIoU
hiou = py_irstd_metrics.HierarchicalIoUBasedErrorAnalysis(num_bins=1, overlap_threshold=0.5, distance_threshold=3)
hiou.update(pred, mask)
print('hIoU errors:', hiou.get())

print('All API calls successful')
"

# 8. Run benchmark comparison
python benchmark_metrics.py
# Shows v1.0.1 → v1.0.2 optimization gains
```

### Reference Test Values (from test_metrics.py)
| Metric | Expected Value |
|--------|---------------|
| IoU (whole) | 0.5667 |
| nIoU (sample) | 0.5436 |
| F1 | 0.7234 |
| PD (basic) | 0.4 |
| FA (basic) | 6.775e-4 |
| PD (shooting) | 1.0 |
| hIoU (OPDC) | 0.1454 |
| seg_IoU | 0.5814 |
| loc_IoU | 0.25 |

### Acceptance Criteria
- [ ] `python test_metrics.py -v` — all tests PASS
- [ ] All 7 pixel-level handlers produce correct output
- [ ] All 3 PD/FA variants produce correct output
- [ ] HierarchicalIoUBasedErrorAnalysis produces all 9 error metrics
- [ ] metric_recorder.py runs and produces plots
- [ ] benchmark_metrics.py runs successfully

---

## PRD-002: ANIMA Evaluation Harness (5h)
**Priority**: P0 — Core integration
**Dependencies**: PRD-001

### Objective
Build a reusable evaluation harness that wraps PyIRSTDMetrics for all ANIMA defense IRSTD modules.

### Steps
```bash
# Create evaluation harness
mkdir -p /mnt/forge-data/shared_infra/eval/irstd/

# anima_irstd_eval.py — the main harness
# Features:
# 1. Load predictions from any ANIMA module (PyTorch output → numpy)
# 2. Load GT masks from standard IRSTD datasets
# 3. Run full PyIRSTDMetrics suite
# 4. Export results as JSON (CI/CD compatible)
# 5. Generate comparison tables across modules
# 6. Support multiple datasets and thresholds
```

### Harness API Design
```python
class ANIMAIRSTDEvaluator:
    """Standardized IRSTD evaluation for all ANIMA defense modules."""

    def __init__(self, num_bins=10, distance_threshold=3, overlap_threshold=0.5):
        self.analysis = IRSTDPerformanceAnalysis(num_bins=num_bins)
        self.basic_pd_fa = ProbabilityDetectionAndFalseAlarmRate(
            num_bins=num_bins, distance_threshold=distance_threshold
        )
        self.shoot_pd_fa = ShootingRuleBasedProbabilityDetectionAndFalseAlarmRate(
            num_bins=num_bins, box_1_radius=1, box_2_radius=4
        )

    def evaluate_predictions(self, pred_dir, mask_dir, dataset_name):
        """Evaluate all predictions in a directory against ground truth."""
        # Load pred/mask pairs, normalize, run update
        pass

    def evaluate_torch_model(self, model, dataloader, device='cuda'):
        """Evaluate a PyTorch model directly."""
        # Run inference, convert output to numpy, run update
        pass

    def export_json(self, output_path, module_name, dataset_name, hardware_info):
        """Export results as standardized JSON for CI/CD."""
        pass

    def compare_modules(self, results_dict):
        """Generate comparison table across multiple modules."""
        pass
```

### Acceptance Criteria
- [ ] ANIMAIRSTDEvaluator class wraps full PyIRSTDMetrics suite
- [ ] `evaluate_predictions()` works with directory of PNG pred/mask pairs
- [ ] `evaluate_torch_model()` works with PyTorch model + dataloader
- [ ] JSON export format includes: module_name, dataset, hardware, all metrics, timestamp
- [ ] Comparison table generation works for 2+ modules
- [ ] Handles edge cases: empty predictions, no targets in image, all background

---

## PRD-003: DEF-dhif Integration (4h)
**Priority**: P0 — First real integration
**Dependencies**: PRD-002, DEF-dhif PRD-005

### Objective
Integrate the evaluation harness with DEF-dhif to produce standardized results.

### Steps
```bash
cd /mnt/forge-data/shared_infra/repos/DHiF/

# 1. Replace DEF-dhif's custom metrics.py with PyIRSTDMetrics
# Create evaluation script that uses ANIMAIRSTDEvaluator

# 2. Evaluate all trained models
python eval_with_pyirstd.py \
  --model_name DNANet \
  --conv standard \
  --checkpoint checkpoints/dnanet_standard_nuaa/best.pth \
  --dataset NUAA-SIRST \
  --data_dir data/NUAA-SIRST \
  --output results/dnanet_standard_nuaa.json

python eval_with_pyirstd.py \
  --model_name DNANet \
  --conv DHiF \
  --checkpoint checkpoints/dnanet_dhif_nuaa/best.pth \
  --dataset NUAA-SIRST \
  --data_dir data/NUAA-SIRST \
  --output results/dnanet_dhif_nuaa.json

# 3. Generate comparison
python compare_results.py \
  --results results/dnanet_standard_nuaa.json results/dnanet_dhif_nuaa.json \
  --output results/comparison_nuaa.json
```

### Expected Output
```json
{
  "module": "DEF-dhif",
  "model": "DNANet",
  "conv": "DHiF",
  "dataset": "NUAA-SIRST",
  "hardware": "RTX 6000 Pro Blackwell",
  "timestamp": "2026-04-XX",
  "metrics": {
    "pixel_level": {"iou": 0.XX, "niou": 0.XX, "f1": 0.XX},
    "target_level": {
      "pd_basic": 0.XX, "fa_basic": 0.XX,
      "pd_opdc": 0.XX, "fa_opdc": 0.XX,
      "pd_shoot": 0.XX, "fa_shoot": 0.XX
    },
    "hybrid_level": {
      "hiou": 0.XX,
      "seg_iou": 0.XX, "seg_mrg_err": 0.XX, "seg_itf_err": 0.XX, "seg_pcp_err": 0.XX,
      "loc_iou": 0.XX, "loc_s2m_err": 0.XX, "loc_m2s_err": 0.XX, "loc_itf_err": 0.XX, "loc_pcp_err": 0.XX
    },
    "curves": {"pr": [...], "roc": [...]}
  }
}
```

### Acceptance Criteria
- [ ] DEF-dhif models evaluated with PyIRSTDMetrics (all 3 conv types)
- [ ] Results match or improve upon DEF-dhif's original metrics.py
- [ ] hIoU error analysis provides insight into WHERE DHiF helps
- [ ] JSON results exported for all model×dataset combinations
- [ ] Comparison shows Standard vs DHiF vs FDConv across all metric levels

---

## PRD-004: Cross-Module Evaluation Dashboard (5h)
**Priority**: P1 — DEMO VALUE for Shenzhen
**Dependencies**: PRD-002

### Objective
Build an interactive HTML dashboard for cross-module IRSTD evaluation results.

### Steps
```bash
# Build interactive dashboard using React/HTML artifact
# Features:
# 1. Module selector (DEF-dhif, future IRSTD modules)
# 2. Dataset selector (NUAA-SIRST, IRSTD-1K, NUDT-SIRST-Sea)
# 3. Metric comparison tables
# 4. PR curves and ROC curves (interactive)
# 5. hIoU error decomposition visualization
# 6. Per-image prediction browser
```

### Dashboard Layout
```
┌─────────────────────────────────────────────────┐
│ ANIMA IRSTD Evaluation Dashboard                │
├─────────────────────────────────────────────────┤
│ [Module: DEF-dhif ▼] [Dataset: NUAA-SIRST ▼]  │
├─────────────────────────────────────────────────┤
│ Pixel-Level    │ Target-Level   │ Hybrid (hIoU) │
│ IoU: 0.XX      │ PD: 0.XX       │ hIoU: 0.XX    │
│ nIoU: 0.XX     │ FA: 0.XX       │ seg_IoU: 0.XX │
│ F1: 0.XX       │                │ loc_IoU: 0.XX │
├─────────────────────────────────────────────────┤
│ Error Analysis                                  │
│ ┌───────────┬──────────┬──────────┬───────────┐ │
│ │ seg_mrg   │ seg_itf  │ seg_pcp  │ loc_itf   │ │
│ │ 0.XX      │ 0.XX     │ 0.XX     │ 0.XX      │ │
│ └───────────┴──────────┴──────────┴───────────┘ │
├─────────────────────────────────────────────────┤
│ [PR Curve Chart]        [ROC Curve Chart]       │
└─────────────────────────────────────────────────┘
```

### Acceptance Criteria
- [ ] Interactive HTML dashboard loads from JSON results
- [ ] Module and dataset selectors work
- [ ] Comparison tables show all metric levels
- [ ] PR and ROC curves render correctly
- [ ] hIoU error decomposition visualized (bar chart)
- [ ] Dashboard works for Shenzhen demo presentation

---

## PRD-005: Metric Computation Optimization (4h)
**Priority**: P1
**Dependencies**: PRD-001

### Objective
Profile and optimize PyIRSTDMetrics computation speed. The OPDC matching uses scipy's linear_sum_assignment which can be slow for images with many targets.

### Steps
```bash
# Profile metric computation
python -c "
import time
import numpy as np
from py_irstd_metrics import *

# Generate test data with many small targets
mask = np.zeros((512, 512), dtype=bool)
for i in range(50):  # 50 targets
    r, c = np.random.randint(10, 500, 2)
    mask[r:r+5, c:c+5] = True

pred = np.random.rand(512, 512) * 0.3
pred[mask] += 0.5
pred = np.clip(pred, 0, 1)

# Benchmark each metric type
for metric_cls, name in [
    (ProbabilityDetectionAndFalseAlarmRate, 'Basic PD/FA'),
    (ShootingRuleBasedProbabilityDetectionAndFalseAlarmRate, 'Shooting PD/FA'),
]:
    m = metric_cls(num_bins=10)
    start = time.perf_counter()
    for _ in range(100):
        m2 = metric_cls(num_bins=10)
        m2.update(pred, mask)
    elapsed = (time.perf_counter() - start) / 100 * 1000
    print(f'{name}: {elapsed:.1f}ms per image')

# OPDC matching (expected bottleneck)
m = MatchingBasedMetrics(num_bins=10, matching_method=OPDCMatching())
start = time.perf_counter()
for _ in range(100):
    m2 = MatchingBasedMetrics(num_bins=10, matching_method=OPDCMatching())
    m2.update(pred, mask)
elapsed = (time.perf_counter() - start) / 100 * 1000
print(f'OPDC Matching: {elapsed:.1f}ms per image')
"
```

### Optimization Targets
| Operation | Bottleneck | Optimization |
|-----------|-----------|--------------|
| `measure.label` | Connected components | Pre-compute once, reuse across metrics |
| `measure.regionprops` | Property extraction | Pre-compute once, reuse across metrics |
| `linear_sum_assignment` | Hungarian matching O(N³) | Already optimized in v1.0.2 |
| `dynamically_binarizing` | Histogram per threshold | Vectorize across bins |
| Multiple metric updates | Redundant computation | Shared pre-processing |

### Acceptance Criteria
- [ ] Per-metric computation time profiled
- [ ] Shared pre-processing eliminates redundant label/regionprops calls
- [ ] ≥2x speedup for full analysis suite on 50-target images
- [ ] Results still match reference values (correctness preserved)

---

## PRD-006: CI/CD Benchmark Tracking (3h)
**Priority**: P1
**Dependencies**: PRD-002

### Objective
Set up automated benchmark tracking that runs after every model training completion.

### Steps
```bash
# Create benchmark tracking infrastructure
mkdir -p /mnt/forge-data/shared_infra/eval/irstd/results/
mkdir -p /mnt/forge-data/shared_infra/eval/irstd/history/

# benchmark_track.py — tracks results over time
# Features:
# 1. Append results to history JSON
# 2. Detect regressions (metric drops > threshold)
# 3. Generate trend plots
# 4. Alert on significant improvements
```

### Result History Format
```json
{
  "history": [
    {
      "timestamp": "2026-04-XX",
      "module": "DEF-dhif",
      "model": "DNANet",
      "conv": "DHiF",
      "dataset": "NUAA-SIRST",
      "commit": "abc1234",
      "metrics": { ... }
    }
  ]
}
```

### Acceptance Criteria
- [ ] Results automatically appended to history
- [ ] Regression detection works (configurable thresholds)
- [ ] Trend visualization for key metrics over time
- [ ] JSON history file grows correctly with new entries

---

## PRD-007: Multi-Dataset Evaluation Standardization (4h)
**Priority**: P2
**Dependencies**: PRD-003

### Objective
Establish standard evaluation protocols for each IRSTD dataset.

### Dataset-Specific Protocols
| Dataset | Input Size | # Targets/img | Distance Threshold | Notes |
|---------|-----------|---------------|-------------------|-------|
| NUAA-SIRST | 256×256 crop / 512×512 test | 1-5 | 3 px | Standard |
| IRSTD-1K | Variable | 1-10 | 3 px | Diverse scenes |
| SIRST3 | Variable | 1-20 | 5 px | More targets per image |
| NUDT-SIRST-Sea | Variable | 1-3 | 3 px | Maritime, low clutter |

### Acceptance Criteria
- [ ] Per-dataset evaluation config files created
- [ ] Distance threshold validated per dataset
- [ ] Standard evaluation protocol documented
- [ ] Cross-dataset comparison methodology established

---

## PRD-008: Extended Metric Integration — SOD + Segmentation (5h)
**Priority**: P3 — Future cross-task evaluation
**Dependencies**: PRD-002

### Objective
Extend the evaluation harness to support metrics from other defense perception tasks (SOD, semantic segmentation, crowd counting) for unified cross-module comparison.

### Metric Mapping
| Task | Module | Metrics | Source |
|------|--------|---------|--------|
| IRSTD | DEF-dhif | IoU, nIoU, PD, FA, hIoU | PyIRSTDMetrics (this) |
| SOD | DEF-hypsam | Sm, maxFm, maxEm, MAE | PySODMetrics |
| Seg | DEF-tuni/cmssm/rtfdnet | mIoU, per-class IoU | torchmetrics |
| Counting | DEF-rgbtcc | GAME0-3, MSE, Re | Custom eval_game() |

### Acceptance Criteria
- [ ] Unified evaluation interface for all defense perception tasks
- [ ] Cross-task comparison table with normalized scores
- [ ] Each task uses its canonical metric set
- [ ] Dashboard supports multi-task view

---

*Updated 2026-04-04 by ANIMA Research Agent*
