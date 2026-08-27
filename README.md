# statistics-correlation

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Open explainer for statistics correlation

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details markdown>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

Open a machine terminal in your `Repos` folder,
change directory (cd) into the new folder,
and run `code .` to open only this project in VS Code:

```shell
git clone https://github.com/open-explainers/statistics-correlation

cd statistics-correlation
code .
```

When VS Code opens, accept the Extension Recommendations
(click **`Install All`** or similar when asked).

### In a VS Code terminal

To set up a local project Python environment (managed by `uv`)
and align VS Code with it, run the following commands.

These are listed for convenience.
For best results, follow the detailed instructions in
[pro-analytics-02 guide](https://denisecase.github.io/pro-analytics-02/).

Use VS Code menu option `Terminal` / `New Terminal` to open a **VS Code terminal**
in the root project folder.
Copy each command, paste into your terminal, and hit ENTER,
to run each command one at a time.

```shell
uv self update
uv python pin 3.14

uv python install
uv lock --upgrade
uv sync
```

If asked: "We noticed a new environment has been created.
Do you want to select it for the workspace folder?" Click **"Yes"**.
If successful, you'll see a new `.venv` folder appear in the root project folder.

Install and run pre-commit checks (twice if necessary as shown below):

```shell
uv run pre-commit install
uv run pre-commit autoupdate

git add -A
uv run pre-commit run --all-files
# repeat if changes were made by pre-commit tasks
uv run pre-commit run --all-files
```

### Daily Workflow (Working With Python Project Code)

VS Code should have only this project open.
Open a VS Code terminal (menu: `Terminal` / `New Terminal`) and run:

```shell
git pull


# Served as an app:
uv run marimo run notebooks/app.py

# Interactive editing:
uv run marimo edit notebooks/app.py

# do chores
uv run ruff format .
uv run ruff check . --fix
uv run ty check
uv run python -m pytest
```

While editing project code and docs, repeat the commands above to
run files, check them, and rebuild docs as needed.

Save progress frequently.
Some tools may make changes;
you may need to **re-run git `add` and `commit`**
to ensure everything gets committed before pushing.

```shell
git add -A
git commit -m "your message here"
# repeat if changes were made (try the UP ARROW)
git add -A
git commit -m "your message here"

git push -u origin main
```

</details>

## Live App

- [Live App](https://denisecase.github.io/statistics-correlation/)

## Citation

- [CITATION.cff](./CITATION.cff)

## License

This project is licensed under the [MIT License](./LICENSE).
