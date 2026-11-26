import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# Secondary window displaying project information, illustration, and repository link
class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    # Build a clean and professional About window layout
    def setupUI(self):
        self.setWindowTitle("About - Heat Transfer Simulation")
        self.setFixedSize(540, 520)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(16)

        # Project title
        title_label = QLabel("Heat Transfer Simulation")
        title_label.setObjectName("aboutTitle")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Mechanical Engineering Practical Programming Project")
        subtitle_label.setObjectName("aboutSubtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Local project illustration
        self.image_label = QLabel()
        self.image_label.setObjectName("aboutImage")
        self.image_label.setAlignment(Qt.AlignCenter)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about_image.jpg")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                440,
                220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("Heat transfer illustration not found.")

        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Short description of the project
        description_label = QLabel(
            "This application provides an interactive graphical interface for exploring "
            "conductive heat transfer between two physical bodies. Users can configure "
            "each body's initial temperature, mass, and specific heat capacity, along "
            "with the thermal conductivity of the connecting bar, and view temperature "
            "graphs over time."
        )
        description_label.setObjectName("aboutDescription")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(description_label)

        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("dividerLine")
        main_layout.addWidget(divider)

        # Clickable GitHub repository link
        github_url = "https://github.com/eladsasson1/Heat-Transfer-Simulation.git"
        self.github_link_label = QLabel(
            f'GitHub Repository: <a href="{github_url}">{github_url}</a>'
        )
        self.github_link_label.setObjectName("aboutLink")
        self.github_link_label.setAlignment(Qt.AlignCenter)
        self.github_link_label.setOpenExternalLinks(True)
        self.github_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        main_layout.addWidget(self.github_link_label)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFixedWidth(120)
        self.close_button.clicked.connect(self.close)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        # Apply shared application stylesheet
        self.load_stylesheet()

    # Load the shared QSS stylesheet if present
    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as style_file:
                self.setStyleSheet(style_file.read())


# Run the About window directly for standalone testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    sys.exit(app.exec())
