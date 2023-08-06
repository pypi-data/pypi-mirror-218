"""Provides a common unit registry.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Final
import pint


#: A unit registry.
OUR: Final[pint.UnitRegistry] = pint.UnitRegistry()
