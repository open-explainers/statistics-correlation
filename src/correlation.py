"""Core calculations for the correlation explainer."""

from collections.abc import Sequence
import math
import random
from typing import TypedDict

__all__ = [
    "Point",
    "calculate_correlation",
    "calculate_regression_line",
    "describe_correlation",
    "generate_points",
]


class Point(TypedDict):
    """A single x-y observation.

    Attributes:
        x (float): The x-coordinate of the observation.
        y (float): The y-coordinate of the observation.
    """

    x: float
    y: float


def generate_points(
    count: int = 10,
    *,
    seed: int = 42,
) -> list[Point]:
    """Generate a reproducible moderately positive relationship.

    Args:
        count (int): The number of points to generate.
        seed (int): The random seed for reproducibility.

    Returns:
        list[Point]: A list of generated points.
    """
    rng = random.Random(seed)

    points: list[Point] = []

    for index in range(count):
        x = 1.0 + (8.0 * index / max(count - 1, 1))
        noise = rng.uniform(-1.5, 1.5)
        y = 1.5 + (0.75 * x) + noise

        points.append(
            {
                "x": round(x, 3),
                "y": round(max(0.5, min(9.5, y)), 3),
            }
        )

    return points


def calculate_correlation(points: Sequence[Point]) -> float | None:
    """Calculate the Pearson correlation coefficient.

    Args:
        points (Sequence[Point]): A sequence of points to calculate the correlation for.

    Returns:
        float | None: The Pearson correlation coefficient, or None if it cannot be calculated.
    """
    if len(points) < 2:
        return None

    x_values = [point["x"] for point in points]
    y_values = [point["y"] for point in points]

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    numerator = sum(
        (x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values, strict=True)
    )

    x_sum_squares = sum((x - x_mean) ** 2 for x in x_values)
    y_sum_squares = sum((y - y_mean) ** 2 for y in y_values)

    denominator = math.sqrt(x_sum_squares * y_sum_squares)

    if denominator == 0:
        return None

    return numerator / denominator


def calculate_regression_line(
    points: Sequence[Point],
) -> tuple[float, float] | None:
    """Return slope and intercept for the least-squares regression line.

    Args:
        points (Sequence[Point]): A sequence of points to calculate the regression line for.

    Returns:
        tuple[float, float] | None: The slope and intercept of the regression line, or None if it cannot be calculated.
    """
    if len(points) < 2:
        return None

    x_values = [point["x"] for point in points]
    y_values = [point["y"] for point in points]

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    denominator = sum((x - x_mean) ** 2 for x in x_values)

    if denominator == 0:
        return None

    slope = (
        sum(
            (x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values, strict=True)
        )
        / denominator
    )

    intercept = y_mean - slope * x_mean

    return slope, intercept


def describe_correlation(correlation: float | None) -> tuple[str, str]:
    """Return direction and strength descriptions.

    Args:
        correlation (float | None): The Pearson correlation coefficient to describe.

    Returns:
        tuple[str, str]: A tuple containing the direction and strength descriptions.
    """
    if correlation is None:
        return "Undefined", "Correlation cannot be calculated."

    absolute_r = abs(correlation)

    if absolute_r >= 0.9:
        strength = "Very strong"
    elif absolute_r >= 0.7:
        strength = "Strong"
    elif absolute_r >= 0.5:
        strength = "Moderate"
    elif absolute_r >= 0.3:
        strength = "Weak"
    else:
        strength = "Little or no linear"

    if correlation > 0:
        direction = "Positive"
    elif correlation < 0:
        direction = "Negative"
    else:
        direction = "No"

    return direction, strength
