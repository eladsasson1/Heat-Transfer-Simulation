import os
import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from AboutWindow import AboutWindow
from Body import Body
from GraphWindow import GraphWindow


# Main application window for the Heat Transfer user interface
class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()

        # Secondary window references
        self.graph_window = None
        self.about_window = None

        # Simulation state variables
        self.body1 = None
        self.body2 = None
        self.conductivity = 1.0
        self.body1_temperature = 200.0
        self.body2_temperature = 0.0

        # Simulation history lists and elapsed time
        self.elapsed_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        # Simulation timer (100 ms interval corresponds to 0.1 s physical time step)
        self.timer_interval_ms = 100
        self.dt = 0.1
        self.timer = QTimer(self)
        self.timer.setInterval(self.timer_interval_ms)
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    # Build the complete main window UI with bodies, sliders, inputs, and buttons
    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setMinimumSize(860, 540)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 22, 28, 22)
        main_layout.setSpacing(20)

        # Central grid holding sliders, bodies, thermal connection, and conductivity input
        diagram_grid = QGridLayout()
        diagram_grid.setHorizontalSpacing(0)
        diagram_grid.setVerticalSpacing(10)

        # --- Body 1 temperature display and vertical slider ---
        self.body1_temp_label = QLabel("200.00 °C")
        self.body1_temp_label.setObjectName("tempDisplay")
        self.body1_temp_label.setAlignment(Qt.AlignCenter)
        self.body1_temp_label.setFixedWidth(96)

        self.body1_slider = QSlider(Qt.Vertical)
        self.body1_slider.setRange(0, 200)
        self.body1_slider.setValue(200)
        self.body1_slider.setTickPosition(QSlider.TicksRight)
        self.body1_slider.setTickInterval(50)
        self.body1_slider.setFixedHeight(210)
        self.body1_slider.valueChanged.connect(self.left_temperature_changed)

        slider1_container = QWidget()
        slider1_layout = QVBoxLayout(slider1_container)
        slider1_layout.setContentsMargins(0, 0, 18, 0)
        slider1_layout.setSpacing(8)
        slider1_layout.addWidget(self.body1_temp_label, alignment=Qt.AlignCenter)
        slider1_layout.addWidget(self.body1_slider, alignment=Qt.AlignCenter)

        # --- Body 1 label and red rectangle ---
        body1_title = QLabel("Body 1")
        body1_title.setObjectName("sectionTitle")
        body1_title.setAlignment(Qt.AlignCenter)

        self.body1_frame = QFrame()
        self.body1_frame.setObjectName("body1Frame")
        self.body1_frame.setFixedSize(170, 210)
        self.body1_frame.setStyleSheet(
            "background-color: #d62828; border: 2px solid #2b2d42; border-radius: 4px;"
        )

        # --- Conductivity input positioned above the horizontal gray connection ---
        conductivity_box = QWidget()
        conductivity_layout = QVBoxLayout(conductivity_box)
        conductivity_layout.setContentsMargins(10, 0, 10, 8)
        conductivity_layout.setSpacing(4)

        conductivity_label = QLabel("Conductivity")
        conductivity_label.setObjectName("fieldLabel")
        conductivity_label.setAlignment(Qt.AlignCenter)

        self.conductivity_spin = QDoubleSpinBox()
        self.conductivity_spin.setRange(0.01, 10000.0)
        self.conductivity_spin.setDecimals(2)
        self.conductivity_spin.setSingleStep(0.10)
        self.conductivity_spin.setValue(1.00)
        self.conductivity_spin.setSuffix(" J/(s·°C)")
        self.conductivity_spin.setMinimumWidth(145)

        conductivity_layout.addWidget(conductivity_label)
        conductivity_layout.addWidget(self.conductivity_spin, alignment=Qt.AlignCenter)

        # Horizontal gray rectangular connection representing thermal conduction
        self.connection_frame = QFrame()
        self.connection_frame.setObjectName("connectionFrame")
        self.connection_frame.setFixedSize(190, 36)
        self.connection_frame.setStyleSheet(
            "background-color: #8d99ae; border-top: 2px solid #2b2d42; border-bottom: 2px solid #2b2d42;"
        )

        # --- Body 2 label and black rectangle ---
        body2_title = QLabel("Body 2")
        body2_title.setObjectName("sectionTitle")
        body2_title.setAlignment(Qt.AlignCenter)

        self.body2_frame = QFrame()
        self.body2_frame.setObjectName("body2Frame")
        self.body2_frame.setFixedSize(170, 210)
        self.body2_frame.setStyleSheet(
            "background-color: #111111; border: 2px solid #2b2d42; border-radius: 4px;"
        )

        # --- Body 2 temperature display and vertical slider ---
        self.body2_temp_label = QLabel("0.00 °C")
        self.body2_temp_label.setObjectName("tempDisplay")
        self.body2_temp_label.setAlignment(Qt.AlignCenter)
        self.body2_temp_label.setFixedWidth(96)

        self.body2_slider = QSlider(Qt.Vertical)
        self.body2_slider.setRange(0, 200)
        self.body2_slider.setValue(0)
        self.body2_slider.setTickPosition(QSlider.TicksLeft)
        self.body2_slider.setTickInterval(50)
        self.body2_slider.setFixedHeight(210)
        self.body2_slider.valueChanged.connect(self.right_temperature_changed)

        slider2_container = QWidget()
        slider2_layout = QVBoxLayout(slider2_container)
        slider2_layout.setContentsMargins(18, 0, 0, 0)
        slider2_layout.setSpacing(8)
        slider2_layout.addWidget(self.body2_temp_label, alignment=Qt.AlignCenter)
        slider2_layout.addWidget(self.body2_slider, alignment=Qt.AlignCenter)

        # Place elements in the central diagram grid
        diagram_grid.addWidget(body1_title, 0, 1, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        diagram_grid.addWidget(conductivity_box, 0, 2, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        diagram_grid.addWidget(body2_title, 0, 3, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        diagram_grid.addWidget(slider1_container, 1, 0, alignment=Qt.AlignVCenter)
        diagram_grid.addWidget(self.body1_frame, 1, 1, alignment=Qt.AlignVCenter)
        diagram_grid.addWidget(self.connection_frame, 1, 2, alignment=Qt.AlignVCenter)
        diagram_grid.addWidget(self.body2_frame, 1, 3, alignment=Qt.AlignVCenter)
        diagram_grid.addWidget(slider2_container, 1, 4, alignment=Qt.AlignVCenter)

        diagram_wrapper = QHBoxLayout()
        diagram_wrapper.addStretch()
        diagram_wrapper.addLayout(diagram_grid)
        diagram_wrapper.addStretch()
        main_layout.addLayout(diagram_wrapper)

        # --- Physical property inputs below each body ---
        inputs_row = QHBoxLayout()
        inputs_row.setSpacing(60)

        # Body 1 mass and specific heat inputs
        body1_card = QFrame()
        body1_card.setObjectName("inputCard")
        body1_form = QFormLayout(body1_card)
        body1_form.setContentsMargins(16, 12, 16, 12)
        body1_form.setSpacing(10)

        self.body1_mass_spin = QDoubleSpinBox()
        self.body1_mass_spin.setRange(0.01, 10000.0)
        self.body1_mass_spin.setDecimals(2)
        self.body1_mass_spin.setSingleStep(1.0)
        self.body1_mass_spin.setValue(10.0)
        self.body1_mass_spin.setSuffix(" kg")
        self.body1_mass_spin.setMinimumWidth(145)

        self.body1_specific_heat_spin = QDoubleSpinBox()
        self.body1_specific_heat_spin.setRange(0.01, 10000.0)
        self.body1_specific_heat_spin.setDecimals(2)
        self.body1_specific_heat_spin.setSingleStep(0.05)
        self.body1_specific_heat_spin.setValue(0.40)
        self.body1_specific_heat_spin.setSuffix(" J/(kg·°C)")
        self.body1_specific_heat_spin.setMinimumWidth(145)

        body1_form.addRow("Mass:", self.body1_mass_spin)
        body1_form.addRow("Specific Heat:", self.body1_specific_heat_spin)

        # Body 2 mass and specific heat inputs
        body2_card = QFrame()
        body2_card.setObjectName("inputCard")
        body2_form = QFormLayout(body2_card)
        body2_form.setContentsMargins(16, 12, 16, 12)
        body2_form.setSpacing(10)

        self.body2_mass_spin = QDoubleSpinBox()
        self.body2_mass_spin.setRange(0.01, 10000.0)
        self.body2_mass_spin.setDecimals(2)
        self.body2_mass_spin.setSingleStep(1.0)
        self.body2_mass_spin.setValue(10.0)
        self.body2_mass_spin.setSuffix(" kg")
        self.body2_mass_spin.setMinimumWidth(145)

        self.body2_specific_heat_spin = QDoubleSpinBox()
        self.body2_specific_heat_spin.setRange(0.01, 10000.0)
        self.body2_specific_heat_spin.setDecimals(2)
        self.body2_specific_heat_spin.setSingleStep(0.05)
        self.body2_specific_heat_spin.setValue(0.40)
        self.body2_specific_heat_spin.setSuffix(" J/(kg·°C)")
        self.body2_specific_heat_spin.setMinimumWidth(145)

        body2_form.addRow("Mass:", self.body2_mass_spin)
        body2_form.addRow("Specific Heat:", self.body2_specific_heat_spin)

        inputs_row.addStretch()
        inputs_row.addWidget(body1_card)
        inputs_row.addWidget(body2_card)
        inputs_row.addStretch()
        main_layout.addLayout(inputs_row)

        # --- Bottom row of action buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.setMinimumWidth(120)
        self.start_button.toggled.connect(self.start_stop_button_method)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setMinimumWidth(120)
        self.graphs_button.clicked.connect(self.open_graph_window)

        self.about_button = QPushButton("About")
        self.about_button.setMinimumWidth(120)
        self.about_button.clicked.connect(self.open_about_window)

        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.graphs_button)
        button_layout.addWidget(self.about_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Apply shared application stylesheet
        self.load_stylesheet()

        # Set initial temperature displays and RGB colors from initial slider values
        self.left_temperature_changed()
        self.right_temperature_changed()

    # Load the shared QSS stylesheet if present
    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as style_file:
                self.setStyleSheet(style_file.read())

    # Update a body's RGB color from black (0 C) to bright red (200 C)
    def update_body_color(self, body_frame, temperature):
        red = int(255 * temperature / 200)
        red = max(0, min(255, red))
        body_frame.setStyleSheet(
            f"background-color: rgb({red}, 0, 0); border: 2px solid #2b2d42; border-radius: 4px;"
        )

    # Update left body temperature display and color when slider 1 moves
    def left_temperature_changed(self):
        temperature = float(self.body1_slider.value())
        self.body1_temperature = temperature
        self.body1_temp_label.setText(f"{temperature:.2f} °C")
        self.update_body_color(self.body1_frame, temperature)

    # Update right body temperature display and color when slider 2 moves
    def right_temperature_changed(self):
        temperature = float(self.body2_slider.value())
        self.body2_temperature = temperature
        self.body2_temp_label.setText(f"{temperature:.2f} °C")
        self.update_body_color(self.body2_frame, temperature)

    # Enable or disable all simulation input controls
    def set_inputs_enabled(self, enabled):
        self.body1_slider.setEnabled(enabled)
        self.body2_slider.setEnabled(enabled)
        self.body1_mass_spin.setEnabled(enabled)
        self.body2_mass_spin.setEnabled(enabled)
        self.body1_specific_heat_spin.setEnabled(enabled)
        self.body2_specific_heat_spin.setEnabled(enabled)
        self.conductivity_spin.setEnabled(enabled)

    # Start or stop the heat transfer simulation when the toggle button changes state
    def start_stop_button_method(self):
        if self.start_button.isChecked():
            # Read physical parameters from the interface
            mass1 = self.body1_mass_spin.value()
            specific_heat1 = self.body1_specific_heat_spin.value()
            mass2 = self.body2_mass_spin.value()
            specific_heat2 = self.body2_specific_heat_spin.value()
            self.conductivity = self.conductivity_spin.value()
            if self.conductivity <= 0:
                raise ValueError("Conductivity must be greater than zero.")

            # Create two Body objects with the current interface values
            self.body1 = Body(mass1, specific_heat1, self.body1_temperature)
            self.body2 = Body(mass2, specific_heat2, self.body2_temperature)

            # Reset history lists and record initial temperatures at time zero
            self.elapsed_time = 0.0
            self.time_history = []
            self.body1_temp_history = []
            self.body2_temp_history = []
            self.time_history.append(self.elapsed_time)
            self.body1_temp_history.append(self.body1.temperature)
            self.body2_temp_history.append(self.body2.temperature)

            # Update button text, lock input controls, and start the simulation timer
            self.start_button.setText("Stop")
            self.set_inputs_enabled(False)
            self.timer.start(self.timer_interval_ms)
        else:
            # Stop the timer, restore button text, and re-enable controls
            self.timer.stop()
            self.start_button.setText("Start")
            self.set_inputs_enabled(True)

    # Periodic simulation step triggered by the QTimer
    def timer_method(self):
        if self.body1 is None or self.body2 is None:
            return

        # Choose smaller internal steps when needed to avoid overshooting equilibrium
        heat_capacity_1 = self.body1.mass * self.body1.specific_heat
        heat_capacity_2 = self.body2.mass * self.body2.specific_heat
        rate = self.conductivity * (1.0 / heat_capacity_1 + 1.0 / heat_capacity_2)

        substeps = 1
        if rate * self.dt > 0.5:
            substeps = int(rate * self.dt / 0.5) + 1

        if substeps > 1000:
            # Extremely rapid conduction reaches thermal equilibrium within a single step
            t1 = self.body1.temperature
            t2 = self.body2.temperature
            equilibrium_temp = (
                heat_capacity_1 * t1 + heat_capacity_2 * t2
            ) / (heat_capacity_1 + heat_capacity_2)
            q1 = heat_capacity_1 * (equilibrium_temp - t1)
            q2 = -q1
            t1_new = self.body1.add_heat(q1)
            t2_new = self.body2.add_heat(q2)
        else:
            step_dt = self.dt / substeps
            t1_new = self.body1.temperature
            t2_new = self.body2.temperature

            for _ in range(substeps):
                # Read both temperatures before updating either body
                t1 = self.body1.temperature
                t2 = self.body2.temperature

                # Calculate heat exchanged during this time step
                q1 = self.conductivity * (t2 - t1) * step_dt
                q2 = -q1

                # Update both bodies using Body.add_heat
                t1_new = self.body1.add_heat(q1)
                t2_new = self.body2.add_heat(q2)

        # Store exact floating-point temperatures for the next step
        self.body1_temperature = t1_new
        self.body2_temperature = t2_new

        # Record elapsed time and floating-point temperatures in history lists
        self.elapsed_time = round(self.elapsed_time + self.dt, 6)
        self.time_history.append(self.elapsed_time)
        self.body1_temp_history.append(t1_new)
        self.body2_temp_history.append(t2_new)

        # Update numerical temperature displays with two decimal places
        self.body1_temp_label.setText(f"{t1_new:.2f} °C")
        self.body2_temp_label.setText(f"{t2_new:.2f} °C")

        # Update slider positions without triggering manual slider handlers
        self.body1_slider.blockSignals(True)
        self.body1_slider.setValue(int(round(t1_new)))
        self.body1_slider.blockSignals(False)

        self.body2_slider.blockSignals(True)
        self.body2_slider.setValue(int(round(t2_new)))
        self.body2_slider.blockSignals(False)

        # Update both body colors according to their current temperatures
        self.update_body_color(self.body1_frame, t1_new)
        self.update_body_color(self.body2_frame, t2_new)

    # Open the Graph window and pass a reference to this main window
    def open_graph_window(self):
        if self.graph_window is None:
            self.graph_window = GraphWindow(self)
        self.graph_window.show()
        self.graph_window.raise_()
        self.graph_window.activateWindow()

    # Open the About window
    def open_about_window(self):
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()
        self.about_window.raise_()
        self.about_window.activateWindow()


# Run the application directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
