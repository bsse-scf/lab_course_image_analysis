# E2: Registration

**~25 min.** Making channels line up.

## Why this is here

Your homework will use images you acquire yourselves on a microscope you built
yourselves. On that setup you change the filter by hand between channels, and the
sample moves a little every time. So the DAPI, GFP and Cy3 images of the *same
cells* will not overlap, and if they do not overlap, you cannot ask "how bright
is the GFP inside this nucleus?", because the nucleus is not where the binary image says
it is.

Fixing that is called **registration**: finding the transform that brings one
image onto another.

This exercise is a rehearsal with a known answer.

## Preparation

Open all three images in `data/fiji/registration/`:

- `channel1_reference.tif`
- `channel2.tif`
- `channel3.tif`

These are three views of the same field, processed to look like different
channels: one dimmer and blurrier, one brighter and noisier. **Two of them have
been deliberately shifted.** Your job is to put them back.

## Practical

1. Merge the three channels into a composite
   (`Image ▸ Color ▸ Merge Channels…`, tick *Create composite*).
   **Can you see the misalignment?** Zoom in on a single nucleus: you should see
   it appear three times in three colours, slightly apart.

2. Estimate the shift by hand first. Pick one clearly isolated nucleus, hover
   over its centre in each channel, and note the `x,y` from the status bar.
   **Roughly how far apart are they, in pixels and in which direction?**

3. Now let Fiji do it. Convert the composite to a stack
   (`Image ▸ Hyperstacks ▸ Hyperstack to Stack`) and run
   `Plugins ▸ Registration ▸ Linear Stack Alignment with SIFT`.
   Leave the defaults, but set *Transformation* to **Translation**: we know the
   sample only shifted, it did not rotate or scale, and allowing a transform more
   flexible than the physics permits is a good way to get a confidently wrong
   answer.

4. **Did it work?** Merge the aligned stack back into a composite and look at the
   same nucleus.

5. Compare with your hand estimate from step 2. **Do they agree?**

```{admonition} The answer key
:class: dropdown
`channel2` was shifted by **-11 rows, +7 columns**, and `channel3` by
**+6 rows, -13 columns**. In Fiji's `x,y` convention that is
`(+7, -11)` and `(-13, +6)`.

If SIFT found something close to these, it worked. If it found something wildly
different, look at whether it was allowed to rotate and scale.
```

## Think about it

6. SIFT works by finding distinctive little patches in each image and matching
   them up. **What would happen if you gave it two channels that stain completely
   different structures**: say, nuclei in one and the cytoskeleton in the other?

7. In your homework you will have exactly that problem: DAPI marks nuclei, Cy3
   marks actin, and they genuinely do not look alike. **Which of your three
   channels would you use as the reference, and why?**

   *There is no single right answer, but there is a good argument to be made.
   Hold onto it: the homework asks you this directly.*

```{note}
In Python you will use `iaf.reg.multi_image_alignment()`, which does the same job
for any number of channels and can show you before/after composites. Same idea,
one line.
```
