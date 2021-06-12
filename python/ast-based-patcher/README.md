# `ast`-based patcher

A simple PoC of `ast`-based patcher. In this example a simple class that reads configuration data from an XML file (`config.xml`) is  patched to use a different XML module (`lxml` instead of a build-in `xml` module).

## Usage
```bash
pipenv install # install requirements
python3 config.py # run the initial version of the code  
python3 patch.py # apply patches and save as config-patched.py
python3 config-patched.py # run the patched version of the code
```

## Links
[Abstract Syntax Tree for Patching Code and Assessing Code Quality](https://engineering.soroco.com/abstract-syntax-tree-for-patching-code-and-assessing-code-quality/)

