# Fiji practical

[Fiji](https://fiji.sc) is ImageJ bundled with plugins for bioimage analysis.
In this practical you will inspect image intensities, apply a threshold, clean
up a mask and measure objects through the graphical interface. The Python
notebooks introduce how to make these steps reproducible and automate them for many images.

## The exercises

| | | |
|---|---|---|
| [E1](e1_basics.md) | Fiji basics | intensities, channels, histogram, data types |
| [E2](e2_registration.md) | Registration | aligning channels that do not overlap |
| [E3](e3_segmentation.md) | Segmentation | filter, threshold, clean up, measure |
| [E4](e4_weka.md) | Machine learning | Trainable Weka Segmentation |
| [E5](e5_macros.md) | Macros *(optional)* | recording and batching |

Two shorter ones to try if you are ahead:
[how wide is a filament?](fun/how_wide_is_a_filament.md) and
[spot the artifact](fun/spot_the_artifact.md).

**Complete E4:** its exported files are used in the day 2 notebooks. E5 is
optional; it introduces Fiji macros for batch processing.

## The data

Everything is in the repository you cloned, under `data/`. The main set is
`data/bbbc020/`: mouse bone-marrow macrophages with two channels.

- `*_nuclei.tif`: DAPI, staining the nuclei
- `*_cells.tif`: CD11b, staining the cell surface

Open one image from each channel and compare them. **The nuclei are compact and
bright against the background. The cell signal is patchier, neighbouring cells
touch, and some edges are faint.** These differences affect which segmentation
methods work well.

```{note}
These images are uncalibrated: Fiji does not know how large a pixel is in
microns, so every measurement it reports will be in pixels. E1 asks you to check
this, and it matters more than it sounds.
```
