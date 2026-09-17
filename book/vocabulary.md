# Vocabulary

This page defines the terms used in the course.

## Images

| Term | Meaning | First used |
|---|---|---|
| **Pixel** | One element of the image. It holds a number, not a colour. | [E1](fiji/e1_basics.md) |
| **Intensity image** | An image whose pixel values are measured brightness, as it comes off the microscope. | [E1](fiji/e1_basics.md) |
| **Bit depth** | How large a pixel value may be. An 8-bit image holds 0 to 255, a 16-bit image 0 to 65535. | [E1](fiji/e1_basics.md) |
| **Calibration** | The physical size of a pixel. Without it, every area and length is in pixels rather than microns. | [E1](fiji/e1_basics.md) |
| **Channel** | One image of a set acquired of the same field through different filters, for example DAPI and GFP. | [E1](fiji/e1_basics.md) |
| **LUT** (lookup table) | The mapping from pixel value to displayed colour. Changing it changes the picture, never the data. Called a *colormap* in matplotlib. | [E1](fiji/e1_basics.md) |
| **Histogram** | A count of how many pixels hold each value. | [E1](fiji/e1_basics.md), [`01`](../notebooks/01_image_handling.ipynb) |
| **Saturation** | Pixels pinned at the maximum value. Their true brightness has been lost and cannot be recovered. | [Spot the artifact](fiji/fun/spot_the_artifact.md) |
| **Registration** | Finding the transform that brings one image into alignment with another. | [E2](fiji/e2_registration.md) |

## Segmentation

| Term | Meaning | First used |
|---|---|---|
| **Segmentation** | Deciding which pixels belong to the objects of interest. | [E3](fiji/e3_segmentation.md) |
| **Threshold** | A value separating foreground from background. Applying one produces a binary image. | [E3](fiji/e3_segmentation.md), [`01`](../notebooks/01_image_handling.ipynb) |
| **Otsu's method** | A rule for choosing a threshold automatically from the histogram. | [E3](fiji/e3_segmentation.md), [`01`](../notebooks/01_image_handling.ipynb) |
| **Foreground / background** | The pixels belonging to objects, and everything else. | [E3](fiji/e3_segmentation.md) |
| **Binary image** | An image with only two values, foreground and background. What a threshold produces. | [`01` §6](../notebooks/01_image_handling.ipynb) |
| **Mask** | A binary image used to *select* pixels from another image. The same array as a binary image, in a different role. | [`01` §6](../notebooks/01_image_handling.ipynb) |
| **Label image** | An image whose pixel values are object numbers: 1 for the first object, 2 for the second, and so on. Its maximum value is the number of objects. | [`01` §7](../notebooks/01_image_handling.ipynb) |
| **Semantic segmentation** | Answers *what kind of thing is this pixel?* Every pixel gets a class, and nothing distinguishes one object from another. | [`01` §6](../notebooks/01_image_handling.ipynb) |
| **Instance segmentation** | Answers *which object is this pixel part of?* Required for anything measured per object. | [`01` §7](../notebooks/01_image_handling.ipynb) |
| **Connected component labeling** | Turning a binary image into a label image by giving every connected group of foreground pixels its own number. Cannot separate objects that touch. | [`01` §7](../notebooks/01_image_handling.ipynb) |
| **Morphological operations** | Operations on the shape of a binary image: erosion, dilation, opening, closing, hole filling. | [E3](fiji/e3_segmentation.md), [`02` §4](../notebooks/02_image_processing.ipynb) |
| **Distance transform** | An image in which each foreground pixel holds its distance to the nearest background pixel. | [`02` §6](../notebooks/02_image_processing.ipynb) |
| **Watershed** | Splitting touching objects by treating the distance transform as a landscape and flooding it from seed points. | [`02` §6](../notebooks/02_image_processing.ipynb) |
| **Seed** | A starting point inside an object, from which the watershed grows that object. | [`02` §6](../notebooks/02_image_processing.ipynb) |

## Processing

| Term | Meaning | First used |
|---|---|---|
| **Filter** | An operation replacing each pixel by a function of its neighbourhood, such as a Gaussian blur or a median filter. | [`02` §3](../notebooks/02_image_processing.ipynb) |
| **Background subtraction** | Removing a slowly varying offset so that a single threshold works across the whole field. | [`02` §2](../notebooks/02_image_processing.ipynb) |
| **Uneven illumination** | Brightness varying across the field because of the optics rather than the sample. Multiplicative, so corrected by division. | [`02` §2](../notebooks/02_image_processing.ipynb) |
| **Denoising** | Reducing noise before segmentation. A Gaussian filter suits general graininess, a median filter suits isolated extreme pixels. | [`02` §3](../notebooks/02_image_processing.ipynb) |

## Machine learning

