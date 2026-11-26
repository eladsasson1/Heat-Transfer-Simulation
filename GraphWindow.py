import csv
import os
import subprocess
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
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
        self.style_axes()
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
        self.draw_button.clicked.connect(self.draw_graph)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)

        self.export_csv_button = QPushButton("Export to CSV")
        self.export_csv_button.clicked.connect(self.export_to_csv)

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

    # Apply standard axis labels, title, and subtle grid styling
    def style_axes(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_title("Temperature Over Time")
        self.ax.grid(True, linestyle="--", alpha=0.5)

    # Check whether the main window currently has recorded simulation data
    def has_simulation_data(self):
        return (
            self.main_window is not None
            and len(self.main_window.time_history) > 0
            and len(self.main_window.body1_temp_history) > 0
            and len(self.main_window.body2_temp_history) > 0
        )

    # Plot the selected body's temperature history onto the existing graph
    def draw_graph(self):
        if not self.has_simulation_data():
            QMessageBox.information(
                self,
                "No Simulation Data",
                "No simulation data is available yet. Please start a simulation first.",
            )
            return

        selected_body = self.body_combo.currentText()
        times = self.main_window.time_history

        if selected_body == "Body 1":
            temperatures = self.main_window.body1_temp_history
            line_color = "red"
        else:
            temperatures = self.main_window.body2_temp_history
            line_color = "blue"

        # Add the new curve without removing previously drawn curves
        self.ax.plot(times, temperatures, color=line_color, linewidth=2, label=selected_body)

        # Keep readable labels, legend, subtle grid, and clean axis limits
        self.style_axes()
        self.ax.legend(loc="best")

        self.ax.relim()
        self.ax.autoscale_view()
        if max(times) > 0:
            self.ax.set_xlim(left=0)
        else:
            self.ax.set_xlim(0, 1)
        self.ax.set_ylim(-5, 205)

        self.figure.tight_layout()
        self.canvas.draw()

    # Clear plotted curves and legend while keeping simulation history intact
    def clear_graph(self):
        self.ax.clear()
        self.style_axes()
        self.figure.tight_layout()
        self.canvas.draw()

    # Export all recorded simulation data (both bodies) to an Excel-compatible CSV file
    def export_to_csv(self):
        if not self.has_simulation_data():
            QMessageBox.information(
                self,
                "No Simulation Data",
                "No simulation data is available to export. Please run a simulation first.",
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Simulation Data",
            "heat_transfer_data.csv",
            "CSV Files (*.csv);;All Files (*)",
        )

        # Stop cleanly if the user cancels the save dialog
        if not file_path:
            return

        if not file_path.lower().endswith(".csv"):
            file_path = f"{file_path}.csv"

        times = self.main_window.time_history
        body1_temps = self.main_window.body1_temp_history
        body2_temps = self.main_window.body2_temp_history

        try:
            # Use UTF-8 with BOM so Microsoft Excel displays degree symbols properly
            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Time (s)", "Temperature 1 (°C)", "Temperature 2 (°C)"])
                for time_value, temp1, temp2 in zip(times, body1_temps, body2_temps):
                    writer.writerow([time_value, temp1, temp2])
        except OSError as error:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to save the CSV file:\n{error}",
            )
            return

        self.open_exported_file(file_path)

    # Open the exported CSV automatically in Microsoft Excel on macOS, or fall back to default app
    def open_exported_file(self, file_path):
        if sys.platform == "darwin":
            excel_result = subprocess.run(
                ["open", "-a", "Microsoft Excel", file_path],
                capture_output=True,
                text=True,
            )
            if excel_result.returncode == 0:
                return

            # Fall back to the default macOS application when Excel is unavailable
            fallback_result = subprocess.run(
                ["open", file_path],
                capture_output=True,
                text=True,
            )
            if fallback_result.returncode == 0:
                QMessageBox.information(
                    self,
                    "CSV Exported",
                    f"Simulation data was saved to:\n{file_path}\n\n"
                    "Microsoft Excel was not found, so the file was opened with the default application.",
                )
            else:
                QMessageBox.information(
                    self,
                    "CSV Exported",
                    f"Simulation data was saved to:\n{file_path}\n\n"
                    "Microsoft Excel was not found and the file could not be opened automatically.",
                )
        elif sys.platform == "win32":
            try:
                os.startfile(file_path)
            except OSError:
                QMessageBox.information(
                    self,
                    "CSV Exported",
                    f"Simulation data was saved to:\n{file_path}",
                )
        else:
            subprocess.run(["xdg-open", file_path], capture_output=True, text=True)

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
