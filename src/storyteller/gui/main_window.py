from PyQt6.QtWidgets import QMainWindow, QLabel
# Import the WelcomeDialog
from .welcome_dialog import WelcomeDialog

class MainWindow(QMainWindow):
    """
    Main application window for StoryTeller.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("StoryTeller")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        # Add a placeholder label
        central_widget = QLabel("StoryTeller Main Window - Content Area")
        self.setCentralWidget(central_widget)

        # Set up UI, load data, etc.
        self.setup_ui()
        self.load_initial_data()

    def setup_ui(self):
        # TODO: Initialize Menu Bar, Tool Bar, Status Bar, Dock Widgets
        pass

    def load_initial_data(self):
        # Placeholder for data loading logic
        pass

    def showEvent(self, event):
        """Override showEvent to show dialog only once when window is first shown."""
        super().showEvent(event)
        # Check and show the welcome dialog using showEvent (ensures parent is visible)
        # Use a flag to ensure it only runs once per instance
        if not hasattr(self, '_welcome_shown'):
            WelcomeDialog.show_welcome_if_needed(self)
            self._welcome_shown = True # Set flag
