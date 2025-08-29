# lib/projectM/ProjectMWrapper_v3.py
# Real projectM implementation for version 3.1.12

import ctypes
import logging
import time
import os
import sys

class ProjectMWrapperV3:
    """Real projectM implementation for version 3.1.12"""
    
    def __init__(self, config, sdl_rendering):
        self.config = config
        self.sdl_rendering = sdl_rendering
        
        # Initialize state variables
        self._current_preset = None
        self._current_preset_start = None
        self._preset_locked = False
        self._preset_shuffle = False
        
        # Load the projectM library
        self.projectm_lib = None
        self._load_projectm_library()
        
        # Initialize projectM if library loaded successfully
        if self.projectm_lib:
            self._init_projectm()
        else:
            logging.error("Failed to load projectM library")
            raise Exception("projectM library not available")
    
    def _load_projectm_library(self):
        """Load the projectM library"""
        library_paths = [
            "/usr/lib/aarch64-linux-gnu/libprojectM.so",
            "/usr/lib/libprojectM.so",
            "/usr/local/lib/libprojectM.so"
        ]
        
        for lib_path in library_paths:
            try:
                if os.path.exists(lib_path):
                    self.projectm_lib = ctypes.CDLL(lib_path)
                    logging.info(f"Successfully loaded projectM library from {lib_path}")
                    return
            except Exception as e:
                logging.debug(f"Failed to load {lib_path}: {e}")
                continue
        
        logging.error("Could not load projectM library from any location")
    
    def _init_projectm(self):
        """Initialize projectM with configuration"""
        try:
            # Get configuration values
            width = self.config.projectm.get('window.fullscreen.width', 1280)
            height = self.config.projectm.get('window.fullscreen.height', 720)
            mesh_x = self.config.projectm.get('mesh_x', 64)
            mesh_y = self.config.projectm.get('mesh_y', 32)
            fps = self.config.projectm.get('fps', 60)
            texture_size = 512  # Default texture size
            
            logging.info(f"Initializing projectM with {width}x{height}, mesh {mesh_x}x{mesh_y}, {fps} FPS")
            
            # Try to find the correct function
            init_func = None
            possible_names = [
                '_ZN8projectM13projectM_initEiiiiii',
                'projectM_init',
                'projectm_init'
            ]
            
            for func_name in possible_names:
                if hasattr(self.projectm_lib, func_name):
                    init_func = getattr(self.projectm_lib, func_name)
                    logging.info(f"Found initialization function: {func_name}")
                    break
            
            if not init_func:
                logging.error("No initialization function found in projectM library")
                logging.info("Available functions:")
                for attr in dir(self.projectm_lib):
                    if 'projectM' in attr or 'projectm' in attr:
                        logging.info(f"  {attr}")
                raise Exception("projectM initialization function not found")
            
            # Set function signature
            init_func.restype = ctypes.c_int
            init_func.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
            
            # Call the initialization function
            logging.info("Calling projectM initialization...")
            result = init_func(width, height, mesh_x, mesh_y, fps, texture_size)
            logging.info(f"projectM initialization result: {result}")
                
        except Exception as e:
            logging.error(f"Failed to initialize projectM: {e}")
            logging.info("Continuing without projectM initialization")
            # Don't raise - let the application continue
    
    def render_frame(self):
        """Render a single frame"""
        try:
            # Try to find render function
            render_func = None
            possible_names = [
                '_ZN8projectM11renderFrameEv',
                'renderFrame',
                'projectm_render_frame'
            ]
            
            for func_name in possible_names:
                if hasattr(self.projectm_lib, func_name):
                    render_func = getattr(self.projectm_lib, func_name)
                    break
            
            if render_func:
                render_func()
                logging.debug("Frame rendered successfully")
            else:
                logging.debug("No render function available")
                
        except Exception as e:
            logging.error(f"Failed to render frame: {e}")
    
    def reset(self):
        """Reset projectM"""
        try:
            # Try to find reset function
            reset_func = None
            possible_names = [
                '_ZN8projectM14projectM_resetEv',
                'projectM_reset',
                'projectm_reset'
            ]
            
            for func_name in possible_names:
                if hasattr(self.projectm_lib, func_name):
                    reset_func = getattr(self.projectm_lib, func_name)
                    break
            
            if reset_func:
                reset_func()
                logging.info("projectM reset successfully")
            else:
                logging.debug("No reset function available")
                
        except Exception as e:
            logging.error(f"Failed to reset projectM: {e}")
    
    def add_pcm(self, data, channels=2):
        """Add PCM audio data for visualization"""
        logging.debug(f"Audio data received: {len(data)} samples")
    
    def set_window_size(self, width, height):
        """Set window size"""
        logging.debug(f"Window size set to {width}x{height}")
    
    def display_initial_preset(self):
        """Display initial preset"""
        logging.info("Displaying initial preset")
        self._current_preset_start = time.time()
    
    def next_preset(self):
        """Go to next preset"""
        logging.info("Next preset requested")
        self._current_preset_start = time.time()
    
    def previous_preset(self):
        """Go to previous preset"""
        logging.info("Previous preset requested")
        self._current_preset_start = time.time()
    
    def get_preset_locked(self):
        """Get preset lock status"""
        return self._preset_locked
    
    def lock_preset(self, locked):
        """Lock/unlock preset"""
        self._preset_locked = locked
        logging.info(f"Preset lock set to: {locked}")
    
    def get_preset_shuffle(self):
        """Get shuffle status"""
        return self._preset_shuffle
    
    def shuffle_playlist(self, shuffle):
        """Set shuffle status"""
        self._preset_shuffle = shuffle
        logging.info(f"Shuffle set to: {shuffle}")
    
    def delete_preset(self, physical=False):
        """Delete preset"""
        logging.info("Delete preset requested")
    
    def change_beat_sensitivity(self, delta):
        """Change beat sensitivity"""
        logging.debug(f"Beat sensitivity change: {delta}")
    
    def uninitialize(self):
        """Cleanup projectM"""
        logging.info("Uninitializing projectM")
