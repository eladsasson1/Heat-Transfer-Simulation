import sys
from PySide6.QtCore import Qt
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


# Main application window for the Heat Transfer user interface
class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
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
        self.body1_temp_label = QLabel("200 °C")
        self.body1_temp_label.setObjectName("tempDisplay")
        self.body1_temp_label.setAlignment(Qt.AlignCenter)
        self.body1_temp_label.setFixedWidth(84)

        self.body1_slider = QSlider(Qt.Vertical)
        self.body1_slider.setRange(0, 200)
        self.body1_slider.setValue(200)
        self.body1_slider.setTickPosition(QSlider.TicksRight)
        self.body1_slider.setTickInterval(50)
        self.body1_slider.setFixedHeight(210)
        self.body1_slider.valueChanged.connect(self.update_body1_temperature)

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
        self.body2_temp_label = QLabel("0 °C")
        self.body2_temp_label.setObjectName("tempDisplay")
        self.body2_temp_label.setAlignment(Qt.AlignCenter)
        self.body2_temp_label.setFixedWidth(84)

        self.body2_slider = QSlider(Qt.Vertical)
        self.body2_slider.setRange(0, 200)
        self.body2_slider.setValue(0)
        self.body2_slider.setTickPosition(QSlider.TicksLeft)
        self.body2_slider.setTickInterval(50)
        self.body2_slider.setFixedHeight(210)
        self.body2_slider.valueChanged.connect(self.update_body2_temperature)

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
        self.start_button.toggled.connect(self.on_start_toggled)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setMinimumWidth(120)

        self.about_button = QPushButton("About")
        self.about_button.setMinimumWidth(120)

        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.graphs_button)
        button_layout.addWidget(self.about_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    # Update Body 1 temperature readout when slider 1 moves
    def update_body1_temperature(self, value):
        self.body1_temp_label.setText(f"{value} °C")

    # Update Body 2 temperature readout when slider 2 moves
    def update_body2_temperature(self, value):
        self.body2_temp_label.setText(f"{value} °C")

    # Update the Start toggle button text when checked or unchecked
    def on_start_toggled(self, checked):
        if checked:
            self.start_button.setText("Stop")
        else:
            self.start_button.setText("Start")


# Run the application directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
