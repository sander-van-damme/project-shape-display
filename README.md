# shape display
A shape display designed for viewing table-top battle maps.

## design
The shape display consists of threaded rods with cubes in a 60 by 60 grid.
These are actuated from underneath, by an array of 60 stepper motors that set the height of every cube row by row.

## planning
1. design the threaded rods and cubes
2. design the actuation layer
3. design the case and cooling
4. design the MVP controller
5. design the web controller
6. design the 2D to 3D converter

## components
### stepper motor
Generic micro stepper motor from [Aliexpress](https://nl.aliexpress.com/item/4000806393169.html) at €0.52 per pair (see also listing on [Amazon](https://www.amazon.com/Abovehill-Stepper-2-Phase-4-Wire-Connection/dp/B08346RFVZ)).


| specifications | |
|-----|------|
| wiring | two phases, four wires|
| resistance | 40 Ω |
| recommended voltage | 5-6V |
| driving current | 0.12A |
| short-circuit current | 0.14A |
| connection lines 1 | blue: A +, black: A-, red: B+, white: B- |
| connection lines 2 | purple: A +, yellow: B-, orange: B+, green: B- |

![](./images/stepper-motor-dimensions.jpg)
(output shaft diameter: 1.5mm)

### stepper motor driver
TMC2208 from [Aliexpress](https://nl.aliexpress.com/item/1005004014058136.html) at €2.04 per piece.

| specifications | |
|-----|------|
| model | MC2208 V1.2 |
| motor voltage range (VM) | 4.75V-36V |
| motor continuous current | 1.4A |
| motor peak current | 2A |
| logic voltage range (VIO) | 3-5V |
| microsteps | 256 |
