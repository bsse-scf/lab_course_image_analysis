# Set up the environment

From inside the repository folder:

```bash
pixi install
```

That reads `pixi.toml` and `pixi.lock` and builds the environment. It downloads
around **3.5 GB** and takes anywhere from a few minutes to half an hour depending
on your connection, so start it and go and do something else.

You only ever run this once. If the environment description changes later,
`pixi install` again and it will bring you up to date.

## Start JupyterLab

```bash
pixi run lab
```

This opens JupyterLab in your browser, already using the course environment. Open
`notebooks/00_python_basics.ipynb` and run the first few cells.

```{tip}
`pixi run <something>` always runs inside the environment. You never need to
"activate" anything, and you should not `pip install` into it: if a package is
missing, it belongs in `pixi.toml`.
```

## Check it works

```bash
pixi run test
```

This imports everything the course uses and verifies that the data files are
present and intact. It takes a minute or so. You want to see a line ending in
**`passed`**.

If it reports missing data files, your clone is incomplete: check that
`git clone` finished without errors.

## If something goes wrong

| symptom | fix |
|---|---|
| `pixi: command not found` | Close the terminal and open a new one. If it persists, the installer did not update your PATH. |
| `pixi install` fails partway | Run it again: it resumes. Repeated failures usually mean a proxy or VPN interfering. |
| JupyterLab opens but a notebook cannot find `course` | You started it from the wrong folder. `cd` into the repository first. |
| A notebook cannot find its data | Run `pixi run fetch-data --verify` to see which files are missing. |

Bring anything unresolved to the Day 0 session.
