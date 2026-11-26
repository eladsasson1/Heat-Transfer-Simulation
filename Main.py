import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# Main application window for the Heat Transfer user interface
class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    # Build the basic window structure, bodies, thermal connection, and buttons
    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setMinimumSize(780, 480)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(18)

        # Row containing the two bodies and the horizontal thermal connection
        diagram_layout = QHBoxLayout()
        diagram_layout.setSpacing(0)

        # Left body (initially red)
        self.body1_frame = QFrame()
        self.body1_frame.setObjectName("body1Frame")
        self.body1_frame.setFixedSize(160, 220)
        self.body1_frame.setStyleSheet("background-color: #d62828; border: 2px solid #222222;")

        # Horizontal gray connection representing thermal conduction
        self.connection_frame = QFrame()
        self.connection_frame.setObjectName("connectionFrame")
        self.connection_frame.setFixedSize(180, 36)
        self.connection_frame.setStyleSheet(
            "background-color: #8d99ae; border-top: 2px solid #222222; border-bottom: 2px solid #222222;"
        )

        # Right body (initially black)
        self.body2_frame = QFrame()
        self.body2_frame.setObjectName("body2Frame")
        self.body2_frame.setFixedSize(160, 220)
        self.body2_frame.setStyleSheet("background-color: #111111; border: 2px solid #222222;")

        diagram_layout.addStretch()
        diagram_layout.addWidget(self.body1_frame, alignment=Qt.AlignVCenter)
        diagram_layout.addWidget(self.connection_frame, alignment=Qt.AlignVCenter)
        diagram_layout.addWidget(self.body2_frame, alignment=Qt.AlignVCenter)
        diagram_layout.addStretch()

        main_layout.addLayout(diagram_layout)

        # Bottom row of action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(14)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.on_start_toggled)

        self.graphs_button = QPushButton("Graphs")
        self.about_button = QPushButton("About")

        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.graphs_button)
        button_layout.addWidget(self.about_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    # Update the Start toggle button text when toggled
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
