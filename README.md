# PyArmChess © Version 0.1

## Requires:

 - Python 3.5+
 - opencv-python
 - numpy 1.11.2

## Installation:

### Virtualenv and VirtualenvWrapper

```sh
pip install --user virtualenv
pip install --user virtualenvwrapper
```

After the installation it's time to add theses lines in ```~/.profile``` (maybe ```~/.bashrc``` or ```~/.bash_profile```)

```sh
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
export PROJECT_HOME=~/pyprojects
mkdir -p $PROJECT_HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.x
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source .local/bin/virtualenvwrapper.sh
```

And finally reload this file :

```source ~/.profile```

### Install Python 3.6.0

```sh
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
tar -xvzf Python-3.6.0
cd Python-3.6.0
sudo ./configure
sudo make install
cd ..
rm Python-3.6.0.tgz
rm -rf Python-3.6.0
```

### Clone this repository

Go into the pyprojects directory :

```cd ~/pyprojects/```

Clone the git :

```git clone https://github.com/CactusTribe/PyArmChess.git```

### Create new virtualenv with Python 3.6.0

```sh
mkvirtualenv PyArmChess -p /usr/local/bin/python3.6         
deactivate
setvirtualenvproject ~/.virtualenvs/PyArmChess ~/pyprojects/PyArmChess
```

### Use the environment and install pip packages

```
workon PyArmChess
pip install opencv-python
```

## Development:

### Makefile rules

```make run``` :  Run the file main.py

### Files description

```src/*``` : .py files

## License:

PyArmChess

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
