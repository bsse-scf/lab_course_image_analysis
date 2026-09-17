# E4: Segmentation using machine learning

**~50 min.** Train and apply a pixel classifier in Fiji.

```{important}
This exercise produces files that the day 2 notebooks read back
in. Do part 3 even if you are running short of time.
```

## Why

In [E3](e3_segmentation.md) the nuclei thresholded well and the cells did not.
The CD11b signal varies within cells and some cell edges are faint, so one
intensity threshold does not separate cells from background well. **Trainable
Weka Segmentation** uses image features such as texture and local edges. You
mark example pixels as cell or background, then train a classifier to label the
rest of the image.

## Part 1: train a classifier

1. Open `data/bbbc020/images/15min_3_cells.tif`.

2. Start `Plugins ▸ Segmentation ▸ Trainable Weka Segmentation`.

3. You get two classes. Rename them (**Settings**) to `cell` and `background`.

4. With the freehand or brush tool, draw a stroke *inside* a cell and click
   **Add to class 1**. Draw a stroke on empty background and **Add to class 2**.

5. Click **Train classifier**. After a moment you get an overlay of the result.

6. Now iterate, and be strategic about it. Do not add more examples of things it
   already gets right: **find a place where it is wrong and correct that**.
   Cell edges, the gaps between touching cells, and any dim cells are where the
   information is.

7. **How many strokes did it take before the result stopped obviously improving?**

```{tip}
Under **Settings** you can see the *features* it computes: Gaussian blur,
Hessian, membrane projections and so on, each at several scales. That list is the
set of questions it is allowed to ask about each pixel. Turning on more features
makes training slower and can make it overfit your handful of strokes.
```

8. Compare against the annotation in
   `data/bbbc020/gt/15min_3_cells_labels.tif`. **Is it better than your best
   threshold from E3? Where is it still wrong?**

9. Save your work: **Save classifier** as `my_classifier.model`.

## Part 2: apply a classifier you did not train

Save the trained classifier so you can apply it to other images.

10. Close the plugin and reopen it on a *different* image:
    `data/bbbc020/images/15min_1_cells.tif`.

11. Click **Load classifier** and choose
    `data/bbbc020/weka/bbbc020_cells.model`: a classifier trained in advance on
    a different field.

12. Click **Apply classifier** *without adding any training strokes of your own.*

13. **How well does someone else's classifier do on your image?** Then repeat on
    `15min_2_cells.tif` and `24h_2_cells.tif`.

14. **Does it do equally well on all three?** If not, what is different about the
    images where it struggles?

```{admonition} Applying a classifier to new images
:class: note
A saved classifier applies the same learned rule to each image. Its performance
may change if the illumination, staining or imaging settings change. Which of
these could differ between two acquisition days?
```

## Part 3: export for day 2

On day 2 these results are loaded into Python and compared against
a deep-learning method, so they need to be on disk.

For each of the three images `15min_1`, `15min_2` and `24h_2`:

15. With the classifier applied, click **Get probability** to produce the
    probability map.

16. Save it as
    `results/weka/<name>_cells_probability.tif`
    (create the `results/weka/` folder in the repository root).

17. Then click **Create result** to get the hard classification, and save it as
    `results/weka/<name>_cells_classified.tif`.

You should end up with six files.

```{note}
If you run out of time or something goes wrong, the day 2 notebook falls back to
a reference copy in `data/bbbc020/weka/`. Using your own exports lets you compare the classifier you trained with the
other methods on day 2.
```

## Think about it

18. You have now segmented the same channel three ways: a threshold (E3), a
    hand-tuned pipeline, and a trained classifier. **Which would you trust on a
    thousand images you have not looked at, and why?**

19. Weka learned from *your* strokes. **If a colleague trained it on the same
    image, would they get the same classifier?** Does that matter?
