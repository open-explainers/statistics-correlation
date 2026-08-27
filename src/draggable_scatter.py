"""Draggable scatterplot anywidget."""

import anywidget
import traitlets

_ESM = r"""

// PASTE ALL draggable_scatter.js

function render({ model, el }) {
  const SVG_NS = "http://www.w3.org/2000/svg";

  const width = 720;
  const height = 470;
  const margin = { top: 24, right: 24, bottom: 55, left: 60 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;

  el.classList.add("correlation-scatter");

  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("role", "img");
  svg.setAttribute(
    "aria-label",
    "Scatterplot with draggable observations and a least-squares regression line.",
  );
  el.appendChild(svg);

  const xMin = () => model.get("x_min");
  const xMax = () => model.get("x_max");
  const yMin = () => model.get("y_min");
  const yMax = () => model.get("y_max");

  function xToScreen(x) {
    return margin.left + ((x - xMin()) / (xMax() - xMin())) * plotWidth;
  }

  function yToScreen(y) {
    return (
      margin.top + plotHeight - ((y - yMin()) / (yMax() - yMin())) * plotHeight
    );
  }

  function screenToX(screenX) {
    const value =
      xMin() + ((screenX - margin.left) / plotWidth) * (xMax() - xMin());
    return Math.max(xMin(), Math.min(xMax(), value));
  }

  function screenToY(screenY) {
    const value =
      yMin() +
      ((margin.top + plotHeight - screenY) / plotHeight) * (yMax() - yMin());
    return Math.max(yMin(), Math.min(yMax(), value));
  }

  function makeLine(x1, y1, x2, y2, className) {
    const line = document.createElementNS(SVG_NS, "line");
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("class", className);
    svg.appendChild(line);
    return line;
  }

  function makeText(x, y, text, className) {
    const label = document.createElementNS(SVG_NS, "text");
    label.setAttribute("x", x);
    label.setAttribute("y", y);
    label.setAttribute("class", className);
    label.textContent = text;
    svg.appendChild(label);
    return label;
  }

  function drawAxes() {
    makeLine(
      margin.left,
      margin.top + plotHeight,
      margin.left + plotWidth,
      margin.top + plotHeight,
      "axis-line",
    );
    makeLine(
      margin.left,
      margin.top,
      margin.left,
      margin.top + plotHeight,
      "axis-line",
    );

    const tickCount = 5;

    for (let index = 0; index <= tickCount; index += 1) {
      const fraction = index / tickCount;

      const xValue = xMin() + fraction * (xMax() - xMin());
      const screenX = margin.left + fraction * plotWidth;
      makeLine(
        screenX,
        margin.top + plotHeight,
        screenX,
        margin.top + plotHeight + 6,
        "tick-line",
      );
      makeText(
        screenX,
        margin.top + plotHeight + 24,
        xValue.toFixed(0),
        "tick-label tick-label-x",
      );

      const yValue = yMin() + fraction * (yMax() - yMin());
      const screenY = margin.top + plotHeight - fraction * plotHeight;
      makeLine(margin.left - 6, screenY, margin.left, screenY, "tick-line");
      makeText(
        margin.left - 12,
        screenY + 5,
        yValue.toFixed(0),
        "tick-label tick-label-y",
      );
    }

    makeText(
      margin.left + plotWidth / 2,
      height - 10,
      "X",
      "axis-label axis-label-x",
    );

    const yLabel = makeText(
      18,
      margin.top + plotHeight / 2,
      "Y",
      "axis-label axis-label-y",
    );
    yLabel.setAttribute(
      "transform",
      `rotate(-90 18 ${margin.top + plotHeight / 2})`,
    );
  }

  const regressionLine = document.createElementNS(SVG_NS, "line");
  regressionLine.setAttribute("class", "regression-line");
  svg.appendChild(regressionLine);

  const pointLayer = document.createElementNS(SVG_NS, "g");
  pointLayer.setAttribute("class", "point-layer");
  svg.appendChild(pointLayer);

  function calculateRegression(points) {
    if (points.length < 2) return null;

    const xMean =
      points.reduce((total, point) => total + point.x, 0) / points.length;
    const yMean =
      points.reduce((total, point) => total + point.y, 0) / points.length;

    let numerator = 0;
    let denominator = 0;

    for (const point of points) {
      numerator += (point.x - xMean) * (point.y - yMean);
      denominator += (point.x - xMean) ** 2;
    }

    if (denominator === 0) return null;

    const slope = numerator / denominator;
    const intercept = yMean - slope * xMean;
    return { slope, intercept };
  }

  function drawRegression(points) {
    const regression = calculateRegression(points);

    if (regression === null) {
      regressionLine.setAttribute("visibility", "hidden");
      return;
    }

    const x1 = xMin();
    const x2 = xMax();
    const y1 = regression.slope * x1 + regression.intercept;
    const y2 = regression.slope * x2 + regression.intercept;

    regressionLine.setAttribute("x1", xToScreen(x1));
    regressionLine.setAttribute("y1", yToScreen(y1));
    regressionLine.setAttribute("x2", xToScreen(x2));
    regressionLine.setAttribute("y2", yToScreen(y2));
    regressionLine.setAttribute("visibility", "visible");
  }

  function syncPoints(points) {
    model.set(
      "points",
      points.map((point) => ({
        x: Number(point.x.toFixed(4)),
        y: Number(point.y.toFixed(4)),
      })),
    );
    model.save_changes();
  }

function drawPoints() {
  pointLayer.replaceChildren();

  const points = model.get("points").map((point) => ({
    x: Number(point.x),
    y: Number(point.y),
  }));

  drawRegression(points);

  let activeIndex = null;

  points.forEach((point, index) => {
    const circle = document.createElementNS(SVG_NS, "circle");

    circle.setAttribute("cx", xToScreen(point.x));
    circle.setAttribute("cy", yToScreen(point.y));
    circle.setAttribute("r", 9);
    circle.setAttribute("class", "data-point");

    circle.addEventListener("pointerdown", (event) => {
      event.preventDefault();

      activeIndex = index;

      circle.classList.add("dragging");

      svg.setPointerCapture(event.pointerId);
    });

    pointLayer.appendChild(circle);
  });

  svg.addEventListener("pointermove", (event) => {
    if (activeIndex === null) {
      return;
    }

    const bounds = svg.getBoundingClientRect();

    const screenX =
      ((event.clientX - bounds.left) / bounds.width) * width;

    const screenY =
      ((event.clientY - bounds.top) / bounds.height) * height;

    const point = points[activeIndex];

    point.x = screenToX(screenX);
    point.y = screenToY(screenY);

    const circles = pointLayer.querySelectorAll(".data-point");
    const circle = circles[activeIndex];

    circle.setAttribute("cx", xToScreen(point.x));
    circle.setAttribute("cy", yToScreen(point.y));

    drawRegression(points);

    model.set(
      "points",
      points.map((item) => ({
        x: Number(item.x.toFixed(4)),
        y: Number(item.y.toFixed(4)),
      }))
    );

    model.save_changes();
  });

  function stopDragging(event) {
    if (activeIndex === null) {
      return;
    }

    const circles = pointLayer.querySelectorAll(".data-point");
    const circle = circles[activeIndex];

    circle?.classList.remove("dragging");

    activeIndex = null;

    if (svg.hasPointerCapture(event.pointerId)) {
      svg.releasePointerCapture(event.pointerId);
    }
  }

  svg.addEventListener("pointerup", stopDragging);
  svg.addEventListener("pointercancel", stopDragging);
}

  drawAxes();
  drawPoints();

  // model.on("change:points", () => {
  //   if (!syncingFromDrag) drawPoints();
  // });
}

export default { render };
"""


