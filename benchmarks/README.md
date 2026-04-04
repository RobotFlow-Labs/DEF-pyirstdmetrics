# Benchmarks — DEF-pyirstdmetrics
# PyIRSTDMetrics: Standardized IRSTD Performance Analysis
# Paper: ArXiv 2509.16888 (NeurIPS 2025 D&B)
# NOTE: This is an EVALUATION TOOLKIT — benchmarks focus on metric computation performance
#        and cross-module result aggregation, NOT model inference

## Reference Test Values (from examples/test_metrics.py)

### Verified Reference Metrics (test_data samples)
| Metric | Level | Value | Method |
|--------|-------|-------|--------|
| IoU (whole-based) | Pixel | 0.5667 | CMMetrics + IoUHandler(sample_based=False) |
| nIoU (sample-based) | Pixel | 0.5436 | CMMetrics + IoUHandler(sample_based=True) |
| F1 | Pixel | 0.7234 | CMMetrics + FmeasureHandler(beta=1) |
| Precision (avg) | Pixel | 0.5203 | CMMetrics + PrecisionHandler(dynamic) |
| Recall (avg) | Pixel | 0.8506 | CMMetrics + RecallHandler(dynamic) |
| TPR (avg) | Pixel | 0.8506 | CMMetrics + TPRHandler(dynamic) |
| FPR (avg) | Pixel | 0.1114 | CMMetrics + FPRHandler(dynamic) |
| PD (basic, thr=0.5) | Target | 0.4 | ProbabilityDetectionAndFalseAlarmRate |
| FA (basic, thr=0.5) | Target | 6.775e-4 | ProbabilityDetectionAndFalseAlarmRate |
| PD (shooting, thr=0.5) | Target | 1.0 | ShootingRuleBasedPD/FA |
| FA (shooting, thr=0.5) | Target | 4.883e-5 | ShootingRuleBasedPD/FA |
| PD (dist-only, thr=0.5) | Target | 0.4 | MatchingBasedMetrics + DistanceOnlyMatching |
| PD (OPDC, thr=0.5) | Target | 0.4 | MatchingBasedMetrics + OPDCMatching |
| hIoU (OPDC, thr=0.5) | Hybrid | 0.1454 | MatchingBasedMetrics + OPDCMatching |
| seg_IoU | Hybrid | 0.5814 | HierarchicalIoUBasedErrorAnalysis |
| seg_mrg_err | Hybrid | 0.2368 | HierarchicalIoUBasedErrorAnalysis |
| seg_itf_err | Hybrid | 0.0736 | HierarchicalIoUBasedErrorAnalysis |
| seg_pcp_err | Hybrid | 0.1081 | HierarchicalIoUBasedErrorAnalysis |
| loc_IoU | Hybrid | 0.25 | HierarchicalIoUBasedErrorAnalysis |
| loc_s2m_err | Hybrid | 0.125 | HierarchicalIoUBasedErrorAnalysis |
| loc_m2s_err | Hybrid | 0.0 | HierarchicalIoUBasedErrorAnalysis |
| loc_itf_err | Hybrid | 0.375 | HierarchicalIoUBasedErrorAnalysis |
| loc_pcp_err | Hybrid | 0.25 | HierarchicalIoUBasedErrorAnalysis |

## Metric Computation Performance

### Per-Image Computation Time (512×512, varying target count)
| # Targets | CMMetrics (ms) | Basic PD/FA (ms) | Shooting PD/FA (ms) | OPDC Matching (ms) | hIoU Analysis (ms) | Full Suite (ms) |
|-----------|---------------|------------------|--------------------|--------------------|--------------------|----|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD |
| 5 | TBD | TBD | TBD | TBD | TBD | TBD |
| 10 | TBD | TBD | TBD | TBD | TBD | TBD |
| 25 | TBD | TBD | TBD | TBD | TBD | TBD |
| 50 | TBD | TBD | TBD | TBD | TBD | TBD |

### Scaling with Image Resolution (5 targets, 10 bins)
| Resolution | CMMetrics (ms) | OPDC (ms) | Full Suite (ms) |
|-----------|---------------|-----------|----------------|
| 128×128 | TBD | TBD | TBD |
| 256×256 | TBD | TBD | TBD |
| 512×512 | TBD | TBD | TBD |
| 1024×1024 | TBD | TBD | TBD |

### Scaling with Number of Bins
| # Bins | CMMetrics (ms) | Target metrics (ms) | Full Suite (ms) |
|--------|---------------|--------------------|----|
| 1 | TBD | TBD | TBD |
| 5 | TBD | TBD | TBD |
| 10 | TBD | TBD | TBD |
| 20 | TBD | TBD | TBD |
| 50 | TBD | TBD | TBD |

