# Impostor Detection (Mouse Dynamics)

This repository implements a feature-extraction and Siamese-model workflow for impostor detection using mouse movement session features (1-minute and 3-minute sessions). The primary interactive analysis and pipeline are contained in `notebooks/notebook1.ipynb`.

This README summarizes the notebook, explains key parameters and how to run training/evaluation, and lists reproducibility and performance notes.

---

## Project Overview

- Goal: Build a model to detect impostor sessions (same-user vs different-user) using session-level mouse features.
- Approach: extract session features from raw CSV session files, build pairwise datasets (cross-pairs between 1min/3min feature tables), train a Siamese network on paired numeric features, and evaluate using ROC, confusion matrix, and per-class metrics (precision/recall/F1).
- Notebooks: `notebooks/notebook1.ipynb` is the main pipeline (data reading, feature extraction, pair building, training, plotting, evaluation).

---

## Repo layout (relevant)

- `data/` - contains `raw/` session CSVs and `processed/` feature CSVs (versioned files e.g. `sapimouse_1min_features_v4.csv`).
- `notebooks/notebook1.ipynb` - primary notebook. Cells have been refactored into smaller focused cells (helpers, feature extraction, pairing, model steps) so you can run sections independently.
- `src/` - (optional) place for helper modules if you choose to extract common functions (not created automatically).

---

## Notebook 1: high-level cell map

The notebook is split into sequential, focused cells. Run top-to-bottom for a full pipeline or run specific cells interactively:

1. Setup & Imports
	- common imports: numpy, pandas, sklearn, tensorflow, mlflow, etc.

2. Utilities & Feature Extraction (split into helpers):
	- `read_session_csv(path, user_id_from_folder)` — robust CSV reader handling variations, returns DataFrame with columns [client, timestamp, button, state, x, y].
	- `_safe_series_stats(arr)` and `_shannon_entropy(arr, bins=8)` — numeric/statistics helpers used within feature extraction.
	- `extract_features(df, user_id)` — core per-session feature extractor; returns a dict of features including temporal, spatial, angular, pause/hover statistics, entropy features, and more. If a session has < 4 events returns an invalid flag.

3. Build feature tables:
	- `build_feature_table(session_list, label)` — loops session files, calls `read_session_csv` and `extract_features`, constructs feature DataFrame.
	- File-collection cell builds `df_1min` and `df_3min` using the processed files or raw session files.

4. Standardization & Saving (split):
	- `NUMERIC_COLS` detection (all columns except `user_id` and `session_file`).
	- `save_versioned_csv(df, basename)` helper to write processed features with a version suffix.
	- Standardization cell applies `StandardScaler` to numeric columns and writes versioned CSVs.

5. Train / Validation / Test split (split):
	- Constants for validation/test ranges (e.g. `VAL_USER_START = 91`, `VAL_USER_END = 104`, `TEST_USER_START = 105`, `TEST_USER_END = 120`).
	- `normalize_user(u)` helper to obtain numeric user ids from strings like `user101`.
	- `split_train_val_test_by_user_ranges(df, val_start, val_end, test_start, test_end)` — constructs `df_train`, `df_val`, `df_test` ensuring no overlap.
	- `load_latest_processed(prefix)` loads latest processed CSV if in-memory tables are missing.
	- Final cell runs the split, prints shapes and user checks, and exposes `df1_train`, `df1_val`, `df1_test`, `df3_train`, `df3_val`, `df3_test`.

6. Pair building (split and refactored):
	- `_normalize_user_id`, `_index_usernums` helpers.
	- `build_all_pairs(df1, df3, ..., neg_sample_ratio=1.0, random_state=None)` — builds exhaustive cross pairs (df1 x df3), labels positives (same user) as 1 and negatives otherwise. Important options:
	  - `neg_sample_ratio` (float 0..1): fraction of negative CROSS pairs to keep. Example: `0.5` keeps ~50% of negatives (sampled reproducibly if `random_state` provided). Positives are always kept.
	  - `include_within`, `include_df1_df1`, `include_df3_df3` to add within-dataset pairs.
	  - `max_total_pairs` to cap the final returned pairs deterministically.
	- The notebook demonstrates building `X1_train, X2_train, y_train` (training pairs), `X1_val, X2_val, y_val` (validation pairs), and `X1_test, X2_test, y_test` (test pairs). Example training call uses `neg_sample_ratio=0.5`, while validation/test use `1.0`.

7. EDA & Numeric conversion:
	- `eda_siamese_inputs(X1, X2, y)` — a helper that prints types, null counts, and basic descriptive stats to validate pair frames.
	- Numeric pair frames: drop `['user_id', 'session_file']` to create `X1_train_numeric`, `X2_train_numeric`, etc., for model input.

8. Model architecture (split):
	- Encoder factory `create_encoder(input_dim, embedding_dim=64)` — small dense network with L2-normalized embeddings.
	- Siamese assembly: inputs, shared encoder, merge via absolute difference, dense head and sigmoid output.

9. Compilation (split):
	- Class weights computed by `sklearn.utils.class_weight` from `y_train` (balanced weights used in `model.fit`).
	- `siamese_model.compile(...)` uses Adam optimizer and metrics: AUC, Precision, Recall.

