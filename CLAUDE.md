# DEF-pyirstdmetrics — PyIRSTDMetrics: Standardized IRSTD Performance Analysis
# Wave 8 Defense Module (EVALUATION TOOLKIT — not a model)
# Paper: "Rethinking Evaluation of Infrared Small Target Detection" — NeurIPS 2025 (D&B)
# Authors: Youwei Pang, Xiaoqi Zhao, Lihe Zhang, Huchuan Lu, Georges El Fakhri, Xiaofeng Liu, Shijian Lu
# ArXiv: 2509.16888
# Repo: https://github.com/lartpang/PyIRSTDMetrics
# PyPI: pyirstdmetrics (v1.0.2)
# Domain: IRSTD Evaluation Toolkit — standardized metrics for infrared small target detection
# Product Stack: ALL STACKS (evaluation infrastructure) — ORACLE, ATLAS, NEMESIS
# Related: DEF-dhif (IRSTD detection, primary evaluation target), DEF-saap (SAR detection)

## Status: ENRICHED — Ready for build

## THIS IS A TOOLKIT, NOT A MODEL
Unlike other DEF modules, this is an **evaluation library** — no training, no inference, no GPU needed for the metrics themselves. It provides standardized IRSTD metrics used to evaluate ALL defense IRSTD modules (DEF-dhif, and any future IRSTD additions). Think of it as the "ruler" that measures all the other modules.

## Paper Summary
"Rethinking Evaluation of Infrared Small Target Detection" (NeurIPS 2025 D&B) proposes **hIoU (Hierarchical IoU)** — a new metric that balances both pixel-level segmentation quality and target-level detection quality for IRSTD. The paper identifies that existing metrics (IoU, PD/FA) are insufficient: pixel-level IoU ignores whether individual targets are detected, while target-level PD ignores segmentation quality. hIoU = seg_IoU × loc_IoU decomposes into interpretable error categories. The toolkit implements the full metric suite: pixel-level (IoU, nIoU, F1, Precision, Recall, TPR, FPR), target-level (PD, FA via 3 matching methods), and hybrid-level (hIoU with error analysis). ArXiv: 2509.16888.

## Architecture

### Module Structure
```
py_irstd_metrics/
├── __init__.py               — Public API exports
├── pixelwise_metrics.py      — CMMetrics + handler classes (IoU, F1, Precision, Recall, TPR, FPR)
├── targetwise_metrics.py     — PD/FA (3 variants), OPDCMatching, DistanceOnlyMatching,
│                                MatchingBasedMetrics, HierarchicalIoUBasedErrorAnalysis
└── utils.py                  — divide_func, prepare_data, adaptive_threshold, ndarray_to_basetype
```

### Metric Hierarchy

#### Level 1: Pixel-Level Metrics (CMMetrics)
Confusion-matrix based metrics operating on binary or dynamically-thresholded predictions:
```python
class CMMetrics:
    # Manages multiple metric handlers with shared threshold computation
    # Supports: dynamic thresholding (bins), binary thresholding, sample-based or whole-based

# Available handlers:
IoUHandler         # IoU = TP / (TP + FP + FN) — Jaccard index
FmeasureHandler    # F1 = (1+β²) × P × R / (β² × P + R)
PrecisionHandler   # P = TP / (TP + FP)
RecallHandler      # R = TP / (TP + FN) — same as TPR
TPRHandler         # TPR = TP / (TP + FN) — alias for Recall
FPRHandler         # FPR = FP / (FP + TN) — false positive rate
```

**Sample-based vs Whole-based**: `sample_based=True` averages per-image metrics (nIoU), `sample_based=False` accumulates TP/FP/TN/FN globally (IoU).

**Dynamic thresholding**: Sweeps threshold from 0 to 1 using `num_bins` bins, computing metrics at each threshold for PR curves and ROC curves.

#### Level 2: Target-Level Metrics (3 PD/FA variants)
Target detection evaluation using connected component matching:

```python
# Variant 1: Original PD/FA (distance-only centroid matching)
ProbabilityDetectionAndFalseAlarmRate(num_bins=1, distance_threshold=3)
# Matches pred targets to GT targets if centroid distance < threshold
# PD = matched_targets / total_GT_targets
# FA = unmatched_pred_area / total_image_area

# Variant 2: Shooting-rule-based PD/FA
ShootingRuleBasedProbabilityDetectionAndFalseAlarmRate(num_bins=1, box_1_radius=1, box_2_radius=4)
# Uses box-based matching: any positive pixel within box_1_radius of GT pixel = detection
# box_2_radius defines exclusion zone for false alarm computation

# Variant 3: OPDC Matching (Overlap Priority + Distance Compensation)
MatchingBasedMetrics(matching_method=OPDCMatching(overlap_threshold=0.5, distance_threshold=3))
# Two-phase matching:
#   Phase 1: Hungarian assignment prioritizing IoU overlap (≥ overlap_threshold)
#   Phase 2: Distance-based compensation for remaining unmatched targets
# Returns: PD, FA, hIoU (seg_IoU × loc_IoU)

# Variant 4: Distance-only matching (for backward compatibility)
MatchingBasedMetrics(matching_method=DistanceOnlyMatching(distance_threshold=3))
# Simple centroid distance matching like Variant 1 but through MatchingBasedMetrics
```

