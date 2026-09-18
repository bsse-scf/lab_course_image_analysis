# Reproducible Research Platform

The [Reproducible Research Platform (RRP)](https://rrp.ethz.ch) runs the whole
course environment - JupyterLab, Fiji, napari and the data - on ETH servers, in
your browser. Nothing needs to be installed on your computer.

1. Open [rrp.ia-res.ethz.ch](https://rrp.ia-res.ethz.ch) and log in with your
   account. The credentials are handed out on Day 0.
2. Click **[+]** next to **Your projects** and choose **Create new project from
   Git repository**. Enter the repository URL
   `https://github.com/bsse-scf/lab_course_image_analysis.git`, click
   **Clone**, enter `main` under **Branch / Tag / commit** and click **Build**.
   The build takes several minutes.
3. Once the project is listed as *not running*, click **▶** to start it, then
   **[↗]** to open JupyterLab.

In JupyterLab you find the course material in the `project` folder and the data
in `openbis`. To use Fiji, open
`File ▸ New Launcher ▸ Desktop`, which starts a Linux desktop in a new browser
tab.

Next: [connect to the Swiss AI Research Platform](swiss_ai.md).
