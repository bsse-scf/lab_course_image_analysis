# Download the example data

Most of the course data comes with the repository, when you cloned it, you got
the images too, and nothing further is needed for day 1 or the day 2 notebooks.

## The challenge dataset

The day 2 challenge uses a separate dataset that is **too large to
ship in the repository** (several gigabytes: forty fields of a drug screening
plate, in Nikon ND2 format).

```{note}
:class: warning

**The download link for this dataset is not yet published.** It will be added
here before the course, and announced in the Day 0 session.

Please do not leave this download until day 2: on a shared
lecture-room network it will not finish in time.
```

Once you have it, extract it and place the `.nd2` file at:

```
data/challenge/plate01.nd2
```

That path is gitignored, so the file will not be committed by accident.

## If the download does not work on the day

The challenge is designed so you can do the analysis without it. A summary table
of per-well object counts is included in the repository, so the reshaping,
fitting and IC50 work can all be done from that alone: you would be skipping the
segmentation half, not the analysis.

Details are in the challenge instructions.
