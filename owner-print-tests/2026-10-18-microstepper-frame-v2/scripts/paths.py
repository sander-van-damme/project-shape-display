"""Locations within this print pack; scripts may be run from any directory."""
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent.parent
CAD = TEST_DIR / 'cad'
COMPONENTS = TEST_DIR / 'components'
METADATA = TEST_DIR / 'metadata'
IMAGES = TEST_DIR / 'images'
