# Install Fiji

[Fiji](https://fiji.sc) is ImageJ with a large collection of scientific plugins
already installed. You want Fiji, not plain ImageJ: the course uses plugins that
only Fiji ships with.

## Download

Get it from [fiji.sc/#download](https://fiji.sc/#download) and pick the version for
your operating system.

Fiji runs from the folder where you unpack it. Place that folder somewhere you
can find again, such as your home directory.

```{warning}
On macOS the first launch might be blocked. If you see *"Fiji cannot be
opened because the developer cannot be verified"*, right-click the app and choose
**Open**, then confirm. Double-clicking might keep failing.
```

## Check it works

1. Start Fiji. Its main window is a narrow toolbar.
2. `File ▸ Open Samples ▸ Blobs` opens a test image.
3. Check the plugins the course needs are present:
   - `Plugins ▸ Segmentation ▸ Trainable Weka Segmentation`
   - `Plugins ▸ Registration ▸ Linear Stack Alignment with SIFT`

If either is missing, run `Help ▸ Update…` and let it finish.
