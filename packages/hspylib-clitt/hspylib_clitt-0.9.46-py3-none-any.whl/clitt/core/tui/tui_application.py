#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import os
import sys

from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

from clitt.core.tui.tui_screen import TUIScreen


class TUIApplication(Application, metaclass=AbstractSingleton):
    """Terminal UI application base class."""

    def __init__(
        self,
        name: str | None,
        version: Version = Version.initial(),
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: str = None,
        log_dir: str = None):

        super().__init__(name, version, description, usage, epilog, resource_dir, log_dir)
        self._screen = TUIScreen.INSTANCE or TUIScreen()
        self._app_name = os.path.basename(sys.argv[0]) if name is None else name

    @property
    def screen(self) -> TUIScreen():
        return self._screen

    @property
    def cursor(self) -> TUIScreen.Cursor:
        return self.screen.cursor

    def _setup_arguments(self) -> None:
        pass

    def _main(self, *params, **kwargs) -> ExitStatus:
        pass

    def _cleanup(self) -> None:
        if self.screen.alternate and self._exit_code == ExitStatus.SUCCESS:
            self.screen.alternate = not self.screen.alternate
