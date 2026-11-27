import csv
import math
from collections.abc import Sequence

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TemperaturePlot(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(280, 240)
        self._data: list[tuple[float, float]] = []

    def set_data(self, data: Sequence[tuple[float, float]]) -> None:
        self._data = list(data)
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        plot = QRectF(52, 14, max(1, self.width() - 66), max(1, self.height() - 54))
        x_values = [point[0] for point in self._data]
        y_values = [point[1] for point in self._data]
        x_min, x_max = self._axis_range(x_values)
        y_min, y_max = self._axis_range(y_values)

        axis_pen = QPen(QColor("#222222"), 1)
        painter.setPen(axis_pen)
        painter.drawLine(plot.bottomLeft(), plot.bottomRight())
        painter.drawLine(plot.bottomLeft(), plot.topLeft())

        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for index in range(6):
            fraction = index / 5
            x = plot.left() + fraction * plot.width()
            y = plot.bottom() - fraction * plot.height()
            x_value = x_min + fraction * (x_max - x_min)
            y_value = y_min + fraction * (y_max - y_min)
            painter.drawLine(int(x), int(plot.bottom()), int(x), int(plot.bottom() + 4))
            painter.drawText(
                QRectF(x - 20, plot.bottom() + 5, 40, 14),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"{x_value:.2g}",
            )
            painter.drawLine(int(plot.left() - 4), int(y), int(plot.left()), int(y))
            painter.drawText(
                QRectF(0, y - 7, plot.left() - 8, 14),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{y_value:.2g}",
            )

        painter.drawText(
            QRectF(plot.left(), self.height() - 22, plot.width(), 18),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
            "Time (s)",
        )
        painter.save()
        painter.translate(14, plot.center().y())
        painter.rotate(-90)
        painter.drawText(
            QRectF(-plot.height() / 2, -9, plot.height(), 18),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
            "Temperature (°C)",
        )
        painter.restore()

        if self._data:
            path = QPainterPath()
            for index, (time_value, temperature) in enumerate(self._data):
                point = self._map_point(
                    plot,
                    time_value,
                    temperature,
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                )
                if index == 0:
                    path.moveTo(point)
                else:
                    path.lineTo(point)
            painter.setPen(QPen(QColor("#2676c9"), 2))
            painter.drawPath(path)
            painter.setBrush(QColor("#2676c9"))
            for time_value, temperature in self._data:
                point = self._map_point(
                    plot,
                    time_value,
                    temperature,
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                )
                painter.drawEllipse(point, 3, 3)

        painter.end()

    @staticmethod
    def _axis_range(values: list[float]) -> tuple[float, float]:
        if not values:
            return 0.0, 1.0
        minimum = min(values)
        maximum = max(values)
        if minimum == maximum:
            padding = max(abs(minimum) * 0.1, 0.5)
        else:
            padding = (maximum - minimum) * 0.1
        return minimum - padding, maximum + padding

    @staticmethod
    def _map_point(
        plot: QRectF,
        x_value: float,
        y_value: float,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
    ) -> QPointF:
        return QPointF(
            plot.left() + (x_value - x_min) / (x_max - x_min) * plot.width(),
            plot.bottom() - (y_value - y_min) / (y_max - y_min) * plot.height(),
        )


class GraphWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Graph Window")
        self.resize(620, 420)
        self._series: dict[str, list[tuple[float, float]]] = {
            "Body 1": [],
            "Body 2": [],
        }

        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(22)
        self.plot = TemperaturePlot()
        layout.addWidget(self.plot, 1)

        controls = QVBoxLayout()
        controls.setSpacing(10)
        self.body_selector = QComboBox()
        self.body_selector.addItems(self._series)
        self.body_selector.setMinimumWidth(140)
        controls.addWidget(self.body_selector)

        draw_button = QPushButton("Draw")
        draw_button.clicked.connect(self.draw_selected_body)
        controls.addWidget(draw_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_selected_body)
        controls.addWidget(clear_button)

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_selected_body)
        controls.addWidget(export_button)
        controls.addStretch()
        layout.addLayout(controls)
        self.setCentralWidget(content)

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #f0f0f0;
                color: #222222;
                font-family: "Segoe UI";
            }
            QComboBox, QPushButton {
                background: #eeeeee;
                border: 1px solid #888888;
                border-radius: 3px;
                padding: 6px 8px;
            }
            QPushButton:hover { background: #e2e2e2; }
            """
        )

    def set_body_data(
        self,
        body_name: str,
        data: Sequence[tuple[float, float]],
    ) -> None:
        if body_name not in self._series:
            raise ValueError(f"Unknown body: {body_name}")
        points = [(float(time_value), float(temperature)) for time_value, temperature in data]
        if any(not math.isfinite(value) for point in points for value in point):
            raise ValueError("Graph data must contain only finite numbers.")
        self._series[body_name] = points
        if self.body_selector.currentText() == body_name:
            self.plot.set_data(points)

    def draw_selected_body(self) -> None:
        self.plot.set_data(self._series[self.body_selector.currentText()])

    def clear_selected_body(self) -> None:
        body_name = self.body_selector.currentText()
        self._series[body_name].clear()
        self.plot.set_data([])

    def export_selected_body(self) -> None:
        body_name = self.body_selector.currentText()
        data = self._series[body_name]
        if not data:
            QMessageBox.information(self, "No data", "There is no graph data to export.")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export graph data",
            f"{body_name.lower().replace(' ', '_')}.csv",
            "CSV files (*.csv)",
        )
        if not file_name:
            return
        with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(("Time (s)", "Temperature (°C)"))
            writer.writerows(data)
