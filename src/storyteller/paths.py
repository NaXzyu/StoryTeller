import os
import sys
from pathlib import Path
from . import const # Import constants from the same package

def get_app_dir() -> Path:
    """Returns the root directory of the application source."""
    # Assumes paths.py is in src/storyteller
    return Path(__file__).parent.parent

def get_project_root() -> Path:
    """Returns the absolute root directory of the project."""
    # Assumes src/storyteller/paths.py structure
    return Path(__file__).parent.parent.parent

def get_config_dir() -> Path:
    """Gets the application's configuration directory."""
    if os.name == 'nt': # Windows
        path = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming')) / const.CONFIG_DIR_NAME
    else: # Linux/macOS (using XDG Base Directory Specification fallback)
        xdg_config_home = os.getenv('XDG_CONFIG_HOME')
        if xdg_config_home:
            path = Path(xdg_config_home) / const.CONFIG_DIR_NAME
        else:
            path = Path.home() / '.config' / const.CONFIG_DIR_NAME

    # Ensure the directory exists
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_config_file_path() -> Path:
    """Gets the full path to the configuration file."""
    return get_config_dir() / const.CONFIG_FILE_NAME

def get_main_script_path() -> Path:
    """Gets the path to the main entry point script (main.py)."""
    # This assumes main.py is in the same directory as paths.py
    return Path(__file__).parent / "main.py"

def get_build_dir() -> Path:
    """Gets the path to the build directory (relative to project root)."""
    path = get_project_root() / "build"
    path.mkdir(parents=True, exist_ok=True) # Ensure exists for specpath etc.
    return path

def get_dist_dir() -> Path:
    """Gets the path to the distribution directory (relative to project root)."""
    return get_project_root() / "dist"

# You might add other paths here like logs, data, etc.
# def get_log_dir() -> Path:
#     log_path = get_app_dir() / "logs" # Or maybe user data area
#     log_path.mkdir(parents=True, exist_ok=True)
#     return log_path
