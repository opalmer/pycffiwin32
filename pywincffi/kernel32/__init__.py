"""
Kernel32 Sub-Package
====================

Provides functions, constants and utilities that wrap functions provided by
``kernel32.dll``.
"""

# Our kernel32 package is broken into several submodules.  The functions
# we're wrapping are imported here so it's easier to access and because
# it's close to the way Windows would present them (as a single module)
from pywincffi.kernel32.file import ReadFile, WriteFile
from pywincffi.kernel32.handle import (
    CloseHandle, GetStdHandle, WaitForSingleObject, handle_from_file)
from pywincffi.kernel32.pipe import (
    CreatePipe, PeekNamedPipe, PeekNamedPipeResult, SetNamedPipeHandleState,
    CreateNamedPipe, GetNamedPipeHandleState)
from pywincffi.kernel32.process import (
    GetProcessId, GetCurrentProcess, OpenProcess, GetExitCodeProcess,
    pid_exists)
