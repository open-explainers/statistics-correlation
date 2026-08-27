"""Tests for the DraggableScatter widget.

These cover the Python side only: trait defaults, the sync contract with the
frontend, and that the JS/CSS assets the widget points at actually exist.
The drag interaction and rendering live in draggable_scatter.js and require a
browser to exercise, so they are intentionally out of scope here.
"""

import inspect
from pathlib import Path

from draggable_scatter import DraggableScatter

SYNCED_TRAITS = ["points", "x_min", "x_max", "y_min", "y_max"]
_MODULE_DIR = Path(inspect.getfile(DraggableScatter)).parent

# --- smoke -------------------------------------------------------------------


def test_instantiates_without_arguments():
    widget = DraggableScatter()
    assert isinstance(widget, DraggableScatter)


# --- defaults ----------------------------------------------------------------


def test_points_defaults_to_empty_list():
    assert DraggableScatter().points == []


def test_bounds_defaults():
    widget = DraggableScatter()
    assert widget.x_min == 0.0
    assert widget.x_max == 10.0
    assert widget.y_min == 0.0
    assert widget.y_max == 10.0


# --- sync contract with the frontend -----------------------------------------


def test_all_state_traits_are_synced():
    widget = DraggableScatter()
    for name in SYNCED_TRAITS:
        assert widget.trait_metadata(name, "sync") is True, f"{name} not synced"


# --- round-trips -------------------------------------------------------------


def test_points_holds_assigned_observations():
    widget = DraggableScatter()
    observations = [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}]
    widget.points = observations
    assert widget.points == observations


def test_bounds_are_settable():
    widget = DraggableScatter(x_min=-5.0, x_max=5.0, y_min=-1.0, y_max=1.0)
    assert (widget.x_min, widget.x_max) == (-5.0, 5.0)
    assert (widget.y_min, widget.y_max) == (-1.0, 1.0)


# --- assets exist (catches a renamed or missing JS/CSS file) -----------------


def test_esm_asset_exists():
    assert (_MODULE_DIR / "draggable_scatter.js").is_file()


def test_css_asset_exists():
    assert (_MODULE_DIR / "draggable_scatter.css").is_file()
