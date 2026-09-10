# Spot the artifact

**~15 min.** Three images. Each has had exactly one thing done to it.

## Preparation

Open all four images in `data/misc/artifacts/`:

- `unmodified.tif`: the original, for reference
- `sample_a.tif`, `sample_b.tif`, `sample_c.tif`: one processing step each

## The task

For each of A, B and C, work out **what was done and how you can tell**.

Some things worth trying:

- Look at the histogram of each (Ctrl/Cmd+H) and compare with the original.
  A histogram often shows what your eye does not.
- Zoom in to 400% on a single nucleus in each.
- Line-profile across the same nucleus in all four (Ctrl/Cmd+K) and compare the
  shapes.
- Check `Image ▸ Type` and the min/max values.

Write down, for each: **what happened, which measurement it would ruin, and which
it would leave alone.**

```{admonition} Answers
:class: dropdown
**A: over-smoothed.** A Gaussian blur with a large sigma. The histogram is
narrower than the original (extreme values have been averaged away) and the line
profile across a nucleus has visibly gentler flanks. Object *counting* mostly
survives this; anything about size, shape or edges does not, and two nearby
nuclei can be merged into one by it.

**B: saturated.** The brightness was pushed up until the bright nuclei clipped.
The giveaway is a **spike at 255** in the histogram: many pixels stacked at the
maximum value, which does not happen naturally. Counting still works. Any
intensity measurement is now meaningless for the bright objects, because you
cannot tell "bright" from "brighter" once they all read 255. This one is
dangerous precisely because the image looks *better*.

**C: salt-and-pepper noise.** Isolated pure-black and pure-white pixels, as from
a failing detector. The clearest histogram signature is the **spike at 255**;
the black pixels are harder to spot there, because a third of this image is
already background at or near zero. Zooming in is more convincing than the
histogram: you will see single white dots on the background and single black
dots *inside* the nuclei, neither of which occurs naturally.

It wrecks thresholding, every white speck becomes an "object", but a median
filter removes it almost perfectly, as the Python notebooks show.
```

## Why this matters

The reason to be able to spot these is that **you will be handed images someone
else processed**, often without being told what they did. A saturated image and a
well-exposed one look similar on screen; only the histogram gives it away.

Adjusting the *display* of an image is fine and necessary. Adjusting the *data*
and then measuring it is not. The rule of thumb: keep the raw file, do your
processing in a script, and be able to say exactly what happened between the
microscope and the number in your paper.
