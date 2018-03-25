## A very simple setup script to create the release


from distutils.core import setup
import py2exe

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "1.0.0",
    description = "Initial version of the ING csv to YNAB 4 csv",
    name = "homebank2YNAB",

    # targets to build
    windows = ["ing_convert_to_ynab.py"],
    console = ["ing_convert_to_ynab.py"],
    )
