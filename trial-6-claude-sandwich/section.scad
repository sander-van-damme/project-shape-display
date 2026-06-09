include <test-strip.scad>
intersection() {
    assembly(lifts = [0, 2, 5, 6, 3]);
    translate([-60, 0, -10]) cube([200, 60, 120]);
}
