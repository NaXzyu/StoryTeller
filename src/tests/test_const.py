import pytest
from storyteller import const

def test_app_name():
    """Test the APP_NAME constant."""
    assert isinstance(const.APP_NAME, str)
    assert const.APP_NAME == "StoryTeller"

def test_config_dir_name():
    """Test the CONFIG_DIR_NAME constant."""
    assert isinstance(const.CONFIG_DIR_NAME, str)
    assert const.CONFIG_DIR_NAME == const.APP_NAME

def test_config_file_name():
    """Test the CONFIG_FILE_NAME constant."""
    assert isinstance(const.CONFIG_FILE_NAME, str)
    assert const.CONFIG_FILE_NAME == "config.ini"

