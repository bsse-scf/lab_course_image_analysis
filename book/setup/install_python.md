# Install Python

You do **not** need to install Python itself, and you should not install Anaconda
for this course. We use [pixi](https://pixi.sh), which reads the environment
description in the repository and installs the packages used in the course.

```{admonition} What is pixi?
Pixi is a tool for managing Python environments. It is similar to Conda or
virtualenv, but it is designed to be simpler and more reproducible. It reads a
description of the environment from a file and installs the packages in a
single command. It also provides a way to run commands inside the environment
without having to activate it first.

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

If you already had pixi installed from before, bring it up to date with
`pixi self-update`: the course needs a recent version.

## 2. Install git

Check whether you already have it with `git --version`. If not:

- **macOS**: `xcode-select --install`
- **Windows**: [git-scm.com/download/win](https://git-scm.com/download/win)
- **Linux**: your package manager, e.g. `sudo apt install git`

Or let pixi do it: `pixi global install git`.

## 3. Get the course material

```bash
git clone https://github.com/m-albert/scu_lab_course_ia_test.git
cd scu_lab_course_ia_test
```

```{warning}
Clone into a folder that is **not synced to the cloud**: not `Documents` or
`Desktop` if those live in OneDrive or iCloud, and not a Dropbox folder. The
environment is several gigabytes in many thousands of files, and a sync client
can interrupt installation or make it much slower. Your home folder is a suitable
location.
```

```{warning}
Use a plain `git clone`, **not** `git clone --recurse-submodules`. The repository
references a `.course/solutions/` submodule that only instructors can read. If you clone
with `--recurse-submodules` you will see an error about *"Could not read from
remote repository"*: the student notebooks and data are still available. The instructor-only
`.course/solutions/` folder may remain empty.
```

Next: [set up the environment](setup_environment.md).
