// Count objects in every image in a folder.
//
// Companion to book/fiji/e5_macros.md. The processing here is exactly the E3
// pipeline; everything else is the loop around it.
//
// Note there is no watershed step: Analyze Particles counts connected regions,
// so touching objects are counted once. Separating them is covered in Python.
//
// Run with Plugins > Macros > Run..., or open in the script editor and press Run.

// Work without showing every intermediate image - much faster.
setBatchMode(true);
run("Close All");
run("Clear Results");

dir = getDirectory("Choose a folder of images");
list = getFileList(dir);
Array.sort(list);

// What to measure. Redirect=None means "measure the mask itself".
run("Set Measurements...", "area mean redirect=None decimal=2");

processed = 0;

for (i = 0; i < list.length; i++) {

    // Skip subfolders and anything that is not a TIFF.
    if (File.isDirectory(dir + list[i])) continue;
    if (!endsWith(toLowerCase(list[i]), ".tif")) continue;

    open(dir + list[i]);

    // --- the E3 pipeline -------------------------------------------------
    run("Gaussian Blur...", "sigma=1");
    setAutoThreshold("Otsu dark");
    run("Convert to Mask");
    run("Fill Holes");
    run("Analyze Particles...", "size=40-Infinity display summarize");
    // ---------------------------------------------------------------------

    close("*");
    processed++;
    print("Processed " + processed + " / " + list.length + ": " + list[i]);
}

print("Done: " + processed + " images.");

// Per-image counts are in Summary; Results contains per-object measurements.
// Save the Summary table here.
if (isOpen("Summary")) {
    Table.save(dir + "counts.csv", "Summary");
    print("Wrote " + dir + "counts.csv");
} else {
    print("No Summary window found - was 'summarize' ticked?");
}

setBatchMode(false);
