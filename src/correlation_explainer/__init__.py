"""Interactive components for teaching correlation."""

from correlation_explainer.correlation import (
    calculate_correlation,
    calculate_regression_line,
    describe_correlation,
    generate_points,
)
from correlation_explainer.draggable_scatter import DraggableScatter

__all__ = [
    "DraggableScatter",
    "calculate_correlation",
    "calculate_regression_line",
    "describe_correlation",
    "generate_points",
]
