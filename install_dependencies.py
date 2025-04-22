#!/usr/bin/env python
import subprocess
import sys

def install_dependencies():
    """
    Script to install the required dependencies for StoryTeller.
    This helps ensure qt-material and other optional packages are installed.
    """
    print("Installing StoryTeller dependencies...")
    
    # Use the current Python executable to install
    python = sys.executable
    
    try:
        # Install required packages
        subprocess.check_call([python, "-m", "pip", "install", "pyqt6>=6.9.0"])
        subprocess.check_call([python, "-m", "pip", "install", "qt-material>=2.14"])
        subprocess.check_call([python, "-m", "pip", "install", "click>=8.0.0"])
        
        # Install development dependencies
        subprocess.check_call([python, "-m", "pip", "install", "pyinstaller>=6.0.0"])
        
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
