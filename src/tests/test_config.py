import pytest
import configparser
import sys # Import sys for the print statement in save_config mock
from unittest.mock import patch, MagicMock

# Use a temporary directory for config files during tests
@pytest.fixture
def temp_config_file(tmp_path):
    """Provides a temporary path for the config file and patches paths.py."""
    temp_file = tmp_path / "test_config.ini"
    # Patch the path *before* config module might be loaded by other imports/fixtures
    with patch('storyteller.config.paths.get_config_file_path', return_value=temp_file):
        yield temp_file # Provide the path to the test

@pytest.fixture(autouse=True)
def manage_config_state(temp_config_file):
    """Manages the config module state for tests."""
    from storyteller import config
    import importlib

    # Ensure config uses the temp file path
    config.config_file_path = temp_config_file

    # Reset the config parser object before each test
    config.config = configparser.ConfigParser()

    # Ensure the temp file doesn't exist before each test
    if temp_config_file.exists():
        temp_config_file.unlink()

    # --- REMOVED automatic load_config() call ---

    yield # Run the test

    # Clean up after test
    if temp_config_file.exists():
        temp_config_file.unlink()
    # Reset config object again for safety between tests
    config.config = configparser.ConfigParser()


# --- Test config functions ---

def test_load_config_no_file(temp_config_file):
    """Test load_config creates default file if none exists."""
    from storyteller import config
    # Assertion should pass now as fixture doesn't create the file
    assert not temp_config_file.exists()
    # Call load_config explicitly
    config.load_config()
    assert temp_config_file.exists()
    # Check content matches defaults
    parser = configparser.ConfigParser()
    parser.read(temp_config_file)
    assert parser.has_section('General')
    assert parser.getboolean('General', 'show_welcome_on_startup') is True

def test_load_config_existing_file_complete(temp_config_file):
    """Test load_config reads existing complete file."""
    from storyteller import config
    # Create a sample config
    parser = configparser.ConfigParser()
    parser['General'] = {'show_welcome_on_startup': 'false'}
    parser['NewSection'] = {'key': 'value'}
    with open(temp_config_file, 'w') as f:
        parser.write(f)

    # Call load_config explicitly
    config.load_config()
    # Check that loaded config matches file content
    # Use the config module's functions which operate on the loaded config object
    assert config.get_bool_setting('General', 'show_welcome_on_startup') is False
    assert config.get_setting('NewSection', 'key') == 'value' # Added closing quote

def test_load_config_existing_file_partial(temp_config_file):
    """Test load_config adds missing defaults to existing file."""
    from storyteller import config
    # Create a sample partial config
    parser = configparser.ConfigParser()
    parser['General'] = {'some_other_setting': 'abc'} # Missing default key
    with open(temp_config_file, 'w') as f:
        parser.write(f)

    # Call load_config explicitly
    config.load_config()

    # Check that missing default was added to the *in-memory* config
    assert config.get_bool_setting('General', 'show_welcome_on_startup') is True
    assert config.get_setting('General', 'some_other_setting') == 'abc'

    # Verify the file *on disk* was updated because defaults were added
    parser_after = configparser.ConfigParser()
    parser_after.read(temp_config_file)
    # This assertion should now pass as save_config() should have been called within load_config()
    assert parser_after.has_option('General', 'show_welcome_on_startup')
    assert parser_after.getboolean('General', 'show_welcome_on_startup') is True
    assert parser_after.get('General', 'some_other_setting') == 'abc'


def test_save_defaults(temp_config_file):
    """Test save_defaults writes default settings."""
    from storyteller import config
    # File shouldn't exist initially
    assert not temp_config_file.exists()
    config.save_defaults()
    assert temp_config_file.exists()
    parser = configparser.ConfigParser()
    parser.read(temp_config_file)
    assert parser.has_section('General')
    assert parser.getboolean('General', 'show_welcome_on_startup') is True

def test_get_setting(temp_config_file):
    """Test get_setting retrieves values correctly."""
    from storyteller import config
    # Need to load defaults or set values first
    config.load_config() # Load defaults first
    config.set_setting('TestSection', 'testkey', 'testvalue')
    config.set_setting('General', 'show_welcome_on_startup', 'false') # Override default

    assert config.get_setting('TestSection', 'testkey') == 'testvalue'
    assert config.get_setting('General', 'show_welcome_on_startup') == 'false'
    # Test fallback for missing key (using default from DEFAULT_SETTINGS)
    assert config.get_setting('General', 'show_welcome_on_startup', fallback='ignored') == 'false'
    # Test fallback for missing section/key
    assert config.get_setting('MissingSection', 'missingkey') is None # Default fallback is None
    assert config.get_setting('MissingSection', 'missingkey', fallback='custom') == 'custom'
    # Test fallback using DEFAULT_SETTINGS value if key existed there (it doesn't here)
    assert config.get_setting('General', 'missing_general_key') is None # No default for this one

def test_set_setting(temp_config_file):
    """Test set_setting writes value and saves."""
    from storyteller import config
    # Assertion should pass now as fixture doesn't create the file
    assert not temp_config_file.exists()
    # Call set_setting, which should create/save the file
    config.set_setting('NewSection', 'newkey', 123) # Test non-string value
    assert temp_config_file.exists()

    parser = configparser.ConfigParser()
    parser.read(temp_config_file)
    assert parser.has_section('NewSection')
    assert parser.get('NewSection', 'newkey') == '123' # Value is saved as string

    # Test updating existing value
    config.set_setting('NewSection', 'newkey', 'updated')
    parser.read(temp_config_file) # Re-read the file
    assert parser.get('NewSection', 'newkey') == 'updated'

def test_get_bool_setting(temp_config_file):
    """Test get_bool_setting retrieves boolean values correctly."""
    from storyteller import config
    # Load defaults first to ensure 'General' section exists if needed
    config.load_config()
    config.set_setting('Flags', 'enabled', 'true')
    config.set_setting('Flags', 'disabled', 'False') # Test different case
    config.set_setting('Flags', 'numeric_true', 1)
    config.set_setting('Flags', 'numeric_false', 0) # configparser bool conversion

    assert config.get_bool_setting('Flags', 'enabled') is True
    assert config.get_bool_setting('Flags', 'disabled') is False
    assert config.get_bool_setting('Flags', 'numeric_true') is True
    assert config.get_bool_setting('Flags', 'numeric_false') is False

    # Test fallback for missing key (using default from DEFAULT_SETTINGS)
    # This should now work correctly as load_config() was called earlier
    assert config.get_bool_setting('General', 'show_welcome_on_startup') is True
    config.set_setting('General', 'show_welcome_on_startup', 'false')
    assert config.get_bool_setting('General', 'show_welcome_on_startup') is False

    # Test fallback for missing section/key
    assert config.get_bool_setting('MissingSection', 'missingkey') is False # Default fallback is False
    assert config.get_bool_setting('MissingSection', 'missingkey', fallback=True) is True

