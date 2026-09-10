# E5: Macros *(optional)*

**~25 min.** Skip this if you are short of time: the Python notebooks cover the same
ground more thoroughly.

## Why this is optional

Fiji can record what you click and replay it. That is genuinely useful for
repeating a fixed pipeline over a folder. But the macro language is peculiar to
ImageJ, the tooling is thin, and once you want to plot the results or do anything
conditional you will wish you were somewhere else.

That somewhere else is the Python notebooks. Treat this as a look at what the recorder
can do, not as a language to learn.

## Practical

1. Open `Plugins ▸ Macros ▸ Record…`.

2. With the recorder open, do the E3 pipeline by hand on
   `data/bbbc020/images/Kontrolle1_nuclei.tif`: duplicate, Gaussian blur
   (`Process ▸ Filters ▸ Gaussian Blur…`, sigma 1), Otsu threshold, Convert to
   Mask, Fill Holes, Analyze Particles with *Summarize* ticked.

3. **Look at what the recorder captured.** Every click is a line.

4. Press **Create** to open it in the script editor, and run it on a fresh copy
   of the image to check it still works.

5. Now make it work on a folder. `macros/count_objects.ijm` in the repository
   does this: open it and compare it with what you recorded. The processing is
   the same; what is wrapped around it is a loop over `getFileList()`.

6. Run it on `data/bbbc020/images/`. **How many images did it process, and how
   long did it take you compared with doing it by hand?**

## Think about it

7. The macro processes every file in the folder. `data/bbbc020/images/` contains
   both `_nuclei` and `_cells` images. **Did it treat them the same? Should it
   have?**

8. **What would you have to change to save a plot of the results?** This is the
   point where a macro stops being the right tool.
