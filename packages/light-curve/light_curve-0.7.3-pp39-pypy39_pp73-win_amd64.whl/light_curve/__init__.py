

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_8():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'light_curve.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-light_curve-0.7.3')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-light_curve-0.7.3')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not ctypes.windll.kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError()))


_delvewheel_init_patch_1_3_8()
del _delvewheel_init_patch_1_3_8
# end delvewheel patch

# Import all Python features
from .light_curve_py import *

# Hide Python features with Rust equivalents
from .light_curve_ext import *

# Hide Rust Extractor with universal Python Extractor
from .light_curve_py import Extractor

from .light_curve_ext import __version__
