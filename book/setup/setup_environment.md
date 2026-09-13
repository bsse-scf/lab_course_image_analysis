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

## Set up the Jupyter AI course tutor

The jupyter lab environment configured in this course includes a "Course Tutor" chat persona. It is a teaching assistant that can help you understand and debug the code in your notebooks, while preserving the learning value of the exercises. It gives hints and explanations, but never provides complete solutions. It knows context about the course and can therefore in many cases be more helpful than a generic AI assistant.

The Course Tutor uses a large language model (LLM) to generate its responses. For this course, we'll use a model hosted by the Swiss AI Research Platform. In order to be able to use it, you need to

### 1) Obtain an API key from the Swiss AI Research Platform (https://swissai.svc.cscs.ch/)

For this, sign in to the Swiss AI Research Platform with your ETH Zurich account. After logging in, go to the "API Keys" section and find your API key. Copy the key to your clipboard (it should look like `sk-...`).

### 2) Set the API key in your environment

In the opened Jupyter Lab environment:
1. Press Settings -> Jupyternaut settings
1. Press "Add secret": 
   - Name: `OPENAI_API_KEY`
   - Value: paste the API key you copied from the Swiss AI Research Platform
1. Close the Jupyternaut settings tab.
1. Verify the Course Tutor works:
   1. Open a chat on the left side of the Jupyter Lab interface and ask a question. Make sure the Course Tutor responds. If it does not, check that you have set the API key correctly.
   1. Open a notebook and identify a code cell. Select the cell (by clicking on it) and press the 🎓 button in the top menu bar of the notebook. Make sure the Course Tutor responds with a hint or explanation.

## Stop JupyterLab

When you are done, close the browser tab and press `Ctrl-C` in the terminal where you started JupyterLab. It will ask you to confirm that you want to stop the server; type `y` and press Enter.