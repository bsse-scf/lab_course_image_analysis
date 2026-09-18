# Set up the environment


## 1. Get the course material

Download (or "clone") the course repository (meaning "course folder") from GitHub. In a terminal, navigate to a folder where you want to put the course folder. You can use `cd` to change the current folder, for example `cd ~` to go to your home folder.

```{warning}
Clone into a folder that is **not synced to the cloud**: not `Documents` or
`Desktop` if those live in OneDrive or iCloud, and not a Dropbox folder. The
environment is several gigabytes in many thousands of files, and a sync client
can interrupt installation or make it much slower. Your home folder is a suitable
location.
```

So, unless you choose a different directory than your home folder, run:

```bash
cd ~
```

Then run the following command to clone the repository:

```bash
git clone https://github.com/bsse-scf/lab_course_image_analysis.git
```

Now you have a folder `lab_course_image_analysis` with the course material. Change into that folder: 

```bash
cd lab_course_image_analysis
```

```{admonition} What is a repository?
A repository is a folder that contains files and a history of changes to those files. It is usually hosted on a service like GitHub, and for this course, it contains the course material, including notebooks, scripts, and data. You can think of it as a "course folder" that you can download and update.
```

## 2. Install the environment

From inside the repository folder, run the following command:

```bash
pixi install
```

This builds the environment. It downloads around **3 GB** and takes some minutes to complete. If the connection drops, run the same command again and it continues where it left off.

```{admonition} Already have conda?
If you already have Anaconda or Miniconda installed, leave it as is — pixi does not interact with it. Just make sure you run the course from a plain terminal, not from within an activated conda environment, and in JupyterLab always pick the **Python 3 (ipykernel)** kernel that appears by default rather than any other kernel you may have registered before.
```


## 3. Start Jupyter Lab

JupyterLab is the main interface for the course. From inside the repository folder, run:

```bash
pixi run jupyter lab
```

```{tip}
`pixi run <something>` always runs the command inside the environment defined in the current directory. For those who are used to using conda, this is similar to running commands in an activated environment. You never need to
"activate" anything, and you should not `pip install` into it: if a package is missing, it belongs in the pixi configuration.
```

## 4. Stop Jupyter Lab

When you are done, press `Ctrl-C` in the terminal where you started JupyterLab.
Confirm with `y` and **Enter**, then close the browser tab.

## 5. Start Jupyter Lab again

*On subsequent days*, you do not need to run `pixi install` again. Just open a terminal, change into the repository folder, and run:

```bash
pixi run jupyter lab
```

Next: [download the example data](download_data.md).
