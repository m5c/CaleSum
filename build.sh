cd cale_sum || exit
pyinstaller --onefile --windowed launcher.py --icon=icon.icns -n "CaleSum"
rm -rf build
mv dist/*app ~/Desktop
rm -rf dist
cd ..
