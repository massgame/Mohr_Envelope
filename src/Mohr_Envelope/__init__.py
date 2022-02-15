# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-01-08
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #
import sys


# Check python compatibility before proceeding
try:
    assert sys.version_info >= (3, 5) and sys.version_info <= (3, 9)
    print("Python Version: %s" % sys.version.split('\n')[0])
except AssertionError:
    print("Python Version: %s" % sys.version.split('\n')[0])
    exit("Compatible Python Version 3.5+ upto 3.8.x")

# Load Classes
from .mohr import (
    Read,
    ReadDF,
    Visualize_User_Defined,
    Visualize,
    getEnvelope,
)

# Load Functions
from .mohr import (
    load_df,
    read_csv
)
