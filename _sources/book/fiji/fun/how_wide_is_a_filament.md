# How wide is a filament?

**~15 min.** Measure a filament profile and consider the resolution limit.

## Preparation

Open `data/misc/microtubules.tif`: microtubules in a cultured cell, labelled
with a fluorescent antibody against tubulin. The image is calibrated: check
`Image ▸ Properties` (Ctrl/Cmd+Shift+P) for the pixel size.

The left half of the image has isolated filaments on a dark background. Use
those. On the right they overlap, which makes a clean profile hard to get.

## The task

1. Select the **straight line** tool and draw a line *across* one filament,
   perpendicular to it. Keep it short.

2. Press Ctrl/Cmd+K (`Analyze ▸ Plot Profile`). You get a plot of intensity along
   your line, with a peak where it crossed the filament.

3. **How wide is that peak?** Click **List** in the plot window to see the
   numbers. Because the image is calibrated, the distance column is in nm.

A width depends on where you place the boundaries of the peak.

4. Try each of these and write down the number you get:
   - the width at the very bottom of the peak, where it meets the background
   - the width at **half** the peak's height above background: this is the
     *full width at half maximum*, or FWHM, and it is what people usually quote
   - the width at 10% of the peak height

5. **How much do they differ?** Which would you put in a paper?

6. Measure the same filament again with a slightly different line: a bit more
   angled, or a bit further along. Then measure a *different* filament. **How
   reproducible is your answer?** Do all the filaments have the same width?

## The catch

7. Draw a line across the *background*: no filament. **Is the profile flat?**
   Whatever wobble you see there is the noise floor, and it sets a limit on how
   precisely any of the above can be measured.

8. Finally, consider the resolution limit. Your FWHM is probably around 400 nm.
   **A microtubule is 25 nm across.** So what did you actually measure?

```{admonition} What you measured
:class: dropdown
The **point spread function** of the microscope, near enough. Anything smaller
than roughly half the wavelength of light, about 200-250 nm for visible light,
is imaged as a blur of that size regardless of how small it really is.

A single microtubule is more than ten times finer than that. What you measured
was the optics, not the filament. That is also why every filament in the image
has the same width: they are all far below the resolution limit, so they all
show the same blur.

When the measured width is close to the resolution limit, it mainly reflects
the microscope's response rather than the filament's physical width. State that
limit when reporting the measurement.
```
