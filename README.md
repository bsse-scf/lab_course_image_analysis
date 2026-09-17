# Image Analysis Lab Course

This repo hosts materials and a website for the Image Analysis module of the lab course held by the Single Cell Unit at the D-BSSE of ETH Zurich.

It hosts a github pages website at https://github.com/m-albert/scu_lab_course_ia.

### Course environment setup on RRP for the exercises

#### Build the course RRP project

1. Log in to the RRP server [https://rrp.ia-res.ethz.ch](https://rrp.ia-res.ethz.ch) with your user credentials (handed out).
2. Click the **[+]** button next to **Your projects** and click **Create new project from Git repository**.
3. Specify the repository URL [https://github.com/m-albert/scu_lab_course_ia.git](https://github.com/m-albert/scu_lab_course_ia.git), then click on **Clone**.
4. Type `latest` to the field below **Branch / Tag / commit**, the project name you can leave unchanged. Next click on **Build**. This will build the Project image from the repository. This step will take several minutes to complete.

#### Start the course RRP Project

1. Once the build of the project is complete, it will be listed under **Your projects**, with Status: _not running_.
2. In the **Details tab** under **Resources** enter Memory in Gb **4.0** and hit **Enter** on the keyboard then under Number of CPUs enter **1.0** and hit **Enter** on the keyboard.
3. Click the **▶** button to start the project. Status will switch to _processing_ and then to _running_.
4. Click the **[↗]** button to start the JupyterLab UI in a new browser tab/window.

> Note:
    For help see the RRP documentaion: [https://rrp.ethz.ch/docs/create-project/](https://rrp.ethz.ch/docs/create-project/) or [https://rrp.ethz.ch/docs/start-project/](https://rrp.ethz.ch/docs/start-project/)

After starting your `RRP course project scu_lab_course_ia`, you will find four folders in the JupyterLab file browser:

```bash
build   # Should not be modified.
openbis # In here you find the necessary data for the course.
project # In this folder, you find all the course material.
results # This is the folder where you should save your results.
```

Navigate to the `project` folder and start with a new notebook for your assignments (File -> New -> Notebook). To load the required data set `plate01.nd2` you can run the following lines in your notebook:

```python
from pathlib import Path
base = Path.home()
Path(base / 'openbis/data/20260819080658667-36/original/plate01.nd2')
```

To download the dataset manually for your local installation type:

```Python
pixi run python data/download_challenge_data.py USERNAME
```
it will the prompt you for the password and download the `plate.01.nd` dataset to `data/challenge_data` for you to use.

For exercises with `ImageJ/Fiji` or `napari` in JupyterLab click top right onto `File` -> `New Launcher` -> `Desktop`. This will start a Linux Desktop in a new Tab of your browser. Then for example click onto the `Fiji` icon on the Desktop to start the application.
### AI course tutor

JupyterLab ships with a chat (the speech-bubble icon in the left sidebar,
or `File -> New -> Chat`). Its **Course Tutor** answers questions about the
notebooks the way a teaching assistant would: with hints, questions and
explanations rather than finished solutions. Every message you send also
carries the notebook cell you currently have selected - including its output
or error - so click the cell you are stuck on and ask, e.g. "why does this
fail?". Quicker still: the **🎓** button - on each cell and in the notebook
toolbar - asks the tutor to explain the selected cell. The tutor can read your notebook but cannot
change or run it.
