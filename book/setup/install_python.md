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
```


## 1. Open a terminal

** macOS**: open the Terminal app (in Applications → Utilities).

**Linux**: open a terminal (Ctrl+Alt+T).

**Windows**: open PowerShell (press Win+R, type `powershell`, and press Enter).


## 2. Install pixi

**macOS / Linux**: in a terminal:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

**Windows**: in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Then **close the terminal and open a new one**, so the change to your PATH takes
effect, and check that the following command works:

```bash
pixi --version
```

If you already had pixi installed from before, bring it up to date with
`pixi self-update`: the course needs a recent version.

## 3. Install git

Check whether you already have it with `git --version`.

If not, type the following command in the terminal, which can take a minute:

```bash
pixi global install git
```

Next: [set up the course Python environment](setup_environment.md).
