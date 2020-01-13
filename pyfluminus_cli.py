import argparse
from pyfluminus.authorization import vafs_jwt
from pyfluminus import api
from pyfluminus.structs import File, Module
import os
from typing import Dict


parser = argparse.ArgumentParser(description="CLI wrapper to pyfluminus")
# NOTE for now take in username and password via command line
parser.add_argument('-username', type=str, help="NUSNET username, e.g. e01234")
parser.add_argument('-password', type=str, help="NUSNET password")

# flags
parser.add_argument("--download_to", type=str) # if downloading files


def download_files(file: File, auth: Dict, download_path: str, verbose=False):
    if not file.directory:
        full_file_path = os.path.join(download_path, file.name)
        if os.path.exists(full_file_path):
            return
        print("- {}".format(full_file_path))
        file.download(auth, download_path, verbose)
        return
    download_path = os.path.join(download_path, file.name)
    if file.children is None:
        file.load_children(auth) 
        if file.children is None: 
            print("Error loading children for file: {}".format(file.name))
            return
    for child in file.children:
        download_files(child, auth, download_path, verbose)
        

if __name__ == "__main__":
    args = parser.parse_args()
    auth = vafs_jwt("nusstu\\" + args.username, args.password)

    if 'jwt' not in auth:
        print("Failed to authenticate:", auth['error'])
        exit()
    

    name_res = api.name(auth)
    if not name_res.ok:
        print("Error getting name: ", name_res.error_msg)
    print("Hello {}".format(name_res.data))

    modules_res = api.modules(auth)
    if not modules_res.ok:
        print("Error: ", modules_res.error_msg)
    print("Your are taking the following mods")
    modules = modules_res.data
    for module in modules:
        if module is None:
            print("Error parsing module data")
            continue
        print("- {} {}".format(module.code, module.name))

    if args.download_to:
        print("\n\nDownloading Files to {}".format(args.download_to))
        for module in modules:
            if module is None:
                continue
            print("{} {}".format(module.code, module.name))
            module_file = File.from_module(auth, module)
            # TODO set verbose=True for now
            download_files(module_file, auth, args.download_to, True)