#### Level 3: Hierarchical IoU + Error Analysis (KEY INNOVATION)
```python
class HierarchicalIoUBasedErrorAnalysis:
    # hIoU = seg_IoU × loc_IoU
    # where:
    #   seg_IoU = average IoU of matched target pairs (pixel-level quality)
    #   loc_IoU = TP_targets / (TP + FP + FN targets) (target-level detection)

    # Error decomposition:
    # Segmentation errors (pixel-level):
    #   seg_mrg_err — merge error: pred overlaps OTHER GT targets (over-segmentation)
    #   seg_itf_err — interference error: pred extends beyond target (false positive pixels)
    #   seg_pcp_err — perception error: missed GT pixels (false negative pixels)

    # Localization errors (target-level):
    #   loc_itf_err — interference: false positive targets with no GT correspondence
    #   loc_pcp_err — perception: missed GT targets with no pred correspondence
    #   loc_m2s_err — many-to-single: multiple GT matched to one pred
    #   loc_s2m_err — single-to-many: one GT matched to multiple preds
```

### Key Algorithm: OPDC Matching (OPDCMatching class)
```python
class OPDCMatching:
    def __call__(self, pred_tgts_map, mask_tgts_map, pred_props, mask_props):
        # Step 1: Compute pairwise info
        paired_distance = centroid_distances(mask_props, pred_props)  # (M, N)
        paired_iou = pixel_iou_per_pair(mask_props, pred_props)      # (M, N)

        # Step 2: Overlap-priority constraint
        # Hungarian assignment on distance matrix, filtered by IoU ≥ overlap_threshold
        valid_iou = paired_iou >= self.overlap_threshold
        row_ind, col_ind = linear_sum_assignment(paired_distance)
        matched = valid_iou[row_ind, col_ind]

        # Step 3: Distance-based compensation
        # For remaining unmatched targets, try distance-only matching
        unmatched_mask = rows not in matched
        unmatched_pred = cols not in matched
        sub_distances = paired_distance[unmatched_mask, :][:, unmatched_pred]
        row2, col2 = linear_sum_assignment(sub_distances)
        # Accept if distance < distance_threshold
```

### API Usage Pattern
```python
import py_irstd_metrics

# Full analysis suite
analyzer = IRSTDPerformanceAnalysis(num_bins=10)
for pred, mask in dataset:
    pred = pred / 255.0          # normalize to [0, 1]
    mask = mask > 127            # binarize to bool
    analyzer.update(pred, mask)

results = analyzer.show(num_bits=4)
# Returns: iou, niou, f1, pd_distonly, pd_opdc, fa_distonly, fa_opdc,
#          hiou_opdc, seg_iou, seg_mrg_err, seg_itf_err, seg_pcp_err,
#          loc_iou, loc_s2m_err, loc_m2s_err, loc_itf_err, loc_pcp_err,
#          pre (curve), rec (curve), tpr (curve), fpr (curve)
```

## Dependencies
- numpy >= 1.23, < 2.0
- scikit-image >= 0.14.1, < 1.0 (for `measure.label`, `measure.regionprops` — connected components)
- scipy >= 1.10, < 2.0 (for `optimize.linear_sum_assignment` — Hungarian matching)
- **NO PyTorch, NO GPU required** — pure numpy/scipy/skimage

## Repo Structure
```
PyIRSTDMetrics/
├── readme.md
├── pyproject.toml              — setuptools build, v1.0.2, pyirstdmetrics on PyPI
├── requirements.txt            — numpy, scikit-image, scipy
├── py_irstd_metrics/
│   ├── __init__.py             — Public API: CMMetrics, handlers, matching, hIoU
│   ├── pixelwise_metrics.py    — CMMetrics + IoU/F1/Precision/Recall/TPR/FPR handlers
│   ├── targetwise_metrics.py   — PD/FA (3 variants), OPDC, DistanceOnly, hIoU error analysis
│   └── utils.py                — divide_func, prepare_data, adaptive_threshold
└── examples/
    ├── test_metrics.py         — Unit tests with known reference values
    ├── metric_recorder.py      — Full usage examples: BasicIRSTDPerformance, IRSTDPerformanceAnalysis
    ├── benchmark_metrics.py    — Performance benchmarking (v1.0.1 vs v1.0.2 optimization)
    ├── benchmark.json          — Benchmark results
    └── test_data/              — Sample pred/mask PNG pairs for testing
```

## Build Requirements
- [ ] Install: `uv pip install pyirstdmetrics` (or clone and `uv pip install -e .`)
- [ ] Verify: `python examples/test_metrics.py` — all tests pass
- [ ] Create ANIMA evaluation harness wrapping PyIRSTDMetrics
- [ ] Integrate with DEF-dhif evaluation pipeline
- [ ] Build cross-module evaluation dashboard
- [ ] Add JSON result export for CI/CD tracking

## Integration Points (CRITICAL for Wave 8)
This module is the **evaluation backbone** for all IRSTD modules:
- **DEF-dhif**: Primary evaluation target — IoU, nIoU, PD, FA, hIoU across all conv types
- **Future IRSTD modules**: Any new IRSTD detection module uses this for standardized eval
- **Cross-stack comparison**: Enables apples-to-apples comparison across defense modules
- **Shenzhen demo**: Provides standardized metrics for demo scoring and presentation

## Defense Marketplace Value
Standardized evaluation is critical for defense procurement: customers need verified performance metrics. PyIRSTDMetrics provides: (1) NeurIPS-published evaluation methodology with academic credibility, (2) multiple matching methods for different evaluation philosophies, (3) hierarchical error analysis showing exactly WHERE models fail (localization vs segmentation vs interference), (4) curve-based analysis (PR, ROC) for threshold-independent evaluation, (5) reproducible benchmark infrastructure. The hIoU metric is particularly valuable because it answers both "did you detect the target?" AND "how well did you segment it?" in a single number.

## Package Manager: uv (NEVER pip)
## Python: >= 3.10
## No GPU required — CPU-only evaluation toolkit
## Git prefix: [DEF-pyirstdmetrics]
