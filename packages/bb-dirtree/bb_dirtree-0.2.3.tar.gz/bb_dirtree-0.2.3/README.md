
# DirTree

##### - create a nice looking directory tree
==============================================

## Installation:
================

##### _**Windows:**_

```bash
py -m pip install "BB-DirTree"
```

##### _**Linux/Mac:**_

```bash
python -m pip install "BB-DirTree"
```

## DirTree usage
================

```bash
dirtree [OPTIONS] [ARGS]
```

### _**Options:**_

**Short**  | **Long**       | **Description**
---------- | -------------- | ---------------------------------------------------------
-b         |   --base-dir   |  Set base directory <br> *Uses current directory if not specified*
-d         |   --depth      |  Integer to set the depth of directory tree <br> *ex: '0' will only print the base directory list*
-D         |   --dotfiles   |  Include hidden files in tree
-e         |   --exclude    |  Filenames/directories to exclude from the tree <br> *See Exclusions*
-h         |   --help       |  This help message
-q         |   --qt-html    |  Print in html format for use with QT
-r         |   --regex      |  Use regex to include/exclude files/directories in tree <br> *See Regex*

>It is recommended to quote all paths

### *Exclusions*

>Provide names of files or directories to exclude. To exclude multiple files/directories, quote entire list and seperate with a colon (**:**). Add a forward slash (**/**) to specify a directory name to exclude.

##### **Example:**
  
```bash
python -m bbdirtree --exclude "excluded dir:excluded file"
```

### *Regex*

>Prefix regex with *include=* or *exclude=*

>Seperate each regex with a space, quoting each individual argument.

##### _**Examples:**_

```bash
python -m bbdirtree --regex "exclude=.*\.ini$"

    # will exclude any files that have a *.ini* extension.

python -m bbdirtree --regex "include=.*\.mp3$"

    # will include only files with a *.mp3* extension.
```

>This has no effect on directories

>Multiple regex can be used by specifying **--regex** multiple times.

## License
==========

<pre>
    MIT License

    Copyright (c) [2022] [Erik Beebe]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
</pre>

## CHANGELOG
============

#### v0.1.0 - 5-29-2022

- initial release

#### v0.1.1 - 5-30-2022

- changed name from DirTree to BB-DirTree
- added README.md

#### v0.1.2 - 5-31-2022

- added a changelog to README.md
- made corrections to help message

#### v0.1.3 - 5-31-2022

- added support for windows hidden files

#### v0.1.5 - 5-31-2022

- made corrections to help message

#### v0.1.7 - 6-7-2022

- changed color of files in html output
- small changes to output format

#### v0.2.2 - 7-9-2023

- added script to run from $PATH (run with 'dirtree')
- cleaned up code
- changed header text at top of output

#### v0.2.3 - 7-9-2023

- added python project titles to output
    - searches for pyproject.toml or setup.py
- added git project titles to output
    - searches for .SRCINFO file
