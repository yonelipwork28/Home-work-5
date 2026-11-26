import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class HeatTransferWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Heat Transfor Simulition")
        self.setMinimumSize(940, 720)

        page = QWidget()
        page.setObjectName("page")
        self.setCentralWidget(page)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(34, 26, 34, 24)
        layout.setSpacing(14)

        eyebrow = QLabel("THERMAL SYSTEMS  /  LAB")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Heat Transfor Simulition")
        title.setObjectName("title")
        subtitle = QLabel("Two-body heat transfer workspace")
        subtitle.setObjectName("subtitle")
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        panel = QFrame()
        panel.setObjectName("panel")
        grid = QGridLayout(panel)
        grid.setContentsMargins(22, 20, 22, 20)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        grid.addWidget(self._make_slider("left"), 0, 0, 3, 1)
        grid.addWidget(self._make_tank("TANK 01", "#d93636"), 0, 1)
        grid.addWidget(self._make_connection(), 0, 2)
        grid.addWidget(self._make_tank("TANK 02", "#111111"), 0, 3)
        grid.addWidget(self._make_slider("right"), 0, 4, 3, 1)

        grid.addWidget(self._make_temperature(), 1, 1)
        grid.addWidget(self._make_temperature(), 1, 3)
        grid.addWidget(self._make_fields(), 2, 1)
        grid.addWidget(self._make_buttons(), 2, 2)
        grid.addWidget(self._make_fields(), 2, 3)
        layout.addWidget(panel, 1)

        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(QPushButton("About Me"))
        footer.addStretch()
        layout.addLayout(footer)

        self.setStyleSheet(
            """
            QWidget#page {
                background: #0c1522;
                color: #e7f0f7;
                font-family: "Segoe UI";
            }
            QLabel#eyebrow { color: #43d6c5; font-size: 11px; }
            QLabel#title { color: #f3f7fb; font-size: 30px; font-weight: 700; }
            QLabel#subtitle { color: #8fa4b8; font-size: 14px; }
            QFrame#panel {
                background: #121f2e;
                border: 1px solid #25384a;
                border-radius: 16px;
            }
            QFrame#tankCard {
                background: #172738;
                border-radius: 12px;
            }
            QLabel#tankName { font-size: 13px; font-weight: 700; }
            QLabel#smallLabel {
                color: #9eb2c4;
                font-size: 10px;
                font-weight: 700;
            }
            QLabel#temperature {
                background: #172738;
                border: 1px solid #2a4053;
                border-radius: 8px;
                color: #43d6c5;
                font-size: 15px;
                padding: 10px;
            }
            QLineEdit {
                background: #0d1926;
                border: 1px solid #30475b;
                border-radius: 7px;
                color: #eef5fa;
                padding: 9px;
            }
            QPushButton {
                background: #1b3446;
                border: 1px solid #31546b;
                border-radius: 8px;
                color: #eaf3f8;
                font-weight: 700;
                padding: 10px 14px;
            }
            QPushButton#startButton { background: #20a497; color: #071918; }
            QSlider::groove:vertical {
                background: #263b4d;
                width: 6px;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background: #43d6c5;
                width: 16px;
                height: 16px;
                margin: 0 -5px;
                border-radius: 8px;
            }
            """
        )

    @staticmethod
    def _make_tank(name: str, color: str) -> QFrame:
        card = QFrame()
        card.setObjectName("tankCard")
        card.setFixedHeight(220)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        name_label = QLabel(name)
        name_label.setObjectName("tankName")
        name_label.setFixedHeight(20)
        tank = QFrame()
        tank.setObjectName("tankGraphic")
        tank.setFixedHeight(160)
        tank.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        tank.setStyleSheet(
            f"background: {color}; border-radius: 8px;"
        )

        layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(tank)
        layout.addStretch()
        return card

    @staticmethod
    def _make_slider(side: str) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        label = QLabel("HEAT")
        label.setObjectName("smallLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        slider = QSlider(Qt.Orientation.Vertical)
        slider.setObjectName(f"{side}HeatSlider")
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.setMinimumHeight(190)

        layout.addWidget(label)
        layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
        return panel

    @staticmethod
    def _make_connection() -> QWidget:
        panel = QWidget()
        panel.setFixedHeight(220)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("CONDUCTIVITY")
        label.setObjectName("smallLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label.setFixedHeight(16)

        conductivity = QLineEdit()
        conductivity.setObjectName("conductivityInput")
        conductivity.setPlaceholderText("W / m·K")
        conductivity.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        conductivity.setFixedSize(140, 36)

        pipe = QFrame()
        pipe.setObjectName("heatConductionPipe")
        pipe.setMinimumWidth(190)
        pipe.setFixedHeight(18)
        pipe.setStyleSheet("background: #ff784f;")

        layout.addWidget(label)
        layout.addWidget(conductivity, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(60)
        layout.addWidget(pipe)
        layout.addStretch()
        return panel

    @staticmethod
    def _make_temperature() -> QLabel:
        label = QLabel("Temperature   -- °C")
        label.setObjectName("temperature")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    @staticmethod
    def _make_fields() -> QWidget:
        fields = QWidget()
        layout = QVBoxLayout(fields)
        layout.addWidget(QLineEdit(placeholderText="Mass (kg)"))
        layout.addWidget(QLineEdit(placeholderText="Heat capacity (J/kg·K)"))
        return fields

    @staticmethod
    def _make_buttons() -> QWidget:
        buttons = QWidget()
        layout = QVBoxLayout(buttons)
        start = QPushButton("Start")
        start.setObjectName("startButton")
        layout.addWidget(start)
        layout.addWidget(QPushButton("Graphs"))
        return buttons


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = HeatTransferWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main()
