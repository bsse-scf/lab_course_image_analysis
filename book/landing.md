# Image Analysis

Course material for the Image Analysis module of the Lab Course of the Single
Cell Facility, D-BSSE, ETH Zurich.

Two days, hands-on, assuming no prior experience with image analysis or
programming.

## What you will do

See the [schedule](course_schedule.md) for how the two days run.

**Day 1** starts in [Fiji](fiji/index.md), because it is the fastest way to get
from an image to a measurement. You will look at what an image actually is,
threshold it, count objects, and measure one channel through another's mask.

Then the same analysis again in Python, not because Python is more powerful,
but because it is *text*: repeatable, reviewable, and able to run over four
hundred images instead of four.

**Day 2** is about the two things that make an analysis trustworthy: methods
that cope with images a threshold cannot handle, and measures that tell you
honestly how well any of it worked. It ends with a challenge on real
screening data.

## Before you arrive

Work through [Setup](setup/index.md) and the
[Python primer](../notebooks/00_python_basics.ipynb). The primer teaches only
what this course uses and needs no data, so it can be done on a train; the
environment install cannot, so do not leave it to the first day.

```{note}
Clone the repository with a plain `git clone`, not `--recurse-submodules`: 
see the README for why.
```

If a term is unfamiliar, the [vocabulary](vocabulary.md) page defines the ones
this course uses and says where each is introduced.

## A note on how this is written

Several notebooks end with a result that is *wrong*, on purpose: a count that
does not match the annotation, a metric that flatters a useless segmentation, a
model that fits well and means little. Those are the parts worth slowing down
for. Getting a plausible-looking number out of an image is easy, and knowing
whether to believe it is the actual skill.
