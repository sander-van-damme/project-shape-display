difference() {
	cube(size = [5.0, 5.0, 50.0]);
	translate(v = [2.5, 0.1, 25.0]) {
		resize(newsize = [2.5, 0, 5.0]) {
			rotate(a = [90, 0, 0]) {
				linear_extrude(height = 1.0) {
					text(direction = "ttb", size = 10, text = "5.00");
				}
			}
		}
	}
}
