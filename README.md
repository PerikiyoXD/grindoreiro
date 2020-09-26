# GRINDOREIRO
Python utilities to unpack Grandoreiro .ZIPs with .MSI sample.

These are some scripts to:
- Extract ZIP file with MSI and ICO
- Decompile and extract MSI with WiX Toolset
- Search for URLs in MSI extracted Delphi DLL strings
- See C&C server of the current sample

The files are scattered inside the samples directory, under the sha256 named directory of its own.

You'll need to download the latest WiX Toolset, and extract 
https://wixtoolset.org/releases/

Right now, tested with https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311-binaries.zip

## Set up
### Prerequesites

Download Wix Toolset. Download wix-binaries.zip from github
Extract them on ./tools/wix, so that dark.exe is inside the wix folder.
### Installing

- Create a virtual environment
- Activate virtual environment
- Install requirements from requirements.txt
- Put Grandoreiro .ZIP files into samples/ folder (ie: DOCUMENT_1234_TEST.zip)
(These zip files have one .MSI and one .GIF file)
-Run:
	```python ./grindoreiro.py DOCUMENT_1234_TEST.zip```
	
Tools:
 - grindoreiro.py: the main program
 - isoabduct.py: is a script to gather and decode .ISO files referenced inside .DLLs
 - stringripper.py: is a script to gather Strings (Both UTF8 & UTF16) from a binary file
