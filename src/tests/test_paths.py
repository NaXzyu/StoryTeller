import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Module to test
from storyteller import paths
from storyteller import const

# Helper to get expected root based on test file location
TEST_FILE_PATH = Path(__file__).resolve()
EXPECTED_PROJECT_ROOT = TEST_FILE_PATH.parent.parent.parent # src/tests -> src -> project root

def test_get_project_root():
    """Test that get_project_root returns the correct absolute path."""
    root = paths.get_project_root()
    assert isinstance(root, Path)
    assert root.is_absolute()
    assert root == EXPECTED_PROJECT_ROOT

def test_get_app_dir():
    """Test that get_app_dir returns the src directory."""
    app_dir = paths.get_app_dir()
    assert isinstance(app_dir, Path)
    assert app_dir == EXPECTED_PROJECT_ROOT / "src"

@patch('storyteller.paths.os.name', 'nt') # Simulate Windows
@patch('storyteller.paths.os.getenv')
def test_get_config_dir_windows(mock_getenv, tmp_path):
    """Test get_config_dir on Windows."""
    # Mock APPDATA to use tmp_path
    mock_getenv.side_effect = lambda key, default=None: str(tmp_path) if key == 'APPDATA' else default
    config_dir = paths.get_config_dir()
    expected_path = tmp_path / const.CONFIG_DIR_NAME

    assert isinstance(config_dir, Path)
    assert config_dir == expected_path
    assert config_dir.exists() # Check directory was created
    mock_getenv.assert_called_with('APPDATA', Path.home() / 'AppData' / 'Roaming')

# Patch os.name AND pathlib.Path for cross-platform testing
@patch('storyteller.paths.os.name', 'posix') # Simulate Linux/macOS
@patch('storyteller.paths.os.getenv')
@patch('storyteller.paths.Path') # Patch Path object
def test_get_config_dir_linux_xdg(mock_path_cls, mock_getenv, tmp_path):
    """Test get_config_dir on Linux with XDG_CONFIG_HOME set."""
    # Configure the mock Path class
    mock_path_instance = MagicMock(spec=Path)
    # Simulate path joining: Path('/tmp') / 'StoryTeller' -> mock_path_instance
    mock_path_cls.return_value.__truediv__.return_value = mock_path_instance
    # Mock getenv to return the temp path string for XDG_CONFIG_HOME
    mock_getenv.side_effect = lambda key: str(tmp_path) if key == 'XDG_CONFIG_HOME' else None

    config_dir = paths.get_config_dir()

    # Assertions
    assert config_dir == mock_path_instance # Should return the final mocked path
    # Check that Path was instantiated with the XDG path
    mock_path_cls.assert_called_with(str(tmp_path))
    # Check that the directory creation was called on the final path object
    mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_getenv.assert_called_with('XDG_CONFIG_HOME')

# Patch os.name AND pathlib.Path for cross-platform testing
@patch('storyteller.paths.os.name', 'posix') # Simulate Linux/macOS
@patch('storyteller.paths.os.getenv')
@patch('storyteller.paths.Path') # Patch Path object
def test_get_config_dir_linux_fallback(mock_path_cls, mock_getenv, tmp_path):
    """Test get_config_dir on Linux without XDG_CONFIG_HOME (fallback)."""
    # Configure the mock Path class and instances
    mock_home_path = MagicMock(spec=Path)
    mock_config_path = MagicMock(spec=Path)
    mock_final_path = MagicMock(spec=Path)

    # Path() -> mock_home_path (when called for home())
    # Path.home() -> mock_home_path
    # mock_home_path / '.config' -> mock_config_path
    # mock_config_path / 'StoryTeller' -> mock_final_path
    mock_path_cls.home.return_value = mock_home_path
    mock_home_path.__truediv__.return_value = mock_config_path
    mock_config_path.__truediv__.return_value = mock_final_path

    # Mock getenv to return None for XDG_CONFIG_HOME
    mock_getenv.return_value = None

    config_dir = paths.get_config_dir()

    # Assertions
    assert config_dir == mock_final_path # Should return the final mocked path
    mock_getenv.assert_called_with('XDG_CONFIG_HOME')
    mock_path_cls.home.assert_called_once() # Check Path.home() was called
    mock_home_path.__truediv__.assert_called_with('.config')
    mock_config_path.__truediv__.assert_called_with(const.CONFIG_DIR_NAME)
    # Check that the directory creation was called on the final path object
    mock_final_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

@patch('storyteller.paths.get_config_dir')
def test_get_config_file_path(mock_get_config_dir, tmp_path):
    """Test get_config_file_path builds upon get_config_dir."""
    mock_get_config_dir.return_value = tmp_path
    config_file = paths.get_config_file_path()
    expected_path = tmp_path / const.CONFIG_FILE_NAME

    assert isinstance(config_file, Path)
    assert config_file == expected_path
    mock_get_config_dir.assert_called_once()

def test_get_main_script_path():
    """Test get_main_script_path returns the correct path relative to paths.py."""
    main_script = paths.get_main_script_path()
    expected_path = Path(paths.__file__).parent / "main.py"
    assert isinstance(main_script, Path)
    assert main_script == expected_path.resolve() # Compare resolved paths

@patch('storyteller.paths.get_project_root')
def test_get_build_dir(mock_get_root, tmp_path):
    """Test get_build_dir creates the directory."""
    mock_get_root.return_value = tmp_path
    build_dir = paths.get_build_dir()
    expected_path = tmp_path / "build"

    assert isinstance(build_dir, Path)
    assert build_dir == expected_path
    assert build_dir.exists() # Check directory was created
    mock_get_root.assert_called_once()

@patch('storyteller.paths.get_project_root')
def test_get_dist_dir(mock_get_root, tmp_path):
    """Test get_dist_dir returns the correct path."""
    mock_get_root.return_value = tmp_path
    dist_dir = paths.get_dist_dir()
    expected_path = tmp_path / "dist"

    assert isinstance(dist_dir, Path)
    assert dist_dir == expected_path
    # Dist dir isn't created by the function itself
    assert not dist_dir.exists()
    mock_get_root.assert_called_once()

