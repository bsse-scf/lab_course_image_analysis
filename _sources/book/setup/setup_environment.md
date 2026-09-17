# Set up the environment


## 1. Get the course material

Download (or "clone") the course repository (meaning "course folder") from GitHub. In a terminal, navigate to a folder where you want to put the course folder. You can use `cd` to change the current folder, for example `cd ~` to go to your home folder. Then run:

```bash
git clone https://github.com/bsse-scf/scu_lab_course_ia.git
```

Now you have a folder `scu_lab_course_ia` with the course material. Change into that folder: 

```bash
cd scu_lab_course_ia
```

```{admonition} What is a repository?
A repository is a folder that contains files and a history of changes to those files. It is usually hosted on a service like GitHub, and for this course, it contains the course material, including notebooks, scripts, and data. You can think of it as a "course folder" that you can download and update.
```


```{warning}
Clone into a folder that is **not synced to the cloud**: not `Documents` or
`Desktop` if those live in OneDrive or iCloud, and not a Dropbox folder. The
environment is several gigabytes in many thousands of files, and a sync client
can interrupt installation or make it much slower. Your home folder is a suitable
location.
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

## 4. Set up the Jupyter AI course tutor

The course environment includes an optional AI-based **Course Tutor** chat in
JupyterLab. It can read the selected notebook cell and its output to help you
understand an error or interactively explain details about the contained code. This chat might be more useful than a general-purpose AI chat, because it knows about the course material and computational environment.

The tutor uses a model hosted by the Swiss AI Research Platform. To enable it, follow these steps:

### 4.1 Obtain an API key from the Swiss AI Research Platform (https://swissai.svc.cscs.ch/)

Sign in with your ETH Zurich account. Open **API Keys** and copy your key. It
should start with `sk-`.

### 4.2 Set the API key in your environment

In JupyterLab:

1. Open **Settings → Jupyternaut settings**.
2. Choose **Add secret**. Set the name to `OPENAI_API_KEY` and paste the key as
   its value.
3. Close the settings tab.
4. Open the chat in the left sidebar and ask a question to check the connection.
5. Select a code cell in a notebook and press **🎓** in the notebook toolbar.
   Check that the tutor responds about the selected cell.

## 5. Stop Jupyter Lab

When you are done, press `Ctrl-C` in the terminal where you started JupyterLab.
Confirm with `y` and **Enter**, then close the browser tab.

## 6. Start Jupyter Lab again

*On subsequent days*, you do not need to run `pixi install` again. Just open a terminal, change into the repository folder, and run:

```bash
pixi run jupyter lab
```