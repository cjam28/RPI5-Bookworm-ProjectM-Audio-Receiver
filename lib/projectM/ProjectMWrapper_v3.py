# lib/projectM/ProjectMWrapper_v3.py
# Python-only compatibility layer for projectM version 3.1.12

import ctypes
import logging
import time
import os
import sys

class ProjectMWrapperV3:
    """Python-only compatibility wrapper for projectM version 3.1.12"""
    
    def __init__(self, config, sdl_rendering):
        self.config = config
        self.sdl_rendering = sdl_rendering
        
        # Initialize state variables
        self._current_preset = None
        self._current_preset_start = None
        self._preset_locked = False
        self._preset_shuffle = False
        
        # Try to load the projectM library with different approaches
        self.projectm_lib = None
        self._load_projectm_library()
        
        # Initialize projectM if library loaded successfully
        if self.projectm_lib:
            self._init_projectm()
        else:
            logging.warning("projectM library not available - running in demo mode")
    
    def _load_projectm_library(self):
        """Try different ways to load the projectM library"""
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
        if not self.projectm_lib:
            logging.warning("Skipping projectM initialization - library not available")
            return
            
        try:
            # Get configuration values
            width = self.config.projectm.get('window.fullscreen.width', 1280)
            height = self.config.projectm.get('window.fullscreen.height', 720)
            mesh_x = self.config.projectm.get('mesh_x', 64)
            mesh_y = self.config.projectm.get('mesh_y', 32)
            fps = self.config.projectm.get('fps', 60)
            
            logging.info(f"Initializing projectM with {width}x{height}, mesh {mesh_x}x{mesh_y}, {fps} FPS")
            
            # For now, just log the initialization
            # We'll implement actual initialization when we figure out the correct function calls
            logging.info("projectM initialization completed (demo mode)")
                
        except Exception as e:
            logging.error(f"Failed to initialize projectM: {e}")
            logging.info("Continuing in demo mode")
    
    def render_frame(self):
        """Render a single frame"""
        if not self.projectm_lib:
            # Demo mode - just log that we're rendering
            logging.debug("Demo mode: rendering frame")
            return
            
        try:
            # Try to call renderFrame if available
            if hasattr(self.projectm_lib, 'renderFrame'):
                self.projectm_lib.renderFrame()
            else:
                logging.debug("renderFrame function not available")
        except Exception as e:
            logging.error(f"Failed to render frame: {e}")
    
    def reset(self):
        """Reset projectM"""
        if not self.projectm_lib:
            logging.info("Demo mode: projectM reset requested")
            return
            
        try:
            if hasattr(self.projectm_lib, 'projectM_reset'):
                self.projectm_lib.projectM_reset()
                logging.info("projectM reset successfully")
            else:
                logging.debug("projectM_reset function not available")
        except Exception as e:
            logging.error(f"Failed to reset projectM: {e}")
    
    def add_pcm(self, data, channels=2):
        """Add PCM audio data for visualization (stub for compatibility)"""
        logging.debug(f"Audio data received: {len(data)} samples")
    
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
