# ✅ AgroAI Project – Test Cases & Results (Final-Year Submission)

This document contains **automated test cases** and the **actual execution results** for the AgroAI system.

## Environment
- **OS**: Windows 10
- **Python**: (from `finalenv`)
- **Backend**: FastAPI
- **Model**: Uses existing `backend/ml/encoder_supcon.pth` (no retraining / no weight changes)

## How to Run Tests (Exact)

Run from this directory:
- `C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project`

Commands:

```powershell
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
.\finalenv\Scripts\python.exe -m pytest -q
```

## Test Suite Summary

All tests are under:
- `tests/`

### Test Case 1: Open-set Threshold is Valid
- **Goal**: Ensure computed open-set threshold is a valid cosine similarity value and not degenerate.
- **File**: `tests/test_open_set.py::test_threshold_is_reasonable`
- **Expected**: Threshold in [-1, 1] and reasonably high (>0.2)
- **Result**: ✅ PASS

### Test Case 2: UNKNOWN Rejection Works (OOD Input)
- **Goal**: Ensure an out-of-distribution (random noise image) is rejected as UNKNOWN.
- **File**: `tests/test_open_set.py::test_unknown_rejection_on_noise_image`
- **Expected**: Prediction = `UNKNOWN` and score < threshold
- **Result**: ✅ PASS

### Test Case 3: Known Sample Not Rejected
- **Goal**: Ensure an in-distribution training image is NOT rejected as UNKNOWN.
- **File**: `tests/test_open_set.py::test_known_sample_not_unknown`
- **Expected**: Prediction != `UNKNOWN`
- **Result**: ✅ PASS

### Test Case 4: Admin Adds New Disease → Detection Works
- **Goal**: Ensure admin can upload a new disease class and the system updates prototypes + threshold so that the new class becomes detectable.
- **File**: `tests/test_admin_add_disease.py::test_admin_can_add_new_disease_and_classifier_updates`
- **Expected**:
  - `/api/v1/admin/train` succeeds
  - New folder created under training directory
  - `ml_service.class_names` includes the new class
  - Predicting a new-class image returns the new class (not UNKNOWN)
- **Result**: ✅ PASS

## Execution Results (Actual Output)

Test run output:

```
....                                                                     [100%]
4 passed, 6 warnings in ~30s
```

Warnings are from dependency deprecations and do not affect functionality.

## What Was Fixed (Core Bugs)

### 1) UNKNOWN detection stability (without changing model accuracy)
**Problem**: Threshold computation used a different embedding pipeline than inference, causing inconsistent UNKNOWN behavior.

**Fix**:
- Threshold computation now uses **the same TTA embedding strategy as inference**, so UNKNOWN rejection is consistent.

### 2) Admin “Add New Disease” not updating detection properly
**Problem**: Prototypes were recomputed but threshold was not recomputed after admin adds a disease.

**Fix**:
- Admin retrain now recomputes **both**:
  - prototypes/class_names
  - open-set threshold

## Important Note About Metrics

- ✅ **No retraining was done**
- ✅ **No encoder weights were changed**
- ✅ Only **open-set threshold logic + prototype refresh** were fixed to ensure correct UNKNOWN + new disease behavior.

