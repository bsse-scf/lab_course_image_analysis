# Cheat sheet: Fiji basics

Keyboard shortcuts use Ctrl on Windows/Linux and Cmd on macOS.

## Opening and looking

| | |
|---|---|
| Open a file | `File ▸ Open…` (Ctrl+O), or drag onto the toolbar |
| Duplicate before you edit | `Image ▸ Duplicate…` (Ctrl+Shift+D) |
| Image type and bit depth | `Image ▸ Type` |
| Pixel size / calibration | `Image ▸ Properties…` (Ctrl+Shift+P) |
| Zoom in / out | `+` / `-`; scroll to pan |
| Pixel value under cursor | read the Fiji status bar |
| Brightness/contrast | `Image ▸ Adjust ▸ Brightness/Contrast…` (Ctrl+Shift+C) |
| Histogram | `Analyze ▸ Histogram` (Ctrl+H) |
| Line profile | straight-line tool, then Ctrl+K |

```{warning}
Brightness/contrast changes **how the image is displayed**, not the pixel values.
Applying a threshold, a filter or `Convert to Mask` changes the **data**. Always
duplicate first.
```

## Channels

| | |
|---|---|
| Combine channels | `Image ▸ Color ▸ Merge Channels…` |
| Split a composite | `Image ▸ Color ▸ Split Channels` |
| Show/hide channels | `Image ▸ Color ▸ Channels Tool…` (Ctrl+Shift+Z) |
| Change the colour (LUT) | `Image ▸ Lookup Tables ▸ …` |

## Segmentation

| | |
|---|---|
| Blur | `Process ▸ Filters ▸ Gaussian Blur…` |
| Median (salt & pepper) | `Process ▸ Filters ▸ Median…` |
| Subtract background | `Process ▸ Subtract Background…` |
| Threshold | `Image ▸ Adjust ▸ Threshold…` (Ctrl+Shift+T) |
| Fill holes | `Process ▸ Binary ▸ Fill Holes` |
| Remove specks | `Process ▸ Binary ▸ Open` |

## Measuring

| | |
|---|---|
| Choose what to measure | `Analyze ▸ Set Measurements…` |
| Measure the selection | `Analyze ▸ Measure` (Ctrl+M) |
| Count and measure objects | `Analyze ▸ Analyze Particles…` |
| Manage regions of interest | `Analyze ▸ Tools ▸ ROI Manager…` (T to add) |
| Scale bar | `Analyze ▸ Tools ▸ Scale Bar…` |

`Analyze Particles…` counts **connected** runs of foreground pixels, so two
objects that touch are counted once. Separating them is a Python topic in this
course: see `02_image_processing`.

**Redirect to:** in `Set Measurements…` uses regions selected in one image to
measure intensities in another image.

**Summarize** in `Analyze Particles…` puts per-image counts in the **Summary**
window. **Results** contains per-object measurements; check which table you
need before saving.

## Getting unstuck

- `Edit ▸ Undo` (Ctrl+Z) undoes exactly one step, and not every step.
  Re-duplicating from the original is usually faster.
- `Plugins ▸ Macros ▸ Record…` shows the command for whatever you just clicked: 
  the quickest way to find out what something is called.
- The Fiji search bar (press `L`) finds any command by name.
