# Schedule

Two days, in *Room BSS E 21*, 9:00–17:30 with a break from 12:30 to 14:00.

## Before the course

Everything in [Setup](setup/index.md), and the
[Python primer](../notebooks/00_python_basics.ipynb). The primer needs no data,
so it can be done anywhere; the environment install cannot, so do not leave it
to the morning.

## Day 1: Image analysis basics

| | |
|---|---|
| morning | Lecture, then [Fiji](fiji/index.md): intensities, channels, thresholding, cleaning up a binary image, measuring objects, and pixel classification with Weka |
| afternoon | The same analysis in Python: [image handling](../notebooks/01_image_handling.ipynb) and [image processing](../notebooks/02_image_processing.ipynb) |

The afternoon deliberately repeats the morning on the same images. Fiji is faster
to start; Python is what you reach for when there are four hundred images, or
when you need to say exactly what you did six months later.

## Day 2: Workflows and analysis

| | |
|---|---|
| morning | [Machine learning for segmentation](../notebooks/03_ml_segmentation.ipynb), [measuring how good a segmentation is](../notebooks/04_segmentation_metrics.ipynb), [features](../notebooks/05_features.ipynb) and [curve fitting](../notebooks/06_curve_fitting.ipynb) |
| afternoon | The challenge: a drug dose-response screen, start to finish |

## After the course

The homework, using images you acquire yourself on the microscope you build in
the microscopy module.

## How the material is written

Each topic has a **walkthrough** to work through together, and an **exercise**
to do yourself. The exercises have laddered hints: take the first one before
the second.

Several of them end with a result that is *wrong*, deliberately: a count that
does not match the annotation, a metric that flatters a useless segmentation, a
model that fits well and means little. Those are the parts worth slowing down
for.
