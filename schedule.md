# Schedule

Days 1 and 2 take place in *Room BSS E 21 from 9:00 to 17:30*.

Timing:
- 9-12:30
- 14:17:30

## Day 0: Intro

*Friday, 18.9.2026*

- Lecture: Introduction to Image Analysis
- Practical course preparation:
  - Download example data
  - Download and install Fiji / ImageJ
  - Download and install Python
  - Setup the Python environment used in the course
	- Installation:
		- Install pixi
		- Install git using pixi
		- Clone repo
		- Run jupyter notebook (there's a task "pixi run jupyter lab")
		- Troubleshoot

Python: Students who've never seen python can do the jupyter-lite exercises

## Day 1:

*Monday, 21.9.2026*

- Recap Image Analysis Basics

## Morning

Fiji show and practical:

- Fiji basics
	- Intensities
	- Color
		- split and merge channels
	- brightness contrast
	- histogram
	- data types
	- Image registration (since this is a topic of the homework)
	- exercise ideas:
		- How wide is a filament?
		- Spot the processing artifact

- Image segmentation
	- filter gauss
	- threshold
		- normal
		- otsu
	- watershed (maybe better python part?)
	- analyse particles
	- redirect measurements
	
- Weka
	- Segment more difficult: Example: something separable but difficult to segment with threshold
	- Same sample as for metrics exercise
	
- Macros
	- easy automatization: counting objects in several images which are easily separable
	- (if no time): apply weka to three images
	- skip if no time, this is optional and should not be overstated since the motivation for using Python is to build more flexible and reproducible workflows / batch processing


## Afternoon

- Using Python for image analysis
  - Introduction to Python and Jupyter Notebooks

- Python basics (pre-done at home)
	- Interactive demo and explanations
	- Questions?
	- Kahoot polls
	- Fun exercise

- Image handling with python
    - example: same workflow as in Fiji, but in Python
	- Use napari
	- basic concepts: image, pixels, channel, stack, z-stack, time series, mask, label image, slicing, croping, indexing, plotting, intensity profile, colormaps
	- Exercise
- Image processing basics
    - background subtraction: global, local
    - Filtering for correcting uneven illumination
	- Basic denoising
	- Simple Morphological operations
	- Exercise
	- visualize with napari?
	- semantic segmentation vs instance segmentation
	- watershed

## Day 2:

*Tuesday, 22.9.2026*

## Morning

Image segmentation using machine learning
- Go through slides / markdown
- Exercise:
	- Apply existing weka classifier to three images of the same type as the ones used in Fiji
	- Can we improve the classifier?
- Exercise:
	- Apply cellpose to the same images
	- Apply cellpose to difficult to segment cells
	- Troubleshoot: diameter
- Slides: Segmentation metrics
	- Intersection over Union, Dice coefficient, Jaccardi
	- Exercise: Create ground truth
	- Compare segmentations using different metrics
	- Dataset: https://bbbc.broadinstitute.org/BBBC020 (control 1, 2, 3)

Feature extraction and plotting
- Regionprops: feature extraction
	- Intensity
	- morphology
	- Exercise:
		- Detective game: separate worms from cells (or different types of worms?) based on morphological features
			- Dataset
				- worm dataset: https://bbbc.broadinstitute.org/BBBC010
				- cells: https://bbbc.broadinstitute.org/BBBC030
			- Use original images and masks
- Preparation for challenge: fitting an exponential curve
- Exercise idea: Quick comparison between conditions

## Afternoon

Challenge: Analysing a drug screening dataset

- Discussion of homework: Analysing data acquired on the DIY microscopes





