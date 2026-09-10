# Install Python

You do **not** need to install Python itself, and you should not install Anaconda
for this course. We use [pixi](https://pixi.sh), which reads the environment
description in the repository and creates exactly the right environment, the same
on every machine.

## 1. Install pixi

**macOS / Linux**: in a terminal:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

**Windows**: in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Then **close the terminal and open a new one**, so the change to your PATH takes
effect, and check:

```bash
pixi --version
```

## 2. Install git

Check whether you already have it with `git --version`. If not:

- **macOS**: `xcode-select --install`
- **Windows**: [git-scm.com/download/win](https://git-scm.com/download/win)
- **Linux**: your package manager, e.g. `sudo apt install git`

Or let pixi do it: `pixi global install git`.

## 3. Get the course material

```bash
git clone git@gitlab.ethz.ch:scu_courses/scu_lab_course_ia.git
cd scu_lab_course_ia
```

```{warning}
Use a plain `git clone`, **not** `git clone --recurse-submodules`. The repository
references a `solutions/` submodule that only instructors can read. If you clone
with `--recurse-submodules` you will see an error about *"Could not read from
remote repository"*: **your clone is still fine**: the notebooks and data are
all there, and `solutions/` is simply left empty. Nothing in the course needs it.
```

Next: [set up the environment](setup_environment.md).