| Term | Meaning | First used |
|---|---|---|
| **Pixel classification** | Training a model to label each pixel by class, using features computed around it. What Trainable Weka does. | [E4](fiji/e4_weka.md) |
| **Feature (for a classifier)** | One measured property of a pixel and its surroundings, such as local blur or edge strength. Not the same as a feature measured per object. | [E4](fiji/e4_weka.md) |
| **Probability map** | An image holding, for each pixel, the classifier's confidence that it belongs to a class. | [E4](fiji/e4_weka.md), [`03` §1](../notebooks/03_ml_segmentation.ipynb) |
| **Classifier** | The trained model itself, saved as a `.model` file and reusable on new images. | [E4](fiji/e4_weka.md) |
| **Shallow learning** | You choose the features, the model learns how to weigh them. | [`03` §2](../notebooks/03_ml_segmentation.ipynb) |
| **Deep learning** | The model learns the features from data as well, which is why it needs a great deal of it. | [`03` §2](../notebooks/03_ml_segmentation.ipynb) |
| **Cellpose** | A pretrained deep model that outputs instance segmentations directly. | [`03` §3](../notebooks/03_ml_segmentation.ipynb) |

## Measuring

| Term | Meaning | First used |
|---|---|---|
| **Feature (of an object)** | One measured property of a segmented object. | [`05`](../notebooks/05_features.ipynb) |
| **Morphology feature** | A feature computed from shape alone: area, perimeter, eccentricity, solidity, extent. | [`05` §2](../notebooks/05_features.ipynb) |
| **Intensity feature** | A feature summarising pixel values inside an object, which needs a second image to measure. | [`05` §3](../notebooks/05_features.ipynb) |
| **Region properties** | The standard set of per-object measurements. `regionprops` in scikit-image, `Analyze Particles` in Fiji. | [E3](fiji/e3_segmentation.md), [`05`](../notebooks/05_features.ipynb) |
| **Effect size** | The difference between two groups expressed in standard deviations, saying how large a difference is rather than only whether it is detectable. | [`05` §6](../notebooks/05_features.ipynb) |

## Validation

| Term | Meaning | First used |
|---|---|---|
| **Ground truth** | A reference segmentation, usually drawn by an expert. A reference, not necessarily the truth. | [`01` §7](../notebooks/01_image_handling.ipynb), [`04` §4](../notebooks/04_segmentation_metrics.ipynb) |
| **IoU** (intersection over union) | Shared pixels divided by pixels covered by either. Also called the **Jaccard index**. | [`04` §1](../notebooks/04_segmentation_metrics.ipynb) |
| **Dice coefficient** | Twice the shared pixels divided by the total of both. Always reads higher than IoU for an imperfect overlap. | [`04` §1](../notebooks/04_segmentation_metrics.ipynb) |
| **True positive, false positive, false negative** | An object correctly found, invented, or missed. | [`04` §3](../notebooks/04_segmentation_metrics.ipynb) |
| **Precision** | Of the objects you found, the fraction that are real. | [`04` §3](../notebooks/04_segmentation_metrics.ipynb) |
| **Recall** | Of the real objects, the fraction you found. | [`04` §3](../notebooks/04_segmentation_metrics.ipynb) |
| **F1 score** | The balance of precision and recall, in one number. | [`04` §3](../notebooks/04_segmentation_metrics.ipynb) |
| **Matching threshold** | How much overlap is required before a predicted object counts as matching a real one. Conventionally an IoU of 0.5, and worth reporting. | [`04` §5](../notebooks/04_segmentation_metrics.ipynb) |

## Fitting

| Term | Meaning | First used |
|---|---|---|
| **Model** | A function with adjustable parameters, chosen to describe the process being measured. | [`06` §2](../notebooks/06_curve_fitting.ipynb) |
| **SSE** (sum of squared errors) | The usual measure of how badly a set of parameters describes the data. | [`06` §2](../notebooks/06_curve_fitting.ipynb) |
| **Residual** | The difference between a data point and the fitted curve. Structure in the residuals means the model is the wrong shape. | [`06` §6](../notebooks/06_curve_fitting.ipynb) |
| **IC50** | The concentration at which an effect is reduced by half. | [Challenge](challenge.md) |

## Easy to confuse

**Binary image and label image.** A binary image says *whether* a pixel is
foreground (True) or background (False). A label image says *which object* it belongs to (e.g. 1, 2, 3 for object IDs 1, 2, 3). Where there's no object at all, the label image has a value of 0.

Binary image: "Semantic segmentation" (what category is this pixel?)
Label image: "Instance segmentation" (which object is this pixel part of?)

**Feature** In pixel classification a feature is a property of a *pixel*,
computed from its neighbourhood. In measurement a feature is a property of an
*object*. Both are standard, and the context makes clear which is meant.
