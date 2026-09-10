# Detailed schedule

**This file is the single source of truth for what is taught, when, and in which
order.** [schedule.md](schedule.md) is the instructor's outline of intent; this
is the contract the material has to satisfy.

To change the course, change this file first, then bring the material into line
with it. `pixi run check-schedule` reports any disagreement and runs as part of
`pixi run test`, so the two cannot drift apart silently.

The book's part captions mirror the headings here: *Course information*,
*Image Analysis Basics with Fiji*, *Workflows in Python*, *Further information*.

The **Section** column must match the level-2 headings in the file it describes,
exactly and in order. `Recap` and `If you finish early` sections are structural
and are deliberately not listed.

---

## Day 0: preparation

Done at home, before the course. Covered by `book/setup/`.

| topic | why |
|---|---|
| Install Fiji | the day 1 Fiji practical needs it |
| Install pixi, clone the repo, `pixi install` | the whole Python track |
| Download the challenge dataset | the day 2 challenge; ~3.3 GB, do not leave to the day |
| Work through `00_python_basics` | so nobody spends the course fighting the language |

### `notebooks/00_python_basics.ipynb`

Covers only what the course notebooks actually use, in the order they are met.
Self-contained: it invents its own numbers, so it can be done before the data is
downloaded.

| Section | Introduces |
|---|---|
| 1. How a notebook works | cells, Shift+Enter, `print`, run order |
| 2. Variables | assignment, `int` / `float` / `str` / `bool`, `type()` |
| 3. Showing values: f-strings | `f"{x}"`, `:.2f`, `:.1%`, `:5d` |
| 4. Lists and tuples | indexing from zero, `[-1]`, slices, unpacking |
| 5. Dictionaries | key/value storage |
| 6. Doing something to everything: loops | `for`, indentation as syntax, `enumerate`, `zip` |
| 7. Making decisions | `if` / `elif` / `else`, `==` vs `=` |
| 8. Functions | `def`, `return`, docstrings, defaults, keyword arguments |
| 9. Using other people's code | `import x as y`, `from x import y` |
| 10. NumPy arrays | an image *is* an array; `shape` is (rows, columns); `zeros`, `arange`, `linspace` |
| 11. Indexing and slicing an array | one pixel, a row, a column, a crop |
| 12. Asking a question of every pixel at once | boolean masks, `.sum()`, `.mean()`, `image[mask]`, **`.copy()`** |
| 13. Summarising an array | `.min()`, `.max()`, `.mean()`, `.std()` |
| 14. Plotting | `plt.plot`, `imshow`, `subplots` + unpacking, `.ravel()` |
| 15. File paths | `pathlib`, the `/` operator |
| 16. Tables | `DataFrame`, a column, filtering, `groupby` |

### `notebooks/00_python_basics_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: variables and f-strings | formatted output |
| Task 2: lists | `len`/`min`/`max`/`sum`, slicing |
| Task 3: loops and decisions | loop with branching, counting |
| Task 4: zip | walking two lists together |
| Task 5: a function | `def` with a default argument |
| Task 6: build an array and describe it | array creation, `shape`, `dtype` |
| Task 7: indexing and cropping | pixel, row, column, rectangle |
| Task 8: masks | boolean masks, selection, `.copy()` |
| Task 9: three panels | `subplots`, `imshow`, `hist` |
| Task 10: a table | DataFrame, filtering, `groupby` |
| Task 11: put it together | applying a function across a column |

---

## Image Analysis Basics with Fiji

*Day 1, first session.*

Everything uses **`data/bbbc020/` field `2h_1`**, the same field the Python
notebooks use, so the two halves of the day are literally the same images.

### `book/fiji/e1_basics.md`

| Section | Introduces |
|---|---|
| Part 1: what is in this image? | image dimensions, bit depth, pixel values, histogram, `x,y` vs `[row, col]` |
| Part 2: how big is a pixel? | calibration, why uncalibrated measurements mislead |
| Part 3: two channels | channel merge, composite, LUTs, display vs data |
| Part 4: save something presentable | scale bar, export |

### `book/fiji/e2_registration.md`

| Section | Introduces |
|---|---|
| Why this is here | motivation: channels that do not overlap |
| Practical | SIFT alignment, Translation vs richer transforms |
| Think about it | why different stains are harder; choosing a reference channel |

### `book/fiji/e3_segmentation.md`

| Section | Introduces |
|---|---|
| Part 1: thresholding | manual threshold, auto-threshold methods, Otsu |
| Part 2: cleaning up | fill holes, binary open, erode/dilate |
| Part 3: measuring | Set Measurements, Analyze Particles, object counts |
| Part 4: measuring the *other* channel | **redirect**: masks from one channel, intensities from another |
| Part 5: the hard channel | where thresholding fails, and why |

Fiji deliberately stops at `Analyze Particles`, which separates objects
*implicitly*. Watershed, and the semantic/instance distinction that motivates it,
belong to the Python track: see `01` §7 and `02` §6.

### `book/fiji/e4_weka.md`

