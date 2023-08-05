#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.cli.vt100
      @file: vt_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import logging as log
import sys
from typing import Any

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.terminal import Terminal
from hspylib.modules.cli.vt100.vt_100 import Vt100


def erase_line(mode: int = 2) -> None:
    """Erase current line keeping the cursor on the same position.
    - mode(0): Erase line from cursor right.
    - mode(1): Erase line from cursor left.
    - mode(2): Erase the entire line.
    :param mode: the erase mode. One of [0,1,2]
    """
    sysout(f"%EL{mode}%\r", end="")


def erase_screen(mode: int = 2) -> None:
    """Erase portions of the screen keeping the cursor on the same position.
    - mode(0): Erase screen from cursor down.
    - mode(1): Erase screen from cursor up.
    - mode(2): Erase the entire screen.
    :param mode: the erase mode. One of [0,1,2]
    """
    sysout(f"%ED{mode}%\r", end="")


def save_cursor() -> None:
    """Save current cursor position and attributes."""
    sysout(Vt100.save_cursor(), end="")


def restore_cursor() -> None:
    """Restore cursor to the saved position and attributes."""
    sysout(Vt100.restore_cursor(), end="")


def alternate_screen(enable: bool = True) -> None:
    """Switch to the alternate screen buffer.
    :param enable: alternate enable on/off.
    """
    sysout(f"%SC{'A' if enable else 'M'}%", end="")


def exit_app(exit_code: int = None, frame: Any = None, exit_msg: str = "") -> None:
    """Exit the application. Commonly called by hooked signals."""
    Terminal.restore()
    log.debug("Application exited with code=%d frame=%s", exit_code, repr(frame))
    sysout(f"%MOD(0)%" f"{exit_msg}")
    sys.exit(exit_code)
