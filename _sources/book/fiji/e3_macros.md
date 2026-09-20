# E3: Automation with Fiji macros

## Preparation

Work with the images in `data/fiji/programming/macro3`

## Questions
1. Open one of the images in Fiji.
1. Open the macro recorder (Plugins > Macros > Record...).
1. Apply a combination of filters and thresholding to segment the objects in the image.
1. When you are satisfied with the result, open the macro editor (Plugins > Macros > Edit...) and copy the relevant lines of code from the recorder window to the editor window.
1. Apply the macro to the other two images. Do you get a good segmentation result? If not, try to improve your macro.
1. Use the following code snippet to process all images in a folder. Save an output mask for each image in the output folder. In the following code, you need to replace the comment `// your code for image segmentation goes here` with your macro code. Make sure to adjust any file paths as needed.

```javascript
input = getDirectory("Choose Input Directory ");
output = getDirectory("Choose Output Directory ");
list = getFileList(input);
for (i=0; i<list.length; i++) {
    if (endsWith(list[i], ".tif")) {
        open(input + list[i]);

        // your code for image segmentation goes here
        // ...

        saveAs("Tiff", output + list[i]);
        close();
    }
}
```