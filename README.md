# pyFluminus
[![Coverage Status](https://coveralls.io/repos/github/raynoldng/pyfluminus/badge.svg?branch=master)](https://coveralls.io/github/raynoldng/pyfluminus?branch=master)
Python port of the excellent [fluminus](https://github.com/indocomsoft/fluminus).

CLI coming soon!

PRs are welcome

Features (at parity with [fluminus](https://github.com/indocomsoft/fluminus))
- Authentication via ADFS (vafs.nus.edu.sg)
- Get name of student
- Get list of modules
    - Taking/Teaching
    - Only this semester's modules
- Get announcements
- Get listing of workbin files and download them
- Get listing of webcasts and download them
- Get listing of weekly lesson plans and their associated files

# CLI Usage

To download your files:

```
mkdir /tmp/fluminus
python pyfluminus_cli.py -username="e123456" -password="passw0rd"  --download-to=/tmp/luminus
```

This downloads files of all your modules to the directory specified. To download files again simply do:

```
python pyfluminus_cli.py -username="e123456" -password="passw0rd"  --download-to=/tmp/luminus
```


# Todos
- [ ] get credentials from environment
- [ ] upload to PyPi
- [ ] (maybe?) GUI