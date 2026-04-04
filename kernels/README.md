# Custom Kernels — DEF-pyirstdmetrics
# PyIRSTDMetrics: Standardized IRSTD Performance Analysis
# NOTE: This is a CPU-based evaluation toolkit — NO CUDA kernels needed
# Optimization targets are numpy/scipy algorithmic, not GPU kernel-level

## Architecture-Specific Optimization Targets

NOTE: PyIRSTDMetrics is a pure CPU evaluation toolkit (numpy + scipy + scikit-image).
There are NO CUDA kernels to build. Instead, optimization focuses on algorithmic
speedups in the metric computation pipeline. These optimizations are Python-level
but follow the same philosophy: eliminate redundant computation, fuse operations,
reduce memory allocations.

### Optimization 1: Shared Connected Component Pre-processing
**Bottleneck**: `measure.label()` and `measure.regionprops()` are called multiple times per image — once per metric class. For images with many small targets, regionprops extraction is expensive.
**Current**: Each metric class (PD/FA, OPDC, hIoU) independently calls label + regionprops
**Target**: Pre-compute once, share across all metric classes

```python
# Current (wasteful):
pd_fa.update(pred, mask)    # calls measure.label(mask), measure.regionprops(...)
opdc.update(pred, mask)     # calls measure.label(mask) AGAIN
hiou.update(pred, mask)     # calls measure.label(mask) AGAIN

# Optimized:
mask_label = measure.label(mask, connectivity=2)
mask_props = measure.regionprops(mask_label)
# Pass pre-computed props to all metrics
pd_fa.update(pred, mask, mask_label=mask_label, mask_props=mask_props)
opdc.update(pred, mask, mask_label=mask_label, mask_props=mask_props)
hiou.update(pred, mask, mask_label=mask_label, mask_props=mask_props)

# Savings: 2x reduction in label() calls per image
```

### Optimization 2: Vectorized Multi-Threshold Binary Evaluation
**Bottleneck**: `dynamically_binarizing()` in CMMetrics creates histogram-based TP/FP arrays. For many bins, the cumulative sum over flipped histograms is already efficient, but the per-threshold label + regionprops in target-wise metrics is not.
**Target**: Batch threshold processing for target-wise metrics

```python
# Current: loop over thresholds
for thr in thresholds:
    bin_prob = prob > thr
    label_map = measure.label(bin_prob)  # expensive per threshold
    props = measure.regionprops(label_map)

# Optimized: sort threshold values and process incrementally
# As threshold decreases, connected components only grow (never split)
# Use union-find structure to track component merges
```

### Optimization 3: Batched OPDC Matching
**Bottleneck**: `linear_sum_assignment` from scipy is O(N³) for N targets. For images with 50+ targets, this dominates.
**Target**: Use faster matching for sparse distance matrices

```python
# Current: full Hungarian assignment
row_ind, col_ind = optimize.linear_sum_assignment(paired_distance)

# Optimized: for sparse cases (most distances >> threshold),
# pre-filter to only valid candidates before Hungarian
valid_pairs = paired_distance < distance_threshold * 2  # rough filter
# Construct sub-problem with only valid pairs
# Run Hungarian on smaller matrix
```

### Optimization 4: Numba JIT for Inner Loops
**Bottleneck**: Python loops in `ShootingRuleBasedProbabilityDetectionAndFalseAlarmRate` iterate over all GT target coordinates.
**Target**: JIT-compile inner loops with numba

```python
# Current: Python loop over mask_tgt.coords
for h, w in mask_tgt.coords:
    h1, h2 = max(0, h - box_2_radius), min(H, h + box_2_radius + 1)
    w1, w2 = max(0, w - box_2_radius), min(W, w + box_2_radius + 1)
    invalid_mask_region[h1:h2, w1:w2] = False

# Optimized: use numpy vectorized operations
coords = np.array(mask_tgt.coords)  # (K, 2)
for dim, radius in [(0, box_2_radius)]:
    # Vectorized bounding box computation
    h_mins = np.maximum(0, coords[:, 0] - radius)
    h_maxs = np.minimum(H, coords[:, 0] + radius + 1)
    # Use numpy slicing instead of Python loop
```

## Performance Targets

| Operation | Current (50 targets, 512×512) | Target | Speedup |
|-----------|------------------------------|--------|---------|
| measure.label + regionprops | ~5ms × 3 calls = 15ms | ~5ms (shared) | 3x |
| OPDC matching (50 targets) | ~20ms | ~10ms (pre-filter) | 2x |
| Shooting rule PD/FA | ~30ms | ~10ms (vectorized) | 3x |
| Full analysis suite | ~80ms/image | ~30ms/image | 2.7x |

## Memory Analysis

| Operation | Current Memory | Optimized | Reduction |
|-----------|---------------|-----------|-----------|
| Label maps (per threshold × per metric) | 512×512×4B × 10 × 3 = 30MB | 512×512×4B × 10 = 10MB (shared) | 67% |
| Paired distance matrix (50 targets) | 50×50×8B = 20KB | Same | 0% |
| Dynamic threshold arrays | 10 bins × 4 arrays = minimal | Same | 0% |

## IP Notes

- **Shared pre-processing pattern** is applicable to ANY multi-metric evaluation pipeline — reduces redundant computation when multiple metric classes analyze the same data.
- **Incremental threshold processing** (union-find for growing components) is a novel approach for multi-threshold connected component analysis.
- **Pre-filtered Hungarian matching** reduces complexity for sparse matching problems.
- No CUDA kernels — all optimizations are algorithmic/Python-level.
- Store optimized evaluator at `/mnt/forge-data/shared_infra/eval/irstd/`.

---
*Updated 2026-04-04 by ANIMA Research Agent*
