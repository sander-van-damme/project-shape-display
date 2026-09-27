+++
id = "M-001"
type = "mechanism"
name = "Travelling multi-row programming head"
status = "hypothesis"
domains = ["D-004", "D-006"]
functions = ["selection", "programming", "power-delivery"]
related_principles = ["P-001", "P-009"]
related_architectures = ["A-005"]
related_backlog = ["R01"]
related_tests = ["test09_test08_validation"]
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Travelling multi-row programming head

## Core principle
Move a shared head between row groups and change several rows and/or columns
during each dwell.

## What it solves well
Concentrates precision and active hardware in one serviceable assembly.

## What it does not solve
Passive height memory and load support still need another mechanism.

## Project evidence
Test09 screened 1–5 rows and 20/40/80 parallel columns. Four/five full-width
shared rows retain conditional timing windows, but selector cost and loaded
dynamics remain unqualified.

## Cheapest discriminating experiment
A 2×4 full-pitch dynamically selected head/latch coupon with measured loaded
engagement and repeatability.
