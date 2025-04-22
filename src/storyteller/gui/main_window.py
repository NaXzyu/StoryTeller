from PyQt6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    """
    Main application window for StoryTeller.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StoryTeller")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        # Add a placeholder label
        central_widget = QLabel("StoryTeller Main Window - Content Area")
        self.setCentralWidget(central_widget)

        # TODO: Initialize Menu Bar, Tool Bar, Status Bar, Dock Widgets
