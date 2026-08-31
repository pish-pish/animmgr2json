# animmgr2json
A python tool to convert Pikmin 1 AnimMgr files between binary (.bin/.key) and .json

# BUILDING
*Requires [mashumaro](https://pypi.org/project/mashumaro/).*

If using windows, a curated distributable version of the tool can be found in the [RELEASES](https://github.com/pish-pish/animmgr2json/releases) tab.
    If using macOs or Linux, either run from source, or build a distributable yourself using [pyinstaller](https://pypi.org/project/pyinstaller/) or other python packagers.

# USAGE
```
usage: animmgr.py [-h] -i INPUT -o OUTPUT [--tojson] [--tobinary]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        <Required> Input path of file to convert.
  -o OUTPUT, --output OUTPUT
                        <Required> Output path of converted file.
  --tojson              <Optional> Converts inputted binary file to json.
  --tobinary            <Optional> Converts inputted json file to binary.
```