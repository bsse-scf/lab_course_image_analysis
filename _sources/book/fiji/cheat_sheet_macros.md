# Cheat sheet: Fiji macros

Only needed for the optional [E5](e5_macros.md).

## Finding the command you want

Open `Plugins ▸ Macros ▸ Record…` and perform a command in Fiji. The recorder
shows the corresponding macro line, including the command's options.

## The shape of a batch macro

```java
setBatchMode(true);              // don't draw windows - much faster
run("Close All");

dir  = getDirectory("Choose a folder");
list = getFileList(dir);
Array.sort(list);

for (i = 0; i < list.length; i++) {
    if (File.isDirectory(dir + list[i])) continue;
    if (!endsWith(toLowerCase(list[i]), ".tif")) continue;

    open(dir + list[i]);
    // ... processing ...
    close("*");
}

setBatchMode(false);
```

## Common lines

| | |
|---|---|
| Open | `open(path);` |
| Save | `saveAs("Tiff", path);` |
| Close all | `close("*");` |
| Blur | `run("Gaussian Blur...", "sigma=1");` |
| Auto-threshold | `setAutoThreshold("Otsu dark");` |
| Binarise | `run("Convert to Mask");` |
| Measurements | `run("Set Measurements...", "area mean redirect=None decimal=2");` |
| Count objects | `run("Analyze Particles...", "size=40-Infinity display summarize");` |
| Print to the Log | `print("text " + variable);` |
| Save a table | `Table.save(path, "Summary");` |

## Notes


**Sizes are in calibrated units.** `size=40-Infinity` means 40 *square microns*
if the image is calibrated and 40 *square pixels* if it is not. The same macro on
the same sample imaged at a different magnification silently filters differently.

**Save inside the loop.** A `saveAs` after the loop closes only sees the last
image, and if the last entry was skipped, whatever variable you used is stale.

## Limits

While Fiji has powerful tools to automate image analysis, it is not a programming language. We recommend using Python for more complex workflows, especially for plotting, working with tables or more complex analysis.
