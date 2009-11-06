#!/usr/bin/python2.5
from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "logcatviewer.py",
            "icon_resources": [(1, "magic.ico")]  
        }       
    ]
    , options={"py2exe":{"includes":["sip"] }}       

)
