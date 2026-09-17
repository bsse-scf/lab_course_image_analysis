# Set up the environment

From inside the repository folder:

```bash
pixi install
```

That reads `pixi.toml` and `pixi.lock` and builds the environment. It downloads
around **3.5 GB** and takes anywhere from a few minutes to half an hour depending
on your connection.


## Download the segmentation models

```bash
pixi run fetch-models
```

The day 2 notebooks use pretrained cellpose models, which cellpose downloads
(about 50 MB) the first time they are used. Using the command above we pre-download the models now.

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

## Set up the Jupyter AI course tutor

The course environment includes an optional AI-based **Course Tutor** chat in
JupyterLab. It can read the selected notebook cell and its output to help you
understand an error or interactively explain details about the contained code. This chat might be more useful than a general-purpose AI chat, because it knows about the course material and computational environment.

The tutor uses a model hosted by the Swiss AI Research Platform. To enable it, follow these steps:

### 1) Obtain an API key from the Swiss AI Research Platform (https://swissai.svc.cscs.ch/)

Sign in with your ETH Zurich account. Open **API Keys** and copy your key. It
should start with `sk-`.

### 2) Set the API key in your environment

In JupyterLab:

1. Open **Settings → Jupyternaut settings**.
2. Choose **Add secret**. Set the name to `OPENAI_API_KEY` and paste the key as
   its value.
3. Close the settings tab.
4. Open the chat in the left sidebar and ask a question to check the connection.
5. Select a code cell in a notebook and press **🎓** in the notebook toolbar.
   Check that the tutor responds about the selected cell.

## Stop JupyterLab

When you are done, press `Ctrl-C` in the terminal where you started JupyterLab.
Confirm with `y` and **Enter**, then close the browser tab.