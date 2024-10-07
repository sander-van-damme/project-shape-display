"""
© 2024 Sander Van Damme - All Rights Reserved.

This scripts provides helper functions to retrieve the dimensions of the shape display.
"""

from environs import Env
from solid2 import cube

# Initialize the environment variables
env = Env()
env.read_env()


def cuboid_width():
    return env.float("CUBOID_WIDTH")


def cuboid_depth():
    return cuboid_width()


def cuboid_height():
    return env.float("CUBOID_HEIGHT")
