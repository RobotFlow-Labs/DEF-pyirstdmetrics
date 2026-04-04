# NEXT_STEPS — DEF-pyirstdmetrics
## Last Updated: 2026-04-04
## Status: ENRICHED — Ready for build
## MVP Readiness: 0%
## Total PRDs: 8 (32 hours estimated)
## Critical Path: PRD-001 → PRD-002 → PRD-003 → PRD-004 → PRD-005

---

### Immediate Next Actions
1. Install: `uv pip install pyirstdmetrics` (or clone + editable install)
2. Verify: `python examples/test_metrics.py -v` — all tests must pass
3. Build ANIMA evaluation harness wrapping PyIRSTDMetrics
4. Integrate with DEF-dhif evaluation pipeline
5. Build cross-module evaluation dashboard for Shenzhen demo

### What This Module Does
**PyIRSTDMetrics** is a standardized evaluation toolkit for Infrared Small Target Detection (NeurIPS 2025). It provides three levels of metrics: (1) **Pixel-level** — IoU, nIoU, F1, Precision, Recall, TPR, FPR via confusion matrix with dynamic/binary thresholding; (2) **Target-level** — Probability of Detection (PD) and False Alarm Rate (FA) via 3 matching methods (basic centroid, shooting-rule, OPDC); (3) **Hybrid-level** — hIoU (Hierarchical IoU) = seg_IoU × loc_IoU with detailed error decomposition into 7 categories (seg_mrg, seg_itf, seg_pcp, loc_itf, loc_pcp, loc_m2s, loc_s2m). Pure CPU toolkit (numpy + scipy + scikit-image), no GPU needed.

### Key Contribution: hIoU (Hierarchical IoU)
The paper's main innovation is hIoU = seg_IoU × loc_IoU:
- **seg_IoU**: How well are detected targets segmented at pixel level?
- **loc_IoU**: How many targets are correctly detected at target level?
- **hIoU**: Single number capturing both quality dimensions
- **Error decomposition**: Tells you exactly WHERE the model fails (interference, perception, merge, split)

### TODO (by PRD)
- [ ] **PRD-001**: Installation + verification (2h)
- [ ] **PRD-002**: ANIMA evaluation harness (5h)
- [ ] **PRD-003**: DEF-dhif integration (4h)
- [ ] **PRD-004**: Cross-module evaluation dashboard (5h)
- [ ] **PRD-005**: Metric computation optimization (4h)
- [ ] **PRD-006**: CI/CD benchmark tracking (3h)
- [ ] **PRD-007**: Multi-dataset evaluation standardization (4h)
- [ ] **PRD-008**: Extended metric integration — SOD + Seg + Counting (5h)

### Blockers
- **None for installation** — PyPI package available (`pip install pyirstdmetrics`)
- **DEF-dhif dependency**: Integration (PRD-003) requires DEF-dhif to have trained models. Can build harness in parallel.
- **Dashboard design**: Need to decide on presentation format for Shenzhen demo

### Datasets/Models Needed
- No datasets needed directly — this is an evaluation toolkit
- Test data included in repo: `examples/test_data/` (pred+mask PNG pairs)
- Will consume predictions from other modules (DEF-dhif, etc.)
- Total: ~1MB (toolkit + test data only)

### Integration Targets
1. **DEF-dhif** — Primary: evaluate DNANet + Standard/DHiF/FDConv across NUAA-SIRST, IRSTD-1K, NUDT-SIRST-Sea
2. **Future IRSTD modules** — Any new IRSTD detection module uses this for standardized evaluation
3. **Cross-task comparison** — Unified evaluation dashboard across IRSTD, SOD, Segmentation, Counting

### Related Modules
- **DEF-dhif** — IRSTD detection, primary evaluation target
- **DEF-hypsam** — RGB-T SOD, uses PySODMetrics (sibling project by same author)
- **DEF-saap** — SAR anomaly detection, different sensor but similar small-target paradigm
- **DEF-tuni/cmssm/rtfdnet** — RGB-T segmentation, different metrics (mIoU)
- **DEF-rgbtcc** — RGB-T crowd counting, different metrics (GAME)

### Note on Module Uniqueness
This is the only **evaluation toolkit** module in Wave 8 (and all of ANIMA). It doesn't detect anything itself — it measures how well other modules detect. Think of it as the "calibration standard" for all IRSTD evaluation. The hIoU metric from NeurIPS 2025 provides a single, interpretable number that captures both detection quality AND segmentation quality. The error decomposition is particularly valuable for defense: it tells procurement officers exactly what kind of errors a system makes (missing targets vs false alarms vs poor segmentation).

---
*Updated 2026-04-04 by ANIMA Research Agent*
