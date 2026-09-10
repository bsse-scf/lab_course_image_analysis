# E1: Fiji basics

**~40 min.** Getting comfortable with what an image *is* before doing anything
clever with it.

## Preparation

Open `data/bbbc020/images/2h_1_nuclei.tif` and
`data/bbbc020/images/2h_1_cells.tif` in Fiji
(`File ▸ Open…`, or drag the file onto the Fiji toolbar).

## Part 1 — what is in this image?

Answer each of these using Fiji. The answer matters less than knowing where to
look.

1. **What are the dimensions of the image, in pixels?**
   *Hint: the title bar of the image window shows them, along with the data type.*

2. **What data type is it, and what range of values can a pixel hold?**
   *Hint: `Image ▸ Type` shows a tick beside the current type.*

3. **What are the darkest and brightest pixel values actually present?**
   *Hint: `Analyze ▸ Histogram` (Ctrl/Cmd+H) reports min, max and mean.*

4. **What is the value of the pixel at x=25, y=336? And at x=472, y=190?**
   *Hint: hover the mouse over the image and read the status bar in the main Fiji
   window. Note Fiji reports `x,y` — column first — which is the opposite order
   from the `(row, column)` you will use in Python this afternoon.*

5. One of those two pixels is inside a nucleus and one is background.
   **Which is which, and by how much do they differ?**

6. **What is the mean intensity of the whole image?** Select everything with
   Ctrl/Cmd+A, then `Analyze ▸ Measure` (Ctrl/Cmd+M).

7. Now draw a small rectangle inside a single nucleus and measure again.
   **How does the mean compare?** This is the difference a threshold has to find.

## Part 2 — how big is a pixel?

8. Open `Image ▸ Properties…` (Ctrl/Cmd+Shift+P). **What does Fiji think the
   pixel width and height are, and in what unit?**

You should find `1 pixel × 1 pixel` — the file carries no calibration, so Fiji
has no idea what physical size these pixels represent.

9. **Why is that dangerous?** Consider: you measure a nucleus and Fiji reports an
   area of 300. Three hundred *what*? And what happens if a colleague repeats
   your analysis on images from a different objective?

```{warning}
An uncalibrated image will still give you numbers. They just will not mean what
you think they mean. This is not hypothetical — the macro used for the day-2
challenge filters objects by `size=0-409` in **calibrated** units, and quietly
does something completely different if the calibration is missing or wrong.
```

10. Set the calibration yourself: in `Image ▸ Properties…`, set the pixel width
    and height to `0.5` and the unit to `micron`. Measure a nucleus again.
    **What changed, and what did not?**

    *(0.5 µm is invented for this exercise — these images were downscaled from
    the originals, so the true value no longer applies. That is itself worth
    noticing: resizing an image invalidates its calibration.)*

## Part 3 — two channels

11. With both channels open, run `Image ▸ Color ▸ Merge Channels…`. Put the
    nuclei in **blue** (C3) and the cells in **green** (C2), and tick *Create
    composite*. **Do the two channels line up?**

12. In the composite, use `Image ▸ Color ▸ Channels Tool…` to turn each channel
    on and off. **Does every nucleus sit inside a stained cell? Does every cell
    have a nucleus?**

13. Adjust `Image ▸ Adjust ▸ Brightness/Contrast…` (Ctrl/Cmd+Shift+C) and press
    **Auto**. **Did the pixel values change?**

    *Hint: check the histogram before and after. This is the single most common
    misunderstanding in image analysis.*

## Part 4 — save something presentable

14. Adjust the contrast of the composite so both channels are visible.
15. Add a scale bar with `Analyze ▸ Tools ▸ Scale Bar…`. (You will need the
    calibration you set in step 10 for this to show microns.)
16. Save as PNG with `File ▸ Save As ▸ PNG…`, with the scale bar visible.

```{admonition} Check yourself
:class: tip
Before moving on, make sure you can answer: what is the difference between
changing the **brightness/contrast** and changing the **pixel values**? If a
figure in a paper has had its contrast adjusted, has the data been altered?
```