### v1.0.1 vs v1.0.2 OPDC Optimization (from repo benchmarks)
| Scenario | v1.0.1 (ms) | v1.0.2 (ms) | Speedup |
|----------|------------|------------|---------|
| OPDC matching (benchmark set) | TBD (from benchmark.json) | TBD | TBD |

## Cross-Module IRSTD Results (AGGREGATION)

### DEF-dhif Results (when available)

#### NUAA-SIRST
| Model | Conv | IoU ↑ | nIoU ↑ | F1 ↑ | PD ↑ | FA ↓ | hIoU ↑ |
|-------|------|-------|--------|------|------|------|--------|
| DNANet | Standard | TBD | TBD | TBD | TBD | TBD | TBD |
| DNANet | DHiF | TBD | TBD | TBD | TBD | TBD | TBD |
| DNANet | FDConv | TBD | TBD | TBD | TBD | TBD | TBD |

#### IRSTD-1K
| Model | Conv | IoU ↑ | nIoU ↑ | F1 ↑ | PD ↑ | FA ↓ | hIoU ↑ |
|-------|------|-------|--------|------|------|------|--------|
| DNANet | Standard | TBD | TBD | TBD | TBD | TBD | TBD |
| DNANet | DHiF | TBD | TBD | TBD | TBD | TBD | TBD |

#### NUDT-SIRST-Sea (Defense Priority)
| Model | Conv | IoU ↑ | nIoU ↑ | F1 ↑ | PD ↑ | FA ↓ | hIoU ↑ |
|-------|------|-------|--------|------|------|------|--------|
| DNANet | Standard | TBD | TBD | TBD | TBD | TBD | TBD |
| DNANet | DHiF | TBD | TBD | TBD | TBD | TBD | TBD |

### hIoU Error Decomposition (NUAA-SIRST, best model)
| Error Type | Level | Value | Interpretation |
|-----------|-------|-------|---------------|
| seg_mrg_err | Pixel | TBD | Over-segmentation: pred bleeds into other targets |
| seg_itf_err | Pixel | TBD | Interference: false positive pixels around target |
| seg_pcp_err | Pixel | TBD | Perception: missed target pixels |
| loc_itf_err | Target | TBD | False positive targets (no GT match) |
| loc_pcp_err | Target | TBD | Missed targets (no pred match) |
| loc_m2s_err | Target | TBD | Many-to-single: GT targets merged in prediction |
| loc_s2m_err | Target | TBD | Single-to-many: one GT split into multiple preds |

## Matching Method Comparison

### PD/FA Across Matching Methods (same model, same dataset)
| Matching Method | PD ↑ | FA ↓ | Notes |
|----------------|------|------|-------|
| Basic centroid distance (d<3) | TBD | TBD | Original method, greedy matching |
| Shooting rule (box_1=1, box_2=4) | TBD | TBD | Box-based, different FA definition |
| Distance-only (d<3, via MatchingBased) | TBD | TBD | Centroid distance via Hungarian |
| OPDC (overlap=0.5, dist=3) | TBD | TBD | Overlap priority + distance compensation |

### Why Matching Method Matters
```
Basic: Simple greedy — first match wins. Can miss optimal assignments.
Shooting: Box-based — more forgiving for small positional errors. Different FA zones.
Distance-only: Hungarian optimal — globally optimal centroid matching.
OPDC: Two-phase — prefers IoU overlap, compensates with distance. Most robust.
```

## Cross-Task Metric Comparison (Wave 8 Defense)

| Task | Module | Primary Metric | Secondary Metrics | Eval Toolkit |
|------|--------|---------------|-------------------|-------------|
| IRSTD | DEF-dhif | hIoU | IoU, nIoU, PD, FA | **This module** |
| RGB-T SOD | DEF-hypsam | Sm | maxFm, maxEm, MAE | PySODMetrics |
| RGB-T Seg | DEF-tuni | mIoU | per-class IoU | torchmetrics |
| RGB-T Seg | DEF-cmssm | mIoU | per-class IoU | torchmetrics |
| RGB-T Count | DEF-rgbtcc | GAME0 | GAME1-3, MSE, Re | Custom eval_game() |

## Hardware & Methodology
- CPU evaluation (no GPU needed): any modern CPU
- NumPy 1.23+, scikit-image 0.14.1+, scipy 1.10+
- Threshold: 0.5 for binary metrics (standard IRSTD)
- Dynamic thresholds: 10 bins from 0 to 1
- Distance threshold: 3 pixels (standard IRSTD)
- Connected components: 8-connectivity (connectivity=2 in skimage)
- Results stored as JSON with full metadata

---
*Updated 2026-04-04 by ANIMA Research Agent*
