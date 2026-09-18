# Download the example data

Most course images are included in the repository. No additional download is
needed for the Fiji exercises or the day 2 notebooks.

## The challenge dataset

The day 2 challenge uses a separate dataset that is **too large to
ship in the course repository**. From inside the repository folder, run:

```bash
pixi run download-challenge-data
```

This downloads the archive (2.2 GB) and unpacks it to
`data/challenge/plate01.nd2` (3.5 GB). If the connection drops, run the same
command again and it continues where it left off.

```{note}
Alternatively, download `plate01.zip` by hand from https://u.ethz.ch/BgsSv,
unzip it, and place `plate01.nd2` in the `data/challenge/` folder of the
repository.
```

Next: [connect to the Swiss AI Research Platform](swiss_ai.md).
