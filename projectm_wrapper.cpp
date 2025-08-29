#include <projectM.hpp>
#include <cstring>

extern "C" {
    // Global projectM instance
    static projectM* g_projectm = nullptr;
    
    // Initialize projectM
    int projectm_init(int width, int height, int mesh_x, int mesh_y, int fps, int texture_size) {
        try {
            if (g_projectm) {
                delete g_projectm;
            }
            
            // Create projectM instance
            g_projectm = new projectM();
            
            // Set basic parameters
            g_projectm->projectM_init(width, height, mesh_x, mesh_y, fps, texture_size);
            
            return 0; // Success
        } catch (...) {
            return -1; // Error
        }
    }
    
    // Render frame
    void projectm_render_frame() {
        if (g_projectm) {
            g_projectm->renderFrame();
        }
    }
    
    // Reset projectM
    void projectm_reset() {
        if (g_projectm) {
            g_projectm->projectM_reset();
        }
    }
    
    // Cleanup
    void projectm_cleanup() {
        if (g_projectm) {
            delete g_projectm;
            g_projectm = nullptr;
        }
    }
}
