# Detailed schedule

**This file is the single source of truth for what is taught, when, and in which
order.** [schedule.md](schedule.md) is the instructor's outline of intent; this
is the contract the material has to satisfy.

To change the course, change this file first, then bring the material into line
with it. `pixi run check-schedule` reports any disagreement and runs as part of
`pixi run test`, so the two cannot drift apart silently.

The **Section** column must match the level-2 headings in the file it describes,
exactly and in order. `Recap` and `If you finish early` sections are structural
and are deliberately not listed.

---

## Day 0 — preparation

Done at home, before the course. Covered by `book/setup/`.

| topic | why |
|---|---|
| Install Fiji | day 1 morning needs it |
| Install pixi, clone the repo, `pixi install` | the whole Python track |
| Download the challenge dataset | day 2 afternoon; ~3.3 GB, do not leave to the day |
| Python basics *(optional)* | for students who have never written any |

---

## Day 1, morning — Fiji

Everything uses **`data/bbbc020/` field `2h_1`**, the same field the afternoon
notebooks use, so the two halves of the day are literally the same images.

### `book/fiji/e1_basics.md`

| Section | Introduces |
|---|---|
| Part 1 — what is in this image? | image dimensions, bit depth, pixel values, histogram, `x,y` vs `[row, col]` |
| Part 2 — how big is a pixel? | calibration, why uncalibrated measurements mislead |
| Part 3 — two channels | channel merge, composite, LUTs, display vs data |
| Part 4 — save something presentable | scale bar, export |

### `book/fiji/e2_registration.md`

| Section | Introduces |
|---|---|
| Why this is here | motivation: channels that do not overlap |
| Practical | SIFT alignment, Translation vs richer transforms |
| Think about it | why different stains are harder; choosing a reference channel |

### `book/fiji/e3_segmentation.md`

