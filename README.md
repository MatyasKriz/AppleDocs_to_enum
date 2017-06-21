# AppleDocs to enum
This simple Python3 script takes an Apple Documentation page and if there are enums, creates a file containing all the cases.

## Instalation
Simply clone the repository and run 2 commands in the terminal:

`pip3 install beautifulsoup4` and `pip3 install requests`

After that you're good to go!

## Usage
You can either let the script guide you through the process (there are only 2 interactions needed) or you can give the script arguments.

`-d` or `--defaultName` don't ask for your input regarding enum's name

`-l` or `--link` LINK gives the last part of URL to script, so it doesn't ask later

`-n` or `--name` NAME gives script desired name of the enum

`-a` or `--all` scrape all types, not just `case`

## Purpose
Created to learn a little bit of Python3 and help with development of [ReactantUI](https://github.com/Brightify/ReactantUI).

## License
Licensed under MIT, feel free to use as you see fit if it's in compliance with LICENSE.
