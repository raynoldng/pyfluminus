from pyfluminus.structs import Module, File
from typing import Dict, List

def get_links_for_module(auth: Dict, module: Module, verbose=False) -> Dict:
    """returns Folder containing nested folders, and files with download links
    Folder: {name: string, type: 'folder', children: List[Folder|File]}
    File: {name: string, type: 'file', link: string}
    Not to be confused with File from pyfluminus.structs
    """

    module_file = File.from_module(auth, module)
    return __traverse(auth, module_file, verbose)


def __traverse(auth: Dict, file: File, verbose=False) -> Dict:
    if not file.directory:
        return {"name": file.name, "type": "file", "link": file.get_download_url(auth)}
    if file.children is None:
        file.load_children(auth)
        if file.children is None:
            if verbose:
                print("Error loading children for file: {}".format(file.name))
            return {"name": file.name, "type": "folder", "children": []}
    return {
        "name": file.name,
        "type": "folder",
        "children": [
            __traverse(auth, children, verbose) for children in file.children
        ],
    }