10. Callbacks & Training (split):
	 - `EarlyStopping` and `ReduceLROnPlateau` callbacks configured.
	 - `MinorityClassMetrics` custom callback added: at each epoch it runs predictions on the full train and val sets and records precision/recall/F1 for the minority class (label=1). This is useful to track minority performance across epochs. Note: this callback runs predictions every epoch (increases runtime).
	 - `siamese_model.fit(...)` uses `[early_stop, reduce_lr, minority_cb]`.

11. Plotting & Evaluation:
	 - Training plotting cell plots Loss, AUC, Precision, Recall, and F1 across epochs. Precision and F1 were separated into distinct subplots for clarity; there is an additional subplot that visualizes minority-class precision and F1 recorded by `minority_cb`.
	 - Evaluation cells compute predictions on `X1_test_numeric`, `X2_test_numeric`, then print confusion matrix, classification report, and ROC curve.

---

## Key parameters and where to change them

- Validation / test user ranges:
  - Edit `VAL_USER_START`, `VAL_USER_END`, `TEST_USER_START`, `TEST_USER_END` in the train/val/test split cell.
  - Make sure those ranges don't overlap and correspond to user ids in your dataset.

- Negative sampling (class imbalance mitigation):
  - `neg_sample_ratio` in `build_all_pairs(...)` controls fraction of negative cross-pairs retained for training. Example: `neg_sample_ratio=0.5` to keep ~50% of negatives.
  - Use `random_state` in `build_all_pairs` to make negative sampling reproducible.

- Minority-class callback and threshold:
  - `MinorityClassMetrics` uses a 0.5 threshold by default for converting probabilities to labels. Change the threshold in the callback code if a different operating point is desired.
  - The callback computes metrics each epoch and appends them to `minority_cb.history`.

- Model hyperparameters: encoder sizes, embedding dim, head layer sizes, optimizer learning rate, batch size, and epochs are all defined in the model/training cells — adjust as needed.

---

## How to run (recommended)

1. (Optional) Create a fresh virtualenv and install dependencies, for example:

```powershell
# Windows PowerShell example
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you don't have a requirements file, install the essentials:

```powershell
pip install pandas numpy scikit-learn tensorflow matplotlib mlflow tqdm
```

2. Open `notebooks/notebook1.ipynb` in Jupyter or VS Code Notebook.
3. Run cells sequentially (or run in logical blocks):
	- Setup & imports
	- Utilities (read_session_csv, stats helpers, extract_features)
	- Build feature tables (or load processed CSVs in `data/processed`)
	- Standardize & save (creates versioned CSVs in `data/processed`)
	- Train/val/test split
	- Build pairs (training/validation/test pairs)
	- Numeric conversion
	- Model encoder and assembly
	- Compile model
	- Callbacks (instantiate) and Train (.fit)
	- Plotting and Evaluation (last cells)

4. Inspect outputs: training history, `minority_cb.history` for minority metrics, ROC, confusion matrix.

---

## Reproducibility & tips

- Use `random_state` when calling `build_all_pairs(..., random_state=42)` for reproducible negative sampling across runs.
- If training is slow due to the minority callback predicting on the whole train/val per epoch, reduce frequency (evaluate every N epochs) or evaluate on a held-out small subset.
- If pairwise dataset size explodes (O(nA * nB)), consider:
  - Using `neg_sample_ratio` < 1.0 to subsample negatives
  - Setting a `max_total_pairs` cap
  - Sampling representatives per user (stratified by user) rather than exhaustive cross-product
- Save intermediate processed CSVs (the notebook already uses versioned CSVs under `data/processed`) so you don't recompute feature extraction every time.

---

## Notes about the refactor performed

- Several crowded cells were split into focused cells (helpers separated from main functions) to improve readability and make it easier to run pieces independently. Functionality and variable names were preserved.
- The following logical splits were made (you can still run notebook top-to-bottom):
  - `read_session_csv`, stats helpers, and `extract_features` split into separate cells
  - `build_feature_table` and the file-collection/build cell split
  - Pair-building helpers and `build_all_pairs` split
  - Standardization & saving split into NUMERIC_COLS, save helper, and the standardization action
  - Train/Val/Test splits split into constants/normalize, helper functions/loaders, and execution/asserts
  - Model encoder and model assembly split, as was compilation and class-weight calculation
  - Callbacks were moved to a separate cell and the `.fit()` call is now its own cell

No logic was removed — only cell boundaries were adjusted for clarity.

---

## Troubleshooting

- If you see errors due to missing variables, ensure you ran the notebook cells above the failing cell (helpers must be executed before functions that depend on them).
- If `df_1min` or `df_3min` are missing, run the build feature table cells or load the latest processed CSV in `data/processed`.
- If memory errors occur during `build_all_pairs`, reduce `neg_sample_ratio` or set `max_total_pairs`.

---

## Contact / Next steps

If you'd like I can:
- Extract repeated helpers into `src/notebook_helpers.py` and import them from the notebook.
- Add a small `requirements.txt` capturing package versions used for development/testing.
- Add a lightweight unit test that validates `build_all_pairs` sampling semantics on a toy dataset.

---

Thank you — if you'd like any section of the README expanded (design decisions, metrics interpretation, or a short experiment log), tell me which section and I'll update it.