_CSS = r"""
/* PASTE ALL draggable_scatter.css here */

.correlation-scatter {
  width: 100%;
  max-width: 760px;
}

.correlation-scatter svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
  touch-action: pan-y;
}

.correlation-scatter .axis-line {
  stroke: currentColor;
  stroke-width: 1.5;
  opacity: 0.7;
}

.correlation-scatter .tick-line {
  stroke: currentColor;
  stroke-width: 1;
  opacity: 0.5;
}

.correlation-scatter .tick-label {
  fill: currentColor;
  font-size: 13px;
  opacity: 0.75;
}

.correlation-scatter .tick-label-x {
  text-anchor: middle;
}

.correlation-scatter .tick-label-y {
  text-anchor: end;
}

.correlation-scatter .axis-label {
  fill: currentColor;
  font-size: 15px;
  font-weight: 600;
  text-anchor: middle;
}

.correlation-scatter .regression-line {
  stroke: #777;
  stroke-width: 3;
  stroke-dasharray: 8 5;
  pointer-events: none;
}

.correlation-scatter .data-point {
  fill: #4c78a8;
  stroke: white;
  stroke-width: 2;
  cursor: grab;
}

.correlation-scatter .data-point:hover {
  stroke-width: 3;
}

.correlation-scatter .data-point:focus {
  outline: none;
  stroke: #111;
  stroke-width: 3;
}

.correlation-scatter .data-point.dragging {
  cursor: grabbing;
  stroke-width: 4;
}

"""


class DraggableScatter(anywidget.AnyWidget):
    """Scatterplot whose observations can be dragged by the user."""

    _esm = _ESM
    _css = _CSS

    points = traitlets.List(
        trait=traitlets.Dict(),
        default_value=[],
    ).tag(sync=True)

    x_min = traitlets.Float(0.0).tag(sync=True)
    x_max = traitlets.Float(10.0).tag(sync=True)
    y_min = traitlets.Float(0.0).tag(sync=True)
    y_max = traitlets.Float(10.0).tag(sync=True)