| Section | Introduces |
|---|---|
| Part 1 — thresholding | manual threshold, auto-threshold methods, Otsu |
| Part 2 — cleaning up | fill holes, binary open, erode/dilate |
| Part 3 — separating what touches | watershed *(Fiji's one-click version)* |
| Part 4 — measuring | Set Measurements, Analyze Particles, object counts |
| Part 5 — measuring the *other* channel | **redirect** — masks from one channel, intensities from another |
| Part 6 — the hard channel | where thresholding fails, and why |

### `book/fiji/e4_weka.md`

| Section | Introduces |
|---|---|
| Why | what a threshold cannot express |
| Part 1 — train a classifier | Trainable Weka, classes, features, iterative correction |
| Part 2 — apply a classifier you did not train | reuse, generalisation, distribution shift |
| Part 3 — export for tomorrow | probability map vs hard classification |
| Think about it | reproducibility of a hand-trained model |

### `book/fiji/e5_macros.md` *(optional)*

| Section | Introduces |
|---|---|
| Why this is optional | when a macro is and is not the right tool |
| Practical | macro recorder, batch loop over a folder |
| Think about it | one recipe applied to two channels; Results vs Summary |

### `book/fiji/fun/how_wide_is_a_filament.md` *(short, optional)*

| Section | Introduces |
|---|---|
| The task | line profile, FWHM vs other width definitions, reproducibility |
| The catch | the diffraction limit — the measurement returns the PSF, not the object |

### `book/fiji/fun/spot_the_artifact.md` *(short, optional)*

| Section | Introduces |
|---|---|
| The task | recognising over-smoothing, saturation and salt-and-pepper from a histogram |
| Why this matters | display vs data; what may and may not be adjusted before measuring |

---

## Day 1, afternoon — Python

The same workflow as the morning, in code. Same field, `2h_1`.

### `notebooks/01_image_handling.ipynb`

| Section | Introduces |
|---|---|
| 1. An image is an array of numbers | `tifffile.imread`, `.shape`, `.dtype`, `(row, col)` ordering |
| 2. Looking at it | `imshow`, colormaps, display is not data |
| 3. Cropping is just indexing | slicing, 1D profiles |
| 4. Two channels | channel arrays, building an RGB composite |
| 5. The histogram | `plt.hist`, log scale, background peak vs object tail |
| 6. From image to mask | comparison operators, boolean masks, `threshold_otsu` |
| 7. From mask to objects | `label`, mask vs label image, comparing against ground truth |
| 8. Viewing images interactively | `stackview`, `napari` |

### `notebooks/01_image_handling_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1 — load an image and describe it | imread, shape, dtype, range |
| Task 2 — crop and display | computed centre crop |
| Task 3 — the histogram | `.ravel()`, bins, log scale, choosing a threshold by eye |
| Task 4 — threshold and count | `threshold_otsu`, `label` |
| Task 5 — check it against the truth | comparing a count with an annotation |
| Task 6 — build a composite | RGB channel assignment |

### `notebooks/02_image_processing.ipynb`

| Section | Introduces |
|---|---|
| 1. Why did we get 34 instead of 39? | inspecting the object size distribution before filtering |
| 2. Uneven illumination | background estimation by heavy blur, `white_tophat` |
| 3. Denoising: Gaussian vs median | which filter suits which noise |
| 4. Morphology: cleaning up a mask | erosion, dilation, `opening`, `closing`, `binary_fill_holes` |
| 5. Putting it together | a full pipeline; `remove_small_objects`; steps that earn nothing |
| 6. Watershed: separating objects that touch | distance transform; **raw peaks → distance threshold → smoothed distance**; seeding is the failure mode |
| 7. Semantic vs instance segmentation | the vocabulary, and why it matters downstream |

### `notebooks/02_image_processing_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1 — measure the vignetting | quantifying uneven illumination |
| Task 2 — flatten the illumination | multiplicative correction by division; correction ≠ better segmentation |
| Task 3 — which filter for which noise? | Gaussian vs median, chosen deliberately |
| Task 4 — a full pipeline on the hard channel | assembling the steps; count vs quality |
| Task 5 — split the merged cells with a watershed | all three seeding strategies; when watershed does not fit |

---

## Day 2, morning — machine learning, metrics, features

Uses **`24h_2`** for the machine-learning walkthrough and **`15min_3`** wherever
a segmentation is scored, because `15min_3` has the most complete annotation.

### `notebooks/03_ml_segmentation.ipynb`

| Section | Introduces |
|---|---|
| 1. Yesterday's classifier, in Python | reading Weka exports; probability vs classification; **checking which class is which** |
| 2. Semantic and instance segmentation | why a pixel classifier under-counts; watershed as the bridge |
| 3. Cellpose | a pretrained deep model that outputs instances |
| 4. The one parameter that matters | `diameter`, and how to sanity-check it |
| 5. Three methods, side by side | qualitative comparison only — **no scoring yet, by design** |
| 6. Does the hard channel need all this? | easy vs hard problems; reach for the simple thing first |

### `notebooks/03_ml_segmentation_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1 — load the classifier output and find the cell class | identifying the class without using ground truth |
| Task 2 — semantic to instance | naming the failure |
| Task 3 — split them with a watershed | re-applying day-1 tooling to a new mask |
| Task 4 — Cellpose, and the diameter | running the model; parameter sensitivity |
| Task 5 — put the three side by side | forming a judgement, and noticing you cannot yet justify it |

### `notebooks/04_segmentation_metrics.ipynb`

| Section | Introduces |
|---|---|
| 1. The two pixel scores | IoU / Jaccard, Dice, and how they differ |
| 2. Scoring yesterday's three methods | applying them; pixel score vs object count |
| 3. Matching objects instead of pixels | per-object matching, TP/FP/FN, precision, recall, F1 |
| 4. When the ground truth is wrong | annotation is not truth; border-cropping; unlabelled objects |
| 5. Choosing the matching threshold | the 0.5 convention; reporting it |

### `notebooks/04_segmentation_metrics_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1 — implement IoU and Dice | writing the metrics, tested on hand-checkable shapes |
| Task 2 — build two segmentations to compare | assembling classical and deep pipelines |
| Task 3 — score them on pixels | applying IoU and Dice |
| Task 4 — score them on objects | implementing per-object matching |
| Task 5 — how strict should the matching be? | threshold sweeps, reading the curves |

### Still to be written

| planned | covers |
|---|---|
| `notebooks/05_features.ipynb` | `regionprops_table`, intensity vs morphology features, pandas |
| `notebooks/05_detective_game_ex.ipynb` | separating worms from cells on morphology alone |
| `notebooks/06_curve_fitting.ipynb` | SSE, `curve_fit`, exponential models |
| `notebooks/06_curve_fitting_ex.ipynb` | growth curve on the phase-contrast timelapse |

---

## Day 2, afternoon — the challenge

| planned | covers |
|---|---|
| `book/challenge.md` | the dose-response task; Track A (full ND2) and Track B (summary CSV) |
| `notebooks/challenge_starter.ipynb` | snake-pattern plate reshape, FOV-to-well area scaling, exponential fit, IC50 |

## Homework

| planned | covers |
|---|---|
| `book/homework.md` | transfection efficiency |
| `notebooks/homework_starter.ipynb` | `iaf.reg.multi_image_alignment`, nuclei segmentation, `iaf.stats.prepare_histogram` |

---

## Where each concept first appears

Useful when moving material: if you move the first appearance, everything below
it that relies on it has to move too.

| concept | first introduced |
|---|---|
| pixel, bit depth, data type | Fiji E1 part 1 |
| calibration | Fiji E1 part 2 |
| channels, composites, LUTs | Fiji E1 part 3 |
| display vs data | Fiji E1 part 3 |
| registration | Fiji E2 |
| histogram | Fiji E1 part 1; Python `01` §5 |
| thresholding, Otsu | Fiji E3 part 1; Python `01` §6 |
| morphological cleanup | Fiji E3 part 2; Python `02` §4 |
| connected components / labelling | Fiji E3 part 4; Python `01` §7 |
| measuring a second channel through a mask | Fiji E3 part 5 |
| ground truth as a reference | Python `01` §7 |
| uneven illumination, background subtraction | Python `02` §2 |
| denoising | Python `02` §3 |
| distance transform and watershed | Fiji E3 part 3 (one click); Python `02` §6 (mechanism) |
| seeding strategies | Python `02` §6 |
| semantic vs instance segmentation | Python `02` §7, named again in `03` §2 |
| pixel classification (Weka) | Fiji E4 |
| shallow vs deep learning | Python `03` §2 |
| Cellpose | Python `03` §3 |
| IoU, Dice | Python `04` §1 — **deliberately not before** |
| per-object matching, precision/recall/F1 | Python `04` §3 |
| limitations of ground truth | Python `04` §4 |
