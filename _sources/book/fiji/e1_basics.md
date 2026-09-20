# E1: Fiji basics

## Preparation

1. Open `data/fiji/segmentation/1894_G3_5.tif` in Fiji.

## Getting started with Fiji

1. Use Fiji to answer the following questions about the image:

    1. What is the pixel size (the physical size of a pixel in the image) of the image in microns? Hint: Check the image properties (under "Image" -> "Properties...").
    2. What is the mean intensity of the image? Hint: Use "Analyze" -> "Measure" after selecting the whole image with "Ctrl+A" (or "Cmd+A" on Mac). You can also select a region of interest with the rectangle tool and measure only that part of the image.
    3. What's the intensity of the least and most bright pixel in the image? Hint: Use "Analyze" -> "Histogram" to see the intensity distribution.
    4. What is the intensity of the pixel at position (100, 150)? Hint: Hover over the pixel with the mouse to see its coordinates and intensity in the status bar at the bottom of the window.
    5. What's a good brightness/contrast setting for this image? Hint: Use "Image" -> "Adjust" -> "Brightness/Contrast..." to open the brightness/contrast adjustment window. You can use the "Auto" button to automatically adjust the brightness/contrast. You can also manually adjust the minimum and maximum intensity values to change the contrast.
    6. What is the width and height of the image in physical units? Hint: Use the pixel size and the number of pixels in each dimension (shown in the title bar of the image window) to calculate the physical size.

1. Working with multichannel images:

    1. Explore different Color Modes in Fiji. Hint: Use "Image" -> "Color" -> "Color Mode" to switch between different color modes (e.g., RGB, Grayscale, Composite). How does it affect the appearance of the image?
    1. Split the image into its individual channels. Hint: Use "Image" -> "Color" -> "Split Channels".
    1. Merge the channels back into a single image ("Image" -> "Color" -> "Merge Channels..."). Make sure that the resulting Composite image is displayed in the same color mode as the original image. If that's already the case, try to play with the LUTs of the individual channels to see how it affects the appearance of the Composite image.

1. Save a representation of the Composite image for a publication:
    1. Adjust the brightness/contrast of the image to a good setting (for each channel).
    2. Add a scale bar to the image. Hint: Use "Analyze" -> "Tools" -> "Scale Bar..." to add a scale bar.
    3. Save the modified image as a PNG file. Make sure that the scale bar is visible in the saved image.

## How wide is the filament?

1. Open `data/misc/microtubules.tif` (microtubules labelled with a fluorescent antibody against tubulin). What is the pixel size of this image?

1. Measure the width of a filament:
    1. Select the straight line tool and draw a short line across one isolated filament (use the left half of the image), perpendicular to it.
    1. Plot the intensity profile along the line. Hint: Use "Analyze" -> "Plot Profile" (Ctrl/Cmd+K). Are the distances shown in pixels or physical units?
    1. Suppose you want to determine the width of the filaments in the image. How would you do that methodically? Hint: One option is to consider the full width at half maximum (FWHM) of the intensity profile.
    1. Repeat the measurement on different filaments / parts of the image. Do you get the same width?

1. A microtubule is about 25 nm in diameter. How does this compare to the width you measured?
