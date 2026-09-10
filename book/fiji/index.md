# Fiji practical

[Fiji](https://fiji.sc) is ImageJ with a large collection of plugins already
installed. It is the most widely used tool in bioimage analysis, and for good
reason: you can open an image and have a measurement thirty seconds later,
without writing anything.

This practical is a complete analysis done by clicking: open images, look at
their intensities, threshold them, separate touching objects and measure the
result. The Python notebooks then repeat the *same* analysis, and the comparison
is the point. Fiji is faster to start; Python is what you reach for
when you have four hundred images instead of four, or when you need to be able
to say exactly what you did six months later.

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

**E4 produces files that are used again on day 2**, so do not skip it. E5 is
genuinely optional: macros are useful, but batch processing is the thing Python
does better, and that is where we are heading.

## The data

Everything is in the repository you cloned, under `data/`. The main set is
`data/bbbc020/`: mouse bone-marrow macrophages with two channels.

- `*_nuclei.tif`: DAPI, staining the nuclei
- `*_cells.tif`: CD11b, staining the cell surface

Open one of each now and look at them side by side. You will spend two days on
these images, and most of what happens will make sense if you remember one thing
about them: **the nuclei are compact and clearly brighter than the background;
the cells are patchy, they touch each other, and their edges fade out.**

```{note}
These images are uncalibrated: Fiji does not know how large a pixel is in
microns, so every measurement it reports will be in pixels. E1 asks you to check
this, and it matters more than it sounds.
```
