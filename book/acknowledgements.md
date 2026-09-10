# Acknowledgements

## The course

This module is taught by the **Single Cell Facility** of D-BSSE, ETH Zurich, as
part of the Lab Course *Methods in Cell Analysis and Laboratory Automation*.

A large part of the material derives, with permission, from teaching developed
over many years by **Aaron Ponti**, and from earlier editions of this course
prepared with **Andreas Cuny**. The `iaf` library that the homework relies on is
their work.

## The data

All example images come from the
**[Broad Bioimage Benchmark Collection](https://bbbc.broadinstitute.org/)**, a
public collection of annotated image sets maintained for exactly this kind of
use. Having expert annotations to compare against is what makes day 2 possible.

The collection as a whole should be cited as:

> Ljosa V, Sokolnicki KL, Carpenter AE (2012). *Annotated high-throughput
> microscopy image sets for validation.* Nature Methods 9(7):637.

The individual sets used here, with the citations their pages ask for:

**[BBBC020](https://bbbc.broadinstitute.org/BBBC020)** — murine bone-marrow
derived macrophages, DAPI and CD11b. The guiding dataset for both days.

> "We used image set BBBC020 from the Broad Bioimage Benchmark Collection
> [Ljosa et al., Nature Methods, 2012]."

**[BBBC010](https://bbbc.broadinstitute.org/BBBC010)** — *C. elegans* live/dead
assay. Used for the detective game.

> "We used the *C. elegans* infection live/dead image set version 1 provided by
> Fred Ausubel and available from the Broad Bioimage Benchmark Collection
> [Ljosa et al., Nature Methods, 2012]."

**[BBBC030](https://bbbc.broadinstitute.org/BBBC030)** — Chinese hamster ovary
cells in DIC.

> "We used image set BBBC030v1 [Koos, K., Molnár, J., Kelemen, L., Tamás, G., &
> Horvath, P. (2016). *DIC image reconstruction using an energy minimization
> framework to visualize optical path length distribution.* Scientific Reports,
> 6.] from the Broad Bioimage Benchmark Collection."

Full provenance for every file — its source, the licence, and exactly what
processing was applied — is recorded in `data/MANIFEST.md`.

```{note}
The BBBC images are cropped and downscaled for teaching. If you use any of them
in your own work, go back to the originals: the versions here have been altered.
```

## The software

This course would not be possible without
[scikit-image](https://scikit-image.org/), [NumPy](https://numpy.org/),
[matplotlib](https://matplotlib.org/), [pandas](https://pandas.pydata.org/),
[SciPy](https://scipy.org/), [Fiji](https://fiji.sc/),
[Cellpose](https://www.cellpose.org/), [napari](https://napari.org/) and
[Jupyter](https://jupyter.org/) — all of it free, and most of it maintained by
people doing so alongside their actual jobs.

If you end up relying on one of these, cite it. It is the main currency the
people who maintain them have.
