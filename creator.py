#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dateien in Archiv einfügen, evtl. mit Passwortschutz und auf jeden fall in 100mb-Teile zerteilt,
die dann in b-Strings eingelagert werden um direkt auf die Festplatte geschrieben und wieder entpackt werden zu können.
"""

debug = True

import gzip, os, tempfile, traceback, l2db

def compress(data:bytes) -> bytes:
    """GZip-compresses `data`."""
    return gzip.compress(data)

def decompress(data:bytes) -> bytes:
    """GZip-decompresses `data`."""
    return gzip.decompress(data)

def list_only_files_in(path:str)->list:
    return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

def list_only_dirs_in(path:str)->list:
    return [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]

def find_files(path:str, pathlist:list=[])->list:
    for dir in list_only_dirs_in(path):
        try:
            pathlist.append(os.path.join(path, dir, ''))
            find_files(os.path.join(path, dir), pathlist)
        except Exception as e:
            print(f"Could not list directory '{dir}' because of {type(e).__name__}: {e}") #debug
    for file in list_only_files_in(path):
        pathlist.append(os.path.join(path, file))
    return pathlist

def archive(from_dir:str)->bytes:
    """Puts all files from `from_dir` into a GZip-compressed L2DB and returns that."""
    errs = 0
    db = l2db.L2DB()
    if debug: print(f'Reading directory structure in {from_dir}')
    for path in find_files(from_dir):
        if debug: print(f'Packing: {path}')
        if path[-1]==os.path.sep: # Is a directory
            db[path] = b'' # Raw, empty value
        else: # Is a file
            try:
                with open(os.path.join(from_dir, path), 'rb') as file:
                    db[path] = file.read()
            except Exception as e:
                traceback.print_exception(e) # Notify the user of the error
                errs+=1
    print(f'Files packed! ({errs} errors occurred)')
    return gzip.compress(db.syncout_db()) # Return GZip-compressed DB

def extract(data:bytes)->str:
    """Extracts all files from the GZip-compressed L2DB to `to_dir` and returns the `to_dir` path."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir: # Create a temporary directory
                                                                                        # and store its name in `tmpdir`
        if debug: print(f'Extracting to: {tmpdir}')
        db = l2db.L2DB(source=gzip.decompress(data))
        for path in db:
            if debug: print(f'Extracting {os.path.join(tmpdir, path)}')
            try:
                if path[-1]==os.path.sep:
                    os.mkdir(path.join(tmpdir, path))
                else:
                    with open(os.path.join(tmpdir, path), 'wb') as file:
                        file.write(db[path])
            except Exception as e:
                traceback.print_exception(e)

            #TODO: run it all

        return tmpdir