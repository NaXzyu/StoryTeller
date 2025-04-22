import configparser
import os
import sys # Import sys module
from pathlib import Path
# Import from new modules
from . import const
from . import paths

# Use path function to get the config file path
config_file_path = paths.get_config_file_path()

# Ensure the config directory exists (handled by get_config_dir in paths.py)
# paths.get_config_dir() # Call ensures directory creation if not already done

config = configparser.ConfigParser()

# Default settings (using const if needed, though not here currently)
DEFAULT_SETTINGS = {
    'General': {
        'show_welcome_on_startup': 'true',
    }
}

def load_config():
    """Loads configuration from the file, applying defaults if necessary."""
    # config_file_path is now defined globally using paths.get_config_file_path()
    if not config_file_path.exists():
        # Create default config if it doesn't exist
        save_defaults()
    else:
        config.read(config_file_path)
        # Ensure all default sections and options exist
        updated = False
        for section, options in DEFAULT_SETTINGS.items():
            if not config.has_section(section):
                config.add_section(section)
                updated = True
            for option, value in options.items():
                if not config.has_option(section, option):
                    config.set(section, option, value)
                    updated = True
        # Save potentially added defaults back to file only if changed
        if updated:
            save_config()


def save_config():
    """Saves the current configuration to the file."""
    # config_file_path is now defined globally using paths.get_config_file_path()
    try:
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    except IOError as e:
        # Handle potential errors during save (e.g., permissions)
        print(f"Error saving configuration to {config_file_path}: {e}", file=sys.stderr)


def save_defaults():
    """Saves the default settings to the config file."""
    global config
    config = configparser.ConfigParser() # Reset to defaults
    for section, options in DEFAULT_SETTINGS.items():
        config[section] = options
    save_config()

def get_setting(section, key, fallback=None):
    """Gets a setting value."""
    # Ensure config is loaded if it hasn't been read yet
    if not config.sections():
        load_config()
    # Provide fallback from DEFAULT_SETTINGS if key is missing
    default_fallback = DEFAULT_SETTINGS.get(section, {}).get(key)
    effective_fallback = fallback if fallback is not None else default_fallback
    return config.get(section, key, fallback=effective_fallback)

def set_setting(section, key, value):
    """Sets a setting value and saves the configuration."""
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, str(value)) # Ensure value is string
    save_config()

def get_bool_setting(section, key, fallback=False):
    """Gets a setting value as a boolean."""
    # Provide fallback from DEFAULT_SETTINGS if key is missing
    default_fallback = DEFAULT_SETTINGS.get(section, {}).get(key, str(fallback)).lower() == 'true'
    effective_fallback = fallback if fallback is not None else default_fallback
    return config.getboolean(section, key, fallback=effective_fallback)

# Load config on module import
load_config()