| Section | Introduces |
|---|---|
| Why | what a threshold cannot express |
| Part 1: train a classifier | Trainable Weka, classes, features, iterative correction |
| Part 2: apply a classifier you did not train | reuse, generalisation, distribution shift |
| Part 3: export for day 2 | probability map vs hard classification |
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
| The catch | the diffraction limit: the measurement returns the PSF, not the object |

### `book/fiji/fun/spot_the_artifact.md` *(short, optional)*

| Section | Introduces |
|---|---|
| The task | recognising over-smoothing, saturation and salt-and-pepper from a histogram |
| Why this matters | display vs data; what may and may not be adjusted before measuring |

---

## Workflows in Python: day 1

The same workflow as the Fiji practical, in code. Same field, `2h_1`.

### `notebooks/01_image_handling.ipynb`

| Section | Introduces |
|---|---|
| 1. An image is an array of numbers | `tifffile.imread`, `.shape`, `.dtype`, `(row, col)` ordering |
| 2. Looking at it | `imshow`, colormaps, display is not data |
| 3. Cropping is just indexing | slicing, 1D profiles |
| 4. Two channels | channel arrays, building an RGB composite |
| 5. The histogram | `plt.hist`, log scale, background peak vs object tail |
| 6. From intensity image to binary image: semantic segmentation | comparison operators, `threshold_otsu`; **semantic segmentation named**; the four kinds of image (intensity, binary, label, probability) |
| 7. From binary image to objects: connected component labeling | **instance segmentation named**; `label` as the first route from semantic to instance, and where it fails |
| 8. Viewing images interactively | `stackview`, `napari` |

### `notebooks/01_image_handling_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: load an image and describe it | imread, shape, dtype, range |
| Task 2: crop and display | computed centre crop |
| Task 3: the histogram | `.ravel()`, bins, log scale, choosing a threshold by eye |
| Task 4: threshold and count | `threshold_otsu`, `label` |
| Task 5: check it against the truth | comparing a count with an annotation |
| Task 6: build a composite | RGB channel assignment |

### `notebooks/02_image_processing.ipynb`

| Section | Introduces |
|---|---|
| 1. Why did we get 34 instead of 39? | inspecting the object size distribution before filtering |
| 2. Uneven illumination | background estimation by heavy blur, `white_tophat` |
| 3. Denoising: Gaussian vs median | which filter suits which noise |
| 4. Morphology: cleaning up a binary image | erosion, dilation, `opening`, `closing`, `binary_fill_holes` |
| 5. Putting it together | a full pipeline; `remove_small_objects`; steps that earn nothing |
| 6. Watershed: a second route from semantic to instance | distance transform; **raw peaks → distance threshold → smoothed distance**; seeding is the failure mode; when connected component labeling is not enough |

### `notebooks/02_image_processing_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: measure the vignetting | quantifying uneven illumination |
| Task 2: flatten the illumination | multiplicative correction by division; correction ≠ better segmentation |
| Task 3: which filter for which noise? | Gaussian vs median, chosen deliberately |
| Task 4: a full pipeline on the hard channel | assembling the steps; count vs quality |
| Task 5: split the merged cells with a watershed | all three seeding strategies; when watershed does not fit |

---

## Workflows in Python: day 2

Uses **`24h_2`** for the machine-learning walkthrough and **`15min_3`** wherever
a segmentation is scored, because `15min_3` has the most complete annotation.

### `notebooks/03_ml_segmentation.ipynb`

| Section | Introduces |
|---|---|
| 1. The Fiji classifier, in Python | reading Weka exports; probability vs classification; **checking which class is which** |
| 2. Semantic and instance segmentation | why a pixel classifier under-counts; watershed as the bridge |
| 3. Cellpose | a pretrained deep model that outputs instances |
| 4. The one parameter that matters | `diameter`, and how to sanity-check it |
| 5. Three methods, side by side | qualitative comparison only: **no scoring yet, by design** |
| 6. Does the hard channel need all this? | easy vs hard problems; reach for the simple thing first |

### `notebooks/03_ml_segmentation_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: load the classifier output and find the cell class | identifying the class without using ground truth |
| Task 2: semantic to instance | naming the failure |
| Task 3: split them with a watershed | re-applying day-1 tooling to a new mask |
| Task 4: Cellpose, and the diameter | running the model; parameter sensitivity |
| Task 5: put the three side by side | forming a judgement, and noticing you cannot yet justify it |

### `notebooks/04_segmentation_metrics.ipynb`

| Section | Introduces |
|---|---|
| 1. The two pixel scores | IoU / Jaccard, Dice, and how they differ |
| 2. Scoring the three methods | applying them; pixel score vs object count |
| 3. Matching objects instead of pixels | per-object matching, TP/FP/FN, precision, recall, F1 |
| 4. When the ground truth is wrong | annotation is not truth; border-cropping; unlabelled objects |
| 5. Choosing the matching threshold | the 0.5 convention; reporting it |

