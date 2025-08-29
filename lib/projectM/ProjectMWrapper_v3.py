# lib/projectM/ProjectMWrapper_v3.py
# Compatibility layer for projectM version 3.1.12

import ctypes
import logging
import time
import os

class ProjectMWrapperV3:
    """Compatibility wrapper for projectM version 3.1.12"""
    
    def __init__(self, config, sdl_rendering):
        self.config = config
        self.sdl_rendering = sdl_rendering
        
        # Initialize state variables
        self._current_preset = None
        self._current_preset_start = None
        self._preset_locked = False
        self._preset_shuffle = False
        
        # Load the projectM library
        try:
            self.projectm_lib = ctypes.CDLL("/usr/lib/aarch64-linux-gnu/libprojectM.so")
            logging.info("Successfully loaded projectM v3.1.12 library")
        except Exception as e:
            logging.error(f"Failed to load projectM library: {e}")
            raise
        
        # Set up function signatures for version 3.1.12
        self._setup_functions()
        
        # Initialize projectM
        self._init_projectm()
    
    def _setup_functions(self):
        """Set up function signatures for version 3.1.12"""
        try:
            # Main initialization function (different name in v3)
            self.projectm_lib.projectM_init.restype = ctypes.c_int
            self.projectm_lib.projectM_init.argtypes = [
                ctypes.c_int,  # width
                ctypes.c_int,  # height
                ctypes.c_int,  # mesh_x
                ctypes.c_int,  # mesh_y
                ctypes.c_int,  # fps
                ctypes.c_int   # texture_size
            ]
            
            # Reset function
            self.projectm_lib.projectM_reset.restype = None
            self.projectm_lib.projectM_reset.argtypes = []
            
            # Render frame function
            self.projectm_lib.renderFrame.restype = None
            self.projectm_lib.renderFrame.argtypes = []
            
            # Get mesh size function
            self.projectm_lib.getMeshSize.restype = None
            self.projectm_lib.getMeshSize.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
            
            # Audio processing function (if available)
            try:
                self.projectm_lib.addPCMFloat.restype = None
                self.projectm_lib.addPCMFloat.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int]
                logging.info("Audio processing function available")
            except:
                logging.warning("Audio processing function not available")
            
            logging.info("Successfully set up projectM v3.1.12 function signatures")
            
        except Exception as e:
            logging.error(f"Failed to set up function signatures: {e}")
            raise
    
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
            
            # Initialize projectM
            result = self.projectm_lib.projectM_init(
                width, height, mesh_x, mesh_y, fps, texture_size
            )
            
            if result == 0:
                logging.info("Successfully initialized projectM v3.1.12")
            else:
                logging.error(f"Failed to initialize projectM, result: {result}")
                raise Exception("projectM initialization failed")
                
        except Exception as e:
            logging.error(f"Failed to initialize projectM: {e}")
            raise
    
    def render_frame(self):
        """Render a single frame"""
        try:
            self.projectm_lib.renderFrame()
        except Exception as e:
            logging.error(f"Failed to render frame: {e}")
            raise
    
    def reset(self):
        """Reset projectM"""
        try:
            self.projectm_lib.projectM_reset()
            logging.info("projectM reset successfully")
        except Exception as e:
            logging.error(f"Failed to reset projectM: {e}")
            raise
    
    def add_pcm(self, data, channels=2):
        """Add PCM audio data for visualization"""
        try:
            if hasattr(self.projectm_lib, 'addPCMFloat'):
                # Convert data to float array
                float_data = (ctypes.c_float * len(data))(*data)
                self.projectm_lib.addPCMFloat(float_data, len(data))
        except Exception as e:
            logging.debug(f"Audio processing not available: {e}")
    
    def set_window_size(self, width, height):
        """Set window size (stub for compatibility)"""
        logging.debug(f"Window size set to {width}x{height}")
    
    def display_initial_preset(self):
        """Display initial preset (stub for compatibility)"""
        logging.info("Displaying initial preset")
        self._current_preset_start = time.time()
    
    def next_preset(self):
        """Go to next preset (stub for compatibility)"""
        logging.info("Next preset requested")
        self._current_preset_start = time.time()
    
    def previous_preset(self):
        """Go to previous preset (stub for compatibility)"""
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
        """Delete preset (stub for compatibility)"""
        logging.info("Delete preset requested")
    
    def change_beat_sensitivity(self, delta):
        """Change beat sensitivity (stub for compatibility)"""
        logging.debug(f"Beat sensitivity change: {delta}")
    
    def uninitialize(self):
        """Cleanup projectM"""
        logging.info("Uninitializing projectM")
