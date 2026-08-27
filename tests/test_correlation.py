"""Tests for the correlation explainer core calculations."""

from collections.abc import Sequence
import math

from correlation import (
    Point,
    calculate_correlation,
    calculate_regression_line,
    describe_correlation,
    generate_points,
)

# --- generate_points ---------------------------------------------------------


def test_generate_points_default_count():
    assert len(generate_points()) == 10


def test_generate_points_respects_count():
    assert len(generate_points(count=25)) == 25


def test_generate_points_is_reproducible():
    assert generate_points(seed=1) == generate_points(seed=1)


def test_generate_points_seed_changes_output():
    assert generate_points(seed=1) != generate_points(seed=2)


def test_generate_points_x_spans_the_range():
    points = generate_points(count=10)
    assert points[0]["x"] == 1.0
    assert points[-1]["x"] == 9.0


def test_generate_points_y_is_clamped():
    for point in generate_points(count=50, seed=7):
        assert 0.5 <= point["y"] <= 9.5


def test_generate_points_count_one_does_not_crash():
    points = generate_points(count=1)
    assert len(points) == 1
    assert points[0]["x"] == 1.0


# --- calculate_correlation ---------------------------------------------------


def test_correlation_perfect_positive():
    points: Sequence[Point] = [{"x": i, "y": 2 * i + 1} for i in range(5)]
    assert calculate_correlation(points) == 1.0


def test_correlation_perfect_negative():
    points: Sequence[Point] = [{"x": i, "y": -3 * i} for i in range(5)]
    assert calculate_correlation(points) == -1.0


def test_correlation_in_valid_bounds():
    r = calculate_correlation(generate_points(seed=42))
    assert r is not None
    assert -1.0 <= r <= 1.0


def test_correlation_none_for_too_few_points():
    assert calculate_correlation([]) is None
    assert calculate_correlation([{"x": 1.0, "y": 2.0}]) is None


def test_correlation_none_when_x_has_no_variance():
    points: Sequence[Point] = [{"x": 5.0, "y": y} for y in range(4)]
    assert calculate_correlation(points) is None


def test_correlation_none_when_y_has_no_variance():
    points: Sequence[Point] = [{"x": x, "y": 5.0} for x in range(4)]
    assert calculate_correlation(points) is None


# --- calculate_regression_line -----------------------------------------------


def test_regression_recovers_known_slope_and_intercept():
    points: Sequence[Point] = [{"x": i, "y": 2 * i + 1} for i in range(5)]
    result = calculate_regression_line(points)
    assert result is not None
    slope, intercept = result
    assert math.isclose(slope, 2.0)
    assert math.isclose(intercept, 1.0)


def test_regression_none_for_too_few_points():
    assert calculate_regression_line([{"x": 1.0, "y": 2.0}]) is None


def test_regression_none_when_x_has_no_variance():
    points: Sequence[Point] = [{"x": 5.0, "y": y} for y in range(4)]
    assert calculate_regression_line(points) is None


# --- describe_correlation ----------------------------------------------------


def test_describe_none():
    assert describe_correlation(None) == (
        "Undefined",
        "Correlation cannot be calculated.",
    )


def test_describe_direction():
    assert describe_correlation(0.8)[0] == "Positive"
    assert describe_correlation(-0.8)[0] == "Negative"
    assert describe_correlation(0.0)[0] == "No"


def test_describe_strength_buckets():
    assert describe_correlation(0.95)[1] == "Very strong"
    assert describe_correlation(0.75)[1] == "Strong"
    assert describe_correlation(0.55)[1] == "Moderate"
    assert describe_correlation(0.35)[1] == "Weak"
    assert describe_correlation(0.10)[1] == "Little or no linear"


def test_describe_strength_boundaries_are_inclusive():
    assert describe_correlation(0.9)[1] == "Very strong"
    assert describe_correlation(0.7)[1] == "Strong"
    assert describe_correlation(0.5)[1] == "Moderate"
    assert describe_correlation(0.3)[1] == "Weak"


def test_describe_uses_absolute_value_for_strength():
    assert describe_correlation(-0.95)[1] == "Very strong"
