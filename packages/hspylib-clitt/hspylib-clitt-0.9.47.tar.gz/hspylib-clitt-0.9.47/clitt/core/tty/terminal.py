#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.cli.vt100
      @file: terminal.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import logging as log
import os
import platform
import re
import select
import shlex
import signal
import subprocess
import sys
import termios
import tty
from abc import ABC
from shutil import get_terminal_size
from typing import Optional, Tuple

from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import NotATerminalError
from hspylib.core.tools.commons import is_debugging
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_100 import Vt100


class Terminal(ABC):
    """Utility class to provide terminal features."""

    @staticmethod
    def is_a_tty() -> bool:
        return sys.stdout.isatty()

    @staticmethod
    def clear() -> None:
        """Clear terminal and move the cursor to HOME position (0, 0)."""
        sysout("%ED2%%HOM%", end="")

    @staticmethod
    def shell_exec(cmd_line: str, **kwargs) -> Tuple[Optional[str], ExitStatus]:
        """Execute command with arguments and return it's run status."""
        try:
            if "stdout" in kwargs:
                del kwargs["stdout"]  # Deleted since we use our own stream
            if "stderr" in kwargs:
                del kwargs["stderr"]  # Deleted since we use our own stream
            log.info("Executing shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            output = subprocess.check_output(cmd_args, **kwargs).decode(Charset.UTF_8.val)
            log.info("Execution result: %s", ExitStatus.SUCCESS)
            return output.strip() if output else None, ExitStatus.SUCCESS
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)
            return None, ExitStatus.FAILED

    @staticmethod
    def shell_poll(cmd_line: str, **kwargs) -> None:
        """Execute command with arguments and continuously poll it's output."""
        if "stdout" in kwargs:
            del kwargs["stdout"]  # Deleted since we use our own stream
        if "stderr" in kwargs:
            del kwargs["stderr"]  # Deleted since we use our own stream
        try:
            log.info("Polling shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            with subprocess.Popen(
                cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, **kwargs) as proc:
                process = select.poll()
                process.register(proc.stdout)
                process.register(proc.stderr)
                while not Keyboard.kbhit():
                    if poll_obj := process.poll(0.5):
                        line = proc.stdout.readline()
                        sysout(line.decode(Charset.UTF_8.val) if isinstance(line, bytes) else line.strip(), end='')
                        log.debug("Polling returned: %s", str(poll_obj))
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (InterruptedError, KeyboardInterrupt):
            log.warning("Polling process has been interrupted command='%s'", cmd_line)
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)

    @staticmethod
    def open(filename: str) -> None:
        """Open the specified file using the default editor."""
        my_os = os.environ.get("HHS_MY_OS", platform.system())
        if "Darwin" == my_os:
            Terminal.shell_exec(f"open {filename}")
        elif "Linux" == my_os:
            Terminal.shell_exec(f"xdg-open {filename}")
        else:
            raise NotImplementedError(f"OS '{my_os}' is not supported")

    @classmethod
    def exit(
        cls,
        exit_msg: str | None = "") -> None:
        """Exit the application. Commonly called by hooked signals.
        :param exit_msg: the exiting message to be displayed.
        """
        cls.restore()
        sysout(f"%MOD(0)%" f"{exit_msg}")

    @classmethod
    def restore(cls) -> None:
        """Clear the terminal and restore default attributes [wrap,cursor,echo]."""
        cls.set_attributes(show_cursor=True, auto_wrap=True, enable_echo=True)

    @classmethod
    def get_dimensions(cls, fallback: Tuple[int, int] = (24, 80)) -> Tuple[int, int]:
        """Retrieve the size of the terminal.
        :return lines, columns
        """
        if not sys.stdout.isatty():
            log.error(NotATerminalError("screen_size:: Requires a terminal (TTY)"))
            return fallback
        dim = get_terminal_size((fallback[1], fallback[0]))
        return dim.lines, dim.columns

    @classmethod
    def get_cursor_position(cls, fallback: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        """Get the terminal cursor position.
        :return line, column
        """
        pos, buf = fallback, ""

        if not cls.is_a_tty():
            log.error(NotATerminalError("get_cursor_position:: Requires a terminal (TTY)"))
            return pos

        if is_debugging():
            return pos

        stdin = sys.stdin.fileno()  # Get the stdin file descriptor.
        attrs = termios.tcgetattr(stdin)  # Save terminal attributes.

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write(Vt100.get_cursor_pos())
            sys.stdout.flush()
            while not buf or buf[-1] != "R":
                buf += sys.stdin.read(1)
            if matches := re.match(r"^\x1b\[(\d*);(\d*)R", buf):  # If the response is 'Esc[r;cR'
                groups = matches.groups()
                pos = int(groups[0]), int(groups[1])
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, attrs)  # Reset terminal attributes

        return pos

    @classmethod
    def set_enable_echo(cls, enabled: bool = True) -> None:
        """Enable echo in the terminal.
        :param enabled: whether is enabled or not.
        """
        if not cls.is_a_tty():
            log.error(NotATerminalError("set_enable_echo:: Requires a terminal (TTY)"))
            return

        os.popen(f"stty {'echo -raw' if enabled else 'raw -echo min 0'}").read()

    @classmethod
    def set_auto_wrap(cls, auto_wrap: bool = True) -> None:
        """Set auto-wrap mode in the terminal.
        :param auto_wrap: whether auto_wrap is set or not.
        """
        if not cls.is_a_tty():
            log.warning(NotATerminalError("set_enable_echo:: Requires a terminal (TTY)"))
            return

        sysout(Vt100.set_auto_wrap(auto_wrap), end="")

    @classmethod
    def set_show_cursor(cls, show_cursor: bool = True) -> None:
        """Show or hide cursor in the terminal.
        :param show_cursor: whether to show or hide he cursor.
        """
        if not cls.is_a_tty():
            log.warning(NotATerminalError("set_enable_echo:: Requires a terminal (TTY)"))
            return

        sysout(Vt100.set_show_cursor(show_cursor), end="")

    @classmethod
    def set_attributes(cls, **attrs) -> None:
        """Wrapper to set all terminal attributes at once."""
        # fmt: off
        enable_echo = attrs['enable_echo']
        auto_wrap   = attrs['auto_wrap']
        show_cursor = attrs['show_cursor']
        # fmt: on
        if enable_echo is not None:
            cls.set_enable_echo(enable_echo)
        if auto_wrap is not None:
            cls.set_auto_wrap(auto_wrap)
        if show_cursor is not None:
            cls.set_show_cursor(show_cursor)
