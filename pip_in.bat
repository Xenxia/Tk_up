@echo off


python setup.py bdist_wheel
cd dist
pip install Tk_up-1.0.0-py3-none-any.whl --force-reinstall
cd ..

rmdir /S /Q "dist"
rmdir /S /Q "build"
rmdir /S /Q "Tk_up.egg-info"