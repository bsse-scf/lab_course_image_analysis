# Challenge

## Measure the dose-response curve of an anti-proliferative drug candidate

In your lab, you are studying the effects of a novel drug that apparently inhibits cell division; from preliminary experiments, this compound appears to be a potential treatment against metastasis in cancer patients. In an experiment, you seeded a constant number of cells (in four replicates) across consecutive wells in a plate and let them proliferate over 48h. In the lab automation facility, you calculated that the **final** cell density after 48h of culture should correspond to **10,240** cells per well (well area is 0.32 cm²) if the proliferation is **not** hampered by the drug.

At the onset of the experiment, you applied increasing concentrations of the drug and let the cells proliferate in the presence of the compound. Following table shows the drug application protocol: four rows ***A*** through ***D*** with each 10 columns ***0*** through ***9*** representing **four replicates**.

| C [µg/µl] | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-------|---|---|---|---|---|---|---|---|---|---|
| A     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| B     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| C     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| D     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |


You collected the data on a Nikon Widefield microscope that stored all 40 images for one plate into an individual ND2 file. Please note that the sequential acquisition performed by the microscope followed a snake pattern with **odd rows being scanned left to right and even rows being scanned right to left**. Also, notice that the field of view of your microscope **does not cover the whole well**.

Now that the experimental part is concluded and you have your data, you want to **measure the dose-response curve of your anti-proliferative drug candidate**.

The dataset is the file `plate01.zip` which you downloaded [earlier](./download_example_data.md). It is in the Nikon ND2 file format.

## Your task

1. Segment the cells in each image and export the results to a csv file. For this, you can use either write a **Fiji macro** or a **Jupyter notebook**.

1. In a **Jupyter Notebook**, load the csv file and calculate the **dose-response curve** (i.e. number of cells per well vs drug concentration). Create a plot of the dose-response curve and determine the **IC50** (the concentration at which the drug inhibits cell proliferation by 50%).

## Hints

### Fiji macro starting point

If you decide to write a Fiji macro, you can use the following code snippet as a starting point. It opens each series in the ND2 file and you can add your image processing code where indicated.

```java
// Choose your ND2 file
path = "/Users/albertm/teaching/lab_course/data/plate01.nd2";

// Use Bio-Formats to open metadata first
run("Bio-Formats Importer", "open=[" + path + "] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");

nSeries = 1;  // manually set number of series to process (there are 40)

for (i = 0; i < nSeries - 1; i++) {
    run("Bio-Formats Importer", 
        "open=[" + path + "] autoscale color_mode=Default view=Hyperstack stack_order=XYCZT series_" + 2 + i);
        
    // at this point, the i-th series is open
    // --> you can add your processing code here
    
}
```
