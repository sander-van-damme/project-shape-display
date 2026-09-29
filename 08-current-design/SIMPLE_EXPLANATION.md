# Simple explanation of the current design

> **Start here if you want to understand the machine without reading the engineering documentation.**
>
> This page explains what the S5-R shape display does, how it works mechanically, what you can use it for, and what is still unproven.

## The idea in one sentence

The display is an **80 × 80 field of 6,400 small vertical columns**. Each column can sit at one of **five heights**, and instead of putting a motor under every column, the machine uses a **shared programming mechanism** to give every column a mechanical "memory" of the height it should stop at.

Then one common lifting plate moves the whole field.

That is the main trick of the design.

## What you get

- **Surface:** about 40.6 × 40.6 cm
- **Resolution:** 80 × 80 = 6,400 movable cells
- **Cell spacing:** 5.08 mm
- **Vertical range:** 40 mm
- **Height levels:** 5 positions, approximately 0 / 10 / 20 / 30 / 40 mm
- **Calculated full-map change time:** about **24.6 seconds**
- **Purchased actuators:** 2 shared bank motors + 40 small writer solenoids
- **Calculated delivered BOM:** about **$404.60**

So, for example, a computer could describe a terrain map as 6,400 numbers from 0 to 4, and the machine would physically turn that into a relief surface.

## The easiest mental model

Think of every cell as having two separate jobs:

1. **Remember a height**
2. **Move to that height**

The machine separates those jobs.

The small mechanism inside each cell remembers the desired height **passively**, using a five-position rotary part. It does not need its own motor.

A shared mechanism first goes through the display and programs those rotary parts. After that, a large common platen lifts the columns and lets each one stop at the height stored in its rotary mechanism.

This is why the machine can control 6,400 cells without 6,400 motors.

## What is inside one cell?

The important parts are:

- **Column** — the visible vertical pin that forms the surface.
- **Rotor / stepped cam** — a tiny rotating five-position part that represents the requested height.
- **Drive pawl** — can temporarily connect that rotor to the shared rack.
- **Keeper** — decides whether the pawl engages.
- **Detent leaf** — helps the rotor stay in the selected position.

The rotor is basically a tiny **five-position mechanical memory**.

When the rotor is turned to another position, the column will later stop at a different height.

## How a new shape is created

### 1. The computer has a height map

Conceptually the input is an 80 × 80 grid.

Each cell asks for one of five levels:

```text
0 = lowest
1
2
3
4 = highest
```

The current repository defines the mechanism and timing for this, but there is not yet a finished end-user map editor / control application in `08-current-design`.

### 2. The writer programs the mechanical memories

The machine does **not** move every column separately with its own motor.

Instead, a shared writer mechanism works across groups of cells.

It has:

- **40 solenoids**, which choose which pawls are allowed to engage;
- a shared rack and steel drive rod;
- **2 bank motors**, which drive that rack.

Selected pawls connect their rotors to the moving rack. Those rotors turn until they reach the requested one of the five positions. Cells that are not selected remain mechanically disconnected and do not change.

This process is repeated until the required rotor positions are stored across the field.

### 3. The common platen moves the columns

Under the field is a common lifting platen.

After the rotor settings have been programmed, the platen makes one vertical stroke:

1. the platen raises the columns;
2. the programmed stepped rotors determine where each column is allowed to settle;
3. the platen lowers;
4. every column remains at its selected height.

The **hard mechanical stop** supports the terrain load. The solenoids and bank motors do not need to continuously hold all 6,400 columns in place.

## What does "R = 4" mean?

This is easy to misread.

**R = 4 does NOT mean four height levels.**

There are **five height levels**.

R = 4 means the shared programming bank handles **four rows of the display as one bank**. This is a timing optimisation: processing several rows in one bank is what brings the calculated complete update below 30 seconds.

## Why only 42 actuators for 6,400 cells?

Because the actuators are used for **programming**, not for permanently driving each cell.

A conventional approach might put a motor on every cell or on every column channel. That becomes very expensive very quickly.

S5-R instead uses:

