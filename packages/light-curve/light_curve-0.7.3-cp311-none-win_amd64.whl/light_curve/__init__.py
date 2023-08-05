

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_8():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'light_curve.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


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
