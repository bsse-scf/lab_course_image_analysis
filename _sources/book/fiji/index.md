# Fiji practical

[Fiji](https://fiji.sc) is ImageJ bundled with plugins for bioimage analysis.
In this practical you will inspect image intensities, apply a threshold, clean
up a mask and measure objects through the graphical interface. The Python
notebooks introduce how to make these steps reproducible and automate them for many images.

The [Fiji manual](fiji_manual.md) explains every tool the exercises use; keep
it open alongside them. Also, the Fiji cheatsheets can be useful (linked in the menu on the left).

## The exercises

| | | |
|---|---|---|
| [E1](e1_basics.md) | Fiji basics | pixel size, intensities, histogram, scale bar, measuring a filament |
| [E2](e2_segmentation.md) | Segmentation | filter, threshold, clean up, measure |
| [E3](e3_macros.md) | Macros | recording and batch processing |
| [E4](e4_weka.md) | Machine learning | Trainable Weka Segmentation |

## The data

Everything is in the repository you cloned, under `data/fiji/`. Each exercise
names the file it uses; E1 and E2 work on the same image.
