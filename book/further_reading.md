# Further reading

Two days is not long. These are the places worth going next, chosen for being
genuinely useful rather than merely comprehensive.

## Learning more image analysis

- **[Introduction to Bioimage Analysis](https://bioimagebook.github.io/)** — Pete
  Bankhead. Free, online, and the best single thing to read after this course.
  It covers what we covered, more carefully, with the same insistence on
  understanding what a number means before reporting it.
- **[Bio-image Analysis Notebooks](https://haesleinhuepf.github.io/BioImageAnalysisNotebooks/)**
  — Robert Haase. A very large collection of worked Python notebooks. Good for
  "how do I do *X*", and the closest thing to a reference for the
  scikit-image-based approach used here.
- **[image.sc forum](https://forum.image.sc/)** — where to actually ask
  questions. The developers of Fiji, napari, CellProfiler, QuPath and
  scikit-image all read and answer there. Post the image and the code; you will
  usually get a better answer than you expected.

## Tools we did not have time for

- **[napari](https://napari.org)** — the viewer we used in passing. Worth
  learning properly if you work with 3D or time-lapse data.
- **[QuPath](https://qupath.github.io/)** — for whole-slide and histology images,
  where the images are far too large for the approach taken here.
- **[CellProfiler](https://cellprofiler.org/)** — pipeline-based analysis without
  writing code. A reasonable middle ground between Fiji and Python for batch
  work.
- **[Ilastik](https://www.ilastik.org/)** — interactive pixel classification, the
  same idea as Trainable Weka but considerably more capable.

## On doing it properly

- **[Points of Significance](https://www.nature.com/collections/qghhqm)** —
  *Nature Methods*' statistics column. Short, readable, and directly relevant:
  the columns on replication, error bars and *p*-values address the mistakes
  quantitative imaging makes most often.
- **Lee, Kitaoka (2018), *A beginner's guide to rigor and reproducibility in
  fluorescence imaging experiments*, Mol. Biol. Cell.** What to record, what to
  report, and what not to adjust.
- **Schmied *et al.* (2024), *Community-developed checklists for publishing
  images and image analyses*, Nature Methods.** A checklist to run through before
  submitting a figure.

## On the images themselves

If you want to understand where the pixel values come from — sampling, the point
spread function, why a filament measures 400 nm — the imaging half of this lab
course covers it, and Bankhead's book has a good chapter on it too.
