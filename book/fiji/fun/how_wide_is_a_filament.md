# How wide is a filament?

**~15 min.** A small exercise with a surprisingly deep answer.

## Preparation

Open `data/misc/actin.tif`: actin filaments, 200×200 pixels.

It will look almost black when it opens: half the pixels have a value of 1 or
less, and only about 5% are bright. Press Ctrl/Cmd+Shift+C and click **Auto** to
see anything. That is a display change only: the values you measure are
unaffected.

## The task

1. Select the **straight line** tool and draw a line *across* one filament,
   perpendicular to it. Keep it short.

2. Press Ctrl/Cmd+K (`Analyze ▸ Plot Profile`). You get a plot of intensity along
   your line, with a peak where it crossed the filament.

3. **How wide is that peak?** Click **List** in the plot window to see the
   numbers.

Now the real question: **what do you mean by "wide"?**

4. Try each of these and write down the number you get:
   - the width at the very bottom of the peak, where it meets the background
   - the width at **half** the peak's height above background: this is the
     *full width at half maximum*, or FWHM, and it is what people usually quote
   - the width at 10% of the peak height

5. **How much do they differ?** Which would you put in a paper?

6. Measure the same filament again with a slightly different line: a bit more
   angled, or a bit further along. **How reproducible is your answer?**

## The catch

7. Draw a line across the *background*: no filament. **Is the profile flat?**
   Whatever wobble you see there is the noise floor, and it sets a limit on how
   precisely any of the above can be measured.

8. Finally, the uncomfortable one. This image is uncalibrated, so your answer is
   in pixels. Suppose a pixel is 100 nm, and your filament measures 4 pixels
   FWHM: 400 nm. **An actin filament is about 7 nm across.** So what did you
   actually measure?

```{admonition} What you measured
:class: dropdown
The **point spread function** of the microscope, near enough. Anything smaller
than roughly half the wavelength of light, about 200-250 nm for visible light, 
is imaged as a blur of that size regardless of how small it really is.

A single actin filament is fifty times finer than that. What you measured was the
optics, not the filament.

This is why "how wide is it?" is a question you should be suspicious of whenever
the answer comes out near the resolution limit. Counting filaments, comparing
intensities, measuring things much larger than the PSF: all fine. Measuring the
width of something you cannot resolve: not fine.
```
