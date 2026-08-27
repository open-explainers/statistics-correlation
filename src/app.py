"""Correlation Explainer Notebook.

This notebook demonstrates the interactive correlation explainer built with marimo.

PLAN CELLS - I need five cells:
1. Introduction and instructions
2. Select number of points
3. Display draggable scatter plot
4. Show correlation and description
5. Conclusion and next steps
"""

import marimo

__generated_with_marimo_version__ = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import anywidget
    import marimo as mo
    import traitlets

    from correlation import (
        calculate_correlation,
        describe_correlation,
        generate_points,
    )
    from draggable_scatter import DraggableScatter

    return (
        DraggableScatter,
        calculate_correlation,
        describe_correlation,
        generate_points,
        mo,
    )


@app.cell
def _(mo):
    mo.md(
        """
        # Correlation Explainer

        Drag any point and watch the correlation change.
        Try creating:

        - a strong positive correlation
        - a strong negative correlation
        - little or no correlation
        - one unusual point that changes the correlation substantially
        """
    )


@app.cell
def _(mo):
    point_count = mo.ui.slider(
        start=3,
        stop=30,
        value=10,
        step=1,
        label="Number of points",
        show_value=True,
    )

    point_count
    return (point_count,)


@app.cell
def _(DraggableScatter, generate_points, mo, point_count):
    scatter = mo.ui.anywidget(
        DraggableScatter(
            points=generate_points(point_count.value),
            x_min=0.0,
            x_max=10.0,
            y_min=0.0,
            y_max=10.0,
        )
    )

    # scatter
    return (scatter,)


@app.cell
def _(calculate_correlation, describe_correlation, mo, scatter):
    correlation = calculate_correlation(scatter.points)
    direction, strength = describe_correlation(correlation)

    correlation_display = "undefined" if correlation is None else f"{correlation:+.3f}"

    mo.md(
        f"""
        ## What is happening?

        **Pearson correlation:** `{correlation_display}`

        - **Direction:** {direction}
        - **Strength:** {strength}

        The correlation coefficient describes the **direction and strength
        of the linear relationship** between the two variables.
        [Source](https://github.com/open-explainers/statistics-correlation)
        """
    )
    explanation = mo.md(
        f"""
        ## What is happening?

        **Pearson correlation:** `{correlation_display}`

        - **Direction:** {direction}
        - **Strength:** {strength}

        The correlation coefficient describes the **direction and strength
        of the linear relationship** between the two variables. ⯁
        [Source](https://github.com/open-explainers/statistics-correlation)
        """
    )

    mo.hstack(
        [explanation, scatter],
        widths=[1, 2],
        gap=2,
        align="start",
    )


if __name__ == "__main__":
    app.run()
