"""Draggable scatterplot anywidget."""

from pathlib import Path

import anywidget
import traitlets

__all__ = ["DraggableScatter"]

_HERE = Path(__file__).parent


class DraggableScatter(anywidget.AnyWidget):
    """Scatterplot whose observations can be dragged by the user."""

    _esm = _HERE / "draggable_scatter.js"
    _css = _HERE / "draggable_scatter.css"

    points = traitlets.List(
        trait=traitlets.Dict(),
        default_value=[],
    ).tag(sync=True)

    x_min = traitlets.Float(0.0).tag(sync=True)
    x_max = traitlets.Float(10.0).tag(sync=True)
    y_min = traitlets.Float(0.0).tag(sync=True)
    y_max = traitlets.Float(10.0).tag(sync=True)
