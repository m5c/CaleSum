cd calendar_intel
pyinstaller --onefile --windowed launcher.py --icon=icon.icns -n "Calendar Intel"
rm -rf build
mv dist/*app ~/Desktop
rm -rf dist
cd ..
