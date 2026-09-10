# Challenge: a drug dose-response curve

**Day 2, afternoon.** Work in pairs.

This exercise applies the whole course to one experiment: images in, a
biological quantity out.

## The experiment

A compound appears to inhibit cell division, and is being considered as a
treatment against metastasis. A constant number of cells was seeded into
consecutive wells of a plate and left to grow for 48 hours.

Without any drug, each well is expected to reach **10,240 cells** after 48 hours.
The well area is 0.32 cm².

Increasing concentrations of the compound were applied at the start. The plate
has four rows **A**–**D**, which are four replicates, and ten columns, one per
concentration:

| C [µg/µl] | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| **B** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| **C** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| **D** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

The goal is to **measure the dose-response curve** and determine the **IC50**,
the concentration at which proliferation is inhibited by half.

## Two properties of the data to account for

Both of these affect the result, and neither is visible in the images
themselves.

```{note}
**The microscope scanned in a snake pattern.** Odd rows were scanned left to
right, even rows right to left. The 40 images are stored in acquisition order,
so reshaping them directly into a 4×10 grid places every second row in reverse.

**The field of view does not cover the whole well.** The counts come from a
fraction of each well, while the 10,240 figure refers to the whole well. Relating
the two requires the field-of-view area and the well area.
```

## Two ways to approach it

The dataset is large. Both routes lead to a dose-response curve.

### Track A — starting from the images

Segment the cells in each of the 40 fields, export the counts, and analyse them.
Either tool works:

- a **Fiji macro** — there is a starting point among the hints below;
- a **Jupyter notebook**, using the methods from day 1. In Python,
  `iaf.io.readers.NikonND2Reader` opens an ND2 file series by series.

The data is `plate01.nd2`; see [Download the example data](setup/download_data.md).

### Track B — starting from the counts

If the download is unavailable, the per-field counts are already in the
repository:

```
data/challenge/plate01_summary.csv
```

This is the result of running a segmentation over all 40 fields: one row per
field, in acquisition order, with a `Count` column. The analysis after
segmentation can be done entirely from it.

Both properties described above still apply on this track, as does the fitting.

## Working through it

A complete analysis involves:

1. **the counts per well**, from either track;
2. **the plate arranged correctly** — 4 replicates × 10 concentrations, with the
   snake pattern accounted for;
3. **a dose-response plot** — cells per well against concentration, showing the
   replicates rather than only their average;
4. **a fitted curve** and the **IC50** derived from it;
5. **an assessment of how reliable that number is.**

## Hints

::::{dropdown} A Fiji macro starting point
An ND2 file holds all 40 fields as separate **series**. Bio-Formats opens one
series at a time, so the macro is a loop over series numbers with the processing
inside it.

```java
// Set this to your own copy of the file.
path = "/path/to/plate01.nd2";

nSeries = 40;
run("Set Measurements...", "area mean redirect=None decimal=3");

setBatchMode(true);
run("Close All");
run("Clear Results");

for (i = 1; i <= nSeries; i++) {

    run("Bio-Formats Importer",
        "open=[" + path + "] autoscale color_mode=Default" +
        " view=Hyperstack stack_order=XYCZT series_" + i);

    // The i-th series is now open.
    // --> your processing and Analyze Particles call go here.

    run("Close All");
    print("series " + i + " of " + nSeries);
}

setBatchMode(false);
```

Two details that matter:

- **Series are numbered from 1**, so `series_1` is the first field, not
  `series_0`.
- **`Analyze Particles...` with `summarize` writes to the Summary window**, not
  to Results. Save that one — `Table.save(outputPath, "Summary")` — or the file
  will contain one row per object rather than one row per field.
::::

::::{dropdown} Arranging 40 rows into a 4×10 plate
The rows are in acquisition order. Reshape to `(4, 10)`, then reverse every
second row — `array[1::2] = array[1::2, ::-1]`.

A check before continuing: column 0 is the untreated control, so those four wells
should hold the highest counts on the plate. If they do not, the arrangement is
not yet correct.
::::

::::{dropdown} Relating the counts to 10,240
The count comes from one field of view; the 10,240 refers to the whole well.
Scaling by the area ratio relates them:

$$\text{cells per well} = \text{counted} \times \frac{\text{well area}}{\text{field area}}$$

The well area is 0.32 cm². The field area follows from the image dimensions and
the pixel size in the file metadata — the calibration point from
[Fiji E1](fiji/e1_basics.md). An error here scales every number by a constant
factor.
::::

::::{dropdown} Choosing a model
Growth inhibition that increases with dose can be described by exponential decay:

$$N(c) = N_0 e^{-kc}$$

giving $\text{IC50} = \ln(2)/k$, in the same way the doubling time was obtained
in [`06_curve_fitting`](../notebooks/06_curve_fitting.ipynb).

The four-parameter logistic used conventionally in pharmacology is also an
option. Either way, the residuals are worth checking.
::::

::::{dropdown} Checking the result
Several things are worth verifying:

- whether the four replicates at each concentration agree, and if one row differs
  systematically, what its images look like;
- whether the untreated control matches the expected 10,240;
- whether the residuals show structure;
- how much the IC50 changes if the segmentation threshold is varied.

The last of these is often the largest contribution to the uncertainty.
::::
