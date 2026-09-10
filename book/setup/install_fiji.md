# Install Fiji

[Fiji](https://fiji.sc) is ImageJ with a large collection of scientific plugins
already installed. You want Fiji, not plain ImageJ: the course uses plugins that
only Fiji ships with.

## Download

Get it from [fiji.sc/#download](https://fiji.sc/#download) and pick the build for
your operating system.

Fiji does not have an installer. It is a folder that runs where you put it, so
unzip it somewhere sensible, your home directory or Applications, and not
inside the Downloads folder, where you will lose it.

```{warning}
On macOS the first launch is blocked by Gatekeeper. If you see *"Fiji cannot be
opened because the developer cannot be verified"*, right-click the app and choose
**Open**, then confirm. Double-clicking will keep failing.
```

## Check it works

1. Start Fiji. You should get a narrow toolbar window rather than a normal
   application window: that is what it looks like.
2. `File ▸ Open Samples ▸ Blobs` opens a test image.
3. Check the plugins the course needs are present:
   - `Plugins ▸ Segmentation ▸ Trainable Weka Segmentation`
   - `Plugins ▸ Registration ▸ Linear Stack Alignment with SIFT`

If either is missing, run `Help ▸ Update…` and let it finish.

## Give it more memory

Fiji defaults to a fraction of your RAM, which is not enough for the larger
images. Under `Edit ▸ Options ▸ Memory & Threads…`, set the maximum memory to
about **two thirds** of your machine's RAM, then restart Fiji.
