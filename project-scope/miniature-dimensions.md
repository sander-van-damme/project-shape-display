# D&D miniature dimensions and vertical-travel target

Research checked **27 September 2026**.

## What "standard miniature height" means

There is no single exact height shared by every Dungeons & Dragons miniature.
Miniature "scale" is a reference size, and the final physical height changes
with race, pose, weapons, hats, wings, scenic bases and sculpting style.

Useful current references:

- WizKids describes its D&D Icons of the Realms Yawning Portal environment as
  **28 mm scale** and says it works with existing D&D Icons of the Realms
  miniatures and sets.
- Modern tabletop/RPG miniature sellers also commonly use **32 mm scale**.
  A current scale guide aimed at D&D/RPG play describes a human-sized 32 mm
  character as typically about **28–35 mm** tall, depending on sculpt and
  measurement convention.
- Scale labels are not maximum overall heights. Raised weapons and poses can
  extend above the nominal figure height, and larger D&D creatures can be far
  taller than a player-character miniature. For example, WizKids' Gargantuan
  Tarrasque is advertised as more than 11 inches tall.

Sources:

- https://wizkids.com/dd-icons-of-the-realms-the-yawning-portal-inn/
- https://novanvil.com/pages/miniature-scale-guide
- https://wizkids.com/dd-nolzurs-marvelous-miniatures-gargantuan-tarrasque/

## Engineering interpretation for this project

The terrain display should not attempt to match the height of the largest monster
miniature. The vertical-travel requirement is intended to give a meaningful
terrain step comparable to a **normal human-sized player/NPC miniature**.

Use the following project rule:

- **Minimum provisional usable vertical travel: 40 mm.**
- 40 mm is intentionally above the common 28–35 mm human-sized figure range and
  leaves some margin for bases, headgear and sculpt variation.
- A design does **not** become qualified solely because it has 40 mm nominal
  geometry. Before claiming compliance, measure at least one representative
  physical D&D player-character/NPC miniature from the bottom of its base to its
  highest normal body/head feature and record the model and measured height.
- If the measured representative miniature exceeds 40 mm, increase the required
  travel and rerun timing, load, packaging and structural calculations.
- Oversized monsters, raised weapons, wings and display poses are useful
  usability cases but are not the reference that sets minimum terrain travel.

This keeps the current test08 40 mm assumption as a reasonable provisional
target while converting it from an arbitrary number into a sourced design rule.
