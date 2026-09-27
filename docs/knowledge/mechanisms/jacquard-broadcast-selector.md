+++
id = "M-002"
type = "mechanism"
name = "Jacquard-style broadcast selector"
status = "hypothesis"
domains = ["D-001"]
functions = ["selection", "addressing"]
related_principles = ["P-001", "P-003"]
related_architectures = ["A-002", "A-003"]
related_backlog = ["R02"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Jacquard-style broadcast selector

## Core principle
A pattern medium or selector layer decides which members of a repeated array
respond to one shared motion.

## What it solves well
Large-scale selection with little local power.

## What it does not solve
It does not inherently provide dynamic rewriting, 40 mm motion or load support.

## Cheapest discriminating experiment
A 5×5 selector coupon with adversarial adjacent patterns and one common stroke.
