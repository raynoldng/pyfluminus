# pyFluminus
[![Coverage Status](https://coveralls.io/repos/github/raynoldng/pyfluminus/badge.svg?branch=master)](https://coveralls.io/github/raynoldng/pyfluminus?branch=master)
Python port of the excellent [fluminus](https://github.com/indocomsoft/fluminus).

Automatically download recently uploaded files from Luminus. I personally use pyFluminus to download files into Dropbox so that I can view all my modules' files on any device.

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
python pyfluminus_cli.py -username="e123456" -password="passw0rd"  --download_to=/tmp/luminus
```

If you are uncomfortable with having to pass your credentials in as plaintext you can instead save it as environment variables: `LUMINUS_USERNAME`, `LUMINUS_PASSWORD` and pass in the `--env` flag.

This downloads files of all your modules to the directory specified. To download files again simply do:

```
python pyfluminus_cli.py -username="e123456" -password="passw0rd"  --download_to=/tmp/luminus
```

More information can be found in the help page:
```
usage: pyfluminus_cli.py [-h] [-username USERNAME] [-password PASSWORD]
                         [--env] [--download_to DOWNLOAD_TO] [--ignore IGNORE]

CLI wrapper to pyfluminus

optional arguments:
  -h, --help            show this help message and exit
  -username USERNAME    NUSNET username, e.g. e01234
  -password PASSWORD    NUSNET password
  --env                 Get username and password from environment variables
  --download_to DOWNLOAD_TO
                        Download destination
  --ignore IGNORE       Comma separated list of modules to ignore (e.g.
                        CS1231,CS4321)
  --announcements       Display announcements
```
# Extending pyFluminus

The original goal for this project was a barebones CLI interface for downloading LumiNUS files. I can imagine that a GUI wrapper would be a strong use case and a useful tool for users not comfortable with CLI tools. You can see a working example [here](https://github.com/J0/pyfluminus_gui/tree/j0_pyfluminus_gui).

To assist with that, there is the `pyfluminus.fluminus.get_links_for_module` utility function that returns all of the download links of a module.

Example use case:
```python
from pyfluminus.authorization import vafs_jwt
from pyfluminus import fluminus
from pyfluminus.structs import Module
modules_res = api.modules(auth)
if not modules_res.ok:
    print("Error: ", modules_res.error_msg)
modules = modules_res.data
for module in modules:
    if module is None:
        continue
    print("{} {}".format(module.code, module.name))
    data = fluminus.get_links_for_module(auth, module)
    print(data)
```

Example output:

```
{   
    'children': [   {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'test2.pdf',
                                            'type': 'file'},
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'Sample test 2.pdf',
                                            'type': 'file'}],
                        'name': 'Tests',
                        'type': 'folder'},
                    {   'children': [   {   'children': [],
                                            'name': 'Revised Project '
                                                    'Objectives',
                                            'type': 'folder'},
                                        {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                                                'name': 'NG YI '
                                                                        'CHONG '
                                                                        'RAYNOLD '
                                                                        '- '
                                                                        'Project '
                                                                        'Objectives.pdf',
                                                                'type': 'file'}],
                                            'name': 'Project Objectives',
                                            'type': 'folder'},
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'CS4215 Project List '
                                                    'AY2019_20 Semester 2.pdf',
                                            'type': 'file'},
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'Project Objectives '
                                                    'Template.docx',
                                            'type': 'file'}],
                        'name': 'Projects',
                        'type': 'folder'},
                    {   'children': [   {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                                                'name': 'NG YI '
                                                                        'CHONG '
                                                                        'RAYNOLD '
                                                                        '- '
                                                                        'qn4.newlayout.js',
                                                                'type': 'file'}],
                                            'name': 'week6_mark_sweep',
                                            'type': 'folder'},
                                        ...
                                        {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                                                'name': 'NG YI '
                                                                        'CHONG '
                                                                        'RAYNOLD '
                                                                        '- '
                                                                        'week2.txt',
                                                                'type': 'file'}],
                                            'name': 'week2_submission',
                                            'type': 'folder'},
                                        ...
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'week2_template.txt',
                                            'type': 'file'}],
                        'name': 'Lab task submission',
                        'type': 'folder'},
                    {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'slides_11.color.pdf',
                                            'type': 'file'},
                                        ...
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'slides_01_corrected_2020_01_13.bw.pdf',
                                            'type': 'file'}],
                        'name': 'Slides',
                        'type': 'folder'},
                    {   'children': [   {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'notes_11.pdf',
                                            'type': 'file'},
                                        ...
                                        
                                        {   'link': 'https://luminus.nus.edu.sg/v2/api/files/download/....',
                                            'name': 'notes_01.pdf',
                                            'type': 'file'}],
                        'name': 'Notes',
                        'type': 'folder'}],
    'name': 'CS4215',
    'type': 'folder'
}
```

Which is a useful data source to build a GUI around.
