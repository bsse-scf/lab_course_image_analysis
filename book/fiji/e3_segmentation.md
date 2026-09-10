# E3: Segmentation

**~50 min.** From an image to counted, measured objects.

## Preparation

Open `data/bbbc020/images/2h_1_nuclei.tif`.

Keep the original open and unmodified throughout — work on duplicates
(`Image ▸ Duplicate…`, Ctrl/Cmd+Shift+D). You will want to compare.

## Part 1 — thresholding

1. Open `Image ▸ Adjust ▸ Threshold…` (Ctrl/Cmd+Shift+T). Drag the sliders and
   watch the red overlay. **Find a setting by eye that captures the nuclei and
   little else. What value did you land on?**

2. Now press **Auto**, and try the dropdown of methods — *Default*, *Otsu*,
   *Li*, *Triangle*. **Do they agree with each other? Do they agree with you?**

3. Pick Otsu and press **Apply** to get a binary mask.

```{admonition} What just happened to your image
:class: warning
Applying a threshold *replaces* the intensities with 0 and 255. The original
values are gone. This is why you duplicated first.
```

## Part 2 — cleaning up

4. Look closely at the mask. **Can you see small specks that are not nuclei? Are
   there nuclei with holes in them?**

5. Fill the holes with `Process ▸ Binary ▸ Fill Holes`.

6. Remove the specks with `Process ▸ Binary ▸ Open`. **What does "open" do?** Try
   `Erode` on its own and then `Dilate` on its own to find out.

## Part 3 — separating what touches

7. Some nuclei are touching and have become a single blob. Run
   `Process ▸ Binary ▸ Watershed`. **Look at where it drew the dividing lines.
   Did it split anything it should not have?**

## Part 4 — measuring

8. Set up what you want measured: `Analyze ▸ Set Measurements…`. Tick **Area**,
   **Mean gray value**, **Min & max gray value** and **Shape descriptors**.

9. Run `Analyze ▸ Analyze Particles…` with *Size* `0-Infinity`, *Show* set to
   **Outlines**, and both *Display results* and *Summarize* ticked.

10. **How many nuclei did it find?**

11. The expert annotation for this field says **39**. Open
    `data/bbbc020/gt/2h_1_nuclei_labels.tif` to see them.
    **How close did you get? Where does your result disagree?**

## Part 5 — measuring the *other* channel

Here is the step that makes this a real workflow rather than an exercise.

You have masks of the nuclei, made from the DAPI channel. But the interesting
question is usually about a *different* channel — how much CD11b is there, in
each cell?

12. Re-run `Analyze ▸ Set Measurements…` and set **Redirect to:** to
    `2h_1_cells.tif` (it must be open).

13. Run `Analyze ▸ Analyze Particles…` again on your mask.

14. **The areas are the same as before, but the mean gray values have changed.
    Why?** Make sure you can explain this to your neighbour — "redirect" is the
    single most useful checkbox in this dialog, and it is the thing you will do
    in your homework to measure GFP inside DAPI-defined nuclei.

## Part 6 — the hard channel

15. Now try the whole pipeline again, from step 1, on
    `data/bbbc020/images/2h_1_cells.tif`. The annotation says **33** cells.

16. **How did it go?** Note that the object *count* may land near 33 — do not let
    that reassure you. Look at the outlines. Some honest questions:
    - Is there a threshold value that captures the cells without merging them?
    - Do the cells have edges that a threshold can find at all?
    - What would you have to know about the image to do better?

If that felt unsatisfying, good. That is what [E4](e4_weka.md) is for.
