# Homework: quantifying transfection efficiency

**After the course.** Work in pairs. Submit Jupyter notebooks.

## The question

The project characterises a U2OS cell line engineered to express **GFP** in the
nucleus. Transfection is not fully efficient: some cells fail to express GFP, or
express it in the wrong compartment. The quantity of interest is what fraction of
them worked.

Three channels were acquired in the microscopy module, on the fluorescence
microscope you built:

| channel | stains | provides |
|---|---|---|
| **DAPI** (blue) | all nuclei | the position of every cell, transfected or not |
| **GFP** (green) | the transfected construct | which cells express it |
| **Cy3** (red) | actin | the extent of the whole cell |

The approach follows from this: segment the nuclei in DAPI, measure the GFP
intensity within each one, and determine how many are positive. The
**transfection efficiency** is the fraction of nuclei that are GFP-positive.

## The complication

The filter was changed by hand between channels, so the sample shifted slightly
each time. **The three channels do not overlap.** Until they are aligned, a
nucleus outline taken from DAPI does not correspond to the same pixels in GFP,
and the measured intensity mixes the nucleus with its surroundings.

Registration is therefore the first step: the task rehearsed in
[Fiji E2](fiji/e2_registration.md).

```{figure} illustrations/alignment.png
:width: 90%
:align: center

Three channels before and after alignment with `iaf.reg.multi_image_alignment()`.
```

## Your data

The pooled set of image triplets, approximately ten `{DAPI, GFP, Cy3}` sets, 
collected by the whole group during the microscopy course.

## Tasks

1. **Register** each `{DAPI, GFP, Cy3}` set so that the channels overlap. Use
   [`iaf.reg.multi_image_alignment()`](https://iaf.readthedocs.io/en/latest/generated/iaf.reg.html#iaf.reg.multi_image_alignment),
   which aligns any number of channels and can return before/after composites.

   Choose a template channel and give the reasoning for it: which channel
   provides the most reliable alignment, and why. Display the result of the
   registrations rather than assuming they succeeded.

2. **Assess whether the images need correcting before measurement.** A
   hand-built microscope rarely illuminates the field evenly, and a fluorescence
   image usually sits on a non-zero background. Both affect intensity
   measurements directly, and both were covered in
   [`02_image_processing`](../notebooks/02_image_processing.ipynb).

   Look at your images and decide:

   - Is the illumination uneven across the field? A useful check is to compare
     the mean intensity of the centre with the edges, or to blur an image
     heavily and see whether the result is flat.
   - Is there a background offset, and does it differ between images?
   - If either is present, which correction is appropriate? Uneven illumination
     is multiplicative and is corrected by division; an additive background is
     corrected by subtraction.

   Apply what you judge to be needed, and note what you decided and why. Note
   also that a correction changes the intensities you go on to measure, so the
   same correction should be applied to every image.

3. **Segment the nuclei** in each triplet and extract the **mean or median GFP
   intensity** within each one.

   State which channel is used for segmentation and which for measurement, and
   why. Section 3 of [`05_features`](../notebooks/05_features.ipynb) covers this
   pattern.

4. **Pool** the per-nucleus intensities from all sets into a single array.

5. **Separate positive from negative nuclei** and count the positives. The
   distribution will resemble the one below;
   [`iaf.stats.prepare_histogram()`](https://iaf.readthedocs.io/en/latest/generated/iaf.stats.html#iaf.stats.prepare_histogram)
   computes a histogram with an appropriate bin width.

   ```{figure} illustrations/populations.png
   :width: 400px
   :align: center

   GFP intensity per nucleus: two overlapping populations.
   ```

   Give the reasoning for the cut-off you choose, and report how the result
   changes if it is moved.

6. **Report the transfection efficiency**: positive nuclei divided by total
   nuclei.

## Points to consider

- **The two populations overlap**, so no cut-off classifies every cell
  correctly. The efficiency therefore carries an uncertainty that can be
  estimated.
- **Corrections applied in step 2 affect step 5.** If the illumination was
  uneven and left uncorrected, nuclei near the edge appear dimmer, and some
  positive ones may fall below the cut-off.
- **Nuclei within one image are not independent observations.** They share a
  preparation, a focus setting and an illumination: the point made in section 5
  of [`05_features`](../notebooks/05_features.ipynb).
- **The data was pooled across a group**, acquired on different self-built
  microscopes. Whether the between-set variation exceeds the within-set
  variation is worth checking.
- **Segmentation errors propagate.** A dim nucleus that is missed is more likely
  to be a negative one, which biases the efficiency upwards.

## Submission

Upload a **zip archive with your family names in the filename** to
[https://u.ethz.ch/ZiBOJ](https://u.ethz.ch/ZiBOJ), containing the Jupyter
notebook(s) with your code and results. The images do not need to be included.

**Deadline: the Sunday of the second week following the microscopy block.**
Resubmission may be requested for corrections or completion.
