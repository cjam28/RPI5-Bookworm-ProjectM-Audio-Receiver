#!/usr/bin/env python3
"""
ProjectM Audio Receiver - Main Entry Point
Raspberry Pi 5 + Bookworm Audio Manager with projectM Visualizations
"""

import sys
import os
import logging
from pathlib import Path

# Add the lib directory to Python path
lib_path = Path(__file__).parent / "lib"
sys.path.insert(0, str(lib_path))

def main():
    """Main application entry point"""
    try:
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Import and run the main application
        from controllers.main_controller import MainController
        controller = MainController()
        controller.run()
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        logging.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
