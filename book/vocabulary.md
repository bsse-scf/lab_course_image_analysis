# Vocabulary

This page defines the terms used in the course.

## Images

| Term | Meaning |
|---|---|
| **Pixel** | One element of the image. It holds a number, not a colour. |
| **Intensity image** | An image whose pixel values are measured brightness, as it comes off the microscope. |
| **Bit depth** | How large a pixel value may be. An 8-bit image holds 0 to 255, a 16-bit image 0 to 65535. |
| **Calibration** | The physical size of a pixel. Without it, every area and length is in pixels rather than microns. |
| **Channel** | One image of a set acquired of the same field through different filters, for example DAPI and GFP. |
| **LUT** (lookup table) | The mapping from pixel value to displayed colour. Changing it changes the picture, never the data. Called a *colormap* in matplotlib. |
| **Histogram** | A count of how many pixels hold each value. |
| **Saturation** | Pixels pinned at the maximum value. Their true brightness has been lost and cannot be recovered. |
| **Registration** | Finding the transform that brings one image into alignment with another. |

## Segmentation

| Term | Meaning |
|---|---|
| **Segmentation** | Deciding which pixels belong to the objects of interest. |
| **Threshold** | A value separating foreground from background. Applying one produces a binary image. |
| **Otsu's method** | A rule for choosing a threshold automatically from the histogram. |
| **Foreground / background** | The pixels belonging to objects, and everything else. |
| **Binary image** | An image with only two values, foreground and background. What a threshold produces. |
| **Mask** | A binary image used to *select* pixels from another image. The same array as a binary image, in a different role. |
| **Label image** | An image whose pixel values are object numbers: 1 for the first object, 2 for the second, and so on. Its maximum value is the number of objects. |
| **Semantic segmentation** | Answers *what kind of thing is this pixel?* Every pixel gets a class, and nothing distinguishes one object from another. |
| **Instance segmentation** | Answers *which object is this pixel part of?* Required for anything measured per object. |
| **Connected component labeling** | Turning a binary image into a label image by giving every connected group of foreground pixels its own number. Cannot separate objects that touch. |
| **Morphological operations** | Operations on the shape of a binary image: erosion, dilation, opening, closing, hole filling. |
| **Distance transform** | An image in which each foreground pixel holds its distance to the nearest background pixel. |
| **Watershed** | Splitting touching objects by treating the distance transform as a landscape and flooding it from seed points. |
| **Seed** | A starting point inside an object, from which the watershed grows that object. |

## Processing

| Term | Meaning |
|---|---|
| **Filter** | An operation replacing each pixel by a function of its neighbourhood, such as a Gaussian blur or a median filter. |
| **Background subtraction** | Removing a slowly varying offset so that a single threshold works across the whole field. |
| **Uneven illumination** | Brightness varying across the field because of the optics rather than the sample. Multiplicative, so corrected by division. |
| **Denoising** | Reducing noise before segmentation. A Gaussian filter suits general graininess, a median filter suits isolated extreme pixels. |

## Machine learning

| Term | Meaning |
|---|---|
| **Pixel classification** | Training a model to label each pixel by class, using features computed around it. What Trainable Weka does. |
| **Feature (for a classifier)** | One measured property of a pixel and its surroundings, such as local blur or edge strength. Not the same as a feature measured per object. |
| **Probability map** | An image holding, for each pixel, the classifier's confidence that it belongs to a class. |
| **Classifier** | The trained model itself, saved as a `.model` file and reusable on new images. |
| **Shallow learning** | You choose the features, the model learns how to weigh them. |
| **Deep learning** | The model learns the features from data as well, which is why it needs a great deal of it. |
| **Cellpose** | A pretrained deep model that outputs instance segmentations directly. |

## Measuring

| Term | Meaning |
|---|---|
| **Feature (of an object)** | One measured property of a segmented object. |
| **Morphology feature** | A feature computed from shape alone: area, perimeter, eccentricity, solidity, extent. |
| **Intensity feature** | A feature summarising pixel values inside an object, which needs a second image to measure. |
| **Region properties** | The standard set of per-object measurements. `regionprops` in scikit-image, `Analyze Particles` in Fiji. |
| **Effect size** | The difference between two groups expressed in standard deviations, saying how large a difference is rather than only whether it is detectable. |

## Validation

| Term | Meaning |
|---|---|
| **Ground truth** | A reference segmentation, usually drawn by an expert. A reference, not necessarily the truth. |
| **IoU** (intersection over union) | Shared pixels divided by pixels covered by either. Also called the **Jaccard index**. |
| **Dice coefficient** | Twice the shared pixels divided by the total of both. Always reads higher than IoU for an imperfect overlap. |
| **True positive, false positive, false negative** | An object correctly found, invented, or missed. |
| **Precision** | Of the objects you found, the fraction that are real. |
| **Recall** | Of the real objects, the fraction you found. |
| **F1 score** | The balance of precision and recall, in one number. |
| **Matching threshold** | How much overlap is required before a predicted object counts as matching a real one. Conventionally an IoU of 0.5, and worth reporting. |

## Fitting

| Term | Meaning |
|---|---|
| **Model** | A function with adjustable parameters, chosen to describe the process being measured. |
| **SSE** (sum of squared errors) | The usual measure of how badly a set of parameters describes the data. |
| **Residual** | The difference between a data point and the fitted curve. Structure in the residuals means the model is the wrong shape. |
| **IC50** | The concentration at which an effect is reduced by half. |

## Easy to confuse

**Binary image and label image.** A binary image says *whether* a pixel is
foreground (True) or background (False). A label image says *which object* it belongs to (e.g. 1, 2, 3 for object IDs 1, 2, 3). Where there's no object at all, the label image has a value of 0.

Binary image: "Semantic segmentation" (what category is this pixel?)
Label image: "Instance segmentation" (which object is this pixel part of?)

**Feature** In pixel classification a feature is a property of a *pixel*,
computed from its neighbourhood. In measurement a feature is a property of an
*object*. Both are standard, and the context makes clear which is meant.
