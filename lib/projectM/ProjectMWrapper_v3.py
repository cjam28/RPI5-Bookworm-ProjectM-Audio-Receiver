# lib/projectM/ProjectMWrapper_v3.py
# Compatibility layer for projectM version 3.1.12

import ctypes
import logging

class ProjectMWrapperV3:
    """Compatibility wrapper for projectM version 3.1.12"""
    
    def __init__(self, config, sdl_rendering):
        self.config = config
        self.sdl_rendering = sdl_rendering
        
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