- 40 small solenoids to select cells in the shared writer,
- 2 shared motors to supply movement,
- thousands of cheap passive printed mechanisms to remember the result.

Once programmed, each cell holds its state mechanically.

## What could you use it for?

The intended result is a programmable physical relief surface.

For a tabletop game such as D&D, for example, you could use it to change the physical terrain between scenes:

- raise hills or ridges;
- create depressions or stepped elevation;
- raise walls, platforms or obstacles;
- load a different terrain height map without manually rebuilding the board.

The important limitation is that this is a **five-level stepped surface**, not a smooth continuously variable surface. The full 40 mm range is divided into roughly 10 mm increments.

A complete worst-case map change is calculated at about **24.6 seconds**, so the design is aimed at scene changes rather than high-frame-rate animation.

## Can only part of the board change?

In principle, yes.

The height choice is stored locally in each cell, so cells outside the region being reprogrammed can keep their existing rotor state.

The shared platen still performs a lift/lower stroke for an update, but the writer only needs to rewrite the affected portion instead of programming the entire 80-row field.

## What physically holds a column up?

Not the solenoid.

Not a motor.

The selected position of the stepped rotor forms a **hard mechanical stop**. When the platen lowers, the column settles onto that stop.

That is important because it means the machine does not need 6,400 powered holding actuators.

## What has actually been designed already?

The current design folder is much more than a concept sketch.

It contains:

- the mechanical definition;
- OpenSCAD geometry;
- **14 distinct printable part types**;
- generated STL files;
- print instructions;
- an assembly manifest;
- a purchased-parts BOM;
- renders of the complete machine and the per-cell mechanism;
- analytic timing, force, clearance and cost checks.

Useful starting points:

- [Full-machine and mechanism renders](fabrication/images/README.md)
- [Printing guide](fabrication/README.md)
- [Print manifest](fabrication/manifests/print_manifest.md)
- [Assembly manifest](fabrication/manifests/assembly_manifest.md)
- [Full technical design document](README.md)

If you only want to understand what the machine looks like, open the **renders first**.

## What is NOT proven yet?

This distinction matters.

The design is **CAD + calculation**, not a tested physical machine.

No complete S5-R has yet been printed and measured.

The remaining uncertainties are mainly things that simulation cannot settle reliably:

- real friction between printed parts;
- wear, creep and fatigue of the small printed keeper/detent features;
- how reliably every keeper sets in a real print;
- the real loaded torque/speed behaviour of the bank motors.

So "printable" in the repository means **the CAD and generated STLs pass the defined fabrication checks**. It does not yet mean that a physical prototype has demonstrated the complete mechanism.

I also do not see a finished user-facing firmware/UI package in `08-current-design` yet. The current folder is primarily the **mechanical machine definition and fabrication package**.

## If you wanted to build it today

The practical route is:

1. Look at the [full-machine renders](fabrication/images/README.md) so the layout makes sense.
2. Read the [fabrication README](fabrication/README.md).
3. Slice the committed STLs according to the [print manifest](fabrication/manifests/print_manifest.md).
4. Source the purchased parts from the BOM.
5. Assemble in the order in the [assembly manifest](fabrication/manifests/assembly_manifest.md).
6. Test the still-unproven physical behaviours before assuming the complete 80 × 80 machine will work reliably.
7. Add the actual controller firmware / map-loading interface needed to turn an 80 × 80 height map into the bank/writer motion sequence.

## In one picture

```text
HEIGHT MAP FROM COMPUTER
        |
        v
+-------------------------+
| shared writer mechanism |
| 40 solenoids            |
| 2 bank motors           |
+-------------------------+
        |
        | programs each cell's
        | 5-position mechanical memory
        v
+------------------------------------+
| 80 x 80 passive rotor mechanisms   |
| one mechanical height state / cell |
+------------------------------------+
        |
        | common lift/lower stroke
        v
+------------------------------------+
| 6,400 vertical columns             |
| form the physical relief surface   |
+------------------------------------+
```

The key idea to remember is:

> **The shared mechanism chooses the height; the passive mechanism remembers it; the common platen performs the vertical movement.**
