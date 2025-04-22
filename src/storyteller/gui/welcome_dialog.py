from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QCheckBox, QPushButton, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from storyteller import config # Import the config module

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to StoryTeller")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Welcome Message
        welcome_label = QLabel(
            "Welcome to StoryTeller!\n\n"
            "This application helps you manage AI dialogues."
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Show on startup checkbox
        self.show_on_startup_checkbox = QCheckBox("Show this welcome message on startup")
        # Load initial state from config
        show_welcome = config.get_bool_setting('General', 'show_welcome_on_startup', True)
        self.show_on_startup_checkbox.setChecked(show_welcome)
        self.show_on_startup_checkbox.stateChanged.connect(self.save_setting)
        layout.addWidget(self.show_on_startup_checkbox)

        # OK Button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def save_setting(self, state):
        """Saves the checkbox state to the config file."""
        show = state == Qt.CheckState.Checked.value
        config.set_setting('General', 'show_welcome_on_startup', str(show).lower())

    @staticmethod
    def show_welcome_if_needed(parent):
        """Checks config and shows the dialog if required."""
        if config.get_bool_setting('General', 'show_welcome_on_startup', True):
            dialog = WelcomeDialog(parent)
            dialog.exec()

