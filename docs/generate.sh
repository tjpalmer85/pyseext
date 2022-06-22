pdoc --force --html -o . --template-dir ./pdoc_templates ../pyseext
mv pyseext/* .
rm -R pyseext