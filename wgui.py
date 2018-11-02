#!/usr/bin/env python3
import os
from pathlib import Path
import pip
from main import *

def main():
    DevopsApp()


if __name__ == '__main__':
    ''' check to see if all dependencies are installed, if not install them '''
    #TODO: need to make an install script to create symlinks, install this repo, and insure the wp_vars is update.

    packages = ['requests', 'git', 'pluginbase']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            from pip._internal import main as pip
            print("....Couldn't find package %s" %package)
            print("....Installing package %s" % package)
            pip(['install', package])

    main()
