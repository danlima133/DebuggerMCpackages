echo "Buildig App"
rm -rf out

echo "Creating 'out' directory"
mkdir out
cd ./out

echo "Genarate Executable"
pyinstaller ../build.spec