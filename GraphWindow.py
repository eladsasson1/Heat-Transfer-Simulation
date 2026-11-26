import os
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# Secondary window for displaying temperature vs. time graphs
class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    # Build the graph canvas on the left and controls on the right
    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.setMinimumSize(780, 480)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Left side: embedded empty Matplotlib graph inside a clean card ---
        graph_card = QFrame()
        graph_card.setObjectName("inputCard")
        graph_card_layout = QVBoxLayout(graph_card)
        graph_card_layout.setContentsMargins(10, 10, 10, 10)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure.patch.set_facecolor("#ffffff")
        self.canvas = FigureCanvas(self.figure)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_title("Temperature Over Time")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.figure.tight_layout()

        graph_card_layout.addWidget(self.canvas)
        main_layout.addWidget(graph_card, stretch=3)

        # --- Right side: body selector and vertical action buttons ---
        controls_card = QFrame()
        controls_card.setObjectName("inputCard")
        controls_layout = QVBoxLayout(controls_card)
        controls_layout.setContentsMargins(16, 16, 16, 16)
        controls_layout.setSpacing(12)

        selector_label = QLabel("Select Body:")
        selector_label.setObjectName("fieldLabel")

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        self.body_combo.setMinimumWidth(160)

        self.draw_button = QPushButton("Draw")
        self.clear_button = QPushButton("Clear")
        self.export_csv_button = QPushButton("Export to CSV")

        controls_layout.addWidget(selector_label)
        controls_layout.addWidget(self.body_combo)
        controls_layout.addSpacing(8)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_csv_button)
        controls_layout.addStretch()

        main_layout.addWidget(controls_card, stretch=1)

        # Apply shared application stylesheet
        self.load_stylesheet()

    # Load the shared QSS stylesheet if present
    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as style_file:
                self.setStyleSheet(style_file.read())


# Run the graph window directly for standalone testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec())
