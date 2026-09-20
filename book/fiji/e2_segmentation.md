# E2: Image segmentation workflow

## Preparation
1. Open the same file as in E1 in Fiji.

## Questions
1. Segment the nuclei by thresholding the image. Is there a clear separation between foreground and background?
1. Use an automatic method to find a threshold. Which one works best?
1. Try to improve the segmentation result by applying a filter before thresholding. Can you find a filter that works well?
1. From the binary mask of the segmented nuclei, extract a mask that only represents an outer ring of each nucleus (i.e. the nuclear envelope). Hint: Use "Process" -> "Binary" -> "Erode" to shrink the objects, then subtract the shrunken objects from the original mask using "Process" -> "Image Calculator...".
1. Extract the mean fluorescence intensity of the green channel for each ring. Hint: Use "Analyze" -> "Analyze Particles..." after thresholding and creating a mask.