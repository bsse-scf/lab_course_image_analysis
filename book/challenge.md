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

The dataset is the file `plate01.zip` which you downloaded [earlier](./setup/download_data.md). It is in the Nikon ND2 file format.

## Your task

1. Segment the cells in each image and export the results to a csv file. For this, you can use either write a **Fiji macro** or a **Jupyter notebook**.

1. In a **Jupyter Notebook**, load the csv file and calculate the **dose-response curve** (i.e. number of cells per well vs drug concentration). Create a plot of the dose-response curve and determine the **IC50** (the concentration at which the drug inhibits cell proliferation by 50%).

## Hints

::::{dropdown} A Fiji macro starting point
In case you decide to segment the images using Fiji, here is a starting point for a macro.

An ND2 file holds all 40 fields as separate **series**. Bio-Formats opens one
series at a time, so the macro is a loop over series numbers with the processing
inside it.

```java
// Set this to your own copy of the file.
path = "/path/to/plate01.nd2";

nSeries = 40;
run("Set Measurements...", "area mean redirect=None decimal=3");

setBatchMode(true);
run("Close All");
run("Clear Results");

for (i = 1; i <= nSeries; i++) {

    run("Bio-Formats Importer",
        "open=[" + path + "] autoscale color_mode=Default" +
        " view=Hyperstack stack_order=XYCZT series_" + i);

    // The i-th series is now open.
    // --> your processing and Analyze Particles call go here.

    run("Close All");
    print("series " + i + " of " + nSeries);
}

setBatchMode(false);
```


::::{dropdown} Well ordering

From looking at the different wells (called "series" in the ND2 file), how do you think the wells are ordered? Taking into account this order will be important when you calculate the dose-response curve, as you will need to know which series corresponds to which well.


::::{dropdown} Total cell numbers

How many cells do you count after 48h of culture in the control wells (i.e. those without drug)? How does this compare to the expected number of cells (10240)?
