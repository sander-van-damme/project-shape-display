// Parameters
frame_width = 25.4 + 10;      // Total width of the frame
frame_height = 60;     // Height of the frame
frame_depth = 5;       // Depth (thickness) of the frame
beam_thickness = 5;    // Thickness of the frame beams
slit_depth = 1.5;         // Depth of the slit into the beams
slit_width = 1.1;         // Width of the slit (for the glass pane)
extra = 0.1;            // Small extension to avoid overlapping faces

// Main Module
difference() {
    frame();
    slits();
}

// Frame Module: Creates the U-shaped frame
module frame() {
    union() {
        // Left vertical beam
        cube([beam_thickness, frame_height, frame_depth]);
        
        // Bottom horizontal beam
        cube([frame_width, beam_thickness, frame_depth]);
        
        // Right vertical beam
        translate([frame_width - beam_thickness, 0, 0])
            cube([beam_thickness, frame_height, frame_depth]);
    }
}

// Slits Module: Creates the continuous slit along the inner faces
module slits() {
    // Left vertical beam slit
    translate([beam_thickness - slit_depth - extra, -extra, (frame_depth - slit_width)/2 - extra])
        cube([slit_depth + extra*2, frame_height + extra*2, slit_width + extra*2]);
    
    // Right vertical beam slit
    translate([frame_width - beam_thickness, -extra, (frame_depth - slit_width)/2 - extra])
        cube([slit_depth + extra*2, frame_height + extra*2, slit_width + extra*2]);
    
}
