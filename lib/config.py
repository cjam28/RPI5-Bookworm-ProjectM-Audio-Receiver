import os
import sys
import traceback
import logging

from configparser import ConfigParser, RawConfigParser

# Get the app root directory more reliably
def get_app_root():
    """Get the application root directory more reliably."""
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'),  # lib/..
        os.path.join(os.getcwd(), 'conf'),  # current_working_dir/conf
        '/app/conf',  # Docker container path
        '/app/lib/conf',  # Alternative Docker path
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            return path
    
    # Fallback to current directory
    return os.getcwd()

APP_ROOT = get_app_root()

class Config:
    """Configuration class for loading and managing application settings.
    @param config_path: path to the configuration file.
    @param config_header: optional header to prepend to the configuration file.
    """
    def __init__(self, config_path, config_header=None):
        # Initialize with default values
        self.general = {
            'log_level': logging.INFO,
            'plugin_ctrl': True,
            'audio_mode': 'automatic'
        }
        
        self.projectM = {
            'preset_path': '/app/resources/presets',
            'texture_path': '/app/resources/textures',
            'fps': 30,
            'mesh_x': 64,
            'mesh_y': 32,
            'hard_cuts_enabled': True,
            'hard_cut_duration': 30
        }
        
        self.audio = {
            'default_sample_rate': 44100,
            'default_sample_format': 's16le',
            'resample_method': 'soxr-vhq',
            'avoid_resampling': True
        }
        
        try:
            # Try to load the configuration file
            if not os.path.exists(config_path):
                logging.warning(f"Configuration file not found: {config_path}")
                logging.info(f"Using default configuration values")
                return
            
            if config_header:
                config = RawConfigParser(allow_no_value=True)
                with open(config_path) as config_file:
                    data = config_file.read()
                    config.read_string(config_header + '\n' + data)
            else:
                config = ConfigParser(allow_no_value=True)
                config.read(config_path)

            # Load configuration sections
            for section in config.sections():
                if not hasattr(self, section):
                    setattr(self, section, dict())
                
                section_dict = getattr(self, section)
                
                for name, str_value in config.items(section):
                    try:
                        if name == "audio_plugins":
                            value = config.get(section, name).split(",")
                        elif name == "audio_cards":
                            value = config.get(section, name).split(",")
                        elif name == "audio_sinks":
                            value = config.get(section, name).split(",")
                        elif name == "audio_sources":
                            value = config.get(section, name).split(",")
                        elif name == "card_profile_types":
                            value = config.get(section, name).split(",")
                        elif name == "card_profile_modes":
                            value = config.get(section, name).split(",")
                        elif self._is_str_bool(str_value):
                            value = config.getboolean(section, name)
                        elif self._is_str_int(str_value):
                            value = config.getint(section, name)
                        elif self._is_str_float(str_value):
                            value = config.getfloat(section, name)
                        else:
                            value = config.get(section, name)

                        section_dict[name] = value
                        
                    except Exception as e:
                        logging.warning(f"Error parsing config value {section}.{name}: {e}")
                        continue

            logging.info(f"Configuration loaded successfully from: {config_path}")
            logging.info(f"Available sections: {list(config.sections())}")

        except Exception as e:
            logging.error(f"Error loading configuration file: {e}")
            logging.warning("Using default configuration values")
            traceback.print_exc()
            # Don't exit, just continue with defaults
    
    def get(self, section, key, default=None):
        """Get a configuration value with fallback to default."""
        try:
            section_dict = getattr(self, section, {})
            return section_dict.get(key, default)
        except:
            return default
    
    def has_section(self, section):
        """Check if a configuration section exists."""
        return hasattr(self, section) and isinstance(getattr(self, section), dict)
    
    """Check if string is a boolean.
    @param value: object to be verified.
    """
    def _is_str_bool(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return True

        return False
    
    """Check if string is an float.
    @param value: object to be verified.
    """
    def _is_str_float(self, value):
        try:
            float(value)
            return True
        except:
            return False
        
    """Check if string is an integer.
    @param value: object to be verified.
    """
    def _is_str_int(self, value):
        try:
            int(value)
            return True
        except:
            return False
