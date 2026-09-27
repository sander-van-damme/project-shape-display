/*
* Set drawing parameters
*/
spacing = 4.64;
wall = 0.44;
height = 25.4 * 2 + 5;
rows = 45;
cols = 45;

/*
* Draw horizontal cuboids for rows
*/
for (y = [0:rows]) {
    translate([0, y * (spacing + wall), 0])
    cube([cols * (spacing + wall) + wall, wall, height]);
}

/*
* Draw vertical cuboids for columns
*/
for (x = [0:cols]) {
    translate([x * (spacing + wall), 0, 0])
    cube([wall, rows * (spacing + wall) + wall, height]);
}
