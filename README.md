# Calendar Intel

A simple tool for MacOS to quickly figure our how much time you spent on tasks.

## Install Instructions

This requires a *recent* version of python and tkinter, to support [apple silicon](https://support.apple.com/en-ca/HT211814).

 * `brew install python3`
 * `brew install python-tk`

Brew may not update the system interpreter. If needed set an alias, and manually set the IDE interpreter:

```bash
alias python='/opt/homebrew/Cellar/python@3.11/3.11.5/bin/python3'
alias python3='/opt/homebrew/Cellar/python@3.11/3.11.5/bin/python3'
```

## Run Instructions

Clone this project, then run from the base directory:  

`python -m calendar_intel.launcher`