### `notebooks/04_segmentation_metrics_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: implement IoU and Dice | writing the metrics, tested on hand-checkable shapes |
| Task 2: build two segmentations to compare | assembling classical and deep pipelines |
| Task 3: score them on pixels | applying IoU and Dice |
| Task 4: score them on objects | implementing per-object matching |
| Task 5: how strict should the matching be? | threshold sweeps, reading the curves |

### `notebooks/05_features.ipynb`

| Section | Introduces |
|---|---|
| 1. From labels to a table | `regionprops_table`, one row per object |
| 2. Morphology features | area, perimeter, eccentricity, solidity, extent; dimensionless ratios travel |
| 3. Intensity features | `intensity_image`: measuring one channel through another's mask |
| 4. Measuring across a whole experiment | pooling fields; keeping `field` and `condition` columns |
| 5. Comparing conditions | grouped summaries, box plots, the unit of replication |
| 6. Which features actually distinguish anything? | effect size; the danger of picking a feature after seeing the result |

### `notebooks/05_detective_game_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: look before you measure | forming a hypothesis before measuring |
| Task 2: measure every worm in every well | pooling 24 wells; keeping `well` and `kind` |
| Task 3: can you classify a single worm? | scoring a single-threshold rule; individual objects overlap |
| Task 4: but you do not have to classify a single worm | aggregating per image averages the noise away |
| Task 5: score the well-level rule | the same features now separate perfectly |
| Task 6: do not believe your own 100% | **leave-one-out cross-validation**; accuracy on the data you tuned on is optimistic |

### `notebooks/06_curve_fitting.ipynb`

| Section | Introduces |
|---|---|
| 1. A measurement with a known answer | simulated data, so the fit can be checked against truth |
| 2. What does 'best fit' mean? | model, misfit measure, SSE |
| 3. Seeing the landscape | the SSE surface; why `p0` matters |
| 4. Doing it properly | `curve_fit`, covariance, parameter uncertainties |
| 5. From parameters to something meaningful | doubling time; propagating an uncertainty |
| 6. Is the model right? | **residuals**: structure means the wrong model |

### `notebooks/06_curve_fitting_ex.ipynb`

| Task | Practises |
|---|---|
| Task 1: why the usual threshold will not work | phase contrast defeats Otsu |
| Task 2: segment on deviation instead | thresholding \|image − background\| |
| Task 3: check the parameter is not doing the work | robustness of a result to an arbitrary cut-off |
| Task 4: fit the growth curve | segment → count → fit, end to end |
| Task 5: check the residuals | reading residual structure on real data |
| Task 6: the same model, fitted two ways | linear-space vs log-space fitting give different answers |
| Task 7: a model that fits | logistic vs exponential; more parameters always fit better |

---

## Independent work

### `book/challenge.md`

Day 2. Written; the starter notebook is not.

| Section | Covers |
|---|---|
| The experiment | the plate layout and the 10,240 cells/well expectation |
| Two properties of the data to account for | the snake scan pattern; field of view vs well area |
| Two ways to approach it | Track A from the ND2 images, Track B from the shipped summary CSV |
| Working through it | plate layout, dose-response plot, fit, IC50, reliability |
| Hints | dropdowns: reshaping, area scaling, model choice, checking the result |

No submission: this is worked through in the session.

### `book/homework.md`

After the course, on images the students acquire themselves. Written; the starter
notebook is not.

| Section | Covers |
|---|---|
| The question | transfection efficiency as a fraction of GFP-positive nuclei |
| The complication | channels do not overlap - registration is required first |
| Your data | the pooled triplets from the microscopy module |
| Tasks | register; **assess illumination and background correction**; segment; pool; threshold the intensity distribution; report |
| Points to consider | overlapping populations, effect of the corrections, replication unit, bias from missed dim nuclei |
| Submission | what to upload, and the deadline |

### Still to be written

| planned | covers |
|---|---|
| `notebooks/challenge_starter.ipynb` | snake-pattern reshape, FOV-to-well scaling, exponential fit, IC50 |
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
| kinds of image (intensity, binary, label, probability) | Python `01` §6 |
| morphological cleanup | Fiji E3 part 2; Python `02` §4 |
| connected component labeling / labeling | Python `01` §7: the first semantic→instance route |
| measuring a second channel through a binary image | Fiji E3 part 4 |
| ground truth as a reference | Python `01` §7 |
| uneven illumination, background subtraction | Python `02` §2 |
| denoising | Python `02` §3 |
| distance transform and watershed | Python `02` §6: the second semantic→instance route |
| seeding strategies | Python `02` §6 |
| semantic vs instance segmentation | Python `01` §6-7, revisited in `02` §6 and `03` §2 |
| pixel classification (Weka) | Fiji E4 |
| shallow vs deep learning | Python `03` §2 |
| Cellpose | Python `03` §3 |
| IoU, Dice | Python `04` §1: **deliberately not before** |
| per-object matching, precision/recall/F1 | Python `04` §3 |
| limitations of ground truth | Python `04` §4 |
