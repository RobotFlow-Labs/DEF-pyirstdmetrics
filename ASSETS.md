# DEF-pyirstdmetrics - Asset Manifest

## Paper
- Title: Rethinking Evaluation of Infrared Small Target Detection
- ArXiv: 2509.16888v2
- URL: https://arxiv.org/abs/2509.16888
- Authors: Youwei Pang, Xiaoqi Zhao, Lihe Zhang, Huchuan Lu, Georges El Fakhri, Xiaofeng Liu, Shijian Lu

## Status
- Module status: READY (scaffold + integration work)
- Training status: NOT APPLICABLE (evaluation toolkit module)
- Source of truth:
  - Paper PDF: `papers/2509.16888.pdf`
  - Reference code: `repositories/PyIRSTDMetrics/`

## Runtime Dependencies
| Asset | Type | Source | Local Path | Status |
|---|---|---|---|---|
| pyirstdmetrics | Python package | PyPI / source repo | runtime dependency | REQUIRED |
| numpy | Python package | PyPI | runtime dependency | REQUIRED |
| scipy | Python package | PyPI | runtime dependency | REQUIRED |
| scikit-image | Python package | PyPI | runtime dependency | REQUIRED |

## Datasets (from paper)
| Dataset | Usage in paper | Expected role in this module | Status |
|---|---|---|---|
| IRSTD1k | benchmark | external evaluation input | OPTIONAL_EXTERNAL |
| SIRST | benchmark | external evaluation input | OPTIONAL_EXTERNAL |
| NUDT | benchmark | external evaluation input | OPTIONAL_EXTERNAL |

## Local Test Data
| Asset | Path | Size | Status |
|---|---|---|---|
| Sample pred/mask PNGs | `repositories/PyIRSTDMetrics/examples/test_data/` | 4 files | DONE |

## Hyperparameters / Protocol Values (paper-aligned)
| Parameter | Value | Paper Reference |
|---|---|---|
| Optimizer | Adam | Sec. 5.1 Implementation Details |
| Initial LR | 0.0005 | Sec. 5.1 Implementation Details |
| LR schedule | Multi-step decay | Sec. 5.1 Implementation Details |
| Epochs | 400 | Sec. 5.1 Implementation Details |
| Batch size | 16 | Sec. 5.1 Implementation Details |
| Input resolution | 256 x 256 | Sec. 5.1 Implementation Details |
| Augmentations | flip, crop, blur | Sec. 5.1 Implementation Details |
| Default prediction threshold | 0.5 | Sec. 3.2 |
| Distance threshold | 3 pixels | Sec. 4.1 |
| OPDC overlap threshold | 0.5 | Sec. 4.1 |

## Metrics Scope
| Level | Metrics |
|---|---|
| Pixel-level | IoU, nIoU, F1, Precision, Recall, TPR, FPR |
| Target-level | Pd, Fa (distance-only, shooting-rule, OPDC matching) |
| Hybrid-level | hIoU with hierarchical error decomposition |

## Acceptance Targets
| Target | Value | Source |
|---|---|---|
| Reference toolkit unit checks | match `examples/test_metrics.py` expected values | reference repo |
| DNANet hIoU (illustrative paper benchmark) | ~0.557 on IRSTD1k test | Table 1 / Sec. 5.2 |

## Notes
- This module does not train a detector; it standardizes evaluation for detector modules.
- Cross-module integration inputs are prediction/mask pairs from other DEF modules (for example DEF-dhif).
