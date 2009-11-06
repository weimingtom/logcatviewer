#!/bin/bash
set -e

if [[ $# != 1 ]]; 
then
    echo "Usage: release-gmuggle  2.4.2"
    exit -1
fi


if [ -e dist ]
then
    rm -rf dist
fi

if [ -e build ]
then
    rm -rf build
fi
export VERSION=$1

python setup.py py2exe
cp filter.ini ./dist/

cd NSIS
makensis logcatviewer.nsi
cd ..

if [ -e dist ]
then
    rm -rf dist
fi

if [ -e build ]
then
    rm -rf build
fi



echo "build success!"
