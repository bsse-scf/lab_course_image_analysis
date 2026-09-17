# Homework

# Quantitative determination of transfection efficiency

The primary objective of our course project is to characterize a new cell line (U2OS) that expresses a nuclear fluorescence marker: Green Fluorescent Protein (GFP). This fluorophore allows us to visualize cell nuclei in live cells during microscopy and flow cytometry experiments. However, the transfection methods used to introduce the gene for GFP expression in the cellular DNA are not entirely efficient;  some cells may fail to express GFP (or may express it in the wrong cell compartment).

In the microscopy practical session, you acquired images of three distinct fluorophores using the fluorescence microscope you built yourselves. DAPI (blue in the image below) marks all nuclei, regardless of whether cells have been successfully transfected or not. GFP (green), our channel of interest, indicates successfully transfected cells. Finally, Cy3 (red) stains the actin cytoskeleton, making the whole cell visible.

To quantify the transfection efficiency, we can segment all nuclei in the DAPI channel and analyze their intensity in the GFP channel. By calculating the ratio of GFP-positive nuclei to the total number of nuclei, we can estimate the transfection efficiency. Unfortunately, due to the limitations of the manual fluorescence microscope, the resulting channels are not perfectly aligned and therefore cannot be directly used to quantify the co-localization of the green and blue channels.

The `iaf` library offers the [`iaf.reg.multi_image_alignment()`](https://ia-res.ethz.ch/docs/iaf/reg/index.html#iaf.reg.multi_image_alignment) function to align any number of channels that can be used to correct for this misalignment. As an example, it can be used to successfully register the three channels shown below.

```{figure} illustrations/alignment.png
:width: 90%
:align: center

Example result of `iaf.reg.multi_image_alignment()`
```

## Data you will use 

As dataset you will use the pooled set of (approximately 10) image triplets (for DAPI, GFP and Cy3) that your entire group collected during the microscopy course.

## Your tasks

Please mind that you are expected to work **in pairs** and that all the code you will submit should be in one or more **Jupyter notebooks**. In your solution, please perform the following tasks:

1. Register all `{DAPI, GFP, Cy3}` sets to get aligned images that can be processed for the purpose of quantifying the transfection efficiency. Pick the best template channel that gives you the best alignment. Which one is it? Why? Make sure to display the result of the registrations in you notebook.

2. For each image triplet `{DAPI, GFP, Cy3}` , segment the nuclei and extract the corresponding (mean or median) GFP intensities. Which channel should you use for extracting nuclei and which for the GFP signal? Why?

3. Pool all individual intensity results from each of the sets in a global list or array.

4. Find a good approach to separate the positive from the negative nuclei and count the positive ones. You should expect to find an intensity distribution similar to this one (the function [iaf.stats.prepare_histogram()](https://ia-res.ethz.ch/docs/iaf/stats/index.html#iaf.stats.prepare_histogram) can be used to calculate an histogram with optimal bin size):

```{figure} illustrations/populations.png
:width: 400px
:align: center

Histogram of GFP intensities in the nuclei
```


5. Return the **transfection efficiency** as the ratio of positive nuclei to the total number of extracted nuclei.

## Your submission

Please upload a **zip archive** with your **family names as part of the file name** to [https://u.ethz.ch/ZiBOJ](https://u.ethz.ch/ZiBOJ) containing the **Jupyter notebook(s)** with the code that implements all requested tasks and the corresponding results. You don't need to submit any of the acquired images.

**Deadline** for submission is **Sunday of the second week following the microscopy block**. You may be required to resubmit your work for corrections or completion.

**Have fun!**